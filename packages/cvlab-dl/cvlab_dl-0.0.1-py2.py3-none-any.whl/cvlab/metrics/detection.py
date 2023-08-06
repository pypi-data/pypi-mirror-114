"""This module holds metrics for detection tasks.
"""
from typing import List, Union

import numpy as np
from sklearn.metrics import auc

from ..common.detection import assign_pred_to_gt
from ..structures import Instance2D
from .classification import ConfusionMatrix


class DetectionMetricTracker:
  """Detection metric analyzer which supports cumulative tracking.
  """

  def __init__(self,
               n_classes=1,
               iou_thresh=0.5,
               num_bins=10,
               key_conf_thresh=[]) -> None:
    """Constructs self.

    Args:
      n_classes (int): Number of classes, **excluding** background.
      iou_thresh (float): The IoU threshold for calculating the metrics.
      num_bins (int): The confidence thresholds for PR curve are evenly sampled
      between [0, 1] by `num_bins` points.
      key_conf_thresh (list): We track confidence thresholds by `num_bins`, but
      conf values in `key_conf_thresh` will always be tracked too.
    """
    self.n_classes = n_classes
    self.iou_thresh = iou_thresh

    # We track confusion matrix under different confidence thresholds:
    # [0, ..., 1]
    self.conf_threshes = np.linspace(0, 1, num_bins)
    for conf in key_conf_thresh:
      if conf not in self.conf_threshes:
        # Insert this one to somewhere
        self.conf_threshes = np.insert(
            self.conf_threshes, np.searchsorted(self.conf_threshes, conf), conf)

    # We add 1 to n_classes to record the background. If a background is
    # predicted as an object, it's a FP.
    self.conf_mats = {
        th: ConfusionMatrix(n_classes + 1) for th in self.conf_threshes
    }

  @staticmethod
  def merge_two(this, other):
    """Merge two tracker, i.e. merge the undelying confusion matrix.
    """
    for th in this.conf_threshes:
      this_mat = this.get_confmat(th)
      other_mat = other.get_confmat(th)
      if this_mat is not None and other_mat is not None:
        this.get_confmat(th).confmat += other.get_confmat(th).confmat
    return this

  def update(self, preds: List[Instance2D], labels: List[Instance2D]) -> None:
    """Update the counts by `preds` and `labels.`.

    Args:
      preds (list of Instance2D): Detection results.
      labels (list of Instance2D): Groundtruth labels.
    """
    for conf_thresh in self.conf_threshes:
      # Filter preds by confidence score
      preds_filtered = [pred for pred in preds if pred.score >= conf_thresh]

      mapping = assign_pred_to_gt(preds_filtered,
                                  labels,
                                  iou_thresh=self.iou_thresh)
      # Record detected labels
      detected = set()

      # We record each prediction label and assigned groundtruth label.
      pred_list, gt_list = [], []

      for idx, pred in enumerate(preds_filtered):
        mapped = mapping[idx]
        pred_list.append(pred.class_id)

        # If this pred is mapped to None, this is a FP
        if mapped[0] is None:
          gt_list.append(self.n_classes)
          continue

        gt_list.append(labels[mapped[0]].class_id)
        detected.add(mapped[0])

      # The rest of gts are FN
      for idx in set(range(len(labels))) - detected:
        pred_list.append(self.n_classes)
        gt_list.append(labels[idx].class_id)

      self.conf_mats[conf_thresh].update(pred_list, gt_list)

  def get_confmat(self, conf_thresh) -> Union[ConfusionMatrix, None]:
    """Returns the confusion matrix under `conf_thresh`.
    """
    return self.conf_mats.get(conf_thresh, None)

  def num_samples(self, cls_id=None) -> int:
    """Returns the total number of samples. If `cls_id` is not None, samples in
    that class is returned, otherwise total number of samples is returned.
    """
    mat = list(self.conf_mats.values())[0]
    if cls_id is not None:
      assert cls_id < self.n_classes
      return np.sum(mat.confmat, axis=0)[cls_id]
    return mat.confmat.sum(axis=0)[:-1].sum()

  def pr_curve(self, cls_id=None) -> List[tuple]:
    """Returns the PR curve under `self.iou_thresh`.

    Args:
      cls_id (int or None): If `cls_id` is None, the PR curve of this class is
      returned, otherwise the mean PR curve across all classes is returned.

    Returns:
      curve (list of tuple): The PR curve represented by a list of
      (recall, precision) points. We guarantee that the recall value monotonic
      increases in the list.
    """
    if cls_id is not None:
      assert cls_id < self.n_classes  # Background has no PR-curve
      p_list = [self.p_cls(th, cls_id) for th in self.conf_threshes]
      r_list = [self.r_cls(th, cls_id) for th in self.conf_threshes]
    else:
      p_list = [self.p_mean(th) for th in self.conf_threshes]
      r_list = [self.r_mean(th) for th in self.conf_threshes]
    points = [(r, p) for r, p in zip(r_list, p_list)]
    points = sorted(points, key=lambda p: p[0])
    # Insert start and end points
    if points[0][0] > 0:
      points = [(0, 1)] + points
    if points[-1][0] < 1:
      points += [(1, 0)]
    return points

  def ap(self, cls_id=None) -> float:
    """Returns the average precision(AP, auc of PR curve). If `cls_id` is not
    None, the AP of this class is returned, otherwise the AP across all classes
    (i.e. mAP) is returned.
    """
    pr_curve = self.pr_curve(cls_id)
    return auc(
        [p[0] for p in pr_curve],  # The recalls
        [p[1] for p in pr_curve]  # The precision
    )

  def p_cls(self, conf_thresh, cls_id=None) -> Union[list, float, None]:
    """Returns the per-class precision under `self.iou_thresh` and `conf_thresh`

    Args:
      cls_id (int or None): If `cls_id` is not None, this function returns the
      precision of this class, otherwise returns the precision of all classes.
    """
    mat = self.get_confmat(conf_thresh)
    if mat is None:
      return None
    if cls_id is not None:
      assert cls_id < self.n_classes
      return mat.p_cls()[cls_id]
    return mat.p_cls()[:-1]  # We don't calc the precision of background

  def p_mean(self, conf_thresh) -> Union[float, None]:
    """Returns the mean precision under self.iou_thresh and conf_thresh across
    all classes. We use arithmetic mean of precisions across all classes rather
    than (total_tp) / (total_tp + total_fp), to avoid bias from imbalanced
    dataset.
    """
    p_cls = self.p_cls(conf_thresh)
    if p_cls is None:
      return None
    return p_cls.mean()

  def r_cls(self, conf_thresh, cls_id=None) -> Union[list, float, None]:
    """Returns the per-class recall under self.iou_thresh and conf_thresh.

    Args:
      cls_id (int or None): If `cls_id` is not None, this function returns the
      recall of this class, otherwise returns the recall of all classes.
    """
    mat = self.get_confmat(conf_thresh)
    if mat is None:
      return None
    if cls_id is not None:
      assert cls_id < self.n_classes
      return mat.r_cls()[cls_id]
    return mat.r_cls()[:-1]

  def r_mean(self, conf_thresh) -> Union[float, None]:
    """Returns the mean recall under self.iou_thresh and conf_thresh across
    all classes. We use arithmetic mean of recall across all classes rather
    than (total_tp) / (total_tp + total_fn), to avoid bias from imbalanced
    dataset.
    """
    r_cls = self.r_cls(conf_thresh)
    if r_cls is None:
      return None
    return r_cls.mean()

  def fn(self, conf_thresh, cls_id=None) -> Union[int, None]:
    """Returns the number of false negative under self.iou_thresh and
    conf_thresh. If `cls_id` is not None, this function returns FN of this
    class, otherwise return number of FN per class.
    """
    mat = self.get_confmat(conf_thresh)
    if mat is None:
      return None
    if cls_id is not None:
      assert cls_id < self.n_classes
      return mat.fn_cls()[cls_id]
    return mat.fn_cls()[:-1]

  def fp(self, conf_thresh, cls_id=None) -> Union[int, None]:
    """Returns the number of false positive under self.iou_thresh and
    conf_thresh. If `cls_id` is not None, this function returns FP of this
    class, otherwise return number of FP per-class.
    """
    mat = self.get_confmat(conf_thresh)
    if mat is None:
      return None
    if cls_id is not None:
      assert cls_id < self.n_classes
      return mat.fp_cls()[cls_id]
    return mat.fp_cls()[:-1]

  def tp(self, conf_thresh, cls_id=None) -> Union[int, None]:
    """Returns the number of true positive under self.iou_thresh and
    conf_thresh. If `cls_id` is not None, this function returns TP of this
    class, otherwise return number of TP per-class.
    """
    mat = self.get_confmat(conf_thresh)
    if mat is None:
      return None
    if cls_id is not None:
      assert cls_id < self.n_classes
      return mat.tp_cls()[cls_id]
    return mat.tp_cls()[:-1]
