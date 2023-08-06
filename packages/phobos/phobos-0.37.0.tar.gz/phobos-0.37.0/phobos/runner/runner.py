from .scheduler import get_scheduler
from .optimizer import get_optimizer
from torch.autograd import Variable
from torch.utils.data.distributed import DistributedSampler
from phobos.loss import get_loss
from phobos.metrics.metrics import Metrics
from torch.utils.tensorboard import SummaryWriter

import torch
import logging
import os
import torch.distributed as dist
import tqdm
import math




class Runner():
    """Runner class.

    Parameters
    ----------
    model : torch.nn.Module
        model to train or validate.
    device : torch.device
        device to move tensors to.
    criterion : str / torch.nn.Module
        criterion to measure loss for model.
    train_loader : torch.utils.data.Dataloader
        dataloader to load training dataset.
    val_loader : torch.utils.data.Dataloader
        dataloader to load validation dataset.
    distributed : boolean
        flag to create runner in distributed mode
    val_node : int
        validation step node if args.distributed=True, -1 for distributed val step
    metrics : str / phobos.metrics.metrics.Metrics
        metrics string
    optimizer : str / torch.optim
        optimizer string / instance
    num_classes : int
        number of classes
    loss_args : dict
        dictionary of loss arguments
    scheduler : str / torch.optim.lr_scheduler
        scheduler string / instance
    optimizer_args : dict
        dictionary of optimizer arguments
    scheduler_args : dict
        dictionary of scheduler arguments
    polyaxon_exp : poyaxon.tracking.Run
        polyaxon experiment.

    Attributes
    ----------
    device : torch.device
        device to move tensors to.
    model : torch.nn.Module
        model to train or validate.
    criterion : phobos.loss
        criterion to measure loss for model.
    train_loader : torch.utils.data.Dataloader
        dataloader to load training dataset.
    val_loader : torch.utils.data.Dataloader
        dataloader to load validation dataset.
    optimizer : torch.optim
        optimizer instance
    scheduler : torch.optim.lr_scheduler
        scheduler instance
    distributed : boolean
        flag to create runner in distributed mode
    distributed_val : boolean
        DDP: distributed validation step if True, val_step on master node otherwise.
    train_metrics : phobos.metrics.metrics.Metrics
        training metrics instance
    val_metrics : phobos.metrics.metrics.Metrics
        validation metrics instance
    polyaxon_exp : poyaxon.tracking.Run
        polyaxon experiment.
    iteration : int
        current iteration
    """

    def __init__(self,
                 model,
                 device,
                 criterion,
                 train_loader,
                 val_loader,
                 metrics,
                 optimizer,
                 distributed=False,
                 max_iters:int = 0,
                 distributed_val=True,
                 mode = 'epoch',
                 val_frequency: int = -1,
                 tensorboard_logging:bool = True,
                 num_classes=None,
                 loss_args=None,
                 scheduler=None,
                 optimizer_args=None,
                 scheduler_args=None,
                 polyaxon_exp=None):
                 
        self.polyaxon_exp = polyaxon_exp
        self.model = model
        self.device = device

        self.train_loader = train_loader
        self.val_loader = val_loader

        self.mode = mode
        self.max_iters = max_iters

        assert mode == 'epoch' or mode == 'batch', 'Enter the correct mode epoch/batch'

        self.criterion = self.get_runner_criterion(criterion, loss_args)
        self.optimizer = self.get_runner_optimizer(optimizer, optimizer_args, model)        
        self.scheduler = self.get_runner_scheduler(scheduler, scheduler_args, self.optimizer)

        self.distributed = False
        if distributed:
            self.set_distributed_params(distributed_val=distributed_val)

        self.train_metrics, self.val_metrics = self.get_runner_metrics(metrics, num_classes)

        if self.distributed and distributed_val == False:
            assert type(self.val_loader.sampler) !=  DistributedSampler, "For single node val_step, val_loader should not have distributed sampler"
            self.val_metrics.distributed = False
        
        self.val_frequency = val_frequency
        self.tboard = None
        
        if tensorboard_logging:
            self.tensorboard_logging = True
            if polyaxon_exp:
                tensorboard_path = os.path.join(polyaxon_exp.get_artifacts_path(),'outputs/tensorboard')
            else:
                tensorboard_path = os.path.join(os.curdir,'outputs/tensorboard')
            if not os.path.exists(tensorboard_path):
                os.makedirs(tensorboard_path)
            self.tboard = SummaryWriter(log_dir=tensorboard_path)
            self.train_metrics.tboard = self.tboard
            self.val_metrics.tboard = self.tboard

    @staticmethod
    def distributed():
        """Initialize process group, default is nccl backend.

        """
        dist.init_process_group(backend='nccl')

    def set_distributed_params(self, distributed_val):
        """Set up distributed params: world size, rank, and distributed or not.

        """
        self.world_size = dist.get_world_size()
        self.rank = dist.get_rank()
        logging.info(f"{self.rank} / {self.world_size}")
        self.distributed = True
        self.distributed_val = distributed_val

    def get_runner_metrics(self, metrics, num_classes=None):
        if type(metrics) == list:
            train_metrics = Metrics(polyaxon_exp=self.polyaxon_exp,
                                    phase='train',
                                    metrics_strings=metrics,
                                    num_classes=num_classes,
                                    distributed=self.distributed
                                    )
            val_metrics   = Metrics(polyaxon_exp=self.polyaxon_exp,
                                    phase='val',
                                    metrics_strings=metrics,
                                    num_classes=num_classes,
                                    distributed=self.distributed
                                    )
            return train_metrics, val_metrics
        else:
            return metrics["train_metrics"], metrics["val_metrics"]           

    def get_runner_criterion(self, criterion, loss_args=None):
        if type(criterion) == str:
            return get_loss(loss_str=criterion, loss_args=loss_args)
        else:
            return criterion

    def get_runner_optimizer(self, optimizer, optimizer_args=None, model=None):
        if type(optimizer) == str:
            return get_optimizer(key=optimizer, args=optimizer_args, model=model)
        else:
            return optimizer

    def get_runner_scheduler(self, scheduler, scheduler_args=None, optimizer=None):
        if scheduler is not None and scheduler_args is not None:
            if type(scheduler) == str:
                return get_scheduler(key=scheduler, args=scheduler_args, optimizer=optimizer)
            else:
                return scheduler
        else:
            return None

    def tensorize_batch(self, input_tensor, label_tensor):
        """Tensorize batch of input images and labels,
            and move them to gpu.

        Parameters
        ----------
        input_tensor : numpy.ndarray
            batch of input images.
        label_tensor : numpy.ndarray
            batch of input labels.

        Returns
        -------
        (torch.Tensor,torch.Tensor)
            input and label tensors in gpu.

        """
        logging.debug("Enter tensorize_batch routine")
        input_tensor = Variable(input_tensor).float()
        label_tensor = Variable(label_tensor).long()

        input_tensor=input_tensor.to(device=self.device)
        label_tensor=label_tensor.to(device=self.device)

        logging.debug("Exit tensorize_batch routine")

        return input_tensor, label_tensor

    def train_forward_backward(self, input_tensor, label_tensor):
        """Performs forward propagation, loss evaluation
        and backward propagation while training model.

        Parameters
        ----------
        input_tensor : torch.Tensor
            tensorised batch of input images.
        label_tensor : torch.Tensor
            tensorised batch of input labels.

        Returns
        -------
        (torch.Tensor,torch.nn.Module)
        prediction_tensor : torch.Tensor
            output/prediction tensor from model.
        loss : torch.nn.Module
            forward propagation loss

        """
        # Zero the gradient
        logging.debug("Enter train_forward_backward routine")
        self.optimizer.zero_grad()

        # Get model predictions, calculate loss, backprop
        prediction_tensor = self.model(input_tensor)
        loss = self.criterion(prediction_tensor, label_tensor)
        loss.backward()
        self.optimizer.step()
        logging.debug("Exit train_forward_backward routine")

        return prediction_tensor, loss

    def eval_forward(self, input_tensor, label_tensor):
        """Performs forward propagation while evaluating model.

        Parameters
        ----------
        input_tensor : torch.Tensor
            tensorised batch of input images.
        label_tensor : torch.Tensor
            tensorised batch of input labels.

        Returns
        -------
        (torch.Tensor,torch.nn.Module)
        prediction_tensor : torch.Tensor
            output/prediction tensor from model.
        loss : torch.nn.Module
            forward propagation loss

        """
        # Get predictions and calculate loss
        logging.debug("Enter eval_forward routine")
        prediction_tensor = self.model(input_tensor)
        loss = self.criterion(prediction_tensor, label_tensor)
        logging.debug("Exit eval_forward routine")

        return prediction_tensor, loss

    def eval_model(self,step):
        """Evaluates model.

        Parameters
        ----------
        step : int
            training step.

        Returns
        -------
        dict
            dictionary of evaluation metrics.

        """
        self.model.eval()
        logging.debug("Enter eval_model routine")
        with torch.no_grad():
            for (input_tensor, label_tensor) in self.val_loader:
                input_tensor, label_tensor = self.tensorize_batch(input_tensor, label_tensor)

                prediction_tensor, loss = self.eval_forward(
                    input_tensor, label_tensor)

                self.val_metrics.compute(prediction_tensor, label_tensor, loss)

                # clear batch variables from memory
                del input_tensor, label_tensor


        metrics = self.val_metrics.crunch_it(step)

        if self.scheduler:
            self.scheduler.step(metrics['val_loss'])
        logging.debug("Exit eval_model routine")

        return metrics

    def getContextIterationValue(self,x):
        val = x//self.train_loader.batch_size
        if self.train_loader.drop_last:
            val += math.ceil(x/self.train_loader.batch_size - x//self.train_loader.batch_size)
        return val

    def logResults(self,step):
        val_metrics = None
        if self.distributed:
            if self.distributed_val or dist.get_rank() == 0:
                val_metrics = self.eval_model(step)
                self.val_metrics.reset()
                dist.barrier()
        else:
            val_metrics = self.eval_model(step)
            self.val_metrics.reset()
        return val_metrics
        
    def condRun(self,iteration,epoch):
        if self.mode == 'epoch' and epoch < self.max_iters:
            return True
        elif self.mode == 'batch' and iteration < self.max_iters:
            return True
        return False

    def trainer(self):
        """Trains model.

        Returns
        -------
        dict
            dictionary of training metrics.

        """
        logging.debug("Enter train_model generator")

        train_metrics, val_metrics = None,None
        iteration,epoch = 0,0

        while  self.condRun(iteration,epoch):
            epoch += 1
            for input_tensor, label_tensor in self.train_loader:
                iteration += 1
                # batch train
                self.model.train()

                input_tensor, label_tensor = self.tensorize_batch(
                    input_tensor, label_tensor)

                prediction_tensor, loss = self.train_forward_backward(
                    input_tensor, label_tensor)
                self.train_metrics.compute(prediction_tensor, label_tensor, loss)

                del input_tensor, label_tensor
                
                if self.mode == 'batch':
                    train_metrics = self.train_metrics.crunch_it(iteration)
                    self.train_metrics.reset()
                    if self.distributed:
                        dist.barrier()
                    #end batch train
                    logging.info(f"{iteration}/{self.max_iters} completed!")
                    if self.val_frequency != -1 and iteration % self.val_frequency == 0:
                        val_metrics = self.logResults(iteration)
                        yield iteration,train_metrics,val_metrics

                if self.mode == "batch" and not self.condRun(iteration,epoch):
                    break
                    
            if self.mode == 'epoch':
                train_metrics = self.train_metrics.crunch_it(epoch)
                self.train_metrics.reset()
                logging.info(f"{epoch}/{self.max_iters} completed!")
                if self.distributed:
                    dist.barrier()
                val_metrics = self.logResults(epoch)
                yield epoch, train_metrics, val_metrics
            elif self.mode == 'batch' and self.val_frequency == -1:
                val_metrics = self.logResults(iteration)
                yield epoch,train_metrics,val_metrics
                
        logging.debug("Exit train_model routine")