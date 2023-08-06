from mcot.utils.build import load_info
__doc__, __version__ = load_info(__name__)
del load_info

from .pipeline import Pipeline, In, Out, Ref, Var, to_templates_dict
pipe = Pipeline()