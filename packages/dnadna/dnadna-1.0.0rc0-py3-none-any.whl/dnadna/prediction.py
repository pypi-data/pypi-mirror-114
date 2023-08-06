"""Implements prediction on existing data using an already trained model."""


import csv
import logging
import os.path as pth
import sys
import warnings
from collections import namedtuple
from contextlib import nullcontext
from functools import lru_cache

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import tqdm
from torch.utils.data import DataLoader

from . import DNADNAWarning
from .data_preprocessing import DataPreprocessor
from .datasets import (NpzSNPSource, FileListSNPSource,
    DatasetTransformationMixIn)
from .nets import Network
from .params import ParamSet
from .utils.config import Config, ConfigMixIn
from .utils.misc import stdio_redirect_tqdm


log = logging.getLogger(__name__)


class DNAPredictionDataset(DatasetTransformationMixIn):
    """
    Dataset for use during prediction.

    This does not take a ``scenario_params`` table as an argument; it just
    loads all data from a data source.

    Parameters are the same as `~.DatasetTransformationMixIn`, though extra
    ``**kwargs`` that might only be relevant during training are ignored.
    """

    def __init__(self, config={}, validate=True, source=None, transforms=None,
                 param_set=None, preprocess=None):
        # NOTE: This __init__ is implemented mostly just for documentation
        # and introspection purposes; otherwise it inherits
        # DatasetTransformationMixIn.__init__ which is more general.
        super().__init__(config=config, validate=validate, source=source,
                         transforms=transforms, param_set=param_set)

        if preprocess:
            self.preprocess = True
            self.min_snp, self.min_indiv = preprocess
        else:
            self.preprocess = False
            self.min_snp = self.min_indiv = None

    @classmethod
    def collate_batch(cls, batch):
        """
        Like `DatasetTransformationMixIn.collate_batch` but also returns the
        replicate indices and sample paths (e.g. filenames) which are used
        in the prediction output.

        .. note::

            This is implemented as a `classmethod` which is necessary to be
            able to call the super-class's ``collate_batch``.
        """

        rep_idxs = [b[1] for b in batch]
        paths = [b[2].path for b in batch]
        out = super().collate_batch(batch)
        return (out[:1] +
                [torch.tensor(rep_idxs, dtype=torch.long), paths] +
                out[1:])

    def _iter_samples(self):
        idx = 0
        for _, sample in super()._iter_samples():
            # We ignore the index (first output) from super()._iter_samples()
            # since if we skip a sample (due to not passing pre-processing)
            # then that sample won't be used for that index
            if self.preprocess:
                scenario_idx, replicate_idx = sample
                snp = self.source[scenario_idx, replicate_idx]
                valid = DataPreprocessor.check_snp_sample(
                        scenario_idx, replicate_idx, snp,
                        min_snp=self.min_snp, min_indiv=self.min_indiv)
                if not valid:
                    continue

            yield idx, sample
            idx += 1


