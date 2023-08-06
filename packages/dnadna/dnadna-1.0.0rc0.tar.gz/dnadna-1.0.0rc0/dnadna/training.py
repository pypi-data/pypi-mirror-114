# -*- coding: utf-8 -*-
"""Implements model training on simulation data using neural nets."""

import copy
import inspect
import logging
import math
import os
import os.path as pth
import re
import shutil
import signal
import sys
import time
import warnings
from functools import partial

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import tqdm
from torch.utils.data import DataLoader, sampler

from . import __version__, DNADNAWarning
from .datasets import DNATrainingDataset
from .nets import Network
from .optim import Optimizer
from .params import LearnedParams
from .utils.config import ConfigMixIn, Config
from .utils.jsonschema import timestamp
from .utils.misc import (format_to_re, indent, reformat_format,
                         stdio_redirect_tqdm, parse_format, AverageMeter)
from .utils.tensor import nanmean
from .utils.plugins import load_plugins

# Ignore annoying log messages to the root logger from from caffe2
# What's worse, caffe2 installs a default handler on the root logger
# which overrides our calls to logging.basicConfig in our scripts.
# Libraries should not do this!
# First check if logging was already configured elsewhere.
logging_configured = len(logging.root.handlers) > 0

logging.getLogger().addFilter(
        lambda rec: not rec.pathname.endswith(pth.join('caffe2', 'python',
        '_import_c_extension.py')))


# tensorboard invokes some DeprecationWarnings from Numpy>=1.20.0
# Easiest is to just squelch them globally for this module.
warnings.filterwarnings(
    'ignore', '.*is a deprecated alias for the builtin.*',
    DeprecationWarning, 'tensorboard.*')
from torch.utils.tensorboard import SummaryWriter  # noqa: E402

# If logging wasn't previously configured but it is now, that means caffe2
# did it; undo that.
if not logging_configured and len(logging.root.handlers) == 1:
    for h in logging.root.handlers:
        logging.root.removeHandler(h)
    del h


log = logging.getLogger(__name__)


TRAINING_RUN_CONFIG_FILENAME_FORMAT = \
        '{model_name}_{run_name}_final_config.yml'
TRAINING_RUN_SCENARIO_PARAMS_FILENAME_FORMAT = \
        '{model_name}_{run_name}_preprocessed_params.csv'


class DummySummaryWriter:
    """
    Replaces `torch.utils.tensorboard.writer.SummaryWriter` when error logging
    is disabled.
    """

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, attr):
        # Return dummy callables for all attributes
        return lambda *args, **kwargs: None


class prepared_property(property):
    """
    Helper descriptor for attributes which are not set until
    `ModelTrainer.prepare()` is called.
    """

    def __get__(self, obj, cls=None):
        if cls is None:
            return super().__get__(obj, cls)

        name = self.fget.__name__
        sentinel = object()
        val = getattr(obj, '_' + name, sentinel)
        if val is sentinel:
            val = super().__get__(obj, cls)
            if val is not None:
                setattr(obj, '_' + name, val)
                return val

            raise AttributeError(name,
                f'{self.__class__.__name__}.prepare() must be called to '
                f'initialize {name}')

        return val


