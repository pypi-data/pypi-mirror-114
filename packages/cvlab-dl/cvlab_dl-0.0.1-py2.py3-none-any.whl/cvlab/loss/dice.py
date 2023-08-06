"""This module provides implementation for DiceLoss on PyTorch. Borrowed from
https://kornia.readthedocs.io/en/v0.1.2/_modules/torchgeometry/losses/dice.html
"""

from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


def one_hot(labels: torch.LongTensor,
            num_classes: int,
            device: Optional[torch.device] = None,
            dtype: Optional[torch.dtype] = None,
            eps: Optional[float] = 1e-6) -> torch.Tensor:
  """Converts an integer label 2D tensor to a one-hot 3D tensor.

  Args:
      labels (torch.Tensor) : tensor with labels of shape :math:`(N, H, W)`,
                              where N is batch siz. Each value is an integer
                              representing correct classification.
      num_classes (int): number of classes in labels.
      device (Optional[torch.device]): the desired device of returned tensor.
        Default: if None, uses the current device for the default tensor type
        (see torch.set_default_tensor_type()). device will be the CPU for CPU
        tensor types and the current CUDA device for CUDA tensor types.
      dtype (Optional[torch.dtype]): the desired data type of returned
        tensor. Default: if None, infers data type from values.

  Returns:
      torch.Tensor: the labels in one hot tensor.

  Examples::
      >>> labels = torch.LongTensor([[[0, 1], [2, 0]]])
      >>> one_hot(labels, num_classes=3)
      tensor([[[[1., 0.],
                [0., 1.]],
                [[0., 1.],
                [0., 0.]],
                [[0., 0.],
                [1., 0.]]]]
  """
  if not torch.is_tensor(labels):
    raise TypeError("Input labels type is not a torch.Tensor. Got {}".format(
        type(labels)))
  if not len(labels.shape) == 3:
    raise ValueError("Invalid depth shape, we expect BxHxW. Got: {}".format(
        labels.shape))
  if not labels.dtype == torch.int64:
    raise ValueError(
        "labels must be of the same dtype torch.int64. Got: {}".format(
            labels.dtype))
  if num_classes < 1:
    raise ValueError("The number of classes must be bigger than one."
                     " Got: {}".format(num_classes))
  batch_size, height, width = labels.shape
  one_hot = torch.zeros(batch_size,
                        num_classes,
                        height,
                        width,
                        device=device,
                        dtype=dtype)
  return one_hot.scatter_(1, labels.unsqueeze(1), 1.0) + eps


class DiceLoss(nn.Module):
  """Criterion that computes Sørensen-Dice Coefficient loss.

  Shape:
      - Input: :math:`(N, C, H, W)` where C = number of classes.
      - Target: :math:`(N, H, W)` where each value is
        :math:`0 ≤ targets[i] ≤ C−1`.

  Examples:
      >>> N = 5  # num_classes
      >>> loss = tgm.losses.DiceLoss()
      >>> input = torch.randn(1, N, 3, 5, requires_grad=True)
      >>> target = torch.empty(1, 3, 5, dtype=torch.long).random_(N)
      >>> output = loss(input, target)
      >>> output.backward()
  """

  def __init__(self) -> None:
    super(DiceLoss, self).__init__()
    self.eps: float = 1e-6

  def forward(self, input: torch.FloatTensor,
              target: torch.LongTensor) -> torch.FloatTensor:
    """Forward pass.

    Args:
      input: The input tensor of shape NCHW, will be normalized by `softmax`
      along dim 1 internally.
      target: The target tensor of shape NHW, it is expected to be LongTensor
      indicating the class id of each pixel.
    """

    if not torch.is_tensor(input):
      raise TypeError("Input type is not a torch.Tensor. Got {}".format(
          type(input)))
    if not len(input.shape) == 4:
      raise ValueError("Invalid input shape, we expect BxNxHxW. Got: {}".format(
          input.shape))
    if not input.shape[-2:] == target.shape[-2:]:
      raise ValueError(
          "input and target shapes must be the same. Got: {} and {}".format(
              input.shape, input.shape))
    if not input.device == target.device:
      raise ValueError(
          "input and target must be in the same device. Got: {} and {}".format(
              input.device, target.device))
    # compute softmax over the classes axis
    input_soft = F.softmax(input, dim=1)

    # create the labels one hot tensor
    target_one_hot = one_hot(target,
                             num_classes=input.shape[1],
                             device=input.device,
                             dtype=input.dtype)

    # compute the actual dice score
    dims = (1, 2, 3)
    intersection = torch.sum(input_soft * target_one_hot, dims)
    cardinality = torch.sum(input_soft + target_one_hot, dims)

    dice_score = 2. * intersection / (cardinality + self.eps)
    return torch.mean(1. - dice_score)


def dice_loss(input: torch.FloatTensor,
              target: torch.LongTensor) -> torch.Tensor:
  """Function that computes Sørensen-Dice Coefficient loss. See `DiceLoss` for
  details.
  """
  return DiceLoss()(input, target)
