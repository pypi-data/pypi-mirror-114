"""Management of parameters to be learned in a training run."""


import warnings

import torch
import torch.nn as nn

from . import DNADNAWarning
from .utils.config import ConfigMixIn
from .utils.decorators import cached_property
from .utils.misc import unique


# NOTE: All loss functions built into pytorch are named like SomethingLoss;
# This just makes a mapping of all lower-case versions of the function names
# (for case-insensitive comparison) minus the redundant "Loss" part to the
# functions themselves (all classes actually)
# TODO: Many of the loss functions in PyTorch are parameterized themselves, and
# we need an interface for specifying loss function parameters.
# TODO: The current code just allows any loss function defined in PyTorch;
# should we restrict this to some specific ones?
LOSS_FUNCS = None


class MCELoss(nn.Module):
    """Mean Circular Error"""

    def forward(self, x, y):
        return torch.min((x - y) % 1, (y - x) % 1).mean().unsqueeze(0)


def _get_loss_funcs():
    global LOSS_FUNCS

    LOSS_FUNCS = {'mce': MCELoss}

    for name, cls in vars(nn).items():
        if not name[0] == '_' and name.endswith('Loss'):
            LOSS_FUNCS[name.lower()[:-4]] = cls


_get_loss_funcs()


class ParamSet(ConfigMixIn):
    """
    Class for managing a set of model parameters as defined by the
    :ref:`param set schema <schema-param-set>`.

    In most cases this is not used directly; instead the `LearnedParams`
    subclass of this is used to manage a parameter set used for model
    training.  This base class implements more basic functionality that
    does not depend on a ``scenario_params`` table and does not support
    training-specific functionality like `LearnedParams`.
    """

    config_schema = 'param-set'

    # TODO: Default loss funcs should come directly out of the schema but
    # that doesn't likely work yet.
    default_loss_funcs = {
        'regression': 'MSE',
        'classification': 'Cross Entropy'
    }

    def __init__(self, config={}, validate=True):
        # Special case: the training.yml schema allows learned_params to be
        # a list of single-element mappings (how PyYAML loads ordered mappings)
        # In this case we build a dict from the list, taking advantage of
        # insertion order preservation of plain dicts in Python 3.6+
        # See https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/46
        if isinstance(config, list):
            new_config = {}
            for param in config:
                if len(param) != 1:
                    raise ValueError(
                        f"when {self.__class__.__name__} is given a list of "
                        f"parameters, each item must be a single-element "
                        f"dict keyed by the parameter name")

                param_name, param = list(param.items())[0]
                new_config[param_name] = param

            config = new_config

        super().__init__(config, validate=validate)
        self._normalize_params()

    @cached_property
    def params(self):
        """
        Returns a dict of params.

        Examples
        --------

        This example also demonstrates that the param details are also filled
        out with defaults not included in the original config (``loss_weight``,
        ``n_classes``, etc.):

        >>> from dnadna.params import ParamSet
        >>> config = {
        ...     'b': {'type': 'regression', 'loss_func': 'MSE'},
        ...     # 'x' gets the default loss func, cross entropy
        ...     'x': {'type': 'classification', 'classes': 3},
        ...     # 'a' gets the default loss func, MSE
        ...     'a': {'type': 'regression'},
        ...     'z': {'type': 'classification', 'classes': ['a', 'b'],
        ...           'loss_func': 'Cross Entropy'},
        ...     'y': {'type': 'regression', 'loss_func': 'MCE'}
        ... }
        >>> learned_params = ParamSet(config)
        >>> learned_params.params
        {'b': {'type': 'regression', 'loss_func': 'MSE', 'loss_weight': 1,
               'log_transform': False, 'tied_to_position': False},
         'x': {'type': 'classification', 'classes': ['0', '1', '2'],
               'loss_func': 'Cross Entropy', 'loss_weight': 1, 'n_classes': 3},
         'a': {'type': 'regression', 'loss_func': 'MSE', 'loss_weight': 1,
               'log_transform': False, 'tied_to_position': False},
         'z': {'type': 'classification', 'classes': ['a', 'b'],
               'loss_func': 'Cross Entropy', 'loss_weight': 1, 'n_classes': 2},
         'y': {'type': 'regression', 'loss_func': 'MCE', 'loss_weight': 1,
               'log_transform': False, 'tied_to_position': False}}
        """

        return self.config.dict()

    @cached_property
    def param_names(self):
        """
        Return list of names of all learned parameters.

        Parameters are given in the order they were specified in the config.
        If an unordered mapping was used, the order will still be preserved
        since Python 3.6+ preserves dictionary insertion order and this holds
        when loading mappings from YAML and JSON.

        It is also possible to instantiate the `ParamSet` with a list of
        mappings, each containing one element.  This is how `omaps
        <https://yaml.org/type/omap.html>`_ (ordered mappings) are encoded in
        YAML, and the same structure can be used in JSON.  In this case the
        order of the elements in the list are preserved.

        Examples
        --------

        >>> from dnadna.params import ParamSet
        >>> config = {
        ...     'b': {'type': 'regression', 'loss_func': 'MSE'},
        ...     # 'x' gets the default loss func, cross entropy
        ...     'x': {'type': 'classification', 'classes': 3},
        ...     # 'a' gets the default loss func, MSE
        ...     'a': {'type': 'regression'},
        ...     'z': {'type': 'classification', 'classes': 3,
        ...           'loss_func': 'Cross Entropy'},
        ...     'y': {'type': 'regression', 'loss_func': 'MCE'}
        ... }
        >>> learned_params = ParamSet(config)
        >>> learned_params.param_names
        ['b', 'x', 'a', 'z', 'y']

        Similar (shorter) example, but from a list:

        >>> config = [
        ...     {'b': {'type': 'regression', 'loss_func': 'MSE'}},
        ...     {'x': {'type': 'classification', 'classes': 3}}
        ... ]
        ...
        >>> learned_params = ParamSet(config)
        >>> learned_params.param_names
        ['b', 'x']
        """

        return list(self.params)

    @property
    def regression_params(self):
        return {k: v for k, v in self.params.items()
                if v['type'] == 'regression'}

    @property
    def classification_params(self):
        return {k: v for k, v in self.params.items()
                if v['type'] == 'classification'}

    @cached_property
    def n_outputs(self):
        """
        Expected number of outputs for a network that is trained for this set
        of parameters.

        This should be one output per regression parameter, and one output *per
        class* of each classification parameter, giving the likelihood of an
        input falling into that class.
        """

        tot_classes = sum(p['n_classes']
                          for p in self.classification_params.values())

        return len(self.regression_params) + tot_classes

    @cached_property
    def param_slices(self):
        """
        Returns a dict mapping parameter names to tuples of slices.

        The slice to take of the targets tensor for values of that parameter,
        and the slice to take of the outputs tensor for that parameter.

        This is used during training: The ``targets`` tensor contains (for a
        batch of one or more scenarios) the known target values for each
        parameter being learned, and the ``outputs`` tensor contains the
        predicted values for each parameter returned from the model being
        trained (where in ``outputs`` there is a predicted likelihood for each
        category in a classification parameter).

        Examples
        --------

        >>> from dnadna.params import ParamSet
        >>> import pandas as pd
        >>> config = {
        ...     'b': {'type': 'regression', 'loss_func': 'MSE'},
        ...     # 'x' gets the default loss func, cross entropy
        ...     'x': {'type': 'classification', 'classes': 3},
        ...     # 'a' gets the default loss func, MSE
        ...     'a': {'type': 'regression'},
        ...     'z': {'type': 'classification', 'classes': 3,
        ...           'loss_func': 'Cross Entropy'},
        ...     'y': {'type': 'regression', 'loss_func': 'MCE'}
        ... }
        >>> learned_params = ParamSet(config)
        >>> learned_params.param_slices
        {'b': (slice(0, 1, None), slice(0, 1, None)),
         'x': (slice(1, 2, None), slice(1, 4, None)),
         'a': (slice(2, 3, None), slice(4, 5, None)),
         'z': (slice(3, 4, None), slice(5, 8, None)),
         'y': (slice(4, 5, None), slice(8, 9, None))}
        """

        targets_idx = 0
        outputs_idx = 0
        slices = {}

        for param_name in self.param_names:
            param = self.params[param_name]
            if param['type'] == 'regression':
                slices[param_name] = (
                        slice(targets_idx, targets_idx + 1),
                        slice(outputs_idx, outputs_idx + 1)
                )
                targets_idx += 1
                outputs_idx += 1
            else:
                # classification
                n_classes = param['n_classes']
                slices[param_name] = (
                        slice(targets_idx, targets_idx + 1),
                        slice(outputs_idx, outputs_idx + n_classes)
                )
                targets_idx += 1
                outputs_idx += n_classes

        return slices

    def _normalize_params(self):
        """
        After being initialized with some parameter configurations, this
        performs additional post-initialization normalization of the parameter
        configurations.

        Currently this normalizes the classes of classification params--the
        configuration may contain either an integer (giving the number of
        classes) or a list of strings (or ints) giving labels to the classes.
        For each classification parameter we add an ``'n_classes'`` property,
        which may be equivalent to ``'classes'`` (in the integer case).  In the
        case where ``'classes'`` is a list of labels, we also normalize so that
        all the labels are unique strings.

        It also sets the default value for ``'loss_func'`` property on each
        parameter that lacks it.  This should be performed automatically via
        the schema, but that is not working yet.
        """

        for param_name, param in self.classification_params.items():
            orig_classes = param['classes']
            if isinstance(orig_classes, list):
                # We want to preserve order so a set isn't used
                classes = unique(map(str, orig_classes))
                if len(classes) != len(orig_classes):
                    warnings.warn(
                        f'classifiation parameter {param_name} has duplicates '
                        f'in its list of class labels; the class labels have '
                        f'been normalized to be unique: {classes}',
                        DNADNAWarning)

                param['n_classes'] = len(classes)
                param['classes'] = classes
            else:
                param['n_classes'] = param['classes']
                # The class names are just numbered
                param['classes'] = [str(cls) for cls in range(param['classes'])]

        for param in self.params.values():
            param.setdefault('loss_func',
                             self.default_loss_funcs[param['type']])


