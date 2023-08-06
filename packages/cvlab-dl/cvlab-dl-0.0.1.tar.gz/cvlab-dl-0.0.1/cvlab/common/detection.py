"""This module holds common utils for object detection task.
"""
from typing import List

import numpy as np
from ..structures import BoxFormat, Instance2D


def iou(bbox_1, bbox_2, fmt=BoxFormat.XYXY_ABS):
  """Returns IoU between bbox_1 and box_2.

  Args:
    bbox_1 (np.ndarray): Bounding box with shape (1, 4) or (4,).
    bbox_2 (np.ndarray): Bounding box with shape (1, 4) or (4,).
    fmt (str): The box format.
  """
  if not isinstance(bbox_1, np.ndarray):
    bbox_1 = np.array(bbox_1)
    bbox_2 = np.array(bbox_2)
  else:
    bbox_1 = bbox_1.copy()
    bbox_2 = bbox_2.copy()
  bbox_1 = bbox_1.reshape(-1)
  bbox_2 = bbox_2.reshape(-1)

  # Convert bbox to XYXY
  if fmt.split('_')[0].upper() == 'XYWH':
    bbox_1[2:] += bbox_1[:2]
    bbox_2[2:] += bbox_2[:2]
  elif fmt.split('_')[0].upper() == 'XCYCWH':
    bbox_1[:2] -= bbox_1[2:] / 2
    bbox_1[2:] += bbox_1[:2]
    bbox_2[:2] -= bbox_2[2:] / 2
    bbox_2[2:] += bbox_2[:2]

  xmin_1, ymin_1, xmax_1, ymax_1 = bbox_1
  xmin_2, ymin_2, xmax_2, ymax_2 = bbox_2

  area_inter = (max(min(xmax_1, xmax_2) - max(xmin_1, xmin_2), 0)) * (max(
      min(ymax_1, ymax_2) - max(ymin_1, ymin_2), 0))
  area_total = (xmax_1 - xmin_1) * (ymax_1 - ymin_1) + (xmax_2 - xmin_2) * (
      ymax_2 - ymin_2) - area_inter

  return area_inter / area_total


def nms(bboxes, scores, thresh, fmt=BoxFormat.XYXY_ABS):
  """Returns filtered `bboxes` by Non-maximum Suppression(NMS) algorithm based
  on IoU and scores.

  Args:
    bboxes (np.ndarray or list): Bounding boxes with shape (N, 4).
    scores (np.ndarray or list): Scores for `bboxes` with shape (N,).
    thresh (float): The threshold for filtering. If `iou(bbox1, bbox2) >
    thresh`, only the bbox with higher score will be reserved.
    fmt (str): The bbox format.

  Returns:
    k (list): Bbox indices to keep.
  """
  if not isinstance(bboxes, np.ndarray):
    bboxes = np.array(bboxes).reshape(-1, 4)
  else:
    bboxes = bboxes.copy()
  if isinstance(scores, list):
    scores = np.array(scores).reshape(-1)

  # Convert bbox to XYXY
  if fmt.split('_')[0].upper() == 'XYWH':
    bboxes[:, 2:] += bboxes[:, :2]
  elif fmt.split('_')[0].upper() == 'XCYCWH':
    bboxes[:, :2] -= bboxes[:, 2:] / 2
    bboxes[:, 2:] += bboxes[:, :2]

  x1, y1, x2, y2 = [bboxes[:, i] for i in range(4)]
  areas = (x2 - x1 + 1) * (y2 - y1 + 1)

  # Sort the scores in descending order, so that bboxes with higher scores are
  # reserved
  score_index = scores.argsort()[::-1]

  # Reserved bbox indices
  keep = []

  while score_index.size > 0:
    i = score_index[0]
    keep.append(i)

    # Compute the IoU between i-th and other bboxes
    inter_x1 = np.maximum(x1[i], x1[score_index[1:]])
    inter_x2 = np.minimum(x2[i], x2[score_index[1:]])
    inter_y1 = np.maximum(y1[i], y1[score_index[1:]])
    inter_y2 = np.minimum(y2[i], y2[score_index[1:]])

    inter_w = np.maximum(0.0, inter_x2 - inter_x1 + 1)
    inter_h = np.maximum(0.0, inter_y2 - inter_y1 + 1)
    inter_area = inter_w * inter_h
    iou = inter_area / (areas[i] + areas[score_index[1:]] - inter_area)

    keep_mask = iou <= thresh

    inds = np.where(keep_mask)[0]
    score_index = score_index[inds + 1]

  return keep


def assign_pred_to_gt(preds: List[Instance2D], gts: List[Instance2D],
                      iou_thresh: float) -> List[tuple]:
  """Returns a list which maps predictions to gts, Each prediction is assigned
  to one groundtruth at most, but each groundtruth can be assigned to multiple
  predictions. Note: the box format of preds and gts should be the same, see
  `BoxFormat` for details.

  Args:
    preds (list of Instance2D): Prediction list.
    gts (list of Instance2D): Groundtruth list.
    iou_thresh (float): The IoU threshold for a valid prediction. if the IoU is
    lower than this value, it's not a successful detection.

  Returns:
    mapping (list of tuple): `mapping[i] = (map_idx, iou)` means the assignment
    of i-th prediction in `preds`.
  """
  mapping = [(None, 0) for _ in range(len(preds))]
  if not preds:  # No prediction at all, should all be FN
    return mapping
  if not gts:  # Can not assign to any gt, should be FP.
    return mapping

  for idx, pred in enumerate(preds):
    # Box format of pred and gt must be the same
    iou_list = [
        iou(np.array(pred.box), np.array(gt.box), fmt=pred.fmt) for gt in gts
    ]
    # Find the gt with which the pred has maximum IoU
    assign_idx = np.argmax(iou_list)
    cur_iou = iou_list[assign_idx]

    # Assign this sample to the gt with highest iou
    if cur_iou >= iou_thresh:
      mapping[idx] = (assign_idx, cur_iou)

  return mapping
