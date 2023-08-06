"""This class holds generic interface for segmentation datasets.
"""
import json
import logging
import random
from typing import Union, List, Tuple

import cv2
import numpy as np
import torch
import yaml
from PIL import Image
from tqdm import tqdm

from ...common.factory import object_from_dict
from ...datasets.base import _BaseDataset
from ...datasets.transform import TransformList, _Transform


class _GenericSegmentationDataset(_BaseDataset):
  """Holds basemap segmentation dataset.
  """

  @classmethod
  def find_samples(cls, **kwargs) -> List[Tuple[str, str]]:
    """Find (image_path, label_image_path) pairs from disk and return them. Need
    implementation in subclasses.

    Returns:
      A list of (image_path, label_image_path) pairs.
    """
    raise NotImplementedError

  @classmethod
  def original_labels(self, **kwargs) -> List[Tuple[str, int]]:
    """Returns original name and id of the classes in this dataset. Need
    implementation in subclasses.

    Returns:
      A list of (label_name, label_id) pairs.
    """
    raise AttributeError('_GenericSegmentationDataset has no labels')

  def __init__(self,
               preprocess: Union[TransformList, List[dict],
                                 List[_Transform]] = None,
               label_mapping: Union[dict, str] = {},
               classes: list = None,
               preload=False,
               logger: logging.Logger = None,
               **kwargs):
    """Construct self. Recursively find images and label files.

    Args:
      preprocess: The pre-transform to apply when getting an item.
      label_mapping: Mapping label name to several interested classes, labels
      mapped to _IGNORE will be dropped in label image, labels not in
      this dict will be keepped as is.
      classes: The class names of the dataset. If set, the class of labels after
      mapping should be in one of these, otherwise they will be dropped.
      preload: If true, data will be loaded to memory
      persistently with an upper limit of `preload` GB.
      logger: The logger to write logs.
      kwargs: Any other keyword args needed to create this dataset.
    """
    if isinstance(preprocess, list):
      for idx, item in enumerate(preprocess):
        if isinstance(item, dict):
          preprocess[idx] = object_from_dict(item)
      preprocess = TransformList(*preprocess)
    self._preprocess = preprocess

    if isinstance(label_mapping, str):
      with open(label_mapping, 'r') as f:
        if label_mapping.endswith('json'):
          label_mapping = json.load(label_mapping)
        elif label_mapping.endswith('yaml'):
          label_mapping = yaml.load(f, Loader=yaml.SafeLoader)

    # Load image and label file path list
    data_pairs = self.find_samples(**kwargs)

    # Downsample pairs if needed
    random_select = kwargs.get('random_select', 0)
    if random_select:
      random_select = min(random_select, len(data_pairs))
      data_pairs = random.sample(data_pairs, random_select)

    if preload and logger:
      logger.warning('Preload data will consume a lot of memory!')

    self._samples = []
    _mem_used = 0  # in MB
    _mem_limit = float(preload) * 1024  # in MB

    for i, (_image, _label) in enumerate(data_pairs):
      if _mem_used < _mem_limit:
        _image = np.asarray(Image.open(_image))
        if _image.ndim == 2:
          # _image should be 3-channel RGB image
          _image = np.tile(_image[..., None], (1, 1, 3))
        _label = np.asarray(Image.open(_label))

        self._samples.append((_image, _label))
        _mem_used += (self._samples[-1][0].nbytes +
                      self._samples[-1][1].nbytes) / 1048576  # In MB
      else:
        self._samples.append((_image, _label))

      if (i + 1) % 500 == 0 and logger:
        logger.info('Loaded {} frames, {} GB used.'.format(
            len(self), _mem_used / 1024))

    # Build interested classes from `classes` or `label_mapping`
    if classes:
      self._classes = classes
    else:
      self._classes = []
      for label in self.original_labels(**kwargs):
        if label.id < 0:  # Skip unknown label
          continue
        mapped_cate_name = label_mapping.get(label[0], label[0])
        if mapped_cate_name == '_IGNORE':  # Drop this class
          continue
        if mapped_cate_name not in self._classes:
          self._classes.append(mapped_cate_name)

    # Mapping from original label id to new label id, i.e. the LUT to apply on
    # label images
    new_class_to_id = {name: idx for idx, name in enumerate(self._classes)}
    self.lut = np.array(list(range(256)), dtype=np.uint8)
    for label in self.original_labels(**kwargs):
      if label[1] < 0:
        continue
      mapped_cate_name = label_mapping.get(label[0], label[0])
      if mapped_cate_name not in self._classes:
        # This class is dropped
        self.lut[label[1]] = 0
      else:
        self.lut[label[1]] = new_class_to_id[mapped_cate_name]

    if logger:
      logger.info('Loaded {} frames, {} GB used.'.format(
          len(self._samples), _mem_used / 1024))
      logger.info('Classes in dataset: {}'.format(', '.join(self._classes)))

  @property
  def classes(self):
    return self._classes

  @property
  def stat(self) -> Tuple[dict, dict]:
    """Returns statistics of this dataset.

    Args:
      num_workers: Number of parallel processes.

    Returns:
      pixel_cnt: Pixel count for each class.
      frame_ct: Frame count for each class.
    """
    pixel_cnt = {name: 0 for name in self.classes}
    frame_cnt = {name: 0 for name in self.classes}

    for index in tqdm(range(len(self))):
      _, label = self.load_sample(index)
      label = cv2.LUT(label, self.lut)

      for cls_id, cls_name in enumerate(self.classes):
        cnt = int((label == cls_id).sum())
        pixel_cnt[cls_name] += cnt
        if cnt > 0:
          frame_cnt[cls_name] += 1

    return pixel_cnt, frame_cnt

  def __len__(self):
    """Returns the capacity of this dataset
    """
    return len(self._samples)

  def load_sample(self, index):
    # Read raw data
    image, label = self._samples[index]
    if isinstance(image, str):
      image = np.asarray(Image.open(image))
      if image.ndim == 2:
        # _image should be 3-channel RGB image
        image = np.tile(image[..., None], (1, 1, 3))
      label = np.asarray(Image.open(label))
    else:
      # Use a separate copy to avoid changeing original data
      image = image.copy()
      label = label.copy()
    return image, label

  def __getitem__(self, index):
    """Returns an item from dataset, with preprocess/augmentation.
    """
    image, label = self.load_sample(index)

    # Apply LUT on label
    label = cv2.LUT(label, self.lut)

    # Apply transformation to image and label
    if self._preprocess:
      image = self._preprocess.apply_image(image)
      label = self._preprocess.apply_label_image(label)

    # To CHW format
    image = np.transpose(image, (2, 0, 1))
    label = label[None]

    return torch.FloatTensor(image), torch.LongTensor(label)
