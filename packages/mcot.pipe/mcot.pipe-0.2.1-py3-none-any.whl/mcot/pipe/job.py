
from functools import lru_cache
from file_tree.file_tree import FileTree
import xarray
from typing import Optional, Set, Dict, List, Collection, Any
from enum import Enum
from fsl.utils.fslsub import func_to_cmd
from loguru import logger
import os
from pathlib import Path
from .pipeline import PipedFunction
from .datalad import get_dataset
import os.path as op


class OutputMissing(IOError):
    """Raised if a job misses the output files.
    """
    pass


class InputMissing(IOError):
    """Raised if a job misses the input files.
    """
    pass


class RunMethod(Enum):
    """
    How to run the individual jobs
    """
    local = 1
    submit = 2
    dask = 3


class ConcretePipeline:
    """
    Pipeline with a concrete set of jobs
    """
    def __init__(self, tree: FileTree, jobs: Dict[PipedFunction, List["SingleJob"]], targets: Dict[str, "FileTarget"]):
        self.tree = tree
        self.jobs = jobs
        for scripts in jobs.values():
            for job in scripts:
                job.pipeline = self
        self.targets = targets

    def filter(self, templates: Collection[str], overwrite=False, overwrite_dependencies=False) -> "ConcretePipeline":
        """Filters out a subset of jobs

        :param templates: target template keys; Any jobs required to produce those files will be kept in the returned pipeline
        :param overwrite: if True overwrite the files matching the template even if they already exist, defaults to False
        :param overwrite_dependencies: if True rerun any dependent jobs even if the output of those jobs already exists, defaults to False
        :return: Concrete pipeline with the jobs needed to produces `templates` (with optional overriding)
        """
        all_jobs: Set[SingleJob] = set()
        for template in templates:
            for wrapper, scripts in self.jobs.items():
                if template in wrapper.filter_templates(output=True):
                    for script in scripts:
                        script.add_to_set(all_jobs, overwrite, overwrite_dependencies)
        return ConcretePipeline(self.tree, {
            w: [j for j in s if j in all_jobs] for w, s in self.jobs.items()
        }, self.targets)

    def run(self, method: RunMethod, raise_errors=False, wait_for=()):
        """Runs all the jobs that are required to produce the given templates

        :param method: defines how to run the job
        :param overwrite: if True overwrite the files matching the template even if they already exist, defaults to False
        :param overwrite_dependencies: if True rerun any dependent jobs even if the output of those jobs already exists, defaults to False
        :param wait_for: job IDs to wait for before running pipeline
        :return: set of all the jobs that need to be run to produce the template files
        """
        if len(self.jobs) == 0:
            logger.info("No new jobs being run/submitted")
            return
        all_jobs: Set[SingleJob] = set()
        for wrapper, scripts in self.jobs.items():
            nrun = len(scripts)
            printer = logger.debug if nrun == 0 else logger.info
            printer(f"{wrapper}: Running {nrun} jobs")
            all_jobs.update(scripts)

        run_jobs: Dict[SingleJob, Any] = {}
        while len(run_jobs) < len(all_jobs):
            for job in all_jobs:
                if job in run_jobs or any(j in all_jobs and j not in run_jobs for j in job.dependencies(only_missing=False)):
                    continue
                dependencies = [run_jobs[j] for j in job.dependencies(only_missing=False) if j in run_jobs]
                if len(dependencies) == 0:
                    dependencies = wait_for
                run_jobs[job] = job(
                    method=method,
                    catch=not raise_errors,
                    wait_for=dependencies,
                )


