"""This module provides basic interface for a dataset.
"""
import torch


class _BaseDataset(torch.utils.data.Dataset):
  """Base dataset class to hold samples.
  """

  def __len__(self):
    raise NotImplementedError

  def __getitem__(self, index):
    raise NotImplementedError

  def get_loader(self,
                 batch_size=1,
                 shuffle=False,
                 num_workers=0,
                 sampler=None,
                 drop_last=True,
                 pin_memory=True,
                 **kwargs):
    """Constructs a dataloader from this dataset and returns it.
    """
    return torch.utils.data.DataLoader(self,
                                       batch_size=batch_size,
                                       shuffle=shuffle,
                                       num_workers=num_workers,
                                       pin_memory=pin_memory,
                                       sampler=sampler,
                                       drop_last=drop_last,
                                       **kwargs)
