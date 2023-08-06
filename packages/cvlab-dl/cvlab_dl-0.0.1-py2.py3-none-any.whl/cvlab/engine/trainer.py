"""This module provides training utils for models.
"""
import argparse
import datetime
import logging
import os
import time
from typing import Union

import cv2
import torch
import yaml
from torch.nn.parallel import DistributedDataParallel
from torch.optim import Optimizer
from torch.optim.lr_scheduler import _LRScheduler
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from ..common.factory import dynamic_import, object_from_dict, findattr
from ..common.utils import manual_seed_all, to_cuda
from ..datasets.base import _BaseDataset
from ..datasets.transform import TransformList
from ..models.base import _BaseModel
from ..optimizer.lr_warmup import GradualWarmupScheduler

# Fix cv2 deadlock in multiprocessing
cv2.setNumThreads(0)


class BasicTrainer:
  """Class which provides basic training interface for general models.
  """

  @staticmethod
  def build_model(model_conf: dict,
                  state_dict: Union[dict, None] = None,
                  logger: logging.Logger = None) -> _BaseModel:
    t1 = time.time()

    if state_dict is not None:
      model = dynamic_import(model_conf['Type'])
      model = model.from_state_dict(state_dict, logger=logger)
    else:
      model_conf.setdefault('KwArgs', {})['logger'] = logger
      model = object_from_dict(model_conf)

    if logger:
      logger.info('Build model {} in {:.3f}s'.format(str(model),
                                                     time.time() - t1))
    return model

  @staticmethod
  def build_optimizer(model: Union[_BaseModel, DistributedDataParallel],
                      optim_conf: dict,
                      logger: logging.Logger = None) -> Optimizer:
    t1 = time.time()
    if isinstance(model, DistributedDataParallel):
      model = model.module

    if isinstance(optim_conf['Freeze'], (list, tuple)):
      for submodule in optim_conf['Freeze']:
        try:
          model.freeze(submodule)
          if logger:
            logger.info('Freeze {}'.format(submodule))
        except AttributeError:
          if logger:
            logger.error(
                'Submodule {} does not exist, skipping...'.format(submodule))

    if 'params' in optim_conf.get('KwArgs', {}):
      # Specify different lr for each param group
      for conf_dict in optim_conf['KwArgs']['params']:
        # Get the submodule of model by conf_dict['params']
        conf_dict['params'] = filter(
            lambda p: p.requires_grad,
            findattr(model, conf_dict['params']).parameters())
    else:
      optim_conf.setdefault('KwArgs',
                            {})['params'] = filter(lambda p: p.requires_grad,
                                                   model.parameters())
    optim = object_from_dict(optim_conf)
    if logger:
      logger.info('Build optimizer {} in {:.3f}s'.format(
          str(optim),
          time.time() - t1))
    return optim

  @staticmethod
  def build_scheduler(optimizer: Optimizer,
                      scheduler_conf: dict,
                      logger: logging.Logger = None
                     ) -> Union[_LRScheduler, GradualWarmupScheduler]:
    t1 = time.time()
    scheduler_conf.setdefault('Args', [None])[0] = optimizer
    scheduler = object_from_dict(scheduler_conf)

    # If lr warmup is enabled, wrap original scheduler in GradualWarmupScheduler
    if scheduler_conf.get('Warmup', None):
      warmup_conf = scheduler_conf['Warmup']
      scheduler = GradualWarmupScheduler(optimizer,
                                         *warmup_conf.get('Args', []),
                                         **warmup_conf.get('KwArgs', {}),
                                         after_scheduler=scheduler)

    if logger:
      logger.info('Build scheduler {} in {:.3f}s'.format(
          str(scheduler),
          time.time() - t1))
    return scheduler

  @staticmethod
  def build_dataset(dataset_conf: dict,
                    logger: logging.Logger = None) -> _BaseDataset:
    t1 = time.time()
    dataset_conf.setdefault('KwArgs', {})['logger'] = logger

    if 'preprocess' in dataset_conf.get('KwArgs', {}):
      # Compose preprocess transformation for dataset
      if isinstance(dataset_conf['KwArgs']['preprocess'], (list, tuple)):
        preprocess = [
            object_from_dict(item)
            for item in dataset_conf['KwArgs']['preprocess']
        ]
      dataset_conf['KwArgs']['preprocess'] = TransformList(*preprocess)

    dataset = object_from_dict(dataset_conf)
    if logger:
      logger.info('Build dataset {} in {:.3f}s with {} frames'.format(
          str(dataset),
          time.time() - t1, len(dataset)))
    return dataset

  @staticmethod
  def build_dataloader(dataset: _BaseDataset, loader_conf) -> DataLoader:
    return dataset.get_loader(*loader_conf.get('Args', []),
                              **loader_conf.get('KwArgs', {}))

  @classmethod
  def launch(cls,
             cfg: Union[str, dict] = {},
             resume: Union[str, None] = None,
             save_dir: Union[str, None] = None):
    """Launch the training process.

    Args:
      cfg: The config file path or config dict itself.
      resume: If set, `cfg` will be ignored, and configs are loaded from resume
      dir.
      device: Specify which device to run this training.
    """
    if isinstance(resume, str):
      with open(os.path.join(resume, 'config.yaml'), 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
      cfg['Train']['Resume'] = resume
    elif isinstance(cfg, str):
      with open(cfg, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    if save_dir:
      cfg['Train']['Loop']['Path'] = save_dir

    exp_id = datetime.datetime.now().strftime(r'%m%d_%H%M')
    cfg['Train']['Loop']['Path'] = cfg['Train']['Loop']['Path'].replace(
        r'{exp_id}', exp_id)

    # Save the training config
    os.makedirs(cfg['Train']['Loop']['Path'], exist_ok=True)
    with open(os.path.join(cfg['Train']['Loop']['Path'], 'config.yaml'),
              'w+') as f:
      yaml.dump(cfg, f)

    if cfg['Train']['DDP']['Enable']:
      assert torch.cuda.is_available()
      # Setup DDP environment
      os.environ['MASTER_ADDR'] = cfg['Train']['DDP']['MASTER_ADDR']
      os.environ['MASTER_PORT'] = cfg['Train']['DDP']['MASTER_PORT']
      torch.multiprocessing.spawn(cls._launch_impl,
                                  nprocs=torch.cuda.device_count(),
                                  args=(cfg, True),
                                  join=True)
    else:
      if torch.cuda.is_available():
        cls._launch_impl(0, cfg, is_dist=False)
      else:
        cls._launch_impl('cpu', cfg, is_dist=False)

  @classmethod
  def _launch_impl(cls, device: Union[str, int], cfg: dict, is_dist=False):
    """Launch the training loop. Basic trainer only support training on CPU or
    single CUDA device. For multi-device training, please see `DDPTrainer`.

    Args:
      device: The device for this process to run on.
      cfg: The training and evaluation config.
      is_dist: Is this process one of the distributed processes.
    """
    manual_seed_all(cfg['Train'].get('Seed', 0))

    # Init distributed training backend
    if cfg['Train']['DDP']['Enable']:
      assert isinstance(device, int), "DDP requires device as integer"
      torch.distributed.init_process_group(backend='nccl',
                                           init_method='env://',
                                           world_size=torch.cuda.device_count(),
                                           rank=device)

    IS_MAIN_PROCESS = (not is_dist) or device == 0

    # Build logger
    loop_conf = cfg['Train']['Loop']
    logger = logging.getLogger(cls.__name__)
    logger.setLevel(getattr(logging, loop_conf['LogLevel']))
    logger.handlers.clear()

    # Log to file for all processes
    logFormatter = logging.Formatter(
        fmt='%(asctime)s:%(name)s:%(levelname)-4s:%(message)s')
    fileHandler = logging.FileHandler(
        os.path.join(loop_conf['Path'], f'trainlog_{device}.log'))
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    # Log to stderr for main process
    if IS_MAIN_PROCESS:
      consoleHandler = logging.StreamHandler()
      consoleHandler.setFormatter(logFormatter)
      logger.addHandler(consoleHandler)

    # Logging to tensorboard for main process
    if IS_MAIN_PROCESS:
      tensorboard_log_dir = os.path.join(loop_conf['Path'], 'tensorboard')
      os.makedirs(tensorboard_log_dir, exist_ok=True)
      writer = SummaryWriter(tensorboard_log_dir)

    # If we are resuming, load last state dict
    if cfg['Train'].get('Resume', None):
      with open(os.path.join(cfg['Train']['Resume'], 'last_ckpt.txt'),
                'r') as f:
        weights_name = f.readline().strip()
      state_dict = os.path.join(cfg['Train']['Resume'], 'checkpoints',
                                weights_name)
      state_dict = torch.load(state_dict, map_location='cpu')
    else:
      state_dict = {}

    # Build the model
    model = cls.build_model(cfg['Model'],
                            state_dict.get('Model', None),
                            logger=logger)
    model = model.to(device)
    if is_dist:
      model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model)
      model = DistributedDataParallel(model,
                                      device_ids=[device],
                                      find_unused_parameters=True)
      real_model = model.module
    else:
      real_model = model

    # Build the optimizer
    optim = cls.build_optimizer(model, cfg['Train']['Optim'], logger)
    if state_dict:
      optim.load_state_dict(state_dict['optim'])

    # Build scheduler
    scheduler = cls.build_scheduler(optim, cfg['Train']['Scheduler'], logger)
    if state_dict:
      scheduler.load_state_dict(state_dict['scheduler'])

    if cfg['Train'].get('AMP', False):
      logger.info('Building scaler')
      scaler = torch.cuda.amp.GradScaler()
    else:
      scaler = None

    # Build datasets and dataloaders
    train_dataset = cls.build_dataset(cfg['Train']['Dataset'], logger)
    if is_dist:
      sampler = torch.utils.data.distributed.DistributedSampler(
          dataset=train_dataset,
          num_replicas=torch.cuda.device_count(),
          rank=device,
          shuffle=cfg['Train']['Dataloader'].get('KwArgs',
                                                 {}).get('shuffle', False))
      cfg['Train']['Dataloader'].setdefault('KwArgs', {})['shuffle'] = False
      cfg['Train']['Dataloader'].setdefault('KwArgs', {})['sampler'] = sampler
    train_loader = cls.build_dataloader(train_dataset,
                                        cfg['Train']['Dataloader'])

    if IS_MAIN_PROCESS:
      val_dataset = cls.build_dataset(cfg['Val']['Dataset'], logger)
      val_loader = cls.build_dataloader(val_dataset, cfg['Val']['Dataloader'])

    loop_conf['StartTime'] = datetime.datetime.now()
    logger.info('Start training at {}'.format(
        loop_conf['StartTime'].strftime(r'%Y-%m-%d %H:%M:%S')))

    cur_iter = state_dict['iter'] if cfg['Train'].get('Resume') else 0
    last_time = datetime.datetime.now()

    while True:
      for images, targets in train_loader:
        cur_iter += 1
        if cur_iter > loop_conf['MaxIter']:
          break

        optim.zero_grad()

        # Warmup should run before optimizer. To avoid the UserWarning about
        # order of calling optimizer and scheduler, we call optim.step here once
        if isinstance(scheduler, GradualWarmupScheduler):
          if cur_iter == 1:
            optim.step()
          scheduler.step()

        model.train()

        if cfg['Train'].get('AMP', False):
          with torch.cuda.amp.autocast():
            images, targets = to_cuda(images, device), to_cuda(targets, device)
            loss = model(images,
                         targets,
                         loss_conf=cfg['Train'].get('Loss', None))
          scaler.scale(loss).backward()
          scaler.step(optim)
          scaler.update()
        else:
          images, targets = to_cuda(images, device), to_cuda(targets, device)
          loss = model(images,
                       targets,
                       loss_conf=cfg['Train'].get('Loss', None))
          loss.backward()
          optim.step()

        if not isinstance(scheduler, GradualWarmupScheduler):
          scheduler.step()

        if IS_MAIN_PROCESS:
          # Log current lr
          writer.add_scalar('Train/lr', scheduler.get_lr()[0], cur_iter)

        if cur_iter % loop_conf['LogStep'] == 0:
          if IS_MAIN_PROCESS and hasattr(real_model, 'summary'):
            try:
              real_model.summary(writer, cur_iter)
            except NotImplementedError:
              logger.error('Model does not support summary, skipping...')
          loss_str = ', '.join([
              '{}={:.5f}'.format(k,
                                 sum(v) / (len(v) + 1e-16))
              for k, v in real_model._loss_dict.items()
          ])
          # Clear the loss dict
          real_model._loss_dict = {}

          now = datetime.datetime.now()
          elapsed = now - loop_conf['StartTime']
          elapsed_h = int(elapsed.total_seconds()) // 3600
          elapsed_min = (int(elapsed.total_seconds()) - elapsed_h * 3600) // 60
          elapsed_sec = int(
              elapsed.total_seconds()) - elapsed_h * 3600 - elapsed_min * 60

          eta = (now - last_time) / loop_conf['LogStep'] * (
              loop_conf['MaxIter'] - cur_iter)
          eta_h = int(eta.total_seconds()) // 3600
          eta_min = (int(eta.total_seconds()) - eta_h * 3600) // 60
          last_time = now

          log_str = ('({:d}/{:d}) {:s} now, {:02d}h:{:02d}m:{:02d}s gone, ' +
                     '{:d}h:{:d}m to go, {:s}').format(
                         cur_iter, loop_conf['MaxIter'],
                         datetime.datetime.now().strftime(r'%m-%d %H:%M'),
                         elapsed_h, elapsed_min, elapsed_sec, eta_h, eta_min,
                         loss_str)
          logger.info(log_str)

        if IS_MAIN_PROCESS and cur_iter % loop_conf['CheckpointStep'] == 0:
          os.makedirs(os.path.join(loop_conf['Path'], 'checkpoints'),
                      exist_ok=True)
          with open(os.path.join(loop_conf['Path'], 'last_ckpt.txt'),
                    'w+') as f:
            print('ckpt_{:06d}.pth'.format(cur_iter), file=f)
          torch.save(
              {
                  'model_type': cfg['Model']['Type'],
                  'model': real_model.make_state_dict(),
                  'optim': optim.state_dict(),
                  'scheduler': scheduler.state_dict(),
                  'iter': cur_iter
              },
              os.path.join(loop_conf['Path'], 'checkpoints',
                           'ckpt_{:06d}.pth'.format(cur_iter)))

        if IS_MAIN_PROCESS and cur_iter % loop_conf['ValStep'] == 0:
          logger.info('Start evaluating...')
          torch.cuda.empty_cache()
          if hasattr(real_model, 'evaluate'):
            try:
              with torch.no_grad():
                if cfg['Train'].get('AMP', False):
                  with torch.cuda.amp.autocast():
                    real_model.evaluate(val_loader,
                                        cur_iter,
                                        logger=logger,
                                        writer=writer)
                else:
                  real_model.evaluate(val_loader,
                                      cur_iter,
                                      logger=logger,
                                      writer=writer)
            except NotImplementedError:
              logger.error('Model dose not support evaluating, skipping...')
          else:
            logger.warning('Model does not support evaluating!')

      if cur_iter > loop_conf['MaxIter']:
        break

    logger.info('All done, logs and checkpoints are saved to {}'.format(
        loop_conf['Path']))


if __name__ == '__main__':
  _parser = argparse.ArgumentParser()
  _parser.add_argument('--config', help='config file path')
  _parser.add_argument('--save-dir',
                       default=None,
                       help='override save dir in config file')
  _parser.add_argument('--resume', default=None, help='resume training')
  args = _parser.parse_args()

  BasicTrainer.launch(args.config, args.resume, args.save_dir)
