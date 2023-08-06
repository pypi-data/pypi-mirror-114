"""Common utilities.
"""
import hashlib
import os
import random
import string
from typing import Union

import torch


def randstr(length):
  """Generates random string.
  """
  return ''.join(random.sample(string.ascii_lowercase, length))


def md5(str, length=0):
  """Generates hash for str, return first `length` letters.
  """
  md5 = hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()
  if length == 0:
    return md5
  return md5[:length]


def manual_seed_all(seed):
  """Manual seeds random algorithms for reproducibility. This function will seed
  random, numpy and torch if possible.

  Args:
    seed (int): The random seed to use.
  """
  random.seed(seed)

  try:
    import numpy as np
    np.random.seed(seed)
  except ImportError:
    pass

  try:
    import torch
    torch.manual_seed(seed)
  except ImportError:
    pass


def to_markdown(listOfDicts):
  """Loop through a list of dicts and return a markdown table as a multi-line
  string.

  Args:
    listOfDicts -- A list of dictionaries, each dict is a row
  """
  markdowntable = ""
  # Make a string of all the keys in the first dict with pipes before after and
  # between each key
  markdownheader = '| ' + ' | '.join(map(str, listOfDicts[0].keys())) + ' |'
  # Make a header separator line with dashes instead of key names
  markdownheaderseparator = '|-----' * len(listOfDicts[0].keys()) + '|'
  # Add the header row and separator to the table
  markdowntable += markdownheader + '\n'
  markdowntable += markdownheaderseparator + '\n'
  # Loop through the list of dictionaries outputting the rows
  for row in listOfDicts:
    markdownrow = ""
    for key, col in row.items():
      markdownrow += '| ' + str(col) + ' '
    markdowntable += markdownrow + '|' + '\n'
  return markdowntable


def recursive_glob(root_dir, suffix=''):
  """Recursively finds specific suffix format data under root directory.

  Args:
    root_dir (str): Root directory to search for.
    suffix (str): Specific suffix pattern, e.g. '.json'.
  """
  assert os.path.isdir(root_dir), f'{root_dir} is not a dir!'
  assert isinstance(suffix, str)

  return [
      os.path.join(folder, filename)
      for folder, _, filenames in os.walk(root_dir)
      for filename in filenames
      if filename.endswith(suffix)
  ]


def to_cuda(data: Union[torch.Tensor, dict, list, tuple],
            device=0) -> Union[torch.Tensor, dict, list, tuple]:
  """Move data to CUDA.

  Args:
    data: Original data, can be either torch Tensor, dict, list of Tensor or
    tuple of tensor.
    device: The cuda device to move to.
  """
  if isinstance(data, torch.Tensor):
    return data.cuda(device)
  elif isinstance(data, dict):
    for k, v in data.items():
      if isinstance(v, torch.Tensor):
        data[k] = v.cuda(device)
  elif isinstance(data, (list, tuple)):
    for i, item in enumerate(data):
      if isinstance(item, torch.Tensor):
        data[i] = item.cuda(device)
  return data
