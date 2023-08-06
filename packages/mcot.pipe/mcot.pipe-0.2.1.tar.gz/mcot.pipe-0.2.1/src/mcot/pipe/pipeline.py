"""
Defines the pipeline before a FileTree is provided

At the first level it is simply a collection of functions with mapping from the function parameters to input/output/reference basenames
"""
from fsl.utils.fslsub import SubmitParams
from typing import List, Optional, Set, Tuple, Dict
import argparse
from dataclasses import dataclass
from file_tree import FileTree
import numpy as np
import os
from .datalad import get_tree


class Pipeline:
    """Collection of python functions forming a pipeline

    You can either create a new pipeline (`from mcot.pipe import Pipeline; pipe = Pipeline()`) or use a pre-existing one (`from mcot.pipe import pipe`)

    Scripts are added to a pipeline by using the pipeline as a decorator (see :meth:`__call__`).

    To run the pipeline based on instructions from the command line run `pipe.cli(tree)`, 
    where tree is a FileTree defining the directory structure of the pipeline input & output files.

    :ivar scripts: list of :class:`PipedFunction`, which define the python functions forming the pipeline and their input/output templates
    """
    def __init__(self):
        """Create a new empty pipeline
        """
        self.scripts: List[PipedFunction] = []

    def __call__(self, function=None, templates=None, placeholders=None, no_iter=None, as_path=False, **submit_params):
        """Adds a python function as a :class:`PipedFunction` to the pipeline

        .. code-block:: python

            from mcot.pipe import pipe, In, Out, Ref, Var

            @pipe(logdir='log', minutes=41)
            def func(in_path: In, out_path: Out, ref_path: Ref, placeholder_key: Var):
                pass

        :param function: Optionally provide the function directly
        :param templates: optional mapping from function keyword arguments to template keys (overrides annotations)
        :param placholder: optional mapping from function keyword arguments to placeholder keys (overrides annotations)
        :param no_iter: optional set of parameters not to iterate over
        :param as_path: Provides function with `pathlib.Path` objects instead of strings (default: False)
        :param submit_params: arguments to use when submitting this job to the cluster
        """
        submit_params = SubmitParams(**submit_params)
        def wrapper(func):
            self.scripts.append(PipedFunction(func, submit_params=submit_params, placeholders=placeholders, templates=templates, no_iter=no_iter, as_path=as_path))
            return func
        if function is None:
            return wrapper
        wrapper(function)

    def make_concrete(self, tree: FileTree):
        """
        Splits the pipeline into individual jobs

        :param tree: set of templates for the input/output/reference files with all possible placeholder values
        """
        from .job import ConcretePipeline, FileTarget
        all_targets: Dict[str, FileTarget] = {}
        jobs = {}
        for script in self.scripts:
            jobs[script] = script.get_jobs(tree, all_targets)
        return ConcretePipeline(tree, jobs, all_targets)

    def cli(self, tree: Optional[FileTree]=None, description="Runs the pipeline", include_vars=None, exclude_vars=()):
        """
        Runs the pipeline from the command line

        :param tree: `file_tree.FileTree` object describing the directory structure for the input/output files (defaults to datalad tree).
        :param description: Description to give of the script in the help message.
        :param include_vars: if provided, only include expose variables in this list to the command line
        :param exclude_vars: exclude variables in this list from the command line
        """
        from .job import RunMethod
        if len(self.scripts) == 0:
            raise ValueError("The pipeline does not contain any scripts...")
        if tree is None:
            tree = get_tree()
        parser = argparse.ArgumentParser(description)
        templates = set.union(*[script.filter_templates(output=True) for script in self.scripts])
        default_method = RunMethod.submit if os.getenv('SGE_ROOT', default='') != '' else RunMethod.local

        parser.add_argument("templates", nargs="*", default=templates,
                            help=f"For which templates to produce the files (default: {', '.join(sorted(templates))})")
        parser.add_argument("-m", '--pipeline_method', default=default_method.name,
                            choices=[m.name for m in RunMethod],
                            help=f"method used to run the jobs (default: {default_method.name})")
        parser.add_argument("-o", '--overwrite', action='store_true', help="If set overwrite any requested files")
        parser.add_argument("-d", '--overwrite_dependencies', action='store_true',
                            help="If set also overwrites dependencies of requested files")
        parser.add_argument("-r", '--raise_errors', action='store_true',
                            help="If set raise errors rather than catching them")
        parser.add_argument("-j", '--job-hold', default='', 
                            help='Place a hold on this pipeline until job has completed')
        for var, values in tree.placeholders.items():
            if not isinstance(var, str):
                continue
            if '/' in var:
                continue
            if var in exclude_vars:
                continue
            if include_vars is not None and var not in include_vars:
                continue
            if np.asarray(values).ndim == 1:
                default = ','.join([str(v) for v in values])
            else:
                default = str(values)
            parser.add_argument(f"--{var}", nargs='+', help=f"Use to set the possible values of {var} to the selected values (default: {default})")
        
        args = parser.parse_args()
        for var in tree.placeholders:
            if isinstance(var, str) and getattr(args, var, None) is not None:
                tree.placeholders[var] = getattr(args, var)
        concrete = self.make_concrete(tree)
        torun = concrete.filter(args.templates, overwrite=args.overwrite, overwrite_dependencies=args.overwrite_dependencies)
        torun.run(RunMethod[args.pipeline_method], raise_errors=args.raise_errors, wait_for=() if args.job_hold == '' else args.job_hold.split(','))


