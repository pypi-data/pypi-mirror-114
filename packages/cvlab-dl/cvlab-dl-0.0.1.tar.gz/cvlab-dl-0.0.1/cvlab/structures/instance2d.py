"""This module holds data structure of 2D object instances.
"""
from .common import BoxFormat, _GeometryObjBase
from ..common.visualization import draw_instances


class Instance2D(_GeometryObjBase):
  _attrs = ['class_name', 'class_id', 'score', 'box', 'fmt']

  def visualize(self, image, color=None):
    """Visualize self on image.
    """
    return draw_instances(image, [self], color=color)

  @staticmethod
  def _xywh2xyxy(box):
    """Convert XYWH_* box to XYXY_* box.

    Args:
      box (list of float): Bounding box.
    """
    return [box[0], box[1], box[0] + box[2], box[1] + box[3]]

  @staticmethod
  def _xcycwh2xyxy(box):
    """Convert XcYcWH_* box to XYXY_* box.

    Args:
      box (list of float): Bounding box.
    """
    box = [box[0] - box[2] / 2, box[1] - box[3] / 2, box[2], box[3]]
    box[2] += box[0]
    box[3] += box[1]
    return box

  @staticmethod
  def _xyxy2xywh(box):
    """Convert XYXY_* box to XYWH_* box.

    Args:
      box (list of float): Bounding box.
    """
    return [box[0], box[1], box[2] - box[0], box[3] - box[1]]

  @staticmethod
  def _xyxy2xcycwh(box):
    """Convert XYXY_* box to XcYcWH_* box.

    Args:
      box (list of float): Bounding box.
    """
    box = [box[0], box[1], box[2] - box[0], box[3] - box[1]]
    box[0] += box[2] / 2
    box[1] += box[3] / 2
    return box

  def convert_to(self, fmt, image_size=None):
    """Returns an instance with `fmt`.

    Args:
      fmt (str): The dest format.
      image_size (str): Conversion between *_REL box requires this arg.
    """
    if BoxFormat.is_same(self.fmt, fmt):
      return self
    if (BoxFormat.is_rel(self.fmt) or
        BoxFormat.is_rel(fmt)) and not BoxFormat.is_same_coord(self.fmt, fmt):
      if image_size is None:
        raise ValueError(
            'You must specify image_size to convert between REL and other types'
        )

    # Convert the box to XYXY_* fmt
    self_boxtype = self.fmt.split('_')[0].lower()
    to_boxtype = fmt.split('_')[0].lower()
    if self_boxtype != 'xyxy':
      box = getattr(self, f'_{self_boxtype}2xyxy')(self.box)
    else:
      box = self.box
    # Convert to another type
    if to_boxtype != 'xyxy':
      box = getattr(self, f'_xyxy2{to_boxtype}')(box)

    # Convert between REL and ABS
    if BoxFormat.is_rel(self.fmt) and BoxFormat.is_abs(fmt):
      box[0] *= image_size[0]
      box[1] *= image_size[1]
      box[2] *= image_size[0]
      box[3] *= image_size[1]
    elif BoxFormat.is_abs(self.fmt) and BoxFormat.is_rel(fmt):
      box[0] /= image_size[0]
      box[1] /= image_size[1]
      box[2] /= image_size[0]
      box[3] /= image_size[1]

    return Instance2D(class_name=self.class_name,
                      class_id=self.class_id,
                      score=self.score,
                      box=box,
                      fmt=fmt)
