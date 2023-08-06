"""This script converts ONNX model to Tensorflow frozen graph(.pb) while
supporting both NCHW and NHWC layouts.
"""
import argparse
import logging
from typing import Tuple, List

import cv2
import numpy as np
import onnx
import onnxruntime as ort
import os
import tensorflow as tf
from onnx import ValueInfoProto, ModelProto, TensorProto, NodeProto
from PIL import Image

logger = logging.getLogger('Converter')


def _get_parser() -> argparse.ArgumentParser:
  _parser = argparse.ArgumentParser()
  _parser.add_argument('--input',
                       type=str,
                       required=True,
                       help='ONNX model path')
  _parser.add_argument('--output',
                       required=False,
                       type=str,
                       default=None,
                       help='Where to save the model')
  _parser.add_argument('--layout',
                       type=str,
                       choices=['nchw', 'nhwc'],
                       default='nhwc',
                       help='The data layout to use inside TF model')
  _parser.add_argument('--test-data',
                       nargs='+',
                       default=[],
                       help='Key-Value pair for test data')
  _parser.add_argument('--test-tolerance',
                       type=float,
                       default=1e-3,
                       help='Testing tolerance for ONNX model and TF graph.')
  _parser.add_argument('--verbose', action='store_true', help='More logs')
  return _parser


class DataTypeHandler:
  """This class contains functions about data type conversion.
  """

  @classmethod
  def onnx_dtype_to_numpy(cls, dtype):
    """Returns equivalent numpy data type of ONNX datatype.
    """
    return onnx.mapping.TENSOR_TYPE_TO_NP_TYPE[dtype]

  @classmethod
  def numpy_dtype_to_tf(cls, dtype):
    """Returns equivalent tf data type of numpy datatype.
    """
    return tf.dtypes.as_dtype(dtype)

  @classmethod
  def onnx_dtype_to_tf(cls, dtype):
    """Returns equivalent tf data type of ONNX datatype.
    """
    return cls.numpy_dtype_to_tf(cls.onnx_dtype_to_numpy(dtype))


