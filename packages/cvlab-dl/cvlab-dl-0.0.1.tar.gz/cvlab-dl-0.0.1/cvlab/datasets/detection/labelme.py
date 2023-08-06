"""This module provides utils for labelme format annotation.
"""
import glob
import json
import os

from ...structures import Instance2D, BoxFormat
from .generic_detection import _GenericDetectionDataset


class LabelMe(_GenericDetectionDataset):
  """A labelme format dataset which stores label in separate json files.
  """

  def __init__(self,
               anno_path,
               label_mapping={},
               classes=[],
               path_prefix='',
               box_mode=BoxFormat.XYXY_ABS):
    """Constructs self.

    Args:
      anno_path (str): The annotation file directory.
      label_mapping (dict): As name.
      classes (list): All class names in this dataset, must be set.
      path_prefix (str): Where to find the images.
      box_mode (str): The format of the boxes, see BoxFormat.
    """
    super().__init__()
    assert box_mode in (BoxFormat.XYXY_ABS, BoxFormat.XYXY_REL)
    # Build final class ids/names from label_mapping
    if not classes:
      raise ValueError('You must specify class names for labelme dataset')
    self._classes = classes
    class_to_id = {name: idx for idx, name in enumerate(self._classes)}

    json_files = glob.glob(os.path.join(anno_path, '*.json'))
    for anno_file in json_files:
      with open(anno_file, 'r') as f:
        anno_ori = json.load(f)

      sample_id = os.path.splitext(os.path.basename(anno_file))[0]
      self._sample_ids.append(sample_id)
      self._images[sample_id] = os.path.join(path_prefix, anno_ori['imagePath'])
      self._anno[sample_id] = []
      self._image_sizes[sample_id] = (anno_ori['imageWidth'],
                                      anno_ori['imageHeight'])

      # Load all annotations
      for shape in anno_ori['shapes']:
        mapped_cate = label_mapping.get(shape['label'], shape['label'])
        if mapped_cate not in self._classes:
          continue
        cate_id = class_to_id[mapped_cate]

        points = sorted(shape['points'], key=lambda p: p[0])
        if points[0][1] > points[1][1]:
          # Convert to left-top and right-bottom corners
          points = [[points[0][0], points[1][1]], [points[1][0], points[0][1]]]

        # Build instance
        instance = Instance2D(class_name=mapped_cate,
                              class_id=cate_id,
                              score=shape.get('score', None),
                              box=points[0] + points[1],
                              fmt=box_mode)
        self._anno[sample_id].append(instance)
