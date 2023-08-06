"""This script exports Pytorch model to ONNX format. An .onnx file will show
in the same folder of checkpoint file with same name.
"""
import argparse
import logging

import torch
import onnx
import onnxsim
from torch.autograd import Variable
from torch import onnx as torch_onnx

from ..common.factory import dynamic_import

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Exporter')


def _get_parser():
  """Returns a parser to parse cli args.
  """
  _parser = argparse.ArgumentParser()
  _parser.add_argument('--ckpt', help='Path to checkpoint file')
  _parser.add_argument('--input-size',
                       nargs='+',
                       type=int,
                       default=[224, 224],
                       help='Input image size')
  _parser.add_argument('--batch-size', type=int, default=1, help='Batch size')
  _parser.add_argument('--input-names',
                       nargs='+',
                       default=['images'],
                       help='Customize the input tensor name in ONNX graph')
  _parser.add_argument('--output-names',
                       nargs='+',
                       default=['outputs'],
                       help='Customize the output tensor name in ONNX graph')
  _parser.add_argument('--simplify',
                       action='store_true',
                       help='Simplify the model.')
  return _parser


def main(args):
  """Main function.
  """
  logger.info(str(args))

  # Load checkpoint
  ckpt = torch.load(args.ckpt, map_location='cpu')
  model = dynamic_import(ckpt['model_type'])

  # Construct model from statedict
  logger.info('Loading model')
  model = model.from_state_dict(ckpt['model'], logger=logger)
  model.eval()

  # Build dummy input
  if len(args.input_size) == 1:
    args.input_size = args.input_size * 2
  dummy_input = Variable(torch.randn(args.batch_size, 3,
                                     *args.input_size[::-1]))

  # Run the export
  logger.info('Exporting the model to ONNX...')
  save_file = args.ckpt.replace('.pth', '.onnx')
  torch_onnx.export(model,
                    dummy_input,
                    save_file,
                    verbose=False,
                    input_names=args.input_names,
                    output_names=args.output_names,
                    opset_version=11)
  logger.info('Exporting done, saved to {}'.format(save_file))

  # Run model check and shape inference
  logger.info('Running ONNX check and shape inference on the exported model')
  model_onnx = onnx.load(save_file)
  onnx.checker.check_model(model_onnx)
  onnx.save(onnx.shape_inference.infer_shapes(model_onnx), save_file)

  # Run simplify on the model
  if args.simplify:
    try:
      logger.info('Simplifying with onnx-simplifier {}...'.format(
          onnxsim.__version__))
      model_onnx, check = onnxsim.simplify(model_onnx, check_n=3)
      assert check, 'assert check failed'
      save_file = args.ckpt.replace('.pth', '.sim.onnx')
      onnx.save(model_onnx, save_file)
      logger.info('Simplifying done, saved to {}'.format(save_file))
    except Exception as e:
      logger.error('Simplifier failure: \n{}'.format(str(e)))

  logger.info('All done.')


if __name__ == '__main__':
  main(_get_parser().parse_args())