class OpAdapter:
  """Adapter for converting ONNX func to TF func.
  """

  @staticmethod
  def Conv(name: str, attrs: dict, inputs: List[tf.Tensor],
           input_names: List[str], input_values: List[np.ndarray]) -> tf.Tensor:
    input_tensor, weight = inputs[:2]  # bias is not required
    input_values = {
        tensor.name: array for tensor, array in zip(inputs, input_values)
    }

    group = attrs['group']
    use_layout = attrs['use_layout']
    dilat_h, dilat_w = attrs['dilations']
    pt, pb, pl, pr = attrs['pads']
    stride_h, stride_w = attrs['strides']
    kh, kw = weight.shape.as_list()[2:]

    # The input_tensor already has `use_layout`, we need to handle other attrs
    if use_layout == 'nhwc':
      _, h, w, c = input_tensor.shape.as_list()
    else:
      _, c, h, w = input_tensor.shape.as_list()

    # Handle the padding. If ONNX padding does not change the input shape, we
    # use tf padding = 'SAME', otherwise we pad the input explicitly and then
    # use tf padding = 'VALID'
    onnx_new_w = (w + pl + pr - dilat_w * (kw - 1) - 1) / stride_w + 1
    onnx_new_w = int(onnx_new_w)
    onnx_new_h = (h + pt + pb - dilat_h * (kh - 1) - 1) / stride_h + 1
    onnx_new_h = int(onnx_new_h)
    if onnx_new_h == h and onnx_new_w == w:
      padding = 'SAME'
      output_tensor = input_tensor
    elif sum(attrs['pads']):
      padding = 'VALID'
      if use_layout == 'nhwc':
        pads = [[0, 0], [pt, pb], [pl, pr], [0, 0]]
      else:  # nchw
        pads = [[0, 0], [0, 0], [pt, pb], [pl, pr]]
      output_tensor = tf.pad(input_tensor, pads, 'CONSTANT', name=name + '.pad')
    else:
      # No padding
      padding = 'VALID'
      output_tensor = input_tensor

    # Handle the strides
    if use_layout == 'nhwc':
      strides = [1, stride_h, stride_w, 1]
    else:
      strides = [1, 1, stride_h, stride_w]

    if group == c:
      # Depth-wise convolution
      # ONNX weights are (out, in/group, h, w), convert to (h, w, in, out/in)
      # Here out/in = in/group = 1, in = out
      weight_data = input_values[weight.name].transpose(2, 3, 0, 1)
      weight = tf.compat.v1.constant(value=weight_data, name=input_names[1])
      output_tensor = tf.nn.depthwise_conv2d(output_tensor,
                                             weight,
                                             strides,
                                             padding,
                                             name=name + '.conv',
                                             data_format=use_layout.upper(),
                                             dilations=(dilat_h, dilat_w))
    else:
      # Normal convolution
      if group != 1:
        raise ValueError(
            f'conv group {group} with {c}-channel input not supported')
      # (out, in, h, w) -> (h, w, in, out)
      weight_data = input_values[weight.name].transpose(2, 3, 1, 0)
      weight = tf.compat.v1.constant(value=weight_data, name=input_names[1])
      output_tensor = tf.nn.conv2d(output_tensor,
                                   weight,
                                   strides,
                                   padding,
                                   data_format=use_layout.upper(),
                                   dilations=(dilat_h, dilat_w),
                                   name=name + '.conv')

    # Handle bias
    if len(inputs) > 2:
      output_tensor = tf.nn.bias_add(output_tensor,
                                     inputs[2],
                                     name=name,
                                     data_format=use_layout.upper())

    return output_tensor

  @staticmethod
  def Clip(name: str, attrs: dict, inputs: List[tf.Tensor]) -> tf.Tensor:
    min_val = attrs.get('min', None)
    min_val = inputs[1] if inputs[1] is not None else min_val
    min_val = min_val if min_val is not None else -1e32

    max_val = attrs.get('max', None)
    max_val = inputs[2] if inputs[2] is not None else max_val
    max_val = max_val if max_val is not None else 1e32

    # If this is actually a RuLU6
    eps = 1e-5
    if abs(min_val.eval()) < eps and abs(max_val.eval() - 6.) < eps:
      return tf.nn.relu6(inputs[0], name=name)

    return tf.clip_by_value(inputs[0], min_val, max_val, name=name)

  @staticmethod
  def Add(name: str, inputs: List[tf.Tensor]) -> tf.Tensor:
    return tf.add(inputs[0], inputs[1], name=name)

  @staticmethod
  def Relu(name: str, inputs: List[tf.Tensor]) -> tf.Tensor:
    return tf.nn.relu(inputs[0], name=name)

  @staticmethod
  def GlobalAveragePool(name: str, inputs: List[tf.Tensor],
                        attrs: dict) -> tf.Tensor:
    if attrs['use_layout'] == 'nhwc':
      return tf.reduce_mean(inputs[0], [1, 2], name=name, keepdims=True)
    return tf.reduce_mean(inputs[0], [2, 3], name=name, keepdims=True)

  @staticmethod
  def Resize(name: str, inputs: List[tf.Tensor], attrs: dict) -> tf.Tensor:
    assert len(inputs) >= 3
    use_layout = attrs['use_layout']

    # Calc the output spatial shape
    if len(inputs) == 3:  # Resize by scales
      sn, sc, _, _ = inputs[2].eval()  # Scales are NCHW for ONNX
      assert sn == 1 and sc == 1, 'Batch and channel axis cannot be resized!'
      if use_layout == 'nhwc':
        shape_ori = tf.cast(tf.shape(inputs[0])[1:3], tf.float32)
      else:
        shape_ori = tf.cast(tf.shape(inputs[0])[2:], tf.float32)
      shape = tf.cast(shape_ori * inputs[2][2:], tf.int32)
    else:  # Resize to sizes
      shape = tf.cast(inputs[3][2:], tf.int32)

    align_corners = (attrs['coordinate_transformation_mode'].decode('utf8') ==
                     'align_corners')
    half_pixel_centers = (attrs['coordinate_transformation_mode'].decode('utf8')
                          == 'pytorch_half_pixel')

    # TF resize supports NHWC only, so do the transpose if needed
    if use_layout == 'nchw':
      inputs[0] = tf.transpose(inputs[0], (0, 2, 3, 1))

    resized = tf.image.resize_bilinear(inputs[0],
                                       shape,
                                       align_corners=align_corners,
                                       half_pixel_centers=half_pixel_centers,
                                       name=name)

    if use_layout == 'nchw':
      resized = tf.transpose(resized, (0, 3, 1, 2))

    return resized

  @staticmethod
  def Concat(name: str, inputs: List[tf.Tensor], attrs: dict) -> tf.Tensor:
    if len(inputs) == 1:
      return inputs[0]
    axis = 'nchw'[attrs['axis']]
    axis = attrs['use_layout'].find(axis)
    return tf.concat(inputs, axis, name=name)

  @staticmethod
  def ArgMax(name: str, inputs: List[tf.Tensor], attrs: dict) -> tf.Tensor:
    axis = 'nchw'[attrs['axis']]
    axis = attrs['use_layout'].find(axis)
    if attrs['keepdims']:
      out = tf.argmax(inputs[0], axis)
      return tf.expand_dims(out, axis, name=name)
    return tf.argmax(inputs[0], axis, name=name)

  @staticmethod
  def Shape(name: str, inputs: List[tf.Tensor]) -> tf.Tensor:
    shape = inputs[0].shape.as_list()
    if None in shape:
      raise ValueError('We expect constant shape!')
    return tf.constant(value=shape, dtype=tf.int64, name=name)

  @staticmethod
  def Constant(name: str, attrs: dict) -> tf.Tensor:
    return tf.constant(value=attrs['value'], name=name)

  @staticmethod
  def MaxPool(name: str, inputs: List[tf.Tensor], attrs: dict) -> tf.Tensor:
    use_layout = attrs['use_layout']
    kh, kw = attrs['kernel_shape']
    stride_h, stride_w = attrs['strides']
    pt, pb, pl, pr = attrs['pads']
    dilat_h, dilat_w = attrs.get('dilation', [1, 1])

    if use_layout == 'nhwc':
      _, h, w, _ = inputs[0].shape.as_list()
    else:
      _, _, h, w = inputs[0].shape.as_list()

    # Handle the padding. If ONNX padding does not change the input shape, we
    # use tf padding = 'SAME', otherwise we pad the input explicitly and then
    # use tf padding = 'VALID'
    onnx_new_w = (w + pl + pr - dilat_w * (kw - 1) - 1) / stride_w + 1
    onnx_new_w = int(onnx_new_w)
    onnx_new_h = (h + pt + pb - dilat_h * (kh - 1) - 1) / stride_h + 1
    onnx_new_h = int(onnx_new_h)
    if onnx_new_h == h and onnx_new_w == w:
      padding = 'SAME'
      output_tensor = inputs[0]
    elif sum(attrs['pads']):
      padding = 'VALID'
      if use_layout == 'nhwc':
        pads = [[0, 0], [pt, pb], [pl, pr], [0, 0]]
      else:  # nchw
        pads = [[0, 0], [0, 0], [pt, pb], [pl, pr]]
      output_tensor = tf.pad(inputs[0], pads, 'CONSTANT', name=name + '.pad')
    else:
      # No padding
      padding = 'VALID'
      output_tensor = inputs[0]

    if use_layout == 'nhwc':
      kernel = [1, kh, kw, 1]
      strides = [1, stride_h, stride_w, 1]
    else:
      kernel = [1, 1, kh, kw]
      strides = [1, 1, stride_h, stride_w]

    return tf.nn.max_pool(output_tensor,
                          kernel,
                          strides,
                          padding=padding,
                          name=name,
                          data_format=use_layout.upper())

  @staticmethod
  def BatchNormalization(name: str, inputs: List[tf.Tensor],
                         attrs: dict) -> tf.Tensor:
    scale, shift, mean, var = inputs[1:]
    return tf.compat.v1.nn.fused_batch_norm(
        inputs[0],
        scale,
        shift,
        mean=mean,
        variance=var,
        epsilon=attrs['epsilon'],
        data_format=attrs['use_layout'].upper(),
        is_training=False,
        name=name)

  @staticmethod
  def ConstantOfShape(name: str, inputs: List[tf.Tensor], attrs) -> tf.Tensor:
    return tf.fill(inputs[0], attrs['value'][0], name=name)