class PipedFunction:
    """
    Represents a function stored in a pipeline
    """
    def __init__(self, function, submit_params: SubmitParams, placeholders=None, templates=None, no_iter=None, as_path=True):
        """
        Wraps a function with additional information to run it in a pipeline

        :param function: python function that will be run in pipeline
        :param submit_params: parameters to submit job running python function to cluster using `fsl_sub`
        :param placeholders: maps function keyword arguments to variables in the FileTree
        :param templates: maps function keyword arguments to templates in the FileTree with additional information on whether the file is input/output/reference
        :param no_iter: which parameters to not iterate over (i.e., they are passed to the function in an array)
        :param as_path: whether to pass on pathlib.Path objects instead of strings to the functions (default: True)
        """
        self.function = function
        self.submit_params = submit_params
        self.as_path = as_path

        self.placeholders = {}
        self.templates = {}
        for key, value in function.__annotations__.items():
            if isinstance(value, Placeholder):
                self.placeholders[key] = value
            elif isinstance(value, Template):
                self.templates[key] = value
        if placeholders is not None:
            self.placeholders.update(placeholders)
        if templates is not None:
            self.templates.update(templates)

        self.no_iter = {key if value.key is None else value.key for key, value in self.placeholders.items() if value.no_iter}
        if no_iter is not None:
            self.no_iter.update(no_iter)

    def filter_templates(self, output=False) -> Set[str]:
        """
        Find all input or output template keys

        :param output: if set to True select the input rather than output templates
        :return: set of input or output templates
        """
        res = set()
        for kwarg_key, template in self.templates.items():
            if ((template.input and not output) or
                (template.output and output)):
                res.add(kwarg_key if template.key is None else template.key)
        return res

    def iter_over(self, tree: FileTree) -> Tuple[str, ...]:
        """
        Finds all the placeholders that should be iterated over before calling the function

        These are all the placeholders that affect the input templates, but are not part of `self.no_iter`.

        :param tree: set of templates with placeholder values
        :return: placeholder names to be iterated over sorted by name
        """
        in_vars = self.all_placeholders(tree, False)
        out_vars = self.all_placeholders(tree, True)
        all_in = in_vars.union(self.no_iter)
        if len(out_vars.difference(all_in)) > 0:
            raise ValueError(f"{self}: Output template depends on {out_vars.difference(all_in)}, which none of the input templates depend on")
        return tuple(sorted(in_vars.difference(self.no_iter)))
        
    def get_jobs(self, tree: FileTree, all_targets: Dict):
        """
        Get a list of all individual jobs defined by this function

        :param tree: set of templates with placeholder values
        :param all_targets: mapping from filenames to Target objects used to match input/output filenames between jobs
        :return: sequence of jobs
        """
        from .job import SingleJob
        to_iter = self.iter_over(tree)
        jobs = [SingleJob(self, sub_tree, all_targets, to_iter) for sub_tree in tree.iter_vars(to_iter)]
        return jobs
        
    def all_placeholders(self, tree: FileTree, output=False) -> Set[str]:
        """
        Identify the placeholders affecting the input/output templates of this function

        :param tree: set of templates with placeholder values
        :param output: if set to True returns the placeholders for the output than input templates
        :return: set of all placeholders that affect the input/output templates
        """
        res = set()
        for t in self.filter_templates(output):
            res.update(tree.get_template(t).placeholders())
        if not output:
            for key, variable in self.placeholders.items():
                res.add(key if variable.key is None else variable.key)
        _, only_multi = tree.placeholders.split()
        no_singular = {key for key in res if key in only_multi}
        return {key.split('/')[-1] if tree.placeholders.find_key(key) is None else tree.placeholders.find_key(key) for key in no_singular}

    def __repr__(self, ):
        return f"PipedFunction({self.function.__name__})"


@dataclass
class Template(object):
    key: Optional[str] = None
    input: bool = False
    output: bool = False

    def __call__(self, key=None):
        return Template(key, self.input, self.output)

@dataclass
class Placeholder(object):
    key: Optional[str] = None
    no_iter: bool = False
    enumerate: bool = False

    def __call__(self, key=None, no_iter=False, enumerate=False):
        return Placeholder(key, no_iter, enumerate)


In = Template(input=True)
Out = Template(output=True)
Ref = Template()
Var = Placeholder()


def to_templates_dict(input_files=(), output_files=(), reference_files=()):
    """Helper function to convert a sequence of input/output/reference files into a template dictionary

    Args:
        input_files (sequence, optional): Template keys representing input files. Defaults to ().
        output_files (sequence, optional): Template keys representing output files. Defaults to ().
        reference_files (sequence, optional): Template keys representing reference paths. Defaults to ().

    Raises:
        KeyError: If the same template key is used as more than one of the input/output/reference options

    Returns:
        dict: mapping of the keyword argument names to the Template objects
    """
    res = {}
    for files, cls in [
        (input_files, In),
        (output_files, Out),
        (reference_files, Ref),
    ]:
        for name in files:
            if isinstance(name, str):
                short_name = name.split('/')[-1]
            else:
                short_name, name = name
            if name in res:
                raise KeyError(f"Dual definition for template {name}")
            res[short_name] = cls(name)

    return res
