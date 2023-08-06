"""
Optimizer plugins for DNADNA.

The base implementation provides support for all of the built-in optimizers
from `torch.optim`.
"""

import warnings
from inspect import signature

from torch import optim as torch_optim
from torch.optim.optimizer import required

from . import DNADNAWarning
from .utils.config import Config
from .utils.misc import dict_merge
from .utils.plugins import Pluggable, gen_name_params_schema


class Optimizer(torch_optim.Optimizer, Pluggable):
    """
    Subclasses `torch.optim.Optimizer` adding support for DNADNA's plugin
    interface.

    This allows creating new optimizers that can be used in DNADNA.  It also
    makes all of PyTorch's built-in optimizers available for use in DNADNA
    (though not all have been tested).
    """

    param_aliases = {'learning_rate': 'lr'}
    """
    Maps optimizer parameters read from the DNADNA config file to the
    corresponding keyword argument name for the Optimizer's initializer.

    In particular, the optimizers in `torch.optim` all take an argument called
    ``lr`` for learning rate, but we also allow ``learning_rate``.
    """

    param_aliases_inverse = {v: k for k, v in param_aliases.items()}

    schema = {
        'properties': {
            'lr': {'type': 'number'}
        }
    }

    @classmethod
    def from_config(cls, config, params, validate=True):
        """
        Initialize an `Optimizer` from the optimizer configuration from a
        config file.

        Examples
        --------

        >>> from dnadna.optim import Optimizer
        >>> import torch.nn
        >>> mod = torch.nn.Linear(1, 1)  # a dummy module
        >>> optim = Optimizer.from_config({
        ...     'name': 'Adam',
        ...     'params': {
        ...         'learning_rate': 0.2,
        ...         'weight_decay': 0.01
        ...     }
        ... }, mod.parameters())
        ...
        >>> optim
        Adam (
        Parameter Group 0
            amsgrad: False
            betas: [0.9, 0.999]
            eps: 1e-08
            lr: 0.2
            weight_decay: 0.01
        )
        """

        if not isinstance(config, Config):
            config = Config(config)

        if validate:
            config.validate(cls.get_schema())

        optim_name = config['name']
        optim_params = config['params'].dict()

        # Apply aliases to optimizer parameters
        for alias, param in cls.param_aliases.items():
            if alias in optim_params:
                if param in optim_params:
                    warnings.warn(
                        f'optimizer params for {optim_name} contains both '
                        f'{alias} and {param} where {alias} is an alias for '
                        f'{param}; the value of {param} will be overridden',
                        DNADNAWarning)
                optim_params[param] = optim_params.pop(alias)

        return cls.get_plugin(optim_name)(params, **optim_params)

    @classmethod
    def get_schema(cls):
        """
        Returns a schema pairing the ``optimizer.name`` property with the valid
        ``optimizer.params`` associated with that optimizer (which may be very
        broad if the `Optimizer` subclass does not specify its
        `Optimizer.schema`).
        """

        if cls is not Optimizer:
            # This is a Network plugin; just return the net's config schema
            return cls.schema

        return gen_name_params_schema(cls, ['params'])

    @classmethod
    def from_torch(cls, torch_cls, schema_overrides={}):
        """
        Registers a `torch.optim.Optimizer` into the DNADNA optimizer plugin
        framework.

        This automatically generates a config schema for each optimizer, though
        the ``schema_overrides`` option allows overrides to the automatically
        generated one via `~dnadna.utils.misc.dict_merge`.

        .. warning::

            This does not yet support per-parameter optimizer options.
        """

        sig = signature(torch_cls)
        param_schemas = {}
        required_params = []

        for param in sig.parameters.values():
            if param.name == 'params':
                # This is model parameters passed to the optimizer; it's not
                # declared as part of the schema, and is common to all
                # optimizers.
                continue

            if param.default is sig.empty:
                param_schemas[param.name] = {}
            else:
                param_schemas[param.name] = \
                    cls._schema_from_default(param.default)

            if param.default is required:
                required_params.append(param.name)

        schema = {
            'properties': param_schemas,
        }

        if required_params:
            schema['required'] = required_params

        schema = dict_merge(cls.schema, schema, schema_overrides)

        # Add aliases to the schema
        # We don't make the aliases mutually exclusive; the expectation will be
        # the user will use one or the other but not both.  We could make them
        # strictly mutually-exclusive but this makes the schema much more
        # complex.
        for param, alias in cls.param_aliases_inverse.items():
            if param in schema['properties']:
                # Convert it into a pattern property supporting the alias
                # One downside to using a patternProperty is that it cannot
                # fill in defaults, but this is OK because we don't want it to
                # provide defaults for *both* the parameter and its alias.
                #
                # If lr/learning rate, for example, has a default value, it
                # will be provided by the __init__ of the Optimizer itself.
                # If it does not have a default value, and it was omitted from
                # the original config, then the config validation will fail
                # anyways due to the missing required parameter.
                param_schema = schema['properties'].pop(param)
                pattern = f'^{param}|{alias}$'
                pattern_props = schema.setdefault('patternProperties', {})
                pattern_props[pattern] = param_schema

            if param in required_params:
                # This is a tricky one to deal with...
                required_params.remove(param)
                all_of = schema.setdefault('allOf', [])
                all_of.append({
                    'oneOf': [
                        {'required': [param]},
                        {'required': [alias]}
                    ]
                })

        if required_params:
            schema['required'] = required_params

        return type(torch_cls.__name__, (torch_cls, Optimizer),
                    {'schema': schema})

    @classmethod
    def _schema_from_default(cls, value, include_default=True):
        """
        Determines a basic schema for a keyword argument based on its default
        value.

        This currently works in a few specific, limited cases derived from the
        existing classes in `torch.optim`.  If it fails to guess, it will
        return just an empty schema.
        """

        param_schema = {}

        if isinstance(value, bool):
            # NOTE: Important for this to come before checking if it's an int,
            # since bools are also considered ints
            param_schema = {'type': 'boolean'}
        elif isinstance(value, (int, float)):
            # Numeric types are always treated as 'number' in the JSON
            # Schema sense: None of the current built-in optimizers have
            # arguments that strictly require ints; should one come along
            # that can be specified in a schema override.
            param_schema = {'type': 'number'}
            value = float(value)
        elif isinstance(value, str):
            param_schema = {'type': 'string'}
        elif isinstance(value, tuple):
            param_schema = {'type': 'array'}
            param_schema['items'] = [cls._schema_from_default(v, False)
                                     for v in value]
            value = list(value)
        elif value is None:
            param_schema = {'type': 'null'}

        if include_default and value is not required:
            param_schema['default'] = value

        return param_schema


# These are special cases for some of the Optimizers that don't conform to the
# general assumptions of the schemas generated by Optimizer.from_torch.
# These need to be updated on a case-by-case basis if new PyTorch Optimizers
# are added.
_SCHEMA_OVERRIDES = {
    'LBFGS': {
        'properties': {
            'history_size': {'type': 'integer'},
            'line_search_fn': {
                'type': ['null', 'string'],
                'oneOf': [
                    {'type': 'null'},
                    {'type': 'string', 'enum': ['strong_wolfe']}
                ]
            }
        }
    }
}


# Register all Optimizers included in torch.optim as available optimizers.
# As flexible as Optimizer.from_torch is, there are still a handful of special
# cases represented in _SCHEMA_OVERRIDES
for cls_name, torch_cls in vars(torch_optim).items():
    if not (isinstance(torch_cls, type) and
            issubclass(torch_cls, torch_optim.Optimizer) and
            torch_cls is not torch_optim.Optimizer):
        continue

    locals()[cls_name] = Optimizer.from_torch(
        torch_cls, _SCHEMA_OVERRIDES.get(cls_name, {}))


# Cleanup
try:
    del cls_name, torch_cls
except NameError:
    pass
