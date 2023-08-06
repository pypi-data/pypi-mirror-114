""" Pythonal is a library for allowing a more functional style of programming
with a haskell like style.

Many of the functions are intended to be used as decorators
i.e. @static_vars
"""

from typing import Callable, Any

def static_vars(**kwargs):
  def function_with_static_args(func):
    for key in kwargs:
      setattr(func, key, kwargs[key])
    return func
  return function_with_static_args


def zipwith(func: Callable[..., Any], *args):
  return map(lambda a: func(*a), zip(*args)) 

def ident(x):
  return x

def compose(*funcs):
  def compose_decorator(unused):
    def composed_function(*args, **kwargs):
      func_iterator = reversed(funcs)
      ret = next(func_iterator)(*args, **kwargs)
      for f in func_iterator:
        ret = f(ret)
      return ret
    return composed_function
  return compose_decorator