class ModelTrainer(ConfigMixIn):
    config_schema = 'training'

    def __init__(self, config, validate=True, progress_bar=False):
        plugins = config.get('plugins', [])
        load_plugins(plugins)

        super().__init__(config=config, validate=validate)

        self._progress_bar = progress_bar and sys.stdout.isatty()
        self._run_dir_ensured = False
        self._prepared = False
        self._worker_init_fn = None

        # A little sanity check that (currently) isn't easily enforced by the
        # schema
        if 'checkpoint' not in parse_format(self.model_filename_format):
            raise ValueError(
                "the 'model_filename_format' must contain the '{checkpoint}' "
                "variable in the format template; for example: "
                "{model_name}_{run_name}_{checkpoint}.pth")

    @classmethod
    def from_config_file(cls, filename, progress_bar=False, **kwargs):
        """Instantiate from a config file."""

        config = Config.from_file(filename, validate=False, **kwargs)
        return cls(config=config, validate=True, progress_bar=progress_bar)

    @prepared_property
    def net(self):
        """
        Returns the `torch.nn.Module` instance for the neural net to be
        trained.
        """

    @prepared_property
    def full_net_params(self):
        """
        Returns the arguments that the `ModelTrainer.net` instance was
        instantiated with as a `dict`.
        """

    @prepared_property
    def optimizer(self):
        """
        Returns the `torch.optim.Optimizer` subclass (see also
        `dnadna.optim.Optimizer`) that provides the optimization step algorithm
        for training the model.
        """

    @prepared_property
    def device(self):
        """The device for PyTorch to use (CPU or a CUDA device)."""

    @prepared_property
    def loss_funcs(self):
        """Loss functions to use for each trained parameter."""

        return self._learned_params.loss_funcs

    @prepared_property
    def loss_weights(self):
        """Weights to apply to the loss functions of each trained parameter."""

        return self._learned_params.loss_weights

    @prepared_property
    def n_outputs(self):
        """
        Number of outputs from the neural net model--this is related to the
        number of parameters.

        Specifically, it is the number of regression parameters, plus the
        number of classes in each classification parameter.
        """

        return self._learned_params.n_outputs

    @prepared_property
    def training_loader(self):
        """`torch.utils.data.DataLoader` for the training data set."""

    @prepared_property
    def validation_loader(self):
        """`torch.utils.data.DataLoader` for the validation data set."""

    @prepared_property
    def dataset(self):
        """Returns a `.DNATrainingDataset` instance."""

    @prepared_property
    def learned_params(self):
        """Returns a `~dnadna.params.LearnedParams` instance from the config."""

    @prepared_property
    def run_id(self):
        """The number or string identifying this training run."""

    @prepared_property
    def run_dir(self):
        """The directory where training run artifacts will be output."""

    @prepared_property
    def run_name(self):
        """The full name of the training run.  Typically ``run_{run_id}``."""

    @prepared_property
    def error_log(self):
        """
        `torch.utils.tensorboard.writer.SummaryWriter` for streaming error
        statistics and other statistics.

        Name might change in the future as it can be used for logging more than
        just errors.
        """

    @prepared_property
    def save_checkpoints(self):
        """Whether or not model checkpoints are being saved."""

    @prepared_property
    def param_names(self):
        """List of the names of trained parameters."""

        return self._learned_params.param_names

    def prepare(self, dataset=None, preprocessed_scenario_params=None,
                run_id=None, overwrite=False, error_log=False, save_best=False,
                save_checkpoints=False):
        """
        Perform initial preparation for model training based on the provided
        `.Config`.

        Parameters
        ----------
        dataset : `.DNATrainingDataset`, optional
            A `.DNATrainingDataset` instance, or if omitted the dataset
            specified by the config.

        preprocessed_scenario_params : `pandas.DataFrame`, optional
            Pandas `~pandas.DataFrame` containing the preprocessed scenario
            parameters returned by
            `.DataPreprocessor.preprocess_scenario_params`.  If omitted, the
            parameters are read from the dataset.

        run_id : int or str, optional
            Unique ID to identify this training run.  If not specified, it
            will be generated automatically from the sequence of existing
            runs in the ``model_root`` directory.

        overwrite : `bool`, optional
            If the output directory for this run already exists and
            ``overwrite=True`` any existing run artifacts will be overwritten,
            otherwise an error is raised.

        error_log : `bool`, optional
            Enable error logging for the training run.  Disabled by default
            except when running `ModelTrainer.run_training`.

        save_best : `bool`, optional
            Enable saving the version of the model with the best losses during
            the training run, overriding this copy of the model each time the
            loss improves over the previous best loss.  Disabled by default
            except when running `ModelTrainer.run_training`.

        save_checkpoints : `bool`, optional
            Enable saving checkpoints of the model during the training run.
            Disabled by default except when running
            `ModelTrainer.run_training`.
        """

        # TODO: This is currently copied right out of the old main() function,
        # and should probably be further refactored into some sub-routines

        # Used for Ctrl-C and other signal interruption
        self._poison_pill = False

        seed = self.config.get('seed')
        if seed is not None:
            # Seed both the Numpy and PyTorch PRNGs for reproducible results
            np.random.seed(seed)
            torch.manual_seed(seed)

        if preprocessed_scenario_params is None:
            preprocessed_scenario_params = \
                    pd.read_csv(self.dataset['scenario_params_path'],
                                sep=None, engine='python',
                                index_col='scenario_idx')

        # Set specified GPU
        device = self._device = torch.device(
                'cuda' if torch.cuda.is_available() and
                self.use_cuda else 'cpu')
        if device.type == 'cuda' and self.cuda_device is not None:
            torch.cuda.set_device(self.cuda_device)

        self._learned_params = LearnedParams(
                self.config['learned_params'], preprocessed_scenario_params,
                validate=False)
        self._learned_params.to(device)

        if dataset is None:
            log.info('Initializing dataset...')
            # Always set ignore_missing=True for training; see
            # https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/65
            config = copy.deepcopy(self.config)
            config['dataset']['ignore_missing'] = True
            # validate=False since the full configuration has already been
            # validated by this point
            dataset = DNATrainingDataset(config,
                                         learned_params=self._learned_params,
                                         validate=False)

        self._dataset = dataset

        # Load the dataset
        training_loader, validation_loader = self.init_data_loaders()

        self._training_loader = training_loader
        self._validation_loader = validation_loader

        self._net, self._full_net_params = self._prepare_net()
        self._optimizer = Optimizer.from_config(self.config['optimizer'],
                                                self._net.parameters(),
                                                validate=False)

        self._run_id, self._run_name, self._run_dir = \
                self.get_run_info(run_id=run_id)

        self.config['run_id'] = self._run_id
        self.config['run_name'] = self._run_name
        self.config['training_datetime'] = timestamp()

        # If we are writing the error log or saving checkpoints we have to
        # make sure the run output directory exists, otherwise we can run
        # ModelTrainer.train() without actually writing anything to disk
        if error_log or save_best or save_checkpoints:
            self.ensure_run_dir(run_id=self._run_id, overwrite=overwrite)

        # Instantiate the Error Log
        if error_log:
            summary_path = pth.join(self.run_dir, 'tensorboard')
            self._error_log = SummaryWriter(summary_path)
        else:
            self._error_log = DummySummaryWriter()

        self._save_best = save_best
        self._save_checkpoints = save_checkpoints

        self._prepared = True

    def _prepare_net(self):
        """
        Subroutine for instantiating the network model with its appropriate
        parameters.
        """

        net_cls = Network.get_plugin(self.network['name'])
        # make a copy to modify below...
        net_params = dict(self.network.get('params', {}))

        # Although some of the network parameters processed above are common to
        # many nets, not all nets support all of these parameters, so reduce
        # now to only those supported by the current net.
        sig = inspect.signature(net_cls)
        expected_params = set(sig.parameters.keys())

        # TODO: This may not actually be reliable, as different data sets can
        # have samples with different numbers of individual samples, or
        # different numbers of SNPs per sample (especially this), so looking at
        # one example datum does not necessarily make sense.  Instead, during
        # pre-processing, it might make sense to determine the minimal number
        # of each (after excluding samples that don't meet a minimum threshold)
        # and record that in the inference parameters for the run.
        example_datum = None

        def get_example_datum():
            nonlocal example_datum
            if example_datum is None:
                example_datum = self._training_loader.dataset[0][2]

            return example_datum

        # TODO: As of now there are a set number of specific net parameters
        # that we have hard-coded support for processing; if the need for
        # supporting additional, user-provided custom nets is added we may
        # wish to expand this (e.g. net classes could have a custom method
        # for initializing themselves based on the full config)
        if 'n_snp' in expected_params and 'n_snp' not in net_params:
            net_params['n_snp'] = get_example_datum().n_snp

        if 'n_indiv' in expected_params and 'n_indiv' not in net_params:
            net_params['n_indiv'] = get_example_datum().n_indiv

        if 'concat' in expected_params and 'concat' not in net_params:
            net_params['concat'] = \
                    get_example_datum().tensor_format == 'concat'

        net_params['n_outputs'] = self._learned_params.n_outputs

        net = net_cls(**net_params)
        try:
            # calling .to() on a trivial module with no child modules breaks,
            # so we test that to be sure; this could be considered a minor bug
            # in pytorch since net.children() should just be empty in this
            # case instead of raising an AttributeError
            next(net.children())
        except AttributeError:
            pass
        else:
            net = net.to(self.device)

        # Dispatch mini-batch on multiple GPUs
        if self.device.type == 'cuda':
            net = nn.DataParallel(net,
                    device_ids=range(torch.cuda.device_count()))

        return net, net_params

    def init_data_loaders(self):
        """
        Returns a training data `~torch.utils.data.DataLoader` and a validation
        `~torch.utils.data.DataLoader` for data from a single model dataset.
        """

        dataset = self.dataset

        log.info(f'{len(dataset.validation_set)} samples in the '
                 f'validation set and {len(dataset.training_set)} in the '
                 f'training set')

        def init_sampler(dataset_slice):
            # NOTE: Sort these sets to ensure better reproducibility, as set
            # order is not otherwise guaranteed deterministic.
            return sampler.SubsetRandomSampler(sorted(dataset_slice))

        def init_data_loader(sampler, num_workers):
            return DataLoader(dataset=dataset,
                              batch_size=self.batch_size,
                              sampler=sampler,
                              num_workers=num_workers,
                              worker_init_fn=self._worker_init_fn,
                              pin_memory=self.use_cuda,
                              collate_fn=DNATrainingDataset.collate_batch)

        training_sampler = init_sampler(dataset.training_set)
        validation_sampler = init_sampler(dataset.validation_set)
        # Make the number of validation workers proportional to the ratio of
        # the validation set to the training set, since validation loaders need
        # to be iterated over more frequently; see
        # https://gitlab.inria.fr/ml_genetics/private/dnadna/-/merge_requests/64#note_493102
        if dataset.training_set:
            # The training set should never be empty, but this at least
            # prevents a ZeroDivisionError here should that be the case (having
            # no training data whatsoever should result in an error elsewhere)
            validation_num_workers = int(len(dataset.validation_set) /
                                         len(dataset.training_set) *
                                         self.loader_num_workers)
        else:
            validation_num_workers = self.loader_num_workers

        self.running_training_loss = AverageMeter('training loss', '.4e')
        self.running_validate_loss = AverageMeter('validation loss', '.4e')

        return (init_data_loader(training_sampler, self.loader_num_workers),
                init_data_loader(validation_sampler, validation_num_workers))

    def train(self):
        if not self._prepared:
            raise RuntimeError(
                f'{self.__class__.__name__}.prepare() must be called before '
                f'{self.__class__.__name__}.train()')

        self.net.train()  # important for BatchNorm (or dropout)

        # N batches per epoch
        training_scenarios = self.training_loader.dataset.training_set
        n_batches = int(math.ceil(len(training_scenarios) /
                                  self.training_loader.batch_size))
        # N batches over all epochx
        n_batches_total = n_batches * self.n_epochs

        with stdio_redirect_tqdm() as orig_stdio:
            with tqdm.tqdm(total=n_batches_total, unit='batch', position=1,
                           file=orig_stdio.stdout, dynamic_ncols=True,
                           disable=(not self._progress_bar)) as bar:
                best_loss = self._train_outer_loop(bar)

                # Bug in tqdm? Have to write one blank line before closing the
                # progress bar, or else subsequent terminal output will overlap
                # it
                if not bar.disable:
                    orig_stdio.stdout.write('\n')

                self._prepared = False

                return best_loss

    def run_training(self, run_id=None, overwrite=False):
        """
        High-level interface to prepare and execute a training run, and save
        the resulting net to a file.

        This is the method run by the command-line interface.
        """

        self._install_signal_handlers()

        log.info(f'Process ID: {os.getpid()}')
        log.info('Preparing training run')

        self.prepare(run_id=run_id, overwrite=overwrite, error_log=True,
                     save_best=True, save_checkpoints=True)

        # copy the preprocessed scenario params into the run directory and
        # update its path in the training config
        # TODO: The fact that we have to do this at all feels a bit sloppy
        # somehow, but it is required for compatibility with the old run_NNN/
        # directory format.  TBD if we still really need this.
        scenario_params_filename = \
                TRAINING_RUN_SCENARIO_PARAMS_FILENAME_FORMAT.format(
                        model_name=self.model_name, run_name=self.run_name)
        scenario_params_path = pth.join(self.run_dir, scenario_params_filename)
        shutil.copy(self.config['dataset']['scenario_params_path'],
                    scenario_params_path)
        self.config['dataset']['scenario_params_path'] = scenario_params_path

        # write the training run config
        config_filename = TRAINING_RUN_CONFIG_FILENAME_FORMAT.format(
                model_name=self.model_name, run_name=self.run_name)
        config_path = pth.join(self.run_dir, config_filename)
        self.config.to_file(config_path, indent=2, sort_keys=False)

        log.info('Start training')
        log.info("Networks states are saved after each validation step")
        log.warning("Current behavior if SNP matrices have different shapes: "
                 "padding with -1 (right and bottom) to fit the maximum dimension "
                 "within each batch.")
        start_time = time.time()
        best_loss = self.train()
        time_spent = time.time() - start_time

        log.info(f'--- {time_spent} seconds ---')
        log.info(f'--- Best loss: {best_loss}')

        if self._poison_pill:
            log.warning('Training interrupted')
            return

        last_epoch_filename = self._model_filename('last_epoch')
        self.save_net(last_epoch_filename)

        log.info("You can test the model's predictions on a test dataset by "
                 "running the command:")
        log.info('')
        log.info(indent(f'dnadna predict {last_epoch_filename} '
                        f'<dataset config file or paths to .npz files>'))

    def _model_filename(self, checkpoint):
        """
        Determines an appropriate model filename from the template in the
        config file, for the given 'checkpoint'.
        """

        filename = self.model_filename_format.format(
            model_name=self.model_name,
            run_name=self.run_name,
            run_id=self.run_id,
            checkpoint=checkpoint
        )

        return pth.join(self.run_dir, filename)

    def save_net(self, filename, quiet=False, **kwargs):
        """
        Save the current network state dict to a pickle file.

        Additional ``**kwargs`` are included in the pickled dict alongside the
        network state dict.
        """

        if not quiet:
            log.info(f'Saving model to "{pth.normpath(filename)}" ...')
        # If the net is wrapped in DataParallel, save just the underlying
        # module, not the DataParallel; otherwise the saved net can only be
        # loaded-again by wrapping it in DataParallel
        if isinstance(self.net, nn.DataParallel):
            state_dict = self.net.module.state_dict()
        else:
            state_dict = self.net.state_dict()

        kwargs.update({
            'network': {
                'name': self.network['name'],
                'params': self.full_net_params
            },
            'preprocessing': self.config['preprocessing'],
            'learned_params': self.config['learned_params'],
            'dataset_transforms': self.config['dataset_transforms'],
            'train_mean': self.config['train_mean'],
            'train_std': self.config['train_std'],
            'model_datetime': timestamp(),
            'dnadna_version': __version__,
            'state_dict': state_dict,
        })
        torch.save(kwargs, filename)

    def _train_outer_loop(self, progress_bar):
        """
        Loop over epochs
        """
        training_step = 0
        best_loss = None

        def update_best_loss():
            nonlocal best_loss

            if best_loss is None or val_loss < best_loss:
                log.info(
                    f'Better loss found on validation set: '
                    f'{best_loss} --> {val_loss}')
                best_loss = val_loss
                if self._save_best:
                    self.save_net(self._model_filename('best'), batch=batch,
                                  step=training_step)

        # TODO: Support saving intermediate nets at the end of each epoch to
        # support resumption
        for epoch in range(self.n_epochs):
            log.info(f'Starting Epoch #{epoch + 1}')
            progress_bar.set_description(f'epoch {epoch + 1}/{self.n_epochs}')

            self.running_training_loss.reset()
            for batch, data in enumerate(self.training_loader):
                scenario_idx, inputs, targets = data

                train_loss, val_loss = self._train_inner_loop(
                        epoch, batch, training_step, scenario_idx, inputs,
                        targets)

                if val_loss is not None:
                    update_best_loss()

                training_step += inputs.shape[0]
                progress_bar.update()

                if self._poison_pill:
                    # Break out of the loop early if interrupted
                    break

            if self._poison_pill:
                break

        # run validation with last net.
        # TODO: Is this really necessary?  We could also put such a condition
        # above in the conditional over run_validation?
        if not self._poison_pill:
            val_losses, errors, errors_grouped = self.validate()
            val_loss = val_losses.mean().numpy()
            if best_loss is None or val_loss < best_loss:
                update_best_loss()

        return best_loss.item()

    def _train_inner_loop(self, epoch, batch, step, scenario_idx,
                          inputs, targets):
        # NOTE: Here targets_train contains all the training parameters in
        # the order of their columns in the scenario parameters table (this
        # could be hard to keep track of so we should have a clearer
        # mapping of parameter indices
        # The first dimension in each array is the batch axis
        log.debug(f"step {step}")
        inputs = inputs.to(self.device)
        targets = targets.to(self.device)
        log.debug("got dataset")

        # Clear the gradients of all optimized tensors
        self.optimizer.zero_grad()

        log.debug("predict on training")

        outputs = self.net(inputs)

        train_losses, errors = self._compute_loss_metrics(outputs, targets)

        self.running_training_loss.update(train_losses.detach().mean().numpy())

        if ((batch % self.evaluation_interval == 0 and batch != 0) or
                (batch == 0 and epoch == 0)):
            log.info(f'Validation at epoch: {epoch + 1} and batch: '
                     f'{batch + 1}')
            # Saving Training datas
            self.error_log.add_scalar('loss/training',
                                      self.running_training_loss.avg, step)

            # Validation
            val_losses, errors, errors_grouped = self.validate()
            self.error_log.add_scalar('loss/validation',
                                      val_losses.detach().mean().numpy(), step)
            log.info(
                f'training loss = {self.running_training_loss.avg} // '
                f'validation loss = {val_losses.detach().mean().numpy()}')

            # Save network
            if self.save_checkpoints:
                self.save_net(self._model_filename('last_checkpoint'),
                              quiet=True, batch=batch, step=step)

            # was switched to net.eval() in validation.
            # TODO: Is there a context manager for managing the
            # networks's evaluation mode? If not, we should add one,
            # and make this transparent.
            self.net.train()

            return (train_losses.detach().mean().numpy(),
                    val_losses.detach().mean().numpy())

        # no val_losses if not a validation step
        return train_losses.detach().mean().numpy(), None

    def validate(self):
        self.net.eval()  # important for BatchNorm (or dropout)

        # TODO: These should probably just be pre-allocated using information from
        # the validation_loader on the number of scenarios it holds.
        all_targets = torch.Tensor()
        all_outputs = torch.Tensor()
        all_scen_idxs = torch.Tensor().long()

        log.info("Compute all outputs for validation dataset... ")

        validation_set = self.validation_loader.dataset.validation_set
        n_batches = int(math.ceil(len(validation_set) /
                                  self.validation_loader.batch_size))

        with stdio_redirect_tqdm() as orig_stdio:
            # Use leave=False, or else subsequent output tends to overlap the
            # second progress bar; not sure if this is a bug in tqdm or
            # something I'm doing wrong, but given the overall flakiness of
            # tqdm's display management with multiple bars I suspect it's a bug
            # In any case there doesn't seem to be much advantage to leaving
            # up the validation progress bars once they've completed.
            bar = tqdm.tqdm(self.validation_loader, total=n_batches,
                            unit='batch', desc='validation', position=0,
                            file=orig_stdio.stdout, dynamic_ncols=True,
                            leave=False, disable=(not self._progress_bar))
            with bar, torch.no_grad():
                # Compute all outputs for validation dataset
                for scen_idx, inputs, targets in bar:
                    # Try to get all IDs workin to match all outputs.
                    scen_idxs, outputs, targets = self._validate_inner_loop(
                            scen_idx, inputs, targets)

                    all_scen_idxs = torch.cat((all_scen_idxs, scen_idxs), 0)
                    all_outputs = torch.cat((all_outputs, outputs), 0)
                    all_targets = torch.cat((all_targets, targets), 0)

                    if self._poison_pill:
                        # Break out of the loop early if interrupted
                        break

        if self._poison_pill:
            log.warning('Interrupted')
        else:
            log.info('Done')

        # error on entire validation dataset
        losses, errors, errors_grouped = self._compute_loss_metrics(
                all_outputs, all_targets, scenario_idxs=all_scen_idxs,
                validation=True)

        return losses, errors, errors_grouped

    def _validate_inner_loop(self, scenario_idx, inputs, targets):
        inputs = inputs.to(self.device)
        targets = targets.to(self.device)
        outputs = self.net(inputs)
        # logging.debug(f"{targets_val.shape}, {outputs.shape}, {scen_idx.shape}")
        if len(scenario_idx) > 1:
            scenario_idx = scenario_idx.squeeze()

        return scenario_idx.cpu(), outputs.cpu(), targets.cpu()

    def _compute_loss_metrics(self, outputs, targets, scenario_idxs=None,
                              validation=False):
        """Given output and target, compute losses and other error metrics."""

        # TODO: For now I have ommitted a number of .to(device) calls as I would
        # like to factor that out of this function entirely; it should operate on
        # existing tensors that already are on the device on which we'd like to
        # compute with them.  I want to have a clearer data flow path by the time
        # all the dust has settled.
        losses = torch.empty(targets.shape[1])  # N parameters
        errors = torch.empty(targets.shape)

        for param_name in self.param_names:
            param = self.learned_params.params[param_name]
            target_slice, output_slice = \
                    self.learned_params.param_slices[param_name]
            target = targets[:, target_slice]
            output = outputs[:, output_slice]

            if param['type'] == 'regression':
                # Compute error metrics
                squared_err = (output - target)**2
                errors[:, target_slice] = squared_err

                # For all regression params, omit samples where the target
                # value was NaN
                mask = torch.isnan(target)
                target = target[~mask]
                output = output[~mask]
            else:
                # If this is a classification param the targets should be a 1-D
                # tensor of the target class indices, so they must be converted
                # to longs
                # The shape is going to be batch_size x 1 so we also need to
                # reduce this to a 1-D array of length batch_size, that is,
                # the target class for each scenario in this batch
                target = target.long().squeeze(1)

                # Compute error metrics
                # position of class with highest prediction
                _, pred = torch.max(output, 1)
                comparison = pred == target
                errors[:, target_slice] = 1 - comparison.float().mean()

            loss_func = self.loss_funcs[param_name]
            loss = loss_func(output, target)
            losses[target_slice] = self.loss_weights[param_name] * loss

        loss_total = losses.sum()

        if not validation:
            # TODO: Need to separate concerns here a bit better.  The idea here is
            # that this same loss function can be used in both training and
            # validation.  I think this could be done more cleanly.
            log.debug(f"{type(loss_total.to(self.device))}, {self.device}")
            loss_total.backward()
            self.optimizer.step()

        # Compute metrics
        errors_mean = nanmean(errors, 0)

        if not validation:
            return losses, errors_mean

        # Use pandas to group errors by their scenaros, and return per-scenario
        # errors for each parameter
        # TODO: I'm not 100% clear on how useful this is as it drops information
        # such as the scenario indices themselves (do we care?).  Need to get more
        # clarification on what information needs to be logged about validation.
        index = pd.Index(scenario_idxs.numpy(), name='scenario_idx')
        errors_grouped = pd.DataFrame(errors.cpu().numpy(),
                                      columns=self.param_names,
                                      index=index)
        errors_grouped = errors_grouped.groupby('scenario_idx').mean()

        # Make the first axis the parameter axis
        errors_grouped = errors_grouped.values.T

        return losses, errors_mean, errors_grouped

    def get_run_info(self, run_id=None):
        """
        Return the run_id (if not specified) and the model_root-relative path
        to the run output directory.
        """

        if run_id is not None:
            run_name = self._format_run_name(run_id, self.model_name)
        else:
            run_id, run_name = self._next_run_dir()

        run_dir = pth.join(self.model_root, run_name)

        return run_id, run_name, run_dir

    def _format_run_name(self, run_id, model_name, fmt=None):
        """
        Use the config's run_name_format property to format the run name.

        By default integer ids are zero-padded out to a minimum of 3
        characters, unless a different format is specified in the
        configuration.
        """

        if fmt is None:
            fmt = self.run_name_format

        if isinstance(run_id, int):
            fmt = reformat_format(fmt, format_replacements={'run_id': '03'})

        return fmt.format(run_id=run_id, model_name=model_name)

    def _next_run_dir(self):
        """
        Determine the next unused run ID and output directory name.

        This iterates over all existing run directories in the run base
        directory, and takes the highest unused run ID.

        If the directory with highest run ID already exists but is empty we can
        reuse it.  Otherwise, non-empty directories are assumed to contain data
        of value and are not re-used.
        """

        run_name_re = re.compile(format_to_re(self.run_name_format,
                run_id=r'(\d+)', model_name=self.model_name))

        highest_id = 0

        for run_dir in os.listdir(self.model_root):
            run_dir_full = pth.join(self.model_root, run_dir)
            if not pth.isdir(run_dir_full):
                continue

            m = run_name_re.match(run_dir)
            if not m:
                continue

            run_id = int(m.group(1))
            if highest_id is None or run_id > highest_id:
                highest_id = run_id

        run_dir = self._format_run_name(highest_id, self.model_name)

        run_dir_full = pth.join(self.model_root, run_dir)
        # If the directory already exists and is non-empty, we can't re-use it,
        # so we increment the run ID
        if pth.isdir(run_dir_full) and any(os.scandir(run_dir_full)):
            highest_id += 1
            run_dir = self._format_run_name(highest_id, self.model_name)

        return highest_id, run_dir

    def _install_signal_handlers(self):
        signal.signal(signal.SIGTERM,
                      partial(self._terminate, 'process termination'))
        signal.signal(signal.SIGALRM,
                      partial(self._terminate, 'alarm interrupt'))
        signal.signal(signal.SIGINT, self._interrupt)

        self._worker_init_fn = self._dataloader_worker_signal_handlers

    @staticmethod
    def _dataloader_worker_signal_handlers(*args):
        """
        Alternate for ``self._worker_init_fn`` when we install our own signal
        handlers.
        """

        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def _interrupt(self, *args):
        """
        Handle SIGINT specially, which pauses the training run and gives
        the option to resume until another SIGINT is received.
        """

        # Restore the normal python SIGINT handler
        signal.signal(signal.SIGINT, signal.default_int_handler)

        try:
            with stdio_redirect_tqdm() as orig_stdio:
                orig_stdio.stdout.write('\n')
                input('Training suspended: press Enter to resume or press '
                      'Ctrl-C again to abort')
        except KeyboardInterrupt:
            self._terminate('keyboard interrupt')
            return
        except EOFError:
            # If the user hits Ctrl-D for some reason, just treat it like they
            # hit Enter
            pass

        # Restore our interrupt handler
        signal.signal(signal.SIGINT, self._interrupt)

    def _terminate(self, reason, *args):
        """Handle process termination due to a signal."""

        self._poison_pill = True
        log.error(
            f'Training stopped due to {reason} and will attempt to shut '
            f'down gracefully')
        log.error(
            'This training run can be resumed from the last checkpoint with:')
        log.error('')
        log.error(f'    dnadna train --resume {self.config.filename}')

    def ensure_run_dir(self, run_id=None, overwrite=False):
        """
        Make sure the run directory for this training run exists.

        Creates the directory if it does not already exists.  If it does
        already exist and ``overwrite=False`` a `FileExistsError` is raised.
        """
        if self._run_dir_ensured:
            return

        _, _, run_dir = self.get_run_info(run_id)

        if pth.isdir(run_dir) and any(os.scandir(run_dir)):
            if overwrite:
                warnings.warn(
                    f'the specified run ID {self.run_id} already exists under '
                    f'{self.run_dir} and its contents will be overwritten',
                    DNADNAWarning)
            else:
                raise FileExistsError(
                    f'the specified run ID {self.run_id} already exists under '
                    f'{self.run_dir} and will not be overwritten unless the '
                    f'overwrite option is given')

        os.makedirs(run_dir, exist_ok=True)
        self._run_dir_ensured = True
