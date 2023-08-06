"""Utils for visulization boxes.
"""
import colorsys

import matplotlib.colors as mplc
import matplotlib.figure as mplfigure
from matplotlib.backends.backend_agg import FigureCanvasAgg


__all__ = ['_change_color_brightness', '_setup_figure']


def _change_color_brightness(color, brightness_factor):
  """Depending on the brightness_factor, gives a lighter or darker color i.e. a
  color with less or more saturation than the original color.

  Args:
    color: color of the polygon. Refer to `matplotlib.colors` for a full list of
    formats that are accepted.
    brightness_factor (float): a value in [-1.0, 1.0] range. A lightness factor
    of 0 will correspond to no change, a factor in [-1.0, 0) range will result
    in a darker color and a factor in (0, 1.0] range will result in a lighter
    color.

  Returns:
    modified_color (tuple[double]): a tuple containing the RGB values of the
    modified color. Each value in the tuple is in the [0.0, 1.0] range.
  """
  assert brightness_factor >= -1.0 and brightness_factor <= 1.0
  color = mplc.to_rgb(color)
  polygon_color = colorsys.rgb_to_hls(*mplc.to_rgb(color))
  modified_lightness = polygon_color[1] + (brightness_factor * polygon_color[1])
  modified_lightness = 0.0 if modified_lightness < 0.0 else modified_lightness
  modified_lightness = 1.0 if modified_lightness > 1.0 else modified_lightness
  modified_color = colorsys.hls_to_rgb(polygon_color[0], modified_lightness,
                                       polygon_color[2])
  return modified_color


def _setup_figure(image):
  """Returns an matplotlib figure based on image.
  """
  height, width = image.shape[:2]
  fig = mplfigure.Figure(frameon=False)
  dpi = fig.get_dpi()

  fig.set_size_inches(
      (width + 1e-2) / dpi,
      (height + 1e-2) / dpi,
  )
  canvas = FigureCanvasAgg(fig)
  ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
  ax.axis("off")
  # Need to imshow this first so that other patches can be drawn on top
  ax.imshow(image, extent=(0, width, height, 0), interpolation="nearest")

  return canvas, fig, ax
