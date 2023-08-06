"""Utils for visualization.
"""
from typing import List, Union

import cv2
import matplotlib as mpl
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from shapely.geometry import Polygon, LineString, MultiPoint
from sklearn.metrics import auc, PrecisionRecallDisplay

from .libs.box import _setup_figure, _change_color_brightness
from .libs.pretty_confmat import pretty_plot_confusion_matrix


def _get_image_from_figure(fig):
  """Returns a RGB image from matplotlib figure.
  """
  fig.canvas.draw()
  img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
  img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
  return img


def get_color_mapping(n):
  """Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
  color.
  """
  return plt.cm.get_cmap(lut=n)


def get_distinct_color(index: int,
                       n_classes: int = 1,
                       scale: float = 1,
                       dtype=int):
  """Returns a distinct color for an class in `n_classes`.

  Args:
    index (int): The class index.
    n_classes (int): Total number of classes.
    scale (float): By default the color is float value in [0, 1], this arg scale
    it by `color = color * scale`.
    dtype (Numpy datatype): Type cast function
  """
  assert index < n_classes
  cm = get_color_mapping(n_classes)
  color = np.array(mplc.to_rgb(cm(index)))
  color *= scale
  color = color.astype(dtype)
  return tuple([dtype(item) for item in color])


def draw_instances(image, instances, show_label=True, color=None):
  """Draw 2D instance(box) on image using matplotlib for better quality, so this
  function is relatively slow.

  Args:
    image (np.ndarray): HWC(RGB) or HW image, users should take care of the data
    type.
    instances (list of Instacne2D): A list of instances.
    show_label (bool): Wether to show the text label.
    color (tuple): The color of the box.
  """
  if not isinstance(image, np.ndarray):
    image = np.asarray(image)
  if not instances:
    return image

  # Make RGB image for drawing
  H, W = image.shape[:2]
  if image.ndim == 2:
    image = np.repeat(image[..., None], 3, axis=2)
  elif image.ndim == 3 and image.shape[-1] == 1:
    image = np.repeat(image, 3, axis=2)
  _, fig, ax = _setup_figure(image)

  font_size = max(np.sqrt(H * W) // 90, 10)
  cmap = get_color_mapping(len(instances))  # Distinct colors
  if color is not None:
    color = (color[0] / 255., color[1] / 255., color[2] / 255., 1)  # RGBA

  for index, instance in enumerate(instances):
    # Convert to XYWH_ABS
    instance = instance.convert_to('XYWH_ABS', image_size=(W, H))

    name = instance.class_name
    score = instance.score
    box = instance.box

    if score is not None:
      label_text = '{} {}'.format(name, int(score * 100))
    else:
      label_text = name

    box = [int(item) for item in box]
    linewidth = max(font_size / 4, 1)

    ax.add_patch(
        mpl.patches.Rectangle(
            tuple(box[:2]),
            box[2],
            box[3],
            fill=False,
            edgecolor=cmap(index) if color is None else color,
            linewidth=linewidth,
            alpha=0.75,
            linestyle='-',
        ))

    if show_label:
      # Draw text
      height_ratio = box[-1] / np.sqrt(H * W)
      label_color = _change_color_brightness(
          cmap(index) if color is None else color, brightness_factor=0.7)
      font_size = (np.clip(
          (height_ratio - 0.02) / 0.08 + 1, 1.2, 2) * 0.5 * font_size)

      # since the text background is dark, we don't want the text to be dark
      color = np.maximum(list(mplc.to_rgb(label_color)), 0.2)
      color[np.argmax(color)] = max(0.8, np.max(color))

      ax.text(
          box[0],
          box[1],
          label_text,
          size=font_size,
          family="sans-serif",
          bbox={
              "facecolor": "black",
              "alpha": 0.9,
              "pad": 0.7,
              "edgecolor": "none"
          },
          verticalalignment="top",
          horizontalalignment='left',
          color=color,
          zorder=10,
      )

  return _get_image_from_figure(fig)


def draw_polygon(
    image: np.ndarray,
    polygon: Union[Polygon, list, np.ndarray],
    color: Union[list, tuple] = (255, 255, 255)
) -> np.ndarray:
  """Draw polygon on image.

  Args:
    image: The image.
    polygon: The polygon to draw.
    color: The color of lines.
  """
  if isinstance(polygon, Polygon):
    x, y = polygon.exterior.xy
    points = np.asarray([[_x, _y] for _x, _y in zip(x, y)], dtype=np.int32)
  else:
    points = np.asarray(polygon, dtype=np.int32).reshape(-1, 2)
  points = points.reshape(-1, 1, 2)
  image = cv2.polylines(image,
                        pts=[points],
                        color=tuple(color),
                        isClosed=True,
                        thickness=2)
  return image


def draw_line(
    image: np.ndarray,
    line: Union[LineString, np.ndarray, list],
    color: Union[list, tuple] = (255, 255, 255)
) -> np.ndarray:
  """Draw line on image.

  Args:
    image (np.ndarray): The image.
    line (shapely LineString or array-like): The line to draw.
    color (tuple): The color of line.
  """
  if isinstance(line, LineString):
    x, y = line.coords.xy
    x = x[:2]
    y = y[:2]
    points = np.asarray([[_x, _y] for _x, _y in zip(x, y)], dtype=np.int32)
  else:
    points = np.asarray(line, dtype=np.int32).reshape(-1, 2)
  points = points.reshape(-1, 1, 2)
  image = cv2.polylines(image,
                        pts=[points],
                        color=tuple(color),
                        isClosed=False,
                        thickness=2)
  return image


def draw_points(image: np.ndarray,
                points: Union[np.ndarray, list, tuple, MultiPoint],
                color: Union[list, tuple] = (255, 255, 255),
                radius: int = 1,
                thickness: int = 1) -> np.ndarray:
  """Draw points on image.

  Args:
    image: The image.
    points: The points to draw.
    color: The color of points.
    radius: The radius of points.
    filled: If true, draw dots rather circels.
  """
  if isinstance(points, MultiPoint):
    points = np.array([[p.x, p.y] for p in points])
  elif isinstance(points, (list, tuple)):
    points = np.array(points)

  # Filter outliers
  H, W = image.shape[:2]
  f = (points[:, 0] >= 0) & (points[:, 0] < W) & (points[:, 1] >=
                                                  0) & (points[:, 1] < H)
  points = points[f, ...].astype(np.int)

  for point in points:
    image = cv2.circle(image,
                       tuple(point),
                       radius=radius,
                       thickness=thickness,
                       color=tuple(color))

  return image


def visualize_confmat(confmat,
                      class_names=None,
                      fig_size: Union[list, tuple] = [12, 12]):
  """Visualize confusion matrix.

  Args:
    confmat (np.ndarray): The confusion matrix, confmat[i, j] means class j
    predicted to class i.
    class_names (list or None): The class name for all the classes.

  Returns:
    img (np.ndarray): RGB image.
  """
  if class_names is None:
    class_names = list(range(confmat.shape[0]))
  if isinstance(fig_size, int):
    fig_size = (fig_size, fig_size)

  data_frame = DataFrame(confmat, index=class_names, columns=class_names)

  fig = pretty_plot_confusion_matrix(data_frame, figsize=fig_size)
  return _get_image_from_figure(fig)


def visualize_pr_curve(curve: List[tuple], name='PR Curve') -> np.ndarray:
  """Draw PR curve.

  Args:
    curve (list of tuple): A list of (recall, precision) points representing the
    PR curve.
    name (str): The name of the title.
  """
  r_list = [p[0] for p in curve]
  p_list = [p[1] for p in curve]
  ap = auc(r_list, p_list)
  vis = PrecisionRecallDisplay(p_list,
                               r_list,
                               average_precision=ap,
                               estimator_name=name).plot()
  return _get_image_from_figure(vis.figure_)


def visualize_multiple_pr_curves(curves: List[List[tuple]],
                                 names=[]) -> np.ndarray:
  """Draw multiple PR curve on one figure.

  Args:
    curves (list of list of tuple): Each item is a PR curve.
    names (list): The names of the curve, same length with curves.
  """
  assert len(curves) == len(names), 'You should specify name for each curve'
  fig, ax = plt.subplots()
  for curve, name in zip(curves, names):
    r_list = [p[0] for p in curve]
    p_list = [p[1] for p in curve]
    ap = auc(r_list, p_list)
    PrecisionRecallDisplay(p_list,
                           r_list,
                           average_precision=ap,
                           estimator_name=name).plot(ax)
  return _get_image_from_figure(fig)


def visualize_label_image(
    image: np.ndarray,
    n_classes: int,
    color_table: Union[dict, list, tuple, None] = None) -> np.ndarray:
  """This function visualize a label image, in which the pixel values are class
  ids.

  Args:
    image: Label image, HW.
    n_classes: Number of classes on the image.
    color_table: Optional specify color for each class.
  """
  if color_table is not None:
    assert len(color_table) == n_classes
  else:
    cmap = get_color_mapping(n_classes)

  assert image.ndim == 2
  H, W = image.shape[:2]
  color_image = np.zeros((H, W, 3), dtype=np.uint8)

  # Assign color to each pixel
  for cls_id in range(1, n_classes):  # cls 0 is always black
    # cls 255 is always white
    if cls_id == 255:
      color_image[image == cls_id] = (255, 255, 255)
      continue
    if color_table:
      color = color_table[cls_id]
    else:
      color = mplc.to_rgb(cmap(cls_id))
      color = [int(item * 255) for item in color]
    color_image[image == cls_id] = color

  return color_image


def overlay_label_image(
    color_image: np.ndarray,
    label_image: np.ndarray,
    alpha: float = 0.5,
    n_classes: int = 1,
    color_table: Union[dict, list, tuple, None] = None) -> np.ndarray:
  """Overlay label image to color image. Black areas on label image is ignored.

  Args:
    color_image: HW or HWC image.
    label_image: Rendered label image or raw label image.
    alpha: Fusion factor for color_image and label_image.
    color_table: The color table for different classes, required when
    label_image hasn't been rendered.
    n_classes: Number of classes, required when label_image hasn't been
    rendered.

  Returns:
    Overlayed color image.
  """
  if color_image.ndim == 2:
    color_image = color_image[..., None]
  if color_image.ndim == 3 and color_image.shape[-1] == 1:
    color_image = np.tile(color_image, (1, 1, 3))
  if color_image.ndim != 3:
    raise NotImplementedError('{} dim image not supported yet'.format(
        color_image.ndim))

  if label_image.ndim == 2:
    label_image = visualize_label_image(label_image, n_classes, color_table)
  if label_image.ndim != 3:
    raise NotImplementedError('{} dim image not supported yet'.format(
        label_image.ndim))

  H, W = color_image.shape[:2]
  color_image = color_image.reshape(-1, 3).astype(np.float32)
  label_image = label_image.reshape(-1, 3).astype(np.float32)

  filter = (label_image != (0, 0, 0)).any(axis=1)  # Non-black pixels
  color_image[filter, :] = alpha * color_image[filter, :] + (
      1 - alpha) * label_image[filter, :]

  return color_image.reshape(H, W, 3).astype(np.uint8)
