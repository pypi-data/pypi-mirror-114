from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler

import torch.distributed as dist


def getDistLoaders(train_dataset,val_dataset,batch_size,num_workers,distributed=True, distributed_val=True):
    """
    
    Creates distributed dataloader:-
        For train_dataset: assigns distributed sampler,
        For val_dataset: assigns distributed sampler for distributed val step i.e. args.val_node=-1, else sampler=None

    Parameters
    ----------
    train_dataset : torch.utils.data.Dataset
        train_dataset
    val_dataset : torch.utils.data.Dataset
        val_dataset
    args : dict
        args.train
            args.train['batch_size'] : int, 
            args.train['num_workers'] : int
        args.val
            args.val['batch_size'] : int, 
            args.val['num_workers'] : int
        args.distributed : boolean
            distributed
        args.val_node : int
            val_node
    ----------
    
    """

    train_sampler,val_sampler = None,None

    if distributed:
        rank, world_size = dist.get_rank(), dist.get_world_size()
        train_sampler = DistributedSampler(
            train_dataset,
            rank = rank,
            num_replicas = world_size
        )
        if distributed_val:
            val_sampler = DistributedSampler(
                val_dataset,
                rank = rank,
                num_replicas = world_size
            )
    # loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        sampler=train_sampler,
        pin_memory=False
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        sampler=val_sampler,
        pin_memory=False
    )
    return train_loader, val_loader