"""This script evaluates object detection results. This script supports several
annotation formats for groundtruth and predictions, namely 'coco', 'yolo' or
'labelme'.

- coco: This kind of annotation stores labels in one json file, each sample has
  an unique image_id and several instances. The bounding box format is
  XYXY_ABS.
- yolo: This kind of annotation stores labels in several txt files, each file
  correspond to an image, each line in the file is an instance with
  [class_id, score(optional), bbox], the bounding box format is `XYWH_REL`
- labelme: This kind of annotation stores labels in several json files, each
  file holds instances for one image, the bounding box is represented as
  two corner points of one of the box diagonal.
"""
import argparse
import collections
import os
import shutil
import logging
from concurrent.futures import as_completed, ProcessPoolExecutor
from functools import reduce

import numpy as np
import yaml
from PIL import Image
from tqdm import tqdm

from ..common.detection import assign_pred_to_gt
from ..common.utils import to_markdown
from ..common.visualization import (visualize_pr_curve, visualize_confmat,
                                    visualize_multiple_pr_curves, draw_instances
                                   )
from ..datasets.detection import COCO, YOLO, LabelMe
from ..metrics.detection import DetectionMetricTracker
from ..structures import BoxFormat


def _get_parser():
  _parser = argparse.ArgumentParser()
  _parser.add_argument('--gt', help='Path to groundtruth labels')
  _parser.add_argument('--gt-type',
                       choices=['coco', 'yolo', 'labelme'],
                       help='Type of groundtruth labels')
  _parser.add_argument('--gt-fmt',
                       choices=BoxFormat.all(),
                       help='Format of groundtruth boxes')
  _parser.add_argument('--gt-label-mapping',
                       default=None,
                       help='Groundtruth label mapping')
  _parser.add_argument('--pred', help='Path to prediction result')
  _parser.add_argument('--pred-type',
                       choices=['coco', 'yolo', 'labelme'],
                       help='Type of prediction results')
  _parser.add_argument('--pred-fmt',
                       choices=BoxFormat.all(),
                       help='Format of prediction boxes')
  _parser.add_argument('--pred-label-mapping',
                       default=None,
                       help='Prediction label mapping')
  _parser.add_argument('--image-path-prefix',
                       default='',
                       help='Input image path prefix')
  _parser.add_argument('--iou-thresh',
                       type=float,
                       default=0.5,
                       help='IoU threshold for a valid detection')
  _parser.add_argument('--conf-thresh',
                       type=float,
                       default=0.5,
                       help='Confidence threshold for a valid detection')
  _parser.add_argument(
      '--classes',
      default=[],
      nargs='+',
      help='For yolo and labelme datasets, you must specify all the class names'
  )
  _parser.add_argument(
      '--image-size',
      default=[],
      nargs='+',
      type=int,
      help='For yolo type dataset, you must specify the image size')
  _parser.add_argument('--output', default='eval_results', help='Output path')
  _parser.add_argument('--num_workers',
                       default=16,
                       type=int,
                       help='Num workers for parallel processing')
  return _parser


def process_sample(pred_sample, label_sample, n_classes, iou_thresh, num_bins,
                   key_conf_thresh):
  (sample_id, preds, _, image_path) = pred_sample
  (_, labels, _, _) = label_sample
  metric_tracker = DetectionMetricTracker(n_classes=n_classes,
                                          iou_thresh=iou_thresh,
                                          num_bins=num_bins,
                                          key_conf_thresh=key_conf_thresh)
  metric_tracker.update(preds, labels)

  # Check if this sample has FN/FP, if so, render and save.
  preds = [pred for pred in preds if pred.score >= args.conf_thresh]
  mapping = assign_pred_to_gt(preds, labels, args.iou_thresh)

  FN_classes, FP_classes, detected = set(), set(), set()
  for idx, pred in enumerate(preds):
    mapped = mapping[idx]
    if mapped[0] is None:  # This is an FP
      FP_classes.add(pred.class_name)
    elif pred.class_id != labels[mapped[0]].class_id:  # Also FP
      FP_classes.add(pred.class_name)
    else:
      detected.add(mapped[0])

  # Others are all FN
  for idx in set(range(len(labels))) - detected:
    FN_classes.add(labels[idx].class_name)

  # Visualize if we have FN/FP
  if image_path and (FN_classes or FP_classes):
    image = Image.open(image_path)

    pred_rendered = draw_instances(image, preds)
    gt_rendered = draw_instances(image, labels)
    rendered = np.concatenate([gt_rendered, pred_rendered], axis=1)
    rendered = Image.fromarray(rendered)

    # Save to each folder
    for fn in FN_classes:
      folder = os.path.join(args.output, 'rendered', fn, 'FN')
      os.makedirs(folder, exist_ok=True)
      rendered.save(os.path.join(folder, f'{sample_id}.jpg'))
    for fp in FP_classes:
      folder = os.path.join(args.output, 'rendered', fp, 'FP')
      os.makedirs(folder, exist_ok=True)
      rendered.save(os.path.join(folder, f'{sample_id}.jpg'))

  return metric_tracker


