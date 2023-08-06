Build pipelines decleratively built on top of file-tree.

.. code-block:: python

    from mcot.pipe import pipe, In, Out, Ref, Var
    from file_tree import FileTree

    @pipe(logdir='log', minutes=41)
    def func(in_path: In, out_path: Out, ref_path: Ref, placeholder_key: Var):
        pass

    pipe.cli(FileTree.from_string("""
    placeholder_key = A, B

    ref_path.txt
    directory-{placeholder_key}
        in_path.txt
        out_path.txt
    """))