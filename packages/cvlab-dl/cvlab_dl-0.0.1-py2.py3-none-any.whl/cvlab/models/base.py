"""This module provides basic interface for PyTorch model.
"""
import logging
from collections import OrderedDict
from typing import Union

import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter

from ..common.factory import findattr


class _BaseModel(nn.Module):

  def freeze(self, submodule: str):
    """Freeze submodule so it will not update during training

    Args:
      submodule (str): The name of submodule
    """
    submodule = findattr(self, submodule)
    for param in submodule.parameters():
      param.requires_grad = False

  def unfreeze(self, submodule: str):
    """Unfreeze submodule so it can update during training.

    Args:
      submodule (str): The name of submodule.
    """
    submodule = getattr(self, submodule)
    for param in submodule.parameters():
      param.requires_grad = True

  def make_state_dict(self) -> dict:
    """Returns state dict of model params and necessary metadata. This model can
    be fully restored with this dict.

    Returns:
      state_dict (Dict): Should contain `model` and `args` entry. `model` should
      be the state dict of params, and `args` should be all kwargs to construct
      the model.
    """
    raise NotImplementedError

  @staticmethod
  def search_weights(state_dict: dict) -> OrderedDict:
    """Search model weights in `state_dict`
    """
    if isinstance(state_dict, OrderedDict):
      return state_dict
    elif isinstance(state_dict, dict):
      for v in state_dict.values():
        if isinstance(v, OrderedDict):
          return v
        elif isinstance(v, dict):
          return _BaseModel.search_weights(v)
    return None

  @classmethod
  def from_state_dict(cls,
                      state_dict: Union[dict, str],
                      map_location='cpu',
                      logger: Union[logging.Logger, None] = None):
    """Restore an object from `state_dict`.

    Args:
      state_dict : Can be a str to checkpoint file, or the state dict it self.
      See the output of `make_state_dict`.
      map_location (str): Where to put the params if we load state_dict from
      disk.
      logger: Logger instance.

    Returns:
      An instance of `cls`, with params and metadata in `state_dict`.
    """
    if isinstance(state_dict, str):
      if logger:
        logger.info('Loading state dict from {}'.format(state_dict))
      state_dict = torch.load(state_dict, map_location=map_location)['model']
    if logger:
      logger.info('Loading model from state dict')
    model = cls(**state_dict['args'])
    ret = model.load_state_dict(state_dict['weights'], strict=False)
    if logger:
      logger.info(str(ret))
    return model

  def evaluate(self,
               dataloader: torch.utils.data.DataLoader,
               iter: int,
               logger: Union[logging.Logger, None] = None,
               writer=None):
    """Evaluate this model on dataloader. The signature of this function should
    be remained as this in subclasses.

    Args:
      dataloader: The dataloader.
      iter (int): Current interation.
      logger (Logger): The logger to write logs.
      writer (SummaryWriter): The tensorboard writer.
    """
    raise NotImplementedError

  def summary(self,
              iter: int,
              logger: Union[logging.Logger, None] = None,
              writer: Union[SummaryWriter, None] = None):
    """Summary intermediate status to `logger` and `writer`.

    Args:
      iter: Current iter.
      logger: The logger.
      writer: The writer.
    """
    raise NotImplementedError
