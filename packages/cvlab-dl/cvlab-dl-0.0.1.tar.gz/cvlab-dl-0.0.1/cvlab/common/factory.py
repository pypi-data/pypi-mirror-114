"""Util for dynamic importing and building objects.
"""
import importlib
from typing import Any, Union, Tuple


def dynamic_import(module_path: str) -> Any:
  """Import module by `module_path` like `models.detector.YOLO`.

  Args:
    module_path (str): The absolute module path.

  Returns:
    The module class specified by `module_path`.
  """
  names = module_path.split('.')
  module = '.'.join(names[:-1])
  name = names[-1]
  return getattr(importlib.import_module(module), name)


def object_from_dict(cls_conf: dict) -> Any:
  """Constructs instance of certain type based on `cls_conf`.

  Args:
    cls_conf: The config for constructing instances. `Type`, `Args` and `KwArgs`
    should be contained.

  Return:
    An instance.
  """
  if 'Type' not in cls_conf:
    return None
  cls = cls_conf['Type']
  if isinstance(cls, str):
    cls = dynamic_import(cls)
  return cls(*cls_conf.get('Args', []), **cls_conf.get('KwArgs', {}))


def findattr(obj, path: Union[str, Tuple[str]]) -> Any:
  """Get the attr of obj specified by `path`.
  """
  if isinstance(path, str):
    path = path.strip().split('.')
  for name in path:
    if not name:
      continue
    obj = getattr(obj, name)
  return obj