class SingleJob:
    """
    Represents a single potential run of the wrapped function in the pipeline
    """
    def __init__(self, wrapper: PipedFunction, single_tree: FileTree, all_targets: Dict[str, "FileTarget"], unique_keys):
        """
        Creates a single job that can be run locally or submitted

        :param wrapper: Wrapped function
        :param single_tree: set of template with placeholder values
        :param all_targets: mapping of filenames to FileTarget objects used to map input & output files between functions
        :param unique_keys: template keys that the wrapper function iterated over to create this job
        """
        self.wrapper = wrapper
        self.exists_before: Set[FileTarget] = set()
        self.exists_after: Set[FileTarget] = set()
        self.single_tree = single_tree
        self.unique_keys = unique_keys
        self.pipeline = None

        for kwarg_key, template in self.wrapper.templates.items():
            key = kwarg_key if template.key is None else template.key
            paths = single_tree.get_mult(key)
            as_target = xarray.apply_ufunc(lambda p: get_target(p, all_targets), paths, vectorize=True)
            if isinstance(as_target, FileTarget):
                targets = [as_target]
            else:
                targets = as_target.values.flat

            for t in targets:
                if template.input:
                    t.required_by.add(self)
                    self.exists_before.add(t)
                elif template.output:
                    t.producer = self
                    self.exists_after.add(t)
    
    @property
    def kwargs(self, ):
        res = {}
        for kwarg_key, template in self.wrapper.templates.items():
            key = kwarg_key if template.key is None else template.key
            res[kwarg_key] = self.single_tree.get_mult(key)
            if not self.as_path:
                res[kwarg_key] = xarray.apply_ufunc(str, res[kwarg_key], vectorize=True)
            if res[kwarg_key].ndim == 0:
                res[kwarg_key] = res[kwarg_key].values[()]
        for kwarg_key, placeholder in self.wrapper.placeholders.items():
            key = kwarg_key if placeholder.key is None else placeholder.key
            value = self.single_tree.placeholders[key]
            if placeholder.enumerate:
                idx = list(self.pipeline.tree.placeholders[key]).index(value)
                res[kwarg_key] = (idx, value)
            else:
                res[kwarg_key] = value
        return res

    @property
    def function(self, ):
        return self.wrapper.function

    @property
    def submit_params(self, ):
        return self.wrapper.submit_params

    @property
    def as_path(self,):
        return self.wrapper.as_path

    def exists(self, output=False, reset=False, error=False):
        """Raises a ValueError if any input/output files are missing
        """
        missing = set()
        check = self.exists_after if output else self.exists_before
        for to_check in check:
            if reset:
                to_check.reset_existence()
            if not to_check.exists:
                if not error:
                    return False
                missing.add(to_check)
        if len(missing) > 0:
            err = OutputMissing if output else InputMissing 
            raise err(f"Missing {'output' if output else 'input'} files: {missing}", missing)
        return True

    @lru_cache(None)
    def dependencies(self, only_missing=True) -> Set[Optional["SingleJob"]]:
        """Return jobs on which this job depends.

        By default it only returns those related with missing input files.
        """
        jobs = set()
        for target in self.exists_before:
            if not (only_missing and target.exists):
                jobs.add(target.producer)
        return jobs

    def expects_input(self, ):
        """Checks whether any input will remain missing even after running dependencies.
        """
        for target in self.exists_before:
            if not target.expected:
                raise InputMissing(f"Missing way to create {target}")

    def add_to_set(self, all_jobs: Set["SingleJob"], overwrite=False, overwrite_dependencies=False):
        """Mark this job and all of its dependencies to run

        This job is marked to run, if any of the output does not yet exist or overwrite is True.
        The dependencies are marked to run, if this job runs and either their output does not exist or overwrite_dependencies is True.

        :param all_jobs: list of individual jobs
        :param overwrite: if True mark this job even if the output already exists, defaults to False
        :param overwrite_dependencies: if True mark the dependencies of this job even if their output already exists, defaults to False
        :return: set of all jobs that have been marked to run
        """
        if self in all_jobs:
            return
        if not overwrite and self.exists(output=True):
            return
        self.expects_input()
        all_jobs.add(self)
        for job in self.dependencies(only_missing=overwrite_dependencies):
            if job is not None:
                job.add_to_set(all_jobs, overwrite_dependencies, overwrite_dependencies)

    def __call__(self, method: RunMethod, catch=False, wait_for=()):
        """Runs the job
        """
        self.prepare_run()
        if method == RunMethod.local:
            self.exists(error=True)
            logger.info(f"running {self}")
            self.job = self.function(**self.kwargs)
            self.exists(output=True, reset=True, error=True)
        elif method == RunMethod.submit:
            logdir = self.single_tree.get(self.submit_params.logdir)
            Path(logdir).mkdir(exist_ok=True, parents=True)
            if self.submit_params.job_name is None:
                self.submit_params.job_name = self.function.__name__
            cmd = func_to_cmd(self.function, (), self.kwargs, logdir, clean="on_success")
            env = dict(os.environ)
            env.update(self.submit_params.env)
            env['PYTHONPATH'] = env.get('PYTHONPATH', '') + ':' + os.getcwd()
            self.job = self.submit_params(cmd, wait_for=wait_for, logdir=logdir, env=env)
            logger.debug(f"submitted {self} with job ID {self.job}")
        elif method == RunMethod.dask:
            import dask
            def dask_job(*other_jobs):
                if any(a != 0 for a in other_jobs):
                    logger.debug(f"{self} skipped because dependencies failed")
                    return 1
                try:
                    self.exists(error=True)
                    self.function(**self.kwargs)
                    self.exists(output=True, reset=True, error=True)
                except Exception as e:
                    if catch:
                        logger.exception(f"{self} failed: {e}")
                        return 1
                    logger.info(f"{self} failed: {e}")
                    raise e
                logger.debug(f"Running {self} using dask")
            self.job = dask.delayed(dask_job, name=str(self))(wait_for)
        return self.job

    def prepare_run(self, ):
        """
        Prepares to run this job

        1. Creates output directory
        2. Ensure all the files are got from datalad
        """
        for target in self.exists_after:
            target.filename.parent.mkdir(parents=True, exist_ok=True)
        ds = get_dataset()
        if ds is not None:
            for source in self.exists_before:
                if op.islink(source.filename):
                    ds.get(source.filename)

    def __repr__(self, ):
        vars = ', '.join([f"{k}={self.single_tree.placeholders[k]}" for k in self.unique_keys])
        return f"SingleJob({self.function.__name__}, {vars})"


