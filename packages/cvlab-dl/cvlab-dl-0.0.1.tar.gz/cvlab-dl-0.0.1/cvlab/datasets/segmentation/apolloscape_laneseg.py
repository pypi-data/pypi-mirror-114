"""This class provides dataset definition for ApolloScape lane marking
segmentation dataset.
"""
import os
from collections import namedtuple
from typing import List, Tuple

from ...common.utils import recursive_glob
from .generic_segmentation import _GenericSegmentationDataset


# a label and all meta information
Label = namedtuple(
    'Label',
    [
        'name',  # The identifier of this label.
        # We use them to uniquely name a class
        'id',  # An integer ID that is associated with this label.
        # The IDs are used to represent the label in ground truth images
        # An ID of -1 means that this label does not have an ID and thus
        # is ignored when creating ground truth images (e.g. license plate).
        # Do not modify these IDs, since exactly these IDs are expected by the
        # evaluation server.
        'trainId',  # Feel free to modify these IDs as suitable for your method. Then create
        # ground truth images with train IDs, using the tools provided in the
        # 'preparation' folder. However, make sure to validate or submit results
        # to our evaluation server using the regular IDs above!
        # For trainIds, multiple labels might have the same ID. Then, these labels
        # are mapped to the same class in the ground truth images. For the inverse
        # mapping, we use the label that is defined first in the list below.
        # For example, mapping all void-type classes to the same ID in training,
        # might make sense for some approaches.
        # Max value is 255!
        'category',  # The name of the category that this label belongs to
        'categoryId',  # The ID of this category. Used to create ground truth images
        # on category level.
        'hasInstances',  # Whether this label distinguishes between single instances or not
        'ignoreInEval',  # Whether pixels having this class as ground truth label are ignored
        # during evaluations or not
        'color',  # The color of this label
    ])

# a list of all labels in ApolloScape dataset
# name, id, trainId, category, categoryId, hansInstances, ignoreInEval, color
labels = [
    Label('void', 0, 0, 'void', 0, False, False, (0, 0, 0)),
    Label('s_w_d', 200, 1, 'dividing', 1, False, False, (70, 130, 180)),
    Label('s_y_d', 204, 2, 'dividing', 1, False, False, (220, 20, 60)),
    Label('ds_w_dn', 213, 3, 'dividing', 1, False, True, (128, 0, 128)),
    Label('ds_y_dn', 209, 4, 'dividing', 1, False, False, (255, 0, 0)),
    Label('sb_w_do', 206, 5, 'dividing', 1, False, True, (0, 0, 60)),
    Label('sb_y_do', 207, 6, 'dividing', 1, False, True, (0, 60, 100)),
    Label('b_w_g', 201, 7, 'guiding', 2, False, False, (0, 0, 142)),
    Label('b_y_g', 203, 8, 'guiding', 2, False, False, (119, 11, 32)),
    Label('db_w_g', 211, 9, 'guiding', 2, False, True, (244, 35, 232)),
    Label('db_y_g', 208, 10, 'guiding', 2, False, True, (0, 0, 160)),
    Label('db_w_s', 216, 11, 'stopping', 3, False, True, (253, 0, 40)),
    Label('s_w_s', 217, 12, 'stopping', 3, False, False, (220, 220, 0)),
    Label('ds_w_s', 215, 13, 'stopping', 3, False, True, (250, 170, 30)),
    Label('s_w_c', 218, 14, 'chevron', 4, False, True, (102, 102, 156)),
    Label('s_y_c', 219, 15, 'chevron', 4, False, True, (128, 0, 0)),
    Label('s_w_p', 210, 16, 'parking', 5, False, False, (128, 64, 128)),
    Label('s_n_p', 232, 17, 'parking', 5, False, True, (238, 232, 170)),
    Label('c_wy_z', 214, 18, 'zebra', 6, False, False, (190, 153, 153)),
    Label('a_w_u', 202, 19, 'thru/turn', 7, False, True, (0, 0, 230)),
    Label('a_w_t', 220, 20, 'thru/turn', 7, False, False, (128, 128, 0)),
    Label('a_w_tl', 221, 21, 'thru/turn', 7, False, False, (128, 78, 160)),
    Label('a_w_tr', 222, 22, 'thru/turn', 7, False, False, (150, 100, 100)),
    Label('a_w_tlr', 231, 23, 'thru/turn', 7, False, True, (255, 165, 0)),
    Label('a_w_l', 224, 24, 'thru/turn', 7, False, False, (180, 165, 180)),
    Label('a_w_r', 225, 25, 'thru/turn', 7, False, False, (107, 142, 35)),
    Label('a_w_lr', 226, 26, 'thru/turn', 7, False, False, (201, 255, 229)),
    Label('a_n_lu', 230, 27, 'thru/turn', 7, False, True, (0, 191, 255)),
    Label('a_w_tu', 228, 28, 'thru/turn', 7, False, True, (51, 255, 51)),
    Label('a_w_m', 229, 29, 'thru/turn', 7, False, True, (250, 128, 114)),
    Label('a_y_t', 233, 30, 'thru/turn', 7, False, True, (127, 255, 0)),
    Label('b_n_sr', 205, 31, 'reduction', 8, False, False, (255, 128, 0)),
    Label('d_wy_za', 212, 32, 'attention', 9, False, True, (0, 255, 255)),
    Label('r_wy_np', 227, 33, 'no parking', 10, False, False, (178, 132, 190)),
    Label('vom_wy_n', 223, 34, 'others', 11, False, True, (128, 128, 64)),
    Label('om_n_n', 250, 35, 'others', 11, False, False, (102, 0, 204)),
    Label('noise', 249, 255, 'ignored', 255, False, True, (0, 153, 153)),
    Label('ignored', 255, 255, 'ignored', 255, False, True, (255, 255, 255)),
]


class ApolloScapeLaneMarkingSeg(_GenericSegmentationDataset):
  """See http://apolloscape.auto/lane_segmentation.html for label definition and
  dataset folder structures.
  """

  @classmethod
  def get_label_image_path(cls, image: str) -> str:
    """Returns the label image path based on color image path.
    """
    return image.replace('ColorImage', 'Label').replace('.jpg', '_bin.png')

  @classmethod
  def find_samples(cls, **kwargs) -> List[Tuple[str, str]]:
    dataset_root = kwargs.get('dataset_root', None)
    if dataset_root is None:
      raise RuntimeError('Please specify root dir of dataset')

    samples = []

    for color_image in recursive_glob(dataset_root, '.jpg'):
      label_image = cls.get_label_image_path(color_image)
      if os.path.isfile(color_image) and os.path.isfile(label_image):
        samples.append((color_image, label_image))

    return samples

  @classmethod
  def original_labels(self, **kwargs) -> List[Tuple[str, int]]:
    return [(label.name, label.id) for label in labels]
