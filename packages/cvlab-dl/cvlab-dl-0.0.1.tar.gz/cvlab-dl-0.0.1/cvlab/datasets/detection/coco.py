"""This module provides driver for COCO like annotations.
"""
import json
import os

from ...structures import Instance2D, BoxFormat
from .generic_detection import _GenericDetectionDataset


class COCO(_GenericDetectionDataset):
  """A COCO-like detection dataset.
  """

  def __init__(self,
               anno_json,
               label_mapping={},
               classes=None,
               path_prefix='',
               box_mode=BoxFormat.XYWH_ABS):
    """Constructs self.

    Args:
      anno_json (str): The annotation file path.
      label_mapping (dict): As name.
      classes (list or None): The class names of the dataset. If set, the class
      of labels after mapping should be in one of these, otherwise they will be
      dropped.
      path_prefix (str): Where to find the images.
      box_mode (str): The format of the boxes, see BoxFormat.
    """
    super().__init__()
    with open(anno_json, 'r') as f:
      anno_ori = json.load(f)

    # Build final class ids/names from label_mapping
    if classes:
      self._classes = classes
    else:
      self._classes = []
      for category in anno_ori['categories']:
        mapped_cate = label_mapping.get(category['name'], category['name'])
        if mapped_cate not in self._classes:
          self._classes.append(mapped_cate)

    # Mapping from original category id to new category id
    new_class_to_id = {name: idx for idx, name in enumerate(self._classes)}
    old_class_id_to_new_id = {}
    for category in anno_ori['categories']:
      # New class name of this cate
      mapped_cate = label_mapping.get(category['name'], category['name'])
      if mapped_cate not in self._classes:
        old_class_id_to_new_id[category['id']] = -1
      else:
        old_class_id_to_new_id[category['id']] = new_class_to_id[mapped_cate]

    # Load all samples
    for image in anno_ori['images']:
      sample_id = image['id']
      self._sample_ids.append(sample_id)
      self._images[sample_id] = os.path.join(path_prefix, image['file_name'])
      self._anno[sample_id] = []
      self._image_sizes[sample_id] = (image['width'], image['height'])

    # Load all annotations
    for anno in anno_ori['annotations']:
      sample_id = anno['image_id']
      cate_id = old_class_id_to_new_id[anno['category_id']]
      if cate_id < 0:  # Drop this instance
        continue
      cate_name = self._classes[cate_id]

      # Build instance
      instance = Instance2D(class_name=cate_name,
                            class_id=cate_id,
                            score=anno.get('score', None),
                            box=anno['bbox'],
                            fmt=box_mode)
      self._anno[sample_id].append(instance)