def get_target(filename: Path, all_targets) -> "FileTarget":
    abs_path = Path(filename).absolute()
    if abs_path not in all_targets:
        all_targets[abs_path] = FileTarget(filename)
    return all_targets[abs_path]

class FileTarget:
    """Input, intermediate, or output file
    """
    def __init__(self, filename: Path, producer=None, required_by=None):
        self.filename = Path(filename)
        self._producer = producer
        self.required_by = set() if required_by is None else set(required_by)

    @property
    def exists(self) -> bool:
        """
        Tests whether file exists on disk

        This function is lazy; once it has been checked once it will keep returning the same result.

        To reset use :meth:`reset_existence`.
        """
        if not hasattr(self, "_exists"):
            self._exists = self.filename.is_symlink() or self.filename.exists()
        return self._exists

    def reset_existence(self, ):
        """Ensure existence is checked again"""
        if hasattr(self, "_exists"):
            del self._exists

    @property
    def expected(self, ):
        """
        Whether the file can be produced by the pipeline (or already exists)
        """
        if self.exists:
            return True
        if self.producer is None:
            return False
        return True

    @property
    def producer(self, ):
        return self._producer

    @producer.setter
    def producer(self, new_value):
        if self._producer is not None:
            if self._producer is new_value:
                return
            raise ValueError(f"{self} can be produced by both {self.producer} and {new_value}")
        self._producer = new_value

    def __repr__(self, ):
        return f"FileTarget({str(self.filename)})"