"""This module provides utils for data transformation.
"""
from numbers import Number
from typing import Union, List

import cv2
import numpy as np
from PIL import Image, ImageEnhance
from shapely import affinity
from shapely.geometry import MultiPoint


def adjust_brightness(img: np.ndarray, brightness_factor: float) -> np.ndarray:
  """Adjust brightness of an image, RGB or BGR or grayscale.

  Args:
    img (numpy ndarray): numpy ndarray to be adjusted.
    brightness_factor (float):  How much to adjust the brightness. Can be
        any non negative number. 0 gives a black image, 1 gives the
        original image while 2 increases the brightness by a factor of 2.

  Returns:
    numpy ndarray: Brightness adjusted image.
  """
  table = np.array([i * brightness_factor for i in range(0, 256)
                   ]).clip(0, 255).astype('uint8')
  if img.ndim == 2 or img.shape[2] == 1:
    return cv2.LUT(img, table)[:, :, np.newaxis]
  else:
    return cv2.LUT(img, table)


def adjust_contrast(img: np.ndarray, contrast_factor: float) -> np.ndarray:
  """Adjust contrast of an image, BGR or RGB or grayscale.

  Args:
    img (numpy ndarray): numpy ndarray to be adjusted.
    contrast_factor (float): How much to adjust the contrast. Can be any
    non negative number. 0 gives a solid gray image, 1 gives the
    original image while 2 increases the contrast by a factor of 2.

  Returns:
    numpy ndarray: Contrast adjusted image.
  """
  mean_value = round(np.mean(img))
  table = np.array([
      (i - mean_value) * contrast_factor + mean_value for i in range(0, 256)
  ]).clip(0, 255).astype('uint8')
  if img.ndim == 2 or img.shape[2] == 1:
    return cv2.LUT(img, table)[:, :, np.newaxis]
  else:
    return cv2.LUT(img, table)


def adjust_saturation(img: np.ndarray, saturation_factor: float) -> np.ndarray:
  """Adjust color saturation of an image, RGB only.

  Args:
    img (numpy ndarray): numpy ndarray to be adjusted.
    saturation_factor (float):  How much to adjust the saturation. 0 will
    give a black and white image, 1 will give the original image while
    2 will enhance the saturation by a factor of 2.

  Returns:
    numpy ndarray: Saturation adjusted image.
  """
  img = Image.fromarray(img)
  enhancer = ImageEnhance.Color(img)
  img = enhancer.enhance(saturation_factor)
  return np.array(img)


def adjust_hue(img: np.ndarray, hue_factor: float) -> np.ndarray:
  """Adjust hue of an image, RGB only.
    The image hue is adjusted by converting the image to HSV and
    cyclically shifting the intensities in the hue channel (H).
    The image is then converted back to original image mode.
    `hue_factor` is the amount of shift in H channel and must be in the
    interval `[-0.5, 0.5]`.
    See `Hue`_ for more details.
    .. _Hue: https://en.wikipedia.org/wiki/Hue

  Args:
    img (numpy ndarray): numpy ndarray to be adjusted.
    hue_factor (float): How much to shift the hue channel. Should be in
    [-0.5, 0.5]. 0.5 and -0.5 give complete reversal of hue channel in
    HSV space in positive and negative direction respectively.
    0 means no shift. Therefore, both -0.5 and 0.5 will give an image
    with complementary colors while 0 gives the original image.

  Returns:
    numpy ndarray: Hue adjusted image.
    """
  if not (-0.5 <= hue_factor <= 0.5):
    raise ValueError('hue_factor {} is not in [-0.5, 0.5].'.format(hue_factor))
  img = Image.fromarray(img)
  input_mode = img.mode
  if input_mode in {'L', '1', 'I', 'F'}:
    return np.array(img)
  h, s, v = img.convert('HSV').split()
  np_h = np.array(h, dtype=np.uint8)
  # uint8 addition take cares of rotation across boundaries
  with np.errstate(over='ignore'):
    np_h += np.uint8(hue_factor * 255)
  h = Image.fromarray(np_h, 'L')
  img = Image.merge('HSV', (h, s, v)).convert(input_mode)
  return np.array(img)