class LearnedParams(ParamSet):
    """
    Class for managing the parameters on which a model is trained.

    Attributes
    ----------
    config : `~dnadna.utils.config.Config` or `dict`
        The learned parameters configuration, confirming to the
        :ref:`learned parameters schema <schema-param-set>`.

    """

    def __init__(self, config, scenario_params, validate=True):
        # If the config was originally given as a list (see ParamSet.__init__),
        # we keep its existing order.  Otherwise, parameters are re-ordered
        # according to their order in the scenario_params table.
        if not isinstance(config, list):
            new_config = {}
            for param_name in scenario_params.columns:
                if param_name in config:
                    new_config[param_name] = config[param_name]

            config = new_config

        super().__init__(config, validate=validate)

        self._scenario_params = scenario_params

    @property
    def scenario_params(self):
        """
        The :ref:`scenario parameters table <dnadna-dataset-scenario-params>`,
        as a `pandas.DataFrame` giving the known values of parameters the
        dataset is being trained on for all scenarios the dataset is being
        trained on.
        """
        return self._scenario_params

    @cached_property
    def loss_funcs(self):
        """Maps parameter names to their loss functions."""

        loss_funcs = {}

        for param_name, param in self.params.items():
            loss_func = param['loss_func']

            loss_func_cls = self._normalize_loss_func(loss_func)

            if loss_func is nn.CrossEntropyLoss:
                # NOTE: Here we make a special case, but there are several
                # other loss functions that take some class weights as an
                # argument, so perhaps we could generalize this a bit if
                # desired.  This is also very specific to classification
                # parameters, which might help later for generalization
                w = self.scenario_params.groupby(param_name).size()
                # inverse of the frequency. Smaller class should weight more in
                # the loss.size()
                weight = torch.Tensor(w.sum() / w)
                loss = loss_func_cls(weight=weight)
            else:
                loss = loss_func_cls()

            loss_funcs[param_name] = loss

        return loss_funcs

    @cached_property
    def loss_weights(self):
        """Maps parameter names to their loss weights (if any)."""

        loss_weights = {}

        for param_name, param in self.params.items():
            # loss_weights should be optional
            if param['type'] == "classification":
                weight = torch.Tensor([1 / param['n_classes']])
            else:
                bad_val = self.scenario_params[param_name].isnull().sum()
                freq_ok = 1 - bad_val / len(self.scenario_params)
                weight = torch.Tensor([1 / freq_ok])

            weight *= param['loss_weight']
            loss_weights[param_name] = weight

        return loss_weights

    def to(self, device=None):
        r"""
        Similarly to `torch.nn.Module.to` with ``device=device``, moves all
        `loss_weights` and the parameters of all `loss_funcs` to the specified
        device.
        """

        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'

        for param, lw in self.loss_weights.items():
            self.loss_weights[param] = lw.to(device)

        for lf in self.loss_funcs.values():
            lf.to(device)

        return self

    @staticmethod
    def _normalize_loss_func(loss_func):
        """
        Maps a loss function name (as given in the configuration) to the actual
        function or class which implements that function.

        The loss function name may be case-insensitive, and contain spaces
        (which are removed).

        Currently, the available loss functions are any defined in the
        `torch.nn` module with a name ending in ``"Loss"``, or additional loss
        functions defined in this module.  In the future this will be made more
        extensible as needed.

        Examples
        --------

        >>> from dnadna.params import LearnedParams
        >>> LearnedParams._normalize_loss_func('MSE')
        <class 'torch.nn.modules.loss.MSELoss'>
        >>> LearnedParams._normalize_loss_func('cross entropy')
        <class 'torch.nn.modules.loss.CrossEntropyLoss'>
        >>> LearnedParams._normalize_loss_func('MCE')
        <class 'dnadna.params.MCELoss'>
        """

        try:
            return LOSS_FUNCS[loss_func.lower().replace(' ', '')]
        except KeyError:
            raise ValueError(
                f'unknown loss function: {loss_func}; must be '
                f'one of {", ".join(sorted(LOSS_FUNCS))}')