class Predictor(ConfigMixIn):
    config_schema = 'training-run'

    def __init__(self, config, net, validate=True):
        super().__init__(config, validate=validate)
        self.net = net
        # Place the network in evaluation mode
        self.net.eval()
        self.params = ParamSet(self.learned_params)

    @classmethod
    def from_config_file(cls, filename, checkpoint='best', validate=True,
                         **kwargs):
        config = Config.from_file(filename, schema=cls.config_schema,
                                  validate=validate, **kwargs)

        config_dir = pth.dirname(filename)
        # Determine the model filename from the config; this assumes
        # the config is valid against the schema (by default this is enforced
        # just above)
        model_filename = config['model_filename_format'].format(
                model_name=config['model_name'],
                run_name=config['run_name'],
                run_id=config['run_id'],
                checkpoint=checkpoint)

        model_path = pth.join(config_dir, model_filename)
        return cls.from_net_file(model_path)

    @classmethod
    def from_net_file(cls, filename):
        # TODO: If we load an old model that was trained with earlier version
        # of the code, and whose stored config is no longer compatible, we need
        # to decide what to do.  Either provide a migration path (possibly
        # onerous) or add the possibility to provide a different
        # configuration...

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model_bundle = torch.load(filename, map_location=device)
        state_dict = model_bundle.pop('state_dict')
        config = model_bundle
        net_config = config['network']
        net_name = net_config['name']
        net_params = net_config['params']
        net_cls = Network.get_plugin(net_name)
        net = net_cls(**net_params)
        net.load_state_dict(state_dict)
        return cls(config, net, validate=False)

    @lru_cache()
    def prediction_cls(self, *, extra_cols=()):
        """
        Returns a `~collections.namedtuple` representing predictions from this
        dataset.

        It includes fields for all the parameters (for classification
        parameters it includes fields for the softmax value of each class (in
        the form ``<param_name>_<class_name>``) as well as the predicted class
        in ``<param_name>``).

        The set of fields is prepended by any listed in ``extra_cols`` which
        can include supplementary information, such as the filename of the
        SNP on which the prediction is was computed.

        .. note::

            This function is cached with `functools.lru_cache`--in order for
            the caching to work properly it's necessary that ``extra_cols`` is
            always passed as a keyword argument (which is enforced by the fact
            that it is a keyword-only argument).

        Examples
        --------

        >>> from dnadna.prediction import Predictor
        >>> from dnadna.utils.config import Config
        >>> from dnadna.nets import CustomCNN

        First we create a (partial) training config listing some parameters:

        >>> config = Config({
        ...     'network': {
        ...         'name': 'CustomCNN',
        ...     },
        ...     'learned_params': {
        ...         'position': {'type': 'regression'},
        ...         'selection': {
        ...             'type': 'classification',
        ...             'classes': ['yes', 'no']
        ...         }
        ...     }
        ... })
        ...

        Initialize a fake instance of the net; this along with the config are
        the bare minimum needed to instantiate a `Predictor`:

        >>> net = CustomCNN(n_snp=500, n_indiv=100, n_outputs=3)
        >>> predictor = Predictor(config, net, validate=False)

        The ``Prediction`` class in this case will have fields for scenario
        index, replicate index, position, selection_yes, selection_no, and
        selection:

        >>> Prediction = predictor.prediction_cls(
        ...     extra_cols=('scenario_idx', 'replicate_idx'))
        ...
        >>> Prediction(1, 2, 0.123, 0.1, 0.9, 'no')
        Prediction(scenario_idx=1, replicate_idx=2, position=0.123,
                   selection_yes=0.1, selection_no=0.9, selection='no')
        """

        fields = list(extra_cols)
        for param_name in self.params.param_names:
            if param_name in self.params.classification_params:
                fields.extend([f'{param_name}_{cls}' for cls in
                               self.params.params[param_name]['classes']])

            fields.append(param_name)

        class Prediction(namedtuple('Prediction', fields)):
            def to_scalars(self):
                """
                Return a copy of ``self`` with all 0-D tensors converted to
                plain scalar values.
                """

                new_values = []
                for val in self:
                    if isinstance(val, torch.Tensor) and val.dim() == 0:
                        val = val.item()

                    new_values.append(val)

                return self.__class__(*new_values)

        return Prediction

    def predict_all(self, samples, extra_cols=()):
        predictions = [p for p in self.iter_predictions(samples,
            extra_cols=extra_cols)]
        columns = self.prediction_cls(extra_cols=extra_cols)._fields
        return pd.DataFrame(predictions, columns=columns)

    def iter_predictions(self, samples, extra_cols=()):
        for sample in samples:
            if isinstance(sample, torch.Tensor):
                sample = (sample,)

            if not len(sample) == len(extra_cols) + 1:
                raise ValueError(
                    f'for extra_cols={extra_cols!r} each sample must be '
                    f'a tuple consisting of the SNP matrix itself, plus '
                    f'one metadata value for each of the extra_cols')

            sample, sample_meta = sample[0], sample[1:]
            prediction = self.predict(sample, sample_meta, extra_cols)

            if prediction is not None:
                # None if the net failed to evaluate on the input
                yield prediction

    def predict(self, sample, sample_meta=(), extra_cols=()):
        """
        Evaluate the network on a single sample and predict its parameters.
        """

        if sample.dim() == 2:
            sample = sample.unsqueeze(0)

        with torch.no_grad():
            try:
                prediction = self.net(sample).squeeze(0)
            except Exception as exc:
                if sample_meta:
                    sample_id = sample_meta
                else:
                    sample_id = sample

                log.warning(
                    f'could not evaluate the network on sample {sample_id}: '
                    f'{type(exc).__name__}: {exc}')

                return None

        prediction_cls = self.prediction_cls(extra_cols=extra_cols)
        prediction_vals = []
        sm = torch.nn.Softmax(dim=0)

        try:
            mu = self.train_mean
            std = self.train_std
            is_std = True
        except AttributeError:  # if data not std ?
            is_std = False
            pass

        for param_name, param in self.params.params.items():
            param_vals = prediction[self.params.param_slices[param_name][1]]
            if param_name in self.params.classification_params:
                prediction_vals.extend(sm(param_vals))
                classes = param['classes']
                prediction_vals.append(classes[param_vals.argmax()])
            else:
                if is_std:
                    param_vals = param_vals * std[param_name] + mu[param_name]

                # Revert log-transform on the parameter, if any
                if param.get('log_transform', False):
                    param_vals = np.exp(param_vals)

                prediction_vals.extend(param_vals)
        return prediction_cls(*sample_meta, *prediction_vals)

    def run_prediction(self, dataset_config=None, filenames=None, output=None,
                       preprocess=False, loader_num_workers=0, gpus=None,
                       progress_bar=False):
        if gpus and not torch.cuda.is_available():
            warnings.warn(
                f'specified gpus={gpus} but CUDA is support is not available; '
                f'running CPU-only', DNADNAWarning)
            gpus = False

        if dataset_config is not None and filenames is not None:
            raise ValueError(
                    "either a dataset_config may be given, or a list of "
                    "filenames, but not both")
        elif dataset_config is not None:
            # load SNPs from the given dataset and include scenario_idx and
            # replicate_idx in the output
            # Currently only NpzSNPSource is supported
            source = NpzSNPSource.from_config_file(dataset_config)
            extra_cols = ('path', 'scenario_idx', 'replicate_idx')

            def iter_batch(batch):
                for item in zip(*batch):
                    s_idx, r_idx, path, snp_matrix, _ = item
                    yield (snp_matrix, path, s_idx, r_idx)
        elif filenames is not None:
            source = FileListSNPSource(filenames)

            # in this case it is not meaningful to include scenario_idx and
            # replicate_idx
            extra_cols = ('path',)

            def iter_batch(batch):
                for item in zip(*batch):
                    _, _, path, snp_matrix, _ = item
                    yield (snp_matrix, path)
        else:
            raise ValueError(
                "one of either dataset_config or filenames must be specified")

        def iter_dataloader(loader):
            try:
                for batch in loader:
                    for item in iter_batch(batch):
                        yield item
            except Exception as exc:
                log.warning(
                    f'error loading batch from the dataset; some of the '
                    f'data in the provided dataset may not conform to the '
                    f'requirements of the model--if so you can try re-running '
                    f'with the --preprocess argument to check the inputs, or '
                    f'run `dnadna preprocess` over the dataset first: '
                    f'{type(exc).__name__}: {exc}')

        if preprocess:
            # The DNAPredictionDataset is passed
            # preprocess=(min_snp, min_indiv) if we want to perform
            # pre-processing before loading each file
            preprocess = (self.preprocessing['min_snp'],
                          self.preprocessing['min_indiv'])
        else:
            preprocess = False

        dataset = DNAPredictionDataset(validate=False,
                                       source=source,
                                       transforms=self.dataset_transforms,
                                       param_set=self.params,
                                       preprocess=preprocess)
        loader = DataLoader(dataset=dataset, batch_size=1,
                            num_workers=loader_num_workers,
                            pin_memory=bool(gpus),
                            collate_fn=DNAPredictionDataset.collate_batch)
        if gpus:
            # Wrap the network in DataParallel
            if gpus is True:
                gpus = list(range(torch.cuda.device_count()))

            self.net = nn.DataParallel(self.net, device_ids=gpus)
            self.net.to(torch.device('cuda', gpus[0]))
            self.net.eval()

        predictions = self.iter_predictions(iter_dataloader(loader),
                                            extra_cols=extra_cols)

        progress_bar = progress_bar and sys.stdin.isatty()

        with stdio_redirect_tqdm() as orig_stdio:
            predictions = tqdm.tqdm(predictions, total=len(dataset),
                                    unit='snp',
                                    file=orig_stdio.stderr, dynamic_ncols=True,
                                    disable=(not progress_bar))
            # This is to fix an issue where the progress bar is displayed too
            # early and the empty progress bar remains on screen before output
            # to stderr begins
            predictions.clear()

            if output is None:
                # NOTE: This is the wrapped stdout created by
                # stdio_redirect_tqdm
                output_ctx = nullcontext(sys.stdout)
            else:
                output_ctx = open(output, 'a', encoding='utf-8')

        with output_ctx as fobj, predictions:
            csv_writer = csv.writer(fobj)
            fields = self.prediction_cls(extra_cols=extra_cols)._fields
            csv_writer.writerow(fields)

            for prediction in predictions:
                # convert 0-D tensors to plain scalars
                csv_writer.writerow(prediction.to_scalars())
