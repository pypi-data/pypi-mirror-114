"""This module provides a class representing a generic object annotation dataset
"""


class _GenericDetectionDataset:
  """Class representing a generic detection dataset.

  Attributes:
    _sample_ids (list): Stores the id of samples.
    _anno (dict): Mappes sample_id to instances.
    _classes (list): All classes in this dataset, excluding background.
    _image_sizes (tuple or dict): Same image size for all samples or mapping
    from sample id to image size.
    _images (dict): Mapping sample id to image path.
  """

  def __init__(self):
    self._sample_ids = []
    self._anno = {}
    self._image_sizes = {}
    self._images = {}
    self._classes = []

  def __len__(self):
    return len(self._sample_ids)

  def __getitem__(self, index):
    if isinstance(index, int):
      sample_id = self._sample_ids[index]
    elif isinstance(index, str):
      sample_id = index

    image_size = self.get_image_size(sample_id)
    return (sample_id, self._anno.get(sample_id, []), image_size,
            self._images.get(sample_id, None))

  def __iter__(self):
    self._iter_index = -1
    return self

  def __next__(self):
    self._iter_index += 1
    if self._iter_index >= len(self):
      raise StopIteration
    return self[self._iter_index]

  def convert_to(self, fmt):
    """Convert all instances in this dataset to certain format.

    Args:
      fmt (str): Destinate format, see `BoxFormat` for details.
    """
    for sample_id, instances in self._anno.items():
      image_size = self.get_image_size(sample_id)
      self._anno[sample_id] = [
          instance.convert_to(fmt, image_size) for instance in instances
      ]

  def get_image_size(self, sample_id=None):
    if isinstance(self._image_sizes, dict):
      return self._image_sizes.get(sample_id, None)
    return self._image_sizes

  def dump_coco(self, path):
    # TODO
    raise NotImplementedError

  def dump_labelme(self, path):
    # TODO
    raise NotImplementedError

  def dump_yolo(self, path):
    # TODO
    raise NotImplementedError