class _Transform:
  """Generic transformation class. Transforms should be considered inplace
  operators generally, so users should take care of the underlying data change.
  """

  def apply_image(self, image: np.ndarray) -> np.ndarray:
    """Apply this transformation to `image`, by default it's a no-op. Should be
    implemented in subclasses. This method is intended for general images.
    """
    return image

  def undo_image(self, image: np.ndarray) -> np.ndarray:
    """Undo this transformation to `image`, by default it's a no-op. Should be
    implemented in subclasses. This method is intended for general images.
    """
    return image

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    """Apply this transformation to label image, by default it's a no-op. This
    method is intended for label images that are commonly used in segmentation
    tasks, with pixel values correspond to the class id they belong to.
    """
    return image

  def undo_label_image(self, image: np.ndarray) -> np.ndarray:
    """Undo this transformation to label image, by default it's a no-op. This
    method is intended for label images that are commonly used in segmentation
    tasks, with pixel values correspond to the class id they belong to.
    """
    return image

  def apply_points(self, points: np.ndarray) -> np.ndarray:
    """Apply this transformation to `points`, by default it's a no-op. Should be
    implemented in subclasses. This method is intended for points with shape
    (N, 2).
    """
    return points

  def undo_points(self, points: np.ndarray) -> np.ndarray:
    """Undo this transformation to `points`, by default it's a no-op. Should be
    implemented in subclasses. This method is intended for points with shape
    (N, 2).
    """
    return points


class Normalize(_Transform):
  """Normalize image with mean and std: image = (image - mean) / std. Has no
  effect on points and label images.
  """

  def __init__(self, mean: Union[tuple, float], std: Union[tuple, float]):
    self.mean = [mean] if isinstance(mean, float) else mean
    self.std = [std] if isinstance(std, float) else std
    assert len(self.mean) in (1, 3) and len(self.std) in (1, 3)

  def apply_image(self, image: np.ndarray) -> np.ndarray:
    """Image can be either grascale or 3-channel.
    """
    H, W = image.shape[:2]
    ch = image.shape[-1] if image.ndim == 3 else 1
    if ch != 1 and ch != 3:
      raise ValueError(f'We do not support {ch} channel image now!')
    if ch == 3 and len(self.mean) == 1:
      mean = self.mean * 3
      std = self.std * 3
    else:
      mean = self.mean
      std = self.std
    image = image.astype(np.float).reshape(-1, ch)
    image = (image - mean) / std
    return image.reshape(H, W) if ch == 1 else image.reshape(H, W, ch)

  def undo_image(self, image: np.ndarray) -> np.ndarray:
    H, W = image.shape[:2]
    ch = image.shape[-1] if image.ndim == 3 else 1
    if ch != 1 and ch != 3:
      raise ValueError(f'We do not support {ch} channel image now!')
    if ch == 3 and len(self.mean) == 1:
      mean = self.mean * 3
      std = self.std * 3
    else:
      mean = self.mean
      std = self.std
    image = image.astype(np.float).reshape(-1, ch)
    image = image * std + mean
    return image.reshape(H, W) if ch == 1 else image.reshape(H, W, ch)


class ColorJitter(_Transform):
  """Apply color jitter to image. Has no effect on points and label images. This
  transformation is irreversible, so the undo-* methods does nothing.
  """

  def __init__(self,
               brightness: Union[tuple, list, None] = None,
               contrast: Union[tuple, list, None] = None,
               saturation: Union[tuple, list, None] = None,
               hue: Union[tuple, list, None] = None):
    """Constructs self.

    Args:
      brightness: Adjust image brightness by random factor in (brightness[0],
      brightness[1]).
      contrast: Adjust image contrast by random factor in (contrast[0],
      contrast[1]).
      saturation: Adjust image saturation by random factor in (saturation[0],
      saturation[1]).
      hue: Adjust image hue by random factor in (hue[0], hue[1]).
    """
    self.brightness = brightness
    self.contrast = contrast
    self.saturation = saturation
    self.hue = hue

  def apply_image(self, image: np.ndarray) -> np.ndarray:
    if self.brightness is not None:
      factor = np.random.uniform(*self.brightness)
      image = adjust_brightness(image, factor)

    if self.contrast is not None:
      factor = np.random.uniform(*self.contrast)
      image = adjust_contrast(image, factor)

    if self.saturation is not None:
      factor = np.random.uniform(*self.saturation)
      image = adjust_saturation(image, factor)

    if self.hue is not None:
      factor = np.random.uniform(*self.hue)
      image = adjust_hue(image, factor)

    return image