def main(args):
  """Main function.
  """
  logger = logging.getLogger('DetEvaluator')
  logger.setLevel(logging.INFO)
  logger.handlers.clear()

  logFormatter = logging.Formatter(fmt='%(asctime)s:EVAL:%(message)s')

  fileHandler = logging.FileHandler(os.path.join(args.output, 'metrics.txt'))
  fileHandler.setFormatter(logFormatter)
  logger.addHandler(fileHandler)
  consoleHandler = logging.StreamHandler()
  consoleHandler.setFormatter(logFormatter)
  logger.addHandler(consoleHandler)

  if len(args.image_size) == 1:
    args.image_size = args.image_size * 2
  if not args.classes:
    args.classes = None
  # Load groundtruth
  if args.gt_type in ('yolo', 'labelme'):
    assert args.classes
  if args.gt_type == 'yolo' and BoxFormat.is_rel(args.gt_fmt):
    assert args.image_size
  if args.pred_type == 'yolo' and BoxFormat.is_rel(args.pred_fmt):
    assert args.image_size

  # Load label mapping
  if args.gt_label_mapping:
    with open(args.gt_label_mapping, 'r') as f:
      gt_label_mapping = yaml.load(f, Loader=yaml.SafeLoader)
  else:
    gt_label_mapping = {}
  if args.pred_label_mapping:
    with open(args.pred_label_mapping, 'r') as f:
      pred_label_mapping = yaml.load(f, Loader=yaml.SafeLoader)
  else:
    pred_label_mapping = {}

  # Build groundtruth dataset
  if args.gt_type == 'yolo':
    gt_data = YOLO(anno_path=args.gt,
                   image_size=args.image_size,
                   label_mapping=gt_label_mapping,
                   classes=args.classes,
                   path_prefix=args.image_path_prefix,
                   box_mode=args.gt_fmt)
  elif args.gt_type == 'coco':
    gt_data = COCO(anno_json=args.gt,
                   label_mapping=gt_label_mapping,
                   classes=args.classes,
                   path_prefix=args.image_path_prefix,
                   box_mode=args.gt_fmt)
  elif args.gt_type == 'labelme':
    gt_data = LabelMe(anno_path=args.gt,
                      label_mapping=gt_label_mapping,
                      classes=args.classes,
                      path_prefix=args.image_path_prefix,
                      box_mode=args.gt_fmt)
  else:
    raise NotImplementedError(f'Dataset type {args.gt_type} not supported yet')
  logger.info('Loaded GT with {} frames'.format(len(gt_data)))

  # Build prediction dataset
  if args.pred_type == 'yolo':
    pred_data = YOLO(anno_path=args.pred,
                     image_size=args.image_size,
                     label_mapping=pred_label_mapping,
                     classes=gt_data._classes,
                     path_prefix=args.image_path_prefix,
                     box_mode=args.pred_fmt)
  elif args.pred_type == 'coco':
    pred_data = COCO(anno_json=args.pred,
                     label_mapping=pred_label_mapping,
                     classes=gt_data._classes,
                     path_prefix=args.image_path_prefix,
                     box_mode=args.pred_fmt)
  elif args.pred_type == 'labelme':
    pred_data = LabelMe(anno_path=args.gt,
                        label_mapping=pred_label_mapping,
                        classes=gt_data.classes,
                        path_prefix=args.image_path_prefix,
                        box_mode=args.pred_fmt)
  else:
    raise NotImplementedError(f'Dataset type {args.gt_type} not supported yet')
  logger.info('Loaded PRED with {} frames'.format(len(pred_data)))

  # Convert to the same type
  gt_data.convert_to(BoxFormat.XYXY_ABS)
  pred_data.convert_to(BoxFormat.XYXY_ABS)

  logger.info('Start parallel processing')
  metric_tracker = []
  with ProcessPoolExecutor(max_workers=args.num_workers) as executor:
    futures = []
    for sample_id in gt_data._sample_ids:
      futures.append(
          executor.submit(process_sample,
                          pred_data[sample_id], gt_data[sample_id],
                          len(gt_data._classes), args.iou_thresh, 20,
                          [args.conf_thresh]))

    for future in tqdm(as_completed(futures),
                       total=len(pred_data),
                       desc='Processing'):
      metric_tracker.append(future.result())

  # Merge all stats
  metric_tracker = reduce(DetectionMetricTracker.merge_two, metric_tracker)

  # Save the results
  logger.info('mAP@{}: {:.2f}%'.format(metric_tracker.iou_thresh,
                                       metric_tracker.ap() * 100))

  # Save overall PR-curve
  pr = visualize_pr_curve(metric_tracker.pr_curve(), name='PR-overall')
  Image.fromarray(pr).save(os.path.join(args.output, 'PR-overall.png'))

  # Save per-class PR-curve
  curves, names = [], []
  for class_id, class_name in enumerate(gt_data._classes):
    curves.append(metric_tracker.pr_curve(class_id))
    names.append(class_name)
  pr = visualize_multiple_pr_curves(curves, names)
  Image.fromarray(pr).save(os.path.join(args.output, 'PR-cls.png'))

  # Save confusion matrix
  confmat = metric_tracker.get_confmat(args.conf_thresh)
  confmat = visualize_confmat(confmat.confmat,
                              class_names=gt_data._classes + ['BG'])
  Image.fromarray(confmat).save(os.path.join(args.output,
                                             'ConfusionMatrix.png'))

  # Save statistic at certain confidence threshold
  p_cls = metric_tracker.p_cls(args.conf_thresh)
  r_cls = metric_tracker.r_cls(args.conf_thresh)

  metrics = [
      collections.OrderedDict(
          Class='Total',
          Samples=metric_tracker.num_samples(),
          TP=metric_tracker.tp(args.conf_thresh).sum(),
          FP=metric_tracker.fp(args.conf_thresh).sum(),
          FN=metric_tracker.fn(args.conf_thresh).sum(),
          Precision='{:>6.2f}'.format(100 *
                                      metric_tracker.p_mean(args.conf_thresh)),
          Recall='{:>6.2f}'.format(100 *
                                   metric_tracker.r_mean(args.conf_thresh)))
  ]
  for class_id, class_name in enumerate(gt_data._classes):
    logger.info('{}: precision {:>6.2f}%, recall {:>6.2f}%'.format(
        class_name, 100 * p_cls[class_id], 100 * r_cls[class_id]))

    metrics.append(
        collections.OrderedDict(
            Class=class_name,
            Samples=metric_tracker.num_samples(class_id),
            TP=metric_tracker.tp(args.conf_thresh, class_id),
            FP=metric_tracker.fp(args.conf_thresh, class_id),
            FN=metric_tracker.fn(args.conf_thresh, class_id),
            Precision='{:>6.2f}'.format(100 * p_cls[class_id]),
            Recall='{:>6.2f}'.format(100 * r_cls[class_id])))
  with open(os.path.join(args.output, 'stats.md'), 'w+') as f:
    print(to_markdown(metrics), file=f)


if __name__ == '__main__':
  args = _get_parser().parse_args()
  if os.path.exists(args.output):
    if input('Output dir exists and will be removed, continue? (y/n): ').lower(
    ) != 'y':
      exit(0)
    shutil.rmtree(args.output)
  os.makedirs(os.path.join(args.output, 'rendered'))

  main(args)
