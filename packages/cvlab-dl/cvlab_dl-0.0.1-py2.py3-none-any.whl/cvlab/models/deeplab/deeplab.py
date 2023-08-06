import os
from collections import OrderedDict
from typing import List, Union

import cv2
import numpy as np
import torch
from PIL import Image
from torch import nn

from ...common.utils import to_markdown
from ...common.visualization import (visualize_confmat, visualize_label_image,
                                     overlay_label_image)
from ...loss import FocalLoss, DiceLoss
from ...metrics.classification import ConfusionMatrix
from ..base import _BaseModel
from .modeling import *  # noqa


class DeeplabV3(_BaseModel):
  """DeeplabV3 model warpper for cvlab.

  Attributes:
    _preds (dict): Cache the intermediate results for analyze.
    _targets (dict): Cache the intermediate results for analyze.
    _loss_dict (dict): Cache the intermediate results for analyze.
    _confmat (ConfusionMatrix): Confusion matrix.
  """
  _preds = None
  _targets = None
  _loss_dict = {}
  _confmat = None

  def __init__(self,
               classes: List[str] = ['BG', 'FG'],
               backbone: str = 'resnet101',
               variant: str = ' v3plus',
               output_stride: int = 8,
               separable_conv: bool = False,
               pretrained: Union[bool, str] = True,
               loss_weights: Union[list, tuple, None] = None,
               logger=None):
    """Constructs self.

    Args:
      classes (list): The classes of the segmentation task including background.
      backbone (str): The backbone of the model, `resnet50` or `resnet101` or
      `mobilenet`.
      variant (str): The variant of Deeplab model, `v3` or `v3plus`.
      output_stride (int): The output stride of model.
      separable_conv (bool): Use separable convolution for v3+ variants.
      pretrained (bool or str): Load pretrained weights from torchvision or
      local file.
      logger (Logger): The logger.
    """

    super(DeeplabV3, self).__init__()

    self.classes = classes
    self.backbone = backbone
    self.variant = variant
    self.output_stride = output_stride
    self.separable_conv = separable_conv

    if logger:
      logger.info('Building deeplab{} with {}, os {}'.format(
          variant, backbone, output_stride))

    _model_func = f'deeplab{variant}_{backbone}'
    try:
      _model_func = eval(_model_func)
    except Exception:
      raise NotImplementedError('{} not supported yet'.format(_model_func))

    # Load pretrained weights from local file or URL
    if isinstance(pretrained, str):
      self.deeplab = _model_func(len(classes), output_stride, False)
      try:
        # Search for the model weights in state_dict
        state_dict = torch.load(pretrained, map_location='cpu')
        weights = self.search_weights(state_dict)
        if weights is not None:
          if list(weights.keys())[0].startswith('deeplab'):
            ret = self.load_state_dict(weights, strict=False)
          else:
            ret = self.deeplab.load_state_dict(weights, strict=False)
          if logger:
            logger.info(str(ret))
        elif logger:
          logger.warning('No model weights in {}'.format(pretrained))
      except Exception as e:
        if logger:
          logger.warning(str(e))
    elif pretrained:
      # Only load pretrained backbone
      self.deeplab = _model_func(len(classes), output_stride, True)
    else:
      # No pretrained weights
      self.deeplab = _model_func(len(classes), output_stride, False)

    if separable_conv and 'plus' in variant:
      convert_to_separable_conv(self.deeplab.classifier)  # noqa

    # Construct loss function
    if loss_weights is not None:
      loss_weights = torch.Tensor(loss_weights)

    self.ce_loss = nn.CrossEntropyLoss(weight=loss_weights,
                                       ignore_index=255,
                                       reduction='mean')
    self.focal_loss = FocalLoss(alpha=0.25,
                                gamma=2,
                                ignore_index=255,
                                size_average=True)
    self.dice_loss = DiceLoss()

  def make_state_dict(self):
    """Returns state dict of model params and necessary metadata. This model can
    be fully restored with this dict.

    Returns:
      state_dict (Dict).
    """
    return {
        'weights': self.state_dict(),
        'args': {
            'classes': self.classes,
            'backbone': self.backbone,
            'variant': self.variant,
            'output_stride': self.output_stride,
            'separable_conv': self.separable_conv
        }
    }

  def evaluate(self,
               dataloader,
               iter,
               logger=None,
               writer=None,
               output_dir=None):
    """Validate this model on dataloader.
    """
    self.eval()
    device = next(self.parameters()).device
    mat = ConfusionMatrix(n_classes=len(self.classes))

    for i, (images, targets) in enumerate(dataloader):
      images = images.to(device)

      preds = self(images)  # NHW, LongTensor
      mat.update(
          preds.detach().cpu().numpy().reshape(-1),
          targets.numpy().reshape(-1),
      )

      metrics = {
          'Precision': mat.p_cls().mean() * 100,  # Skip background
          'Recall': mat.r_cls().mean() * 100,
          'IoU': mat.iou_cls().mean() * 100
      }
      logstr = ', '.join([f'{k}: {v}' for k, v in metrics.items()])

      if logger:
        logger.info('Eval {}/{}: {}'.format(i + 1, len(dataloader), logstr))

    # Overall performance
    metrics = [
        OrderedDict(Class='Total',
                    Samples=mat.num_samples().sum(),
                    Precision='{:.2f}'.format(mat.p_mean() * 100),
                    Recall='{:.2f}'.format(mat.r_mean() * 100),
                    F1='{:.2f}'.format(mat.f1_mean() * 100),
                    IoU='{:.2f}'.format(mat.iou_mean() * 100)),
    ]

    # Per-class performance
    for idx, class_name in enumerate(self.classes):
      metrics.append(
          OrderedDict(Class=f'{idx}-{class_name}',
                      Samples=mat.num_samples()[idx],
                      Precision='{:.2f}'.format(mat.p_cls()[idx] * 100),
                      Recall='{:.2f}'.format(mat.r_cls()[idx] * 100),
                      F1='{:.2f}'.format(mat.f1_cls()[idx] * 100),
                      IoU='{:.2f}'.format(mat.iou_cls()[idx] * 100)))

    if logger:
      for entry in metrics:
        log_str = ', '.join([f'{k}: {v}' for k, v in entry.items()])
        logger.info(log_str)

    if writer:
      writer.add_scalars(
          'Val/Metric/All', {
              'Precision': mat.p_mean() * 100,
              'Recall': mat.r_mean() * 100,
              'IoU': mat.iou_mean() * 100
          }, iter)
      # Per-class metric
      for i, cls in enumerate(self.classes):
        if i == 0:
          continue
        writer.add_scalars(
            f'Val/Metric/{cls}', {
                'Precision': mat.p_cls()[i] * 100,
                'Recall': mat.r_cls()[i] * 100,
                'IoU': mat.iou_cls(i)[i] * 100
            }, iter)

    if output_dir is not None:
      # Write results to output dir
      with open(os.path.join(output_dir, 'stats.md'), 'w+') as f:
        print(to_markdown(metrics), file=f)

      # Visualize confusion matrix
      v = visualize_confmat(mat.confmat, class_names=self.classes, fig_size=16)
      Image.fromarray(v).save(os.path.join(output_dir, 'ConfusionMatrix.png'))

  def summary(self, writer, iter):
    """Summary intermediate status.

    Args:
      writer (tensorboard.SummaryWriter): The writer.
      iter (int): Current iter.
    """
    # Log loss value
    for k, loss_list in self._loss_dict.items():
      avg_loss = sum(loss_list) / (len(loss_list) + 1e-16)
      writer.add_scalar(f'Train/{k}', avg_loss, iter)

    # Build visualization of this batch, max width is 1920
    preds = torch.argmax(self._preds, dim=1).numpy()
    targets = self._targets.squeeze_().numpy()
    images = self._images.numpy()

    rendered = []
    for image, pred, target in zip(images, preds, targets):
      # Recover original image
      image = np.transpose(image, (1, 2, 0))
      H, W = image.shape[:2]
      image = image.reshape(-1, 3) * np.array(
          [0.229, 0.224, 0.225]) * 255 + 255 * np.array([0.485, 0.456, 0.406])
      np.clip(image, 0, 255, out=image)
      image = image.astype(np.uint8).reshape(H, W, 3)

      # Visualize predicted label image
      pred = visualize_label_image(pred, len(self.classes))

      # Visualize target label image
      target = visualize_label_image(target, len(self.classes))

      # Visualize overlayed label image
      overlay = overlay_label_image(image, pred)

      # Compose these images
      sample = np.concatenate([image, target, pred, overlay], axis=0)
      rendered.append(sample)

    rendered = np.concatenate(rendered, axis=1)
    if rendered.shape[1] > 8192:
      new_w = 8192
      new_h = int(rendered.shape[0] * new_w / rendered.shape[1])
      rendered = cv2.resize(rendered, (new_w, new_h))
    writer.add_image('Train/Image', rendered, iter, dataformats='HWC')

  def forward(self, images, targets=None, loss_conf={}):
    preds = self.deeplab(images)

    # Save this batch
    self._images = images.cpu()  # FloatTensor
    self._preds = preds.detach().cpu().float()  # FloatTensor
    if targets is not None:
      self._targets = targets.cpu()  # LongTensor

    if targets is not None:
      loss = OrderedDict()
      if 'focal' in loss_conf.get('Includes', []):
        loss['focal'] = self.focal_loss(preds, targets.squeeze())
      if 'ce' in loss_conf.get('Includes', []):
        loss['ce'] = self.ce_loss(preds, targets.squeeze())
      if 'dice' in loss_conf.get('Includes', []):
        loss['dice'] = self.dice_loss(preds, targets.squeeze())

      assert len(loss_conf['Includes']) == len(loss_conf['Weights'])
      total_loss = 0
      for loss_name, weight in zip(loss_conf['Includes'], loss_conf['Weights']):
        total_loss += weight * loss[loss_name]

      loss['total'] = total_loss

      # Accumulate loss values of this logging period
      for k, v in loss.items():
        self._loss_dict.setdefault(k, []).append(v.detach().item())

      return loss['total']

    return torch.argmax(preds, dim=1)  # LongTensor