class Scale(_Transform):
  """Scales the image to certain size.
  """

  def __init__(self,
               original_size: Union[tuple, list],
               to_size: Union[tuple, list],
               interp=cv2.INTER_LINEAR):
    """Constructs self.

    Args:
      original_size: The original size of image, (W, H).
      to_size: The scaled size of image (W, H).
      interp: Interpolation method.
    """
    self.original_size = tuple(original_size)
    self.to_size = tuple(to_size)
    self.interp = interp

  def apply_image(self, image: np.ndarray, interp=None) -> np.ndarray:
    """Apply transformation on image. Use `interp` to override `self.interp`.
    """
    interp = interp if interp is not None else self.interp
    return cv2.resize(image, self.to_size, interpolation=interp)

  def undo_image(self, image: np.ndarray, interp=None) -> np.ndarray:
    """Undo the transformation. Use `interp` to override `self.interp`.
    """
    interp = interp if interp is not None else self.interp
    return cv2.resize(image, self.original_size, interpolation=interp)

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    """Apply the transformation on image, but with label images, we use nearest
    interpolation.
    """
    return self.apply_image(image, interp=cv2.INTER_NEAREST)

  def undo_label_image(self, image: np.ndarray) -> np.ndarray:
    """Undo the transformation on image, but with label images, we use nearest
    interpolation.
    """
    return self.undo_image(image, interp=cv2.INTER_NEAREST)

  def apply_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    x_factor = self.to_size[0] / self.original_size[0]
    y_factor = self.to_size[1] / self.original_size[1]
    points[:, 0] *= x_factor
    points[:, 1] *= y_factor
    return points

  def undo_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    x_factor = self.original_size[0] / self.to_size[0]
    y_factor = self.original_size[1] / self.to_size[1]
    points[:, 0] *= x_factor
    points[:, 1] *= y_factor
    return points


