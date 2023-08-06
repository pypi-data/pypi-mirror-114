"""This module provides utils for YOLO like annotation.
"""
import glob
import os

from ...structures import Instance2D, BoxFormat
from .generic_detection import _GenericDetectionDataset


def _get_annotation(txt_file):
  """Parse instances from txt file.
  """
  boxes = []
  with open(txt_file, 'r') as f:
    for line in f.readlines():
      line = line.strip()
      if line == '':
        continue
      line = line.split(' ')
      class_name = line[0]
      if len(line) == 6:
        score = float(line[1])
        box = [float(item) for item in line[2:6]]
      elif len(line) == 5:
        score = None
        box = [float(item) for item in line[1:5]]
      boxes.append({'class_name': class_name, 'score': score, 'box': box})
  return boxes


class YOLO(_GenericDetectionDataset):
  """A YOLO format dataset which stores labels in separate txt files, with each
  line representing an object.
  """

  def __init__(self,
               anno_path,
               image_size=None,
               label_mapping={},
               classes=[],
               path_prefix='',
               box_mode=BoxFormat.XcYcWH_REL):
    """Constructs self.

    Args:
      anno_path (str): The annotation file directory.
      label_mapping (dict): As name.
      classes (list): All class names in this dataset, must be set.
      path_prefix (str): Where to find the images.
      box_mode (str): The format of the boxes, see BoxFormat.
    """
    super().__init__()
    if image_size:
      self._image_sizes = tuple(image_size)
    # Build final class ids/names from label_mapping
    if not classes:
      raise ValueError('You must specify class names for YOLO dataset')
    self._classes = classes
    class_to_id = {name: idx for idx, name in enumerate(self._classes)}

    txt_files = glob.glob(os.path.join(anno_path, '*.txt'))
    for anno_file in txt_files:
      sample_id = os.path.splitext(os.path.basename(anno_file))[0]
      self._sample_ids.append(sample_id)
      self._images[sample_id] = os.path.join(path_prefix, f'{sample_id}.jpg')
      self._anno[sample_id] = []

      # Load all annotations
      boxes = _get_annotation(anno_file)
      for box in boxes:
        mapped_cate = label_mapping.get(box['class_name'], box['class_name'])
        if mapped_cate not in self._classes:
          continue
        box['class_name'] = mapped_cate
        cate_id = class_to_id[mapped_cate]

        # Build instance
        instance = Instance2D(class_id=cate_id, fmt=box_mode, **box)
        self._anno[sample_id].append(instance)
