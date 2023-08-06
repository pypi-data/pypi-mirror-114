"""This module provides metrics for classification task.
"""
import numpy as np

from ..common.visualization import visualize_confmat


class ConfusionMatrix:
  """The confusion matrix of classification results. confmap[i, j] means class j
  predicted to class i, i.e. the x axis is actual class.
  """
  confmat = None  # The confusion matrix

  def __init__(self, n_classes=2):
    """Constructs self.

    Args:
      n_classes (int): Number of classes, excluding background.
    """
    self.n_classes = n_classes
    self.confmat = np.zeros((n_classes, n_classes), dtype=np.long)

  def update(self, preds, labels):
    """Update the counts by `preds` and `labels.`.

    Args:
      preds (list): Prediction results.
      labels (list): Groundtruth labels.
    """
    n_classes = self.confmat.shape[0]
    # Mapping each pred-label pair to an unique index in flatten self.confmat
    # and count the occurrence of each index, then accumulate to self.confmat
    indices = preds * n_classes + labels
    self.confmat += np.bincount(indices, minlength=n_classes**2).reshape(
        n_classes, n_classes)

  def visualize(self, class_names=None):
    """Returns the confusion matrix image.
    """
    if class_names is not None:
      assert len(class_names) == self.n_classes
    return visualize_confmat(self.confmat, class_names)

  def r_cls(self, eps=1e-5):
    """Returns the per-class recall.
    """
    return np.diag(self.confmat + eps) / (np.sum(self.confmat, axis=0) + eps)

  def r_mean(self, eps=1e-5):
    """Returns the mean recall across all classes.
    """
    return self.r_cls(eps).mean()

  def p_cls(self, eps=1e-5):
    """Returns the per-class precision.
    """
    return np.diag(self.confmat + eps) / (np.sum(self.confmat, axis=1) + eps)

  def p_mean(self, eps=1e-5):
    """Returns the mean precision across all classes.
    """
    return self.p_cls(eps).mean()

  def f1_cls(self, eps=1e-5):
    """Returns the per-class F1 score.
    """
    r_cls = self.r_cls(eps)
    p_cls = self.p_cls(eps)
    return (2 * r_cls * p_cls + eps) / (r_cls + p_cls + eps)

  def f1_mean(self, eps=1e-5):
    """Returns the mean F1 score across all classes.
    """
    return self.f1_cls(eps).mean()

  def iou_cls(self, eps=1e-5):
    """Returns the IoU per-class, this is mostly used in segmentation.
    """
    return (np.diagonal(self.confmat) + eps) / (np.sum(self.confmat, axis=0) +
                                                np.sum(self.confmat, axis=1) -
                                                np.diagonal(self.confmat) + eps)

  def iou_mean(self, eps=1e-5):
    return self.iou_cls(eps).mean()

  def fn_cls(self):
    """Returns number of FN per-class.
    """
    return np.sum(self.confmat, axis=0) - np.diagonal(self.confmat)

  def fp_cls(self):
    """Returns number of FP per-class.
    """
    return np.sum(self.confmat, axis=1) - np.diagonal(self.confmat)

  def tp_cls(self):
    """Returns number of TP per-class.
    """
    return np.diagonal(self.confmat)

  def num_samples(self):
    """Returns the number of samples in each class.
    """
    return self.confmat.sum(axis=0)
