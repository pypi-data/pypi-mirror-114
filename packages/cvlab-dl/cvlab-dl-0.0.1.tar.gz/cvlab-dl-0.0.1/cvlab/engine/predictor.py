"""This module provides basic interface of predictors (used when inference).
"""
import logging
import time
from typing import Any, List, Union, Tuple

import numpy as np
import tensorflow as tf
import torch
from PIL import Image

from ..common.factory import dynamic_import
from ..datasets.transform import _Transform
from ..models.base import _BaseModel

logger = logging.getLogger('GenericPredictor')


class _GenericPredictor:
  """Basic framework of predictor, which supports Tensorflow and PyTorch models.
  """

  def __init__(self,
               backend: str = 'pytorch',
               post_processor: callable = None,
               **kwargs):
    """Constructs self

    Args:
      backend: The backend of this predictor, `pytorch` or `tf`.
      post_processor: A callable which takes model outputs as inputs, and runs
      post process.
      kwargs: Other args.
    """
    # Common
    self._model = None
    self._weights_path = None
    self._post_processor = post_processor
    self._backend = backend.lower()

    # For PyTorch model
    self._model_type = None
    self._device = None

    # For TF model
    self._input_names = []
    self._input_tensors = []
    self._output_names = []
    self._output_tensors = []
    self._tf_session = None

    self.__dict__.update(kwargs)

  def _get_image(self,
                 image: Union[np.ndarray, Image.Image, str],
                 transform: Union[_Transform, None] = None,
                 dtype=None) -> np.ndarray:
    """Returns data from `image`. `image` can be string(path to image), PIL
    image(will be converted to np.ndarray) or np.ndarray. This function will
    always return 3-channel RGB image in HWC layout. Additional transformation
    can be applied if `transform` is not None. Datatype cast will be applied if
    `dtype` is specified.

    Args:
      image: The path to image or image itself.
      transform: The transformation to apply on image.
      dtype: If specified, data type will be casted.

    Returns:
      image: HWC RGB image.
    """
    if isinstance(image, str):
      image = np.asarray(Image.open(image))
    if isinstance(image, Image.Image):
      image = np.asarray(image)
    if image.ndim > 3:
      raise ValueError(f'We do not support {image.ndim}-dim image now.')
    # Convert to 3-channel HWC image
    if image.ndim == 2 or (image.ndim == 3 and image.shape[-1] == 1):
      image = np.tile(image, (1, 1, 3))
    if transform is not None:
      image = transform.apply_image(image)
    if dtype is not None:
      image = image.astype(dtype)
    return image

  def prepare_torch_model(self,
                          model_type: Union[_BaseModel, str],
                          state_dict: Union[str, dict],
                          device='cuda',
                          amp=False):
    """Prepare PyTorch model from state_dict

    Args:
      model_type: Full import path of the model or the model class itself.
      state_dict: Path to checkpoint or the state dict itself.
    """
    if isinstance(state_dict, str):
      logger.info('Loading model {} from {}'.format(model_type, state_dict))
    else:
      logger.info('Loading model {} from checkpoint'.format(model_type))
    assert model_type and state_dict

    if isinstance(model_type, str):
      try:
        model = dynamic_import(model_type)
      except ImportError as e:
        raise NotImplementedError(f'{model_type} is not valid') from e
    else:
      model = model_type
    model = model.from_state_dict(state_dict, logger=logger)
    if device.lower() in ('cuda', 'gpu'):
      device = 'cuda'
      model = model.cuda()

    self._model = model
    self._model.eval()
    self._weights_path = state_dict if isinstance(state_dict, str) else None
    self._model_type = model_type
    self._device = device

    if amp and device != 'cuda':
      logger.error(
          'AMP not supported on device {}, thus disabled.'.format(device))
      amp = False
    self._amp = amp

    logger.info('Loading model finished')

  def prepare_tf_model(self,
                       pb_path: str,
                       input_shapes: List[List[int]],
                       input_names: List[str],
                       output_names: List[str],
                       input_types: dict = {}):
    """Prepare tensorflow graph from PB file.

    Args:
      pb_path: Path to .pb file.
      input_shapes: The shape of inputs.
      input_names: The name of input tensors in the graph.
      output_names: The name of output tensors in the graph, no need for the
      `import/` prefix and `:0` suffix, will be added internally.
      input_types: The datatype for all input tensors, default np.float32.
    """
    logger.info('Loading Tensorflow graph from {}'.format(pb_path))
    assert pb_path

    self._input_names = input_names
    self._output_names = output_names
    self._weights_path = pb_path
    self._model = tf.Graph()

    # Load graph definition from pb file
    with tf.io.gfile.GFile(pb_path, 'rb') as f:
      graph_def = tf.compat.v1.GraphDef()
      graph_def.ParseFromString(f.read())
    with self._model.as_default():
      # Initialize input tensor placeholders
      self._input_tensors = [
          tf.compat.v1.placeholder(input_types.get(name, np.float32),
                                   shape=input_shape,
                                   name=name)
          for name, input_shape in zip(input_names, input_shapes)
      ]
      tf.import_graph_def(graph_def, {
          name: tensor for name, tensor in zip(input_names, self._input_tensors)
      })
    self._model.finalize()

    # Get output placeholders
    self._output_tensors = [
        self._model.get_tensor_by_name(f'import/{name}:0')
        for name in self._output_names
    ]

    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    self._tf_session = tf.compat.v1.Session(graph=self._model, config=config)

    logger.info('Loading model finished')

  def prepare_data(self):
    """Prepare model input from original data, should implement in subclasses.
    """
    raise NotImplementedError

  def run(self, data: Any, log_stats: bool, *args,
          **kwargs) -> Tuple[Any, dict]:
    """Run prediction on data.

    1. Prepare model inputs from `data`, so the `prepare_data` method must be
    implemented in subclasses.
    2. Feed data to model and get outputs
    3. If possible, model outputs will be feed into self._post_processor to
    generate final results. By default, raw model outputs are returned.

    Args:
      data: The model inputs, will be feed into self.prepare_data.
      log_stats: Wether to log running time stats.
      *args: More args to feed into self.prepare_data and self.post_process.
      **kwargs: More kwargs to feed into self.prepare_data and self.post_process

    Returns:
      output: The inference output.
      stat: The running time stats.
    """
    t1 = time.time()  # Start
    data = self.prepare_data(data, *args, **kwargs)
    if self._backend == 'pytorch':
      if self._device == 'cuda':
        data = data.cuda()
      t2 = time.time()  # Data preparation done
      with torch.no_grad():
        if self._amp:
          with torch.cuda.amp.autocast():
            model_out = self._model(data)
        else:
          model_out = self._model(data)
        if isinstance(model_out, torch.Tensor):
          model_out = model_out.detach().cpu().numpy()
      t3 = time.time()  # Model computation done
    elif self._backend == 'tf':
      if not isinstance(data, tuple):
        data = (data,)
      feed_dict = {
          placeholder: item
          for placeholder, item in zip(self._input_tensors, data)
      }
      t2 = time.time()  # Data preparation done
      model_out = self._tf_session.run(self._output_tensors,
                                       feed_dict=feed_dict)
      t3 = time.time()  # Model computation done
      model_out = {
          name: data for name, data in zip(self._output_names, model_out)
      }

    output = self.post_process(model_out, *args, **kwargs)
    t4 = time.time()  # Post process done.

    if log_stats:
      log_str = 'Inference done, ' \
              'total: {:.3f}s, ' \
              'data: {:.3f}s, model: {:.3f}s, post: {:.3f}s'.format(
                  t4 - t1, t2 - t1, t3 - t2, t4 - t3)
      logger.info(log_str)

    return output, {
        'total': t4 - t1,
        'data': t2 - t1,
        'model': t3 - t2,
        'post': t4 - t3
    }

  def post_process(self, model_out, *args, **kwargs):
    """Run post processing from model output.
    """
    if self._post_processor is not None:
      return self._post_processor(model_out, *args, **kwargs)
    return model_out