class Converter:
  """Converter which parses an ONNX model and build an equivalent one for TF 1.x
  """

  def __init__(self, layout: str = 'nhwc', verbose: bool = False) -> None:
    self._verbose = verbose
    self._layout = layout
    if verbose:
      logging.basicConfig(level=logging.DEBUG)
    else:
      logging.basicConfig(level=logging.INFO)

    # Runtime var
    self._tf_input_tensors = {}  # name -> tf tensor
    self._tf_output_tensors = {}  # node name -> tf tensor
    self._name_to_tf_tensor = {}  # name -> tf tensor
    self._constants = {}  # name -> np.ndarray

  def create_input(self, tensor: ValueInfoProto):
    """Adds an input tensor to tf and returns it.
    """
    shape = [int(x.dim_value) for x in tensor.type.tensor_type.shape.dim]
    # Data layout in ONNX is always NCHW for 4D tensors
    assert len(shape) == 4, 'We expect NCHW layout for ONNX model!'
    n, c, h, w = shape

    # The desired input shape based on self._layout
    if self._layout == 'nchw':
      shape = (n, c, h, w)
    else:
      shape = (n, h, w, c)

    # Create tf placeholder.
    dtype = DataTypeHandler.onnx_dtype_to_tf(tensor.type.tensor_type.elem_type)
    placeholder = tf.compat.v1.placeholder(dtype, shape=shape, name=tensor.name)
    return placeholder

  def create_initializer(self,
                         tensor: TensorProto) -> Tuple[tf.Tensor, np.ndarray]:
    """Create initializers in the graph. Initializers are constant tensors.
    """

    # Load tensor data as numpt array
    tensor_data = tensor.raw_data
    dtype = DataTypeHandler.onnx_dtype_to_numpy(tensor.data_type)
    tensor_data = np.frombuffer(tensor_data, dtype=dtype)

    if len(tensor_data) == 0:
      # Find value in other places
      if hasattr(tensor, 'float_data') and dtype == np.float32:
        tensor_data = np.array(tensor.float_data, dtype=dtype)
      if hasattr(tensor, 'double_data') and dtype == np.float:
        tensor_data = np.array(tensor.double_data, dtype=dtype)
      if hasattr(tensor, 'int32_data') and dtype == np.int32:
        tensor_data = np.array(tensor.int32_data, dtype=dtype)
      if hasattr(tensor, 'int64_data') and dtype == np.int64:
        tensor_data = np.array(tensor.int64_data, dtype=dtype)

    dims = tuple(tensor.dims)
    if len(dims) > 0 or len(tensor_data) > 1:
      tensor_data = tensor_data.reshape(dims)
    logger.debug('constant {} with shape {}'.format(tensor.name, str(dims)))

    # If this tensor is the weight of conv layer, we append a suffix to it
    name = tensor.name
    if name.endswith('weight') and tensor_data.ndim == 4:
      name += '_convweights'
    tftype = DataTypeHandler.onnx_dtype_to_tf(tensor.data_type)
    constant = tf.compat.v1.constant(value=tensor_data,
                                     dtype=tftype,
                                     shape=dims,
                                     name=name)
    return constant, tensor_data

  @staticmethod
  def parse_node_attrs(node: NodeProto) -> dict:
    """Parse the node attrs to Python dict.
    """
    attrs = {}
    for attr in node.attribute:
      if attr.type == 4:  # AttributeType is TENSOR
        dtype = DataTypeHandler.onnx_dtype_to_numpy(attr.t.data_type)
        data = np.frombuffer(attr.t.raw_data, dtype=dtype)
        shape = attr.t.dims
        if shape or len(data) > 1:
          data = data.reshape(shape)
        else:
          data = dtype.type(data[0])
        attrs[attr.name] = data
      else:
        # Other attributes
        attrs[attr.name] = onnx.helper.get_attribute_value(attr)
    return attrs

  def create_node(self, node: NodeProto) -> dict:
    """Converts an ONNX node to TF graph, returns the mapping from output name
    to output tensor.

    Args:
      node: The ONNX node to add.

    Returns:
      A dict mapping output name to output tensor.
    """
    logger.debug('-----------------')
    op_type = node.op_type
    if not hasattr(OpAdapter, op_type):
      logger.error(str(node))
      raise AttributeError(
          f'Op {op_type} not supported yet, please add it to OpAdapter')

    # Construct node attributes
    attrs = self.parse_node_attrs(node)
    attrs['use_layout'] = self._layout
    logger.info('ONNX node: {}, op: {}, attrs: {}'.format(
        node.name, op_type, str(attrs)))

    # Get all input tensors for this node
    inputs = [self._name_to_tf_tensor[name] for name in node.input]
    for name, tensor in zip(node.input, inputs):
      logger.debug('ONNX tensor {} -> TF tensor {} with shape {}'.format(
          name, tensor.name, tensor.shape))

    # Handeling some ONNX ops
    if op_type == 'Constant':
      # Store the raw data of constants
      for output in node.output:
        self._constants[output] = attrs['value']

    params = {
        'inputs': inputs,
        'attrs': attrs,
        'name': node.name,
        'input_names': node.input,
        'output_names': node.output,
        # Some input are constants
        'input_values': [
            self._constants.get(name, None) for name in node.input
        ]
    }
    _func = getattr(OpAdapter, op_type)
    # Run _func with the params it need
    ret = _func(
        **{k: v for k, v in params.items() if k in _func.__code__.co_varnames})

    if isinstance(ret, tf.Tensor):
      ret = [ret]

    for name, tensor in zip(node.output, ret):
      self._name_to_tf_tensor[name] = tensor
      logger.debug('ONNX tensor {} -> TF tensor {} with shape {}'.format(
          name, tensor.name, tensor.shape))

    return {name: tensor for name, tensor in zip(node.output, ret)}

  def convert(self, onnx_model: ModelProto) -> None:
    """Entry point for converting.
    """
    # Find initializers in the graph, they are constants
    initializers = set([tensor.name for tensor in onnx_model.graph.initializer])

    # Find input nodes that need runtime feed-in (i.e. non-initializers)
    logger.info('Adding network inputs...')
    tensors_need_feed_in = [
        tensor for tensor in onnx_model.graph.input
        if tensor.name not in initializers
    ]
    # Create all input placeholders for TF
    for tensor in tensors_need_feed_in:
      placeholder = self.create_input(tensor)
      self._tf_input_tensors[tensor.name] = placeholder
      self._name_to_tf_tensor[tensor.name] = placeholder

    # Create all initializers(constants) for TF
    logger.info('Adding network constants...')
    for tensor in onnx_model.graph.initializer:
      constant, constatn_data = self.create_initializer(tensor)
      self._name_to_tf_tensor[tensor.name] = constant
      self._constants[tensor.name] = constatn_data

    # Add all output nodes which constructs the whole graph
    logger.info('Adding all nodes...')
    output_to_add = set([tensor.name for tensor in onnx_model.graph.output])
    for node in onnx_model.graph.node:
      # If this node generates model output, rename the node to output name
      for name in node.output:
        if name in output_to_add:
          node.name = name
          break
      ret = self.create_node(node)
      for name in node.output:
        if name in output_to_add:
          output_to_add.remove(name)
          self._tf_output_tensors[node.name] = ret[name]
      if len(output_to_add) == 0:
        break

    logstr = ''
    for k, v in self._tf_output_tensors.items():
      logstr += 'name: {}, shape: {}\n'.format(k, str(v.shape))
    logger.info('Model outputs:\n' + logstr)

  def save(self, sess: tf.compat.v1.Session, output: str) -> None:
    """Save the graph.
    """
    constant_graph = tf.compat.v1.graph_util.convert_variables_to_constants(
        sess, sess.graph_def, list(self._tf_output_tensors.keys()))
    with open(output, mode='wb') as f:
      f.write(constant_graph.SerializeToString())
    logger.info('Graph saved to {}'.format(output))

  def check(self,
            sess: tf.compat.v1.Session,
            onnx_model_path: str,
            test_data: dict,
            tolerance: float = 1e-3) -> bool:
    """Check the consistency of ONNX model and converted TF graph with same
    input.

    Args:
      sess: The tf session.
      onnx_model_path: Path to ONNX model.
      test_data: Dict mapping input name to test data
      tolerance: Tolerance of absolute mean bias for ONNX model and TF outputs.
    """
    # Prepare data
    input_dict = {}
    for k, v in self._tf_input_tensors.items():
      if k not in test_data:
        raise KeyError(f'{k} is required for checking!')
      if isinstance(test_data[k], str):
        image = np.asarray(Image.open(test_data[k]))
        if self._layout == 'nhwc':
          n, h, w, c = v.shape.as_list()
        else:
          n, c, h, w = v.shape.as_list()
        # Resize image to desired shape
        if image.shape[:2] != (h, w):
          image = cv2.resize(image, (w, h))
        if image.ndim == 2:
          image = image[..., None]  # to HWC
        if image.shape[-1] == 1 and c > 1:
          image = np.tile(image, (1, 1, c))
        image = np.tile(image[None, ...], (n, 1, 1, 1))  # NHWC
      input_dict[k] = image

    # Calculate the output of ONNX model
    onnx_sess = ort.InferenceSession(onnx_model_path)
    onnx_out_names = [item.name for item in onnx_sess.get_outputs()]
    onnx_outputs = onnx_sess.run(
        onnx_out_names,
        {
            k: v.transpose(0, 3, 1, 2).astype(np.float32)
            for k, v in input_dict.items()
        },
    )
    onnx_outputs = {k: v for k, v in zip(onnx_out_names, onnx_outputs)}

    # Calculate the output of TF model
    sess.run(tf.compat.v1.global_variables_initializer())
    # Build feed dict
    input_dict = {
        self._tf_input_tensors[k]:
        v.astype(np.float32) if self._layout == 'nhwc' else v.transpose(
            0, 3, 1, 2).astype(np.float32) for k, v in input_dict.items()
    }
    # Run the session
    tf_output_names = list(self._tf_output_tensors.keys())
    tf_outputs = sess.run([self._tf_output_tensors[k] for k in tf_output_names],
                          input_dict)
    tf_outputs = {k: v for k, v in zip(tf_output_names, tf_outputs)}

    # Calculate the diff between onnx_outputs and tf_outputs
    passed = True
    for k, onnx_output in onnx_outputs.items():
      tf_output = tf_outputs[k]
      diff = np.abs(onnx_output - tf_output).mean()
      logger.info('Mean diff for {}: {}'.format(k, diff))
      if diff > tolerance:
        passed = False

    return passed


if __name__ == '__main__':
  args = _get_parser().parse_args()
  model = onnx.load(args.input)

  with tf.compat.v1.Session() as sess:
    converter = Converter(verbose=args.verbose, layout=args.layout)
    converter.convert(model)
    if args.output is None:
      args.output = os.path.splitext(args.input)[0] + '.pb'
    converter.save(sess, args.output)

    if len(args.test_data):
      # Build test data dict
      test_data = {
          args.test_data[i]: args.test_data[i + 1]
          for i in range(len(args.test_data) // 2)
      }

      logger.info('Checking consistency of ONNX model and TF graph...')
      if converter.check(sess, args.input, test_data, args.test_tolerance):
        logger.info('Consistency check passed.')
      else:
        logger.warning('Consistency check failed!')
