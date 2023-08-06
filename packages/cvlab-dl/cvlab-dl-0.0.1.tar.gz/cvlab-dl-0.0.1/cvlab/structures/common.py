"""Basic data structures representing geometry shapes.
"""


class _GeometryObjBase:
  """Most base class for geometry shapes.
  """
  _attrs = []

  def __init__(self, *args, **kwargs):
    """Construct self and init attributes based on args and kwargs.
    """
    for attr in self._attrs:
      self.__dict__[attr] = None
    assert len(args) <= len(self._attrs)
    for i, attr in enumerate(args):
      self.__dict__[self._attrs[i]] = attr
    self.__dict__.update(kwargs)

  def visualize(self, image, color):
    """Draw this shape on the image, need implementation in subclasses.
    """
    raise NotImplementedError


class BoxFormat:
  """Class representing the format of axis-aligned bounding boxes.
  """

  XYXY_ABS = 'XYXY_ABS'  # Absolute x_min, y_min, x_max, y_max coords on image
  XYXY_REL = 'XYXY_REL'  # Relative (normalized by image size) XYXY coords
  XYWH_ABS = 'XYWH_ABS'  # x_min, y_min, width, height, absolute
  XYWH_REL = 'XYWH_REL'  # x_min, y_min, width, height, relative
  XcYcWH_ABS = 'XcYcWH_ABS'  # x_center, y_center, width, height, absolute
  XcYcWH_REL = 'XcYcWH_REL'  # x_center, y_center, width, height, relative

  @classmethod
  def all(cls):
    return [
        cls.XYXY_ABS, cls.XYXY_REL, cls.XYWH_ABS, cls.XYWH_REL, cls.XcYcWH_ABS,
        cls.XcYcWH_REL
    ]

  @staticmethod
  def is_same(fmt1, fmt2):
    return fmt1.upper() == fmt2.upper()

  @staticmethod
  def is_abs(fmt):
    return fmt.upper().split('_')[-1] == 'ABS'

  @staticmethod
  def is_rel(fmt):
    return fmt.upper().split('_')[-1] == 'REL'

  @staticmethod
  def is_same_coord(fmt1, fmt2):
    """Returns if two formats has the same coord type: both ABS or both REL.
    """
    return fmt1.upper().split('_')[-1] == fmt2.upper().split('_')[-1]