class RandomScale(_Transform):
  """Randomly scales the objects, this is irreversible, so the `undo_*` method
  does nothing. We follow the same calling convention as `RandomRotate`.
  """

  def __init__(self,
               scale_range: Union[list, tuple] = (0.5, 2),
               keep_shape=True,
               interp=cv2.INTER_LINEAR):
    """Construct self.

    Args:
      scale_range: Scale the imgae by a random factor in this range.
      keep_shape: Keep original shape by center cropping or padding.
    """
    self.scale_range = tuple(scale_range)
    self.keep_shape = keep_shape
    self.interp = interp
    self._last_factor = 1
    self._last_ori_shape = None
    self._been_called = set()

  def _get_factor(self, caller: str) -> float:
    """Returns a random scaling factor and save to cache.
    """
    if caller in self._been_called:
      factor = np.random.uniform(*self.scale_range)
      self._last_factor = factor
      self._been_called = set([caller])
    else:
      factor = self._last_factor
      self._been_called.add(caller)
    return factor

  def _recover_image_to(self, image: np.ndarray, to_shape: tuple) -> np.ndarray:
    """Recover image shape by cropping or padding.
    """
    H, W = image.shape[:2]
    to_H, to_W = to_shape

    if H < to_H:
      pad_top = (to_H - H) // 2
      pad_bottom = to_H - H - pad_top
      image = cv2.copyMakeBorder(image,
                                 pad_top,
                                 pad_bottom,
                                 0,
                                 0,
                                 borderType=cv2.BORDER_CONSTANT,
                                 value=0)
    elif H > to_H:
      offset = abs((to_H - H) // 2)
      image = image[offset:offset + to_H, :, ...]

    if W < to_W:
      pad_left = (to_W - W) // 2
      pad_right = to_W - W - pad_left
      image = cv2.copyMakeBorder(image,
                                 0,
                                 0,
                                 pad_left,
                                 pad_right,
                                 borderType=cv2.BORDER_CONSTANT,
                                 value=0)
    elif W > to_W:
      offset = abs((to_W - W) // 2)
      image = image[:, offset:offset + to_W, ...]

    return image

  def apply_image(self, image: np.ndarray, interp=None) -> np.ndarray:
    interp = interp if interp is not None else self.interp
    factor = self._get_factor(caller='image')
    ori_shape = image.shape[:2]
    self._last_ori_shape = ori_shape
    new_shape = np.round(np.array(ori_shape) * factor).astype(np.int)
    image = cv2.resize(image, tuple(new_shape)[::-1], interpolation=interp)

    # If keep shape, crop or pad the image ro original shape
    if self.keep_shape:
      image = self._recover_image_to(image, ori_shape)

    return image

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    factor = self._get_factor(caller='label_image')
    ori_shape = image.shape[:2]
    self._last_ori_shape = ori_shape
    new_shape = np.round(np.array(ori_shape) * factor).astype(np.int)
    image = cv2.resize(image,
                       tuple(new_shape)[::-1],
                       interpolation=cv2.INTER_NEAREST)

    # If keep shape, crop or pad the image ro original shape
    if self.keep_shape:
      image = self._recover_image_to(image, ori_shape)

    return image

  def apply_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    factor = self._get_factor(caller='points')

    # Scale points by factor
    points *= factor

    # If keep shape, recover to original image coords
    if self.keep_shape:
      H, W = np.round(np.array(self._last_ori_shape) * factor).astype(np.int)
      to_H, to_W = self._last_ori_shape
      points += np.array([(to_W - W) // 2, (to_H - H) // 2],
                         dtype=points.dtype).reshape(1, 2)

    return points


class Crop(_Transform):
  """Crop images by ROI.
  """

  def __init__(self, original_size: Union[tuple, list], roi: Union[tuple,
                                                                   list]):
    """Constructs self.

    Args:
      original_size: Original size of image, (W, H).
      roi: The crop roi, (X, Y, X, Y)
    """
    self.original_size = tuple(original_size)

    # Compute real roi
    if roi[0] >= original_size[0] or roi[1] >= original_size[1]:
      raise ValueError('ROI {} out of range {}.')
    if roi[2] < 1 or roi[3] < 1:
      raise ValueError('ROI {} out of range {}.')

    # We use [xmin, ymin, xmax, ymax] for self.roi, so the roi range is
    # [x_min, xmax), [y_min, y_max)
    self.roi = (max(0, roi[0]), max(0, roi[1]), min(original_size[0], roi[2]),
                min(original_size[1], roi[3]))

  def apply_image(self, image: np.ndarray) -> np.ndarray:
    return image[self.roi[1]:self.roi[3], self.roi[0]:self.roi[2], ...]

  def undo_image(self, image: np.ndarray, fill=0) -> np.ndarray:
    """Since the original pixels are lost, we fill them with value `fill`.
    """
    left = self.roi[0]
    right = self.original_size[0] - self.roi[2]
    top = self.roi[1]
    bottom = self.original_size[1] - self.roi[3]
    return cv2.copyMakeBorder(image,
                              top,
                              bottom,
                              left,
                              right,
                              borderType=cv2.BORDER_CONSTANT,
                              value=fill)

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    return self.apply_image(image)

  def undo_label_image(self, image: np.ndarray, fill=0) -> np.ndarray:
    return self.undo_image(image, fill)

  def apply_points(self, points: np.ndarray, drop_outliers=True) -> np.ndarray:
    """Run transformation on points.

    Args:
      points (np.ndarray): The original points with shape (N, 2).
      drop_outliers (bool): Drop points outside the roi.
    """
    if not len(points):
      return points
    offset = [-self.roi[0], -self.roi[1]]
    points += offset

    if drop_outliers:
      points = points[np.logical_and(points[:, 0] >= 0, points[:, 1] >= 0), :]
      points = points[np.logical_and(points[:, 0] <
                                     (self.roi[2] -
                                      self.roi[0]), points[:, 1] < self.roi[3] -
                                     self.roi[1]), :]
    return points

  def undo_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    offset = [self.roi[0], self.roi[1]]
    points += offset
    return points


class RandomCrop(_Transform):
  """Crops objects by a random ROI. This is irreversible, so the `undo_*` method
  does nothing. We follow the same calling convention as `RandomRotate`.
  """

  def __init__(self, crop_size: Union[list, tuple]):
    """Constructs self.

    Args:
      crop_size: The random ROI size.
    """
    self.crop_size = crop_size
    self._last_roi = (0, 0, *crop_size)
    self._been_called = set()

  def _get_roi(self,
               caller: str,
               image_shape: Union[tuple, None] = None) -> float:
    """Returns a random ROI of certain size and save to cache.
    """
    if caller in self._been_called:
      assert image_shape
      H, W = image_shape
      left_offset = np.random.randint(0, W - self.crop_size[0] + 1)
      top_offset = np.random.randint(0, H - self.crop_size[1] + 1)
      # xyxy roi
      roi = (left_offset, top_offset, left_offset + self.crop_size[0],
             top_offset + self.crop_size[1])
      self._last_roi = roi
      self._been_called = set([caller])
    else:
      roi = self._last_roi
      self._been_called.add(caller)
    return roi

  def apply_image(self, image: np.ndarray) -> np.ndarray:
    roi = self._get_roi(caller='image', image_shape=image.shape[:2])
    return image[roi[1]:roi[3], roi[0]:roi[2], ...]

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    roi = self._get_roi(caller='label_image', image_shape=image.shape[:2])
    return image[roi[1]:roi[3], roi[0]:roi[2], ...]

  def apply_points(self, points: np.ndarray, drop_outliers=True) -> np.ndarray:
    if not len(points):
      return points
    roi = self._get_roi(caller='points')
    offset = [-roi[0], -roi[1]]
    points += offset
    if drop_outliers:
      points = points[np.logical_and(points[:, 0] >= 0, points[:, 1] >= 0), :]
      points = points[np.logical_and(points[:, 0] <
                                     (roi[2] - roi[0]), points[:, 1] < roi[3] -
                                     roi[1]), :]
    return points


class Rotate(_Transform):
  """Rotate objects by some angle. For images, we always rotate around it's
  center, each time the `apply_image` and `apply_label_image` gets called, the
  rotation center is stored for `apply_points` to use, so take care of the
  calling order.
  """

  def __init__(self, angle: float, interp=cv2.INTER_LINEAR):
    """Constructs self.

    Args:
      angle (float): Rotation angle, degree, positive for counter-clockwise.
      interp: Interpolation method.
    """
    self.angle = angle
    self.interp = interp
    self._rot_center = (0, 0)

  @classmethod
  def rotate_image(cls, image: np.ndarray, angle: float, interp) -> np.ndarray:
    H, W = image.shape[:2]
    center = (W / 2, H / 2)
    rotation_mat = cv2.getRotationMatrix2D(center, angle, 1)
    return cv2.warpAffine(image, rotation_mat, (W, H), flags=interp)

  def apply_image(self, image: np.ndarray, interp=None) -> np.ndarray:
    """Apply transformation on image. Use `interp` to override `self.interp`.
    """
    interp = interp if interp is not None else self.interp
    self._rot_center = (image.shape[1] / 2, image.shape[0] / 2)  # (x, y)
    return self.rotate_image(image, self.angle, interp)

  def undo_image(self, image: np.ndarray, interp=None) -> np.ndarray:
    """Undo transformation on image. Use `interp` to override `self.interp`.
    """
    return self.rotate_image(image, -self.angle, interp)

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    """We use nearest interpolation for label images.
    """
    self._rot_center = (image.shape[1] / 2, image.shape[0] / 2)  # (x, y)
    return self.rotate_image(image, self.angle, cv2.INTER_NEAREST)

  def undo_label_image(self, image: np.ndarray) -> np.ndarray:
    """We use nearest interpolation for label images.
    """
    return self.rotate_image(image, -self.angle, cv2.INTER_NEAREST)

  def apply_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    pts = affinity.rotate(MultiPoint(points),
                          -self.angle,
                          origin=self._rot_center)
    return np.array([(p.x, p.y) for p in pts])

  def undo_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    pts = affinity.rotate(MultiPoint(points),
                          self.angle,
                          origin=self._rot_center)
    return np.array([(p.x, p.y) for p in pts])


class RandomRotate(_Transform):
  """Rotate object by random angle, this is irreversible, so the `undo_*` method
  does nothing. Each time the `apply_*` methods gets called, the rotation angle
  is generated and stored to be used in next transformation, so it's safe to
  call:

  >>> t = RandomRotate(...)
  >>> img = t.apply_image(img)
  >>> label = t.apply_label_image(label)
  >>> pts = t.apply_points(pts)

  And the rotation for `img`, `label` and `pts` will be the same. But DO NOT
  call same methods multiple times:

  >>> t = RandomRotate(...)
  >>> img = t.apply_image(img)
  >>> label = t.apply_label_image(label)
  >>> label = t.apply_label_image(label)
  >>> pts = t.apply_points(pts)

  In this case, the rotation angle is different for `img`, `label` and `pts`.
  """

  def __init__(self,
               rotation_range: Union[tuple, list] = (-90, 90),
               interp=cv2.INTER_LINEAR):
    """Constructs self.

    Args:
      rotation_range : Rotate image by a random angle in this range, positive
      for counter-clockwise.
    """
    self.rotation_range = tuple(rotation_range)
    self.interp = interp
    self._rot_center = (0, 0)
    self._last_angle = 0
    self._been_called = set()

  def _get_angle(self, caller: str) -> float:
    """Returns a random angle and save to cache. If the `caller` is in
    self._been_called, regenerate the angle and save to cache.
    """
    if caller in self._been_called:
      angle = np.random.uniform(*self.rotation_range)
      self._last_angle = angle
      self._been_called = set([caller])
    else:
      angle = self._last_angle
      self._been_called.add(caller)
    return angle

  def apply_image(self, image: np.ndarray, interp=None) -> np.ndarray:
    interp = interp if interp is not None else self.interp
    angle = self._get_angle(caller='image')
    self._rot_center = (image.shape[1] / 2, image.shape[0] / 2)  # (x, y)
    return Rotate.rotate_image(image, angle, interp)

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    angle = self._get_angle(caller='label_image')
    self._rot_center = (image.shape[1] / 2, image.shape[0] / 2)  # (x, y)
    return Rotate.rotate_image(image, angle, cv2.INTER_NEAREST)

  def apply_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    angle = self._get_angle(caller='points')
    pts = affinity.rotate(MultiPoint(points), -angle, origin=self._rot_center)
    return np.array([(p.x, p.y) for p in pts])


class Flip(_Transform):
  """Flip the image. The flip center is remembered when calling `apply_image`
  and `apply_label_image` for `apply_points` to use, so take care of the calling
  order.
  """
  FLIP_BOTH = -1  # Flip both axis
  FLIP_TD = 0  # Flip top-down
  FLIP_LR = 1  # Flip left-right

  def __init__(self, flip_code):
    self.flip_code = flip_code
    self._center = (0, 0)

  def apply_image(self, image: np.ndarray) -> np.ndarray:
    self._center = (image.shape[1] / 2, image.shape[0] / 2)
    return cv2.flip(image, self.flip_code)

  def undo_image(self, image: np.ndarray) -> np.ndarray:
    return cv2.flip(image, self.flip_code)

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    self._center = (image.shape[1] / 2, image.shape[0] / 2)
    return self.apply_image(image)

  def undo_label_image(self, image: np.ndarray) -> np.ndarray:
    return self.undo_image(image)

  def apply_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    if self.flip_code == self.FLIP_LR:
      # y remain unchanged, flip x
      points[:, 0] += 2 * (self._center[0] - points[:, 0])
    elif self.flip_code == self.FLIP_TD:
      # x remain unchanged, flip y
      points[:, 1] += 2 * (self._center[1] - points[:, 1])
    else:
      # flip x, y
      points += 2 * (self._center - points)
    return points

  def undo_points(self, points: np.ndarray) -> np.ndarray:
    return self.apply_points(points)


class RandomHorizontalFlip(_Transform):
  """Randomly flip object left-right. This class follows the calling convention
  of `RandomRotate`. This is irreversible, so the `undo_*` method does nothing.
  """

  def __init__(self) -> None:
    self._center = (0, 0)
    self._last_flip = None
    self._been_called = set()

  def _get_flip(self, caller: str):
    if caller in self._been_called:
      flip = np.random.uniform(0, 1) > 0.5
      self._last_flip = flip
      self._been_called = set([caller])
    else:
      flip = self._last_flip
      self._been_called.add(caller)
    return flip

  def apply_image(self, image: np.ndarray) -> np.ndarray:
    self._center = (image.shape[1] / 2, image.shape[0] / 2)
    if self._get_flip('image'):
      return cv2.flip(image, Flip.FLIP_LR)
    return image

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    self._center = (image.shape[1] / 2, image.shape[0] / 2)
    if self._get_flip('label_image'):
      return cv2.flip(image, Flip.FLIP_LR)
    return image

  def apply_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    if self._get_flip('points'):
      points[:, 0] += 2 * (self._center[0] - points[:, 0])
    return points


class RandomVerticalFlip(_Transform):
  """Randomly flip object top-down. This class follows the calling convention
  of `RandomRotate`. This is irreversible, so the `undo_*` method does nothing.
  """

  def __init__(self) -> None:
    self._center = (0, 0)
    self._last_flip = None
    self._been_called = set()

  def _get_flip(self, caller: str):
    if caller in self._been_called:
      flip = np.random.uniform(0, 1) > 0.5
      self._last_flip = flip
      self._been_called = set([caller])
    else:
      flip = self._last_flip
      self._been_called.add(caller)
    return flip

  def apply_image(self, image: np.ndarray) -> np.ndarray:
    self._center = (image.shape[1] / 2, image.shape[0] / 2)
    if self._get_flip('image'):
      return cv2.flip(image, Flip.FLIP_TD)
    return image

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    self._center = (image.shape[1] / 2, image.shape[0] / 2)
    if self._get_flip('label_image'):
      return cv2.flip(image, Flip.FLIP_TD)
    return image

  def apply_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    if self._get_flip('points'):
      points[:, 1] += 2 * (self._center[1] - points[:, 1])
    return points


class RandomGaussianNoise(_Transform):
  """Add random noise for each channel on image, has no effect on label image
  and points. This is irreversible, so the `undo_*` method does nothing. Please
  take extra care of the data type cast too.
  """

  def __init__(self,
               mean: float = 0,
               var: float = 1,
               channel_agnostic: bool = False,
               ignore_background: bool = False) -> None:
    """Constructs self.

    Args:
      mean: The mean of Gaussian distribution.
      var: The variance of Gaussion distribution.
      channel_agnostic: If true, same noise will be applied to every channel.
      ignore_background: If true, black area on original image remains black.
    """
    assert var >= 0
    self.mean = mean
    self.var = var
    self.channel_agnostic = channel_agnostic
    self.ignore_background = ignore_background

  def apply_image(self, image: np.ndarray) -> np.ndarray:
    image_shape = image.shape
    H, W = image_shape[:2]
    noise = np.random.normal(self.mean, self.var**0.5, image_shape)
    image = image.reshape(H * W, -1).astype(np.float)
    noise = noise.reshape(H * W, -1)
    if self.ignore_background:
      f = (image > 0).any(axis=1)
    else:
      f = [True] * (H * W)
    if self.channel_agnostic:
      image[f, :] += noise[f, 0].reshape(-1, 1)
    else:
      image[f, :] += noise[f, :]
    return image.reshape(*image_shape)


class Translate(_Transform):
  """Translate the object by certain offset (x, y), while dropping area outside
  the ROI and filling blank area with scalar.
  """

  def __init__(self,
               offset: Union[list, tuple, int] = 0,
               fill: Number = 0,
               interp=cv2.INTER_LINEAR):
    if isinstance(offset, Number):
      offset = (offset, offset)
    self.offset = tuple(offset)
    self.fill = fill
    self.interp = interp

  @classmethod
  def translate_image(cls, image: np.ndarray, offset: tuple, fill,
                      interp: int) -> np.ndarray:
    M = np.eye(2, 3)
    M[0, 2] = offset[0]
    M[1, 2] = offset[1]
    return cv2.warpAffine(image,
                          M, (image.shape[1], image.shape[0]),
                          flags=interp,
                          borderMode=cv2.BORDER_CONSTANT,
                          borderValue=fill)

  def apply_image(self, image: np.ndarray, interp=None) -> np.ndarray:
    interp = interp if interp is not None else self.interp
    return self.translate_image(image, self.offset, interp)

  def undo_image(self, image: np.ndarray, interp=None) -> np.ndarray:
    interp = interp if interp is not None else self.interp
    self.translate_image(image, (-self.offset[0], -self.offset[1]), interp)

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    return self.translate_image(image, self.offset, cv2.INTER_NEAREST)

  def undo_label_image(self, image: np.ndarray) -> np.ndarray:
    self.translate_image(image, (-self.offset[0], -self.offset[1]),
                         cv2.INTER_NEAREST)

  def apply_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    return points + self.offset

  def undo_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    return points - self.offset


class RandomTranslate(_Transform):
  """Randomly translate object by certain offset. This class follows the calling
  convention of `RandomRotate`. This is irreversible, so the `undo_*` method
  does nothing.
  """

  def __init__(self,
               x_range: Union[tuple, list] = (0, 1),
               y_range: Union[tuple, list] = (0, 1),
               fill: Number = 0,
               interp=cv2.INTER_LINEAR):
    self.x_range = tuple(x_range)
    self.y_range = tuple(y_range)
    self.fill = fill
    self.interp = interp

    # Calling cache
    self._last_offset = (0, 0)
    self._been_called = set()

  def _get_offset(self, caller: str) -> tuple:
    """Returns a random translation offset and save to cache.
    """
    if caller in self._been_called:
      _x = np.random.randint(self.x_range[0], self.x_range[1])
      _y = np.random.randint(self.y_range[0], self.y_range[1])
      offset = (_x, _y)
      self._last_offset = offset
      self._been_called = set([caller])
    else:
      offset = self._last_offset
      self._been_called.add(caller)
    return offset

  def apply_image(self, image: np.ndarray, interp=None) -> np.ndarray:
    interp = interp if interp is not None else self.interp
    offset = self._get_offset(caller='image')
    return Translate.translate_image(image, offset, self.fill, interp)

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    offset = self._get_offset(caller='label_image')
    return Translate.translate_image(image, offset, self.fill,
                                     cv2.INTER_NEAREST)

  def apply_points(self, points: np.ndarray) -> np.ndarray:
    if not len(points):
      return points
    offset = self._get_offset(caller='points')
    return points + offset


class TransformList(_Transform):
  """A list of sequential transforms, which can be applied to objects in chain.
  """

  def __init__(self, *args: List[_Transform]):
    self.transforms = list(args)

  def __getitem__(self, index: int) -> _Transform:
    return self.transforms[index]

  def append(self, transform: _Transform):
    self.transforms.append(transform)

  def insert(self, index: int, transform: _Transform):
    self.transforms.insert(index, transform)

  def apply_image(self, image: np.ndarray) -> np.ndarray:
    for transform in self.transforms:
      image = transform.apply_image(image)
    return image

  def undo_image(self, image: np.ndarray) -> np.ndarray:
    for transform in self.transforms[::-1]:
      image = transform.undo_image(image)
    return image

  def apply_label_image(self, image: np.ndarray) -> np.ndarray:
    for transform in self.transforms:
      image = transform.apply_label_image(image)
    return image

  def undo_label_image(self, image: np.ndarray) -> np.ndarray:
    for transform in self.transforms[::-1]:
      image = transform.undo_label_image(image)
    return image

  def apply_points(self, points: np.ndarray) -> np.ndarray:
    for transform in self.transforms:
      points = transform.apply_points(points)
    return points

  def undo_points(self, points: np.ndarray) -> np.ndarray:
    for transform in self.transforms[::-1]:
      points = transform.undo_points(points)
    return points
