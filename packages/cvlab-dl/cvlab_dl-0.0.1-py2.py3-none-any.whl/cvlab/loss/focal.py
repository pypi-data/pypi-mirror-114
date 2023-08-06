"""This module provides implementation of focal loss.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class FocalLoss(nn.Module):
  """Focal cross entropy loss.
  """

  def __init__(self,
               alpha=1,
               gamma=0,
               size_average=True,
               ignore_index=255):
    super(FocalLoss, self).__init__()
    self.alpha = alpha
    self.gamma = gamma
    self.ignore_index = ignore_index
    self.size_average = size_average

  def forward(self, inputs: torch.FloatTensor, targets: torch.LongTensor):
    """Forward pass.

    Args:
      inputs: Model output of shape NCHW, float, can be either normalized or not
      targets: Grondtruth label, LongTensor of shape NHW.
    """
    ce_loss = F.cross_entropy(inputs,
                              targets,
                              reduction='none',
                              ignore_index=self.ignore_index)
    pt = torch.exp(-ce_loss)
    focal_loss = self.alpha * (1 - pt)**self.gamma * ce_loss
    if self.size_average:
      return focal_loss.mean()
    else:
      return focal_loss.sum()
