import datalad.api as dl
from datalad.utils import File
from file_tree import FileTree
import os.path as op
from functools import lru_cache


def get_tree(relative_dir='.', full_dir=None):
    if full_dir is None:
        full_dir = relative_dir
    ds = get_dataset(full_dir)
    if ds is None:
        return None
    if op.isfile(op.join(full_dir, 'data.tree')):
        tree = FileTree.read(op.join(full_dir, 'data.tree'), top_level=relative_dir)
    else:
        tree = FileTree.empty(top_level=relative_dir)
    for sub_ds in dl.subdatasets(dataset=ds):
        sub_path = sub_ds['gitmodule_name']
        tree_name = op.split(sub_path)[-1]
        tree.add_template(sub_path, "__" + tree_name)
        tree.add_subtree(get_tree(sub_path, sub_ds['path']), tree_name, "__" + tree_name)
    return tree


@lru_cache(None)
def get_dataset(directory='.'):
    ds = dl.Dataset(directory)
    if not ds.is_installed():
        return None
    return ds