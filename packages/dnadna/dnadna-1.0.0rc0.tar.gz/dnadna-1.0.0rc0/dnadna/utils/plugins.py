"""Utilities for loading and managing DNADNA plugins."""


import importlib
import importlib.machinery
import logging
import os
import os.path as pth
import runpy
import warnings
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime
from inspect import signature

from .. import DNADNAWarning
from .misc import decamelcase


# Keep track of which plugins have already been loaded so the are not loaded
# multiple times
_plugins_cache = defaultdict(set)


log = logging.getLogger(__name__)


def load_plugins(plugins):
    """
    Import a list of "plugins".

    In DNADNA's simple plugin system, a "plugin" is just an additional Python
    module that should be loaded, e.g. to provide new implementations of some
    of DNADNA's primitive types (simulators, config templates, etc.)

    Parameters
    ----------
    plugins : list
        Either Python module names in dotted ``foo.bar`` format, or a
        file path to a Python module with one of the valid module filename
        extensions as returned by `importlib.machinery.all_suffixes`.  Every
        module in this list will be attempted to be imported, and any
        exceptions that occur (`ImportError` or other exceptions raised by
        modules) will be raised.
    """

    all_suffixes = importlib.machinery.all_suffixes()
    for plugin in plugins:
        if plugin in _plugins_cache:
            continue

        _, ext = pth.splitext(plugin)
        is_file_plugin = pth.isfile(plugin) and ext in all_suffixes

        if is_file_plugin:
            # It at least looks like a possible Python module filename; try
            # importing by filename first
            def load_plugin(plugin):
                # All we care about is executing the module; if the module (or
                # any modules it imports) define a Simulator subclass it will
                # be added to Simulator._registry and hence kept in scope; we
                # don't necessarily care about keeping anything else
                globs = runpy.run_path(plugin)
                # If __version__ in the module's globals return its version,
                # otherwise return its last modified time as a datetime
                if '__version__' in globs:
                    return globs['__version__']
                else:
                    return datetime.fromtimestamp(os.stat(plugin).st_mtime)
        else:
            def load_plugin(plugin):
                # Try treating it as a normal importable module
                mod = importlib.import_module(plugin)
                if hasattr(mod, '__version__'):
                    return mod.__version__
                elif hasattr(mod, '__file__') and pth.exists(mod.__file__):
                    return datetime.fromtimestamp(
                            os.stat(mod.__file__).st_mtime)
                else:
                    return None

        try:
            if plugin.startswith('dnadna.'):
                # For built-in plugins only log at the default level to
                # reduce noise during normal runs
                log_level = logging.DEBUG
            else:
                log_level = logging.INFO

            with Pluggable._loading(provider=plugin) as registry_log:
                version = load_plugin(plugin)
                if isinstance(version, datetime):
                    version_fmt = f' (modified {version})'
                elif version is not None:
                    version_fmt = f' (version {version})'
                else:
                    version_fmt = ''

                log.log(log_level,
                        f'loaded plugin {plugin}{version_fmt} providing:')
                for msg in registry_log:
                    log.log(log_level, f'  -> {msg}')
        except Exception as exc:
            raise ImportError(
                f'exception raised trying to import plugin module '
                f'{plugin}: {exc}')


def loaded_plugins():
    """Returns the names (filenames or module names) of all loaded plugins."""

    return frozenset(_plugins_cache)


class Pluggable:
    """
    Base class for all interfaces that can be extended via a plugin.

    Each subclass of `Pluggable` maintains its own registry of loaded plugins.
    For example the list of available networks can be extended simply by
    subclassing `~dnanda.nets.Network` in a plugin.
    """

    _registry = {}
    """
    This is the registry of all types of pluggables.

    All direct subclasses of `Pluggable` are in effect plugins to the plugin
    framework.
    """

    _provider = None
    """
    Used when loading a plugin module to set the name of the module which
    provided each loaded plugin.
    """

    _registry_log = None
    """
    Used when loading a plugin module to record loaded plugins.
    """

    _plugin_name = 'pluggable'
    """
    A 'canonical' name for the plugin that is typically all lower-case used
    to identify the plugin internally.

    By default it is derived automatically from the class name using
    `~dnadna.utils.misc.decamelcase`.
    """

    _pluggable = None
    """
    References the `Pluggable` subclass to which a plugin belongs; on
    pluggables this references the class itself (e.g. ``Transform._pluggable is
    Transform``).
    """

    name = _plugin_name
    """
    The user-facing name of the plugin, which can be provided by a user
    implementing a plugin.

    Typically it is automatically the same as the internal ``Pluggable._name``
    but users are free to provide their own custom name here when implementing
    a plugin.
    """

    schema = {}
    """
    Schema for the plugin's configuration, if any.

    It can be either a string containing the name (without the ``.yml``
    extension) of a schema in the default schema path (for built-in plugins) or
    a `dict` representing the schema.

    Not all plugins must have schemas.

    For now a class can only be a subclass of one pluggable; in other words
    a single class cannot provide multiple plugin interfaces.
    """

    def __init_subclass__(cls):
        """
        If a direct subclass of `Pluggable` is created (i.e. it has `Pluggable`
        directly in it ``__bases__``) then it is added to the registry of
        pluggables.

        If a subclass of a subclass of a pluggable is created, then it is added
        to the registry of plugins to that pluggable.

        Subclasses of pluggables that are also pluggable interfaces cannot be
        created for now.

        Examples
        --------

        >>> from dnadna.utils.plugins import Pluggable
        >>> class MyPluggable(Pluggable):
        ...     pass
        ...
        >>> Pluggable._registry['my_pluggable']
        <class 'dnadna.utils.plugins.MyPluggable'>
        >>> Pluggable._registry['my_pluggable']._registry
        {}
        >>> class MyPlugin(MyPluggable):
        ...     pass
        ...
        >>> Pluggable._registry['my_pluggable']._registry
        {'my_plugin': <class 'dnadna.utils.plugins.MyPlugin'>}

        It is also possible to subclas a plugin, in which case it will become
        a new plugin to the sample pluggable:

        >>> class MyPlugin2(MyPlugin):
        ...     pass
        ...
        >>> Pluggable._registry['my_pluggable']._registry
        {'my_plugin': <class 'dnadna.utils.plugins.MyPlugin'>,
        'my_plugin2': <class 'dnadna.utils.plugins.MyPlugin2'>}

        >>> del Pluggable._registry['my_pluggable']  # cleanup
        """

        if Pluggable in cls.__bases__:
            registry = Pluggable._registry
            # Give the pluggable its own registry of plugins overriding
            # Pluggable._registry
            cls._registry = {}
            cls._pluggable = cls
        else:
            registry = cls._registry

        plugin_name = decamelcase(cls.__name__)

        if '_plugin_name' not in cls.__dict__:
            # Set the plugin's own name using the default scheme; in some
            # cases (e.g. Simulator) the pluggable's '.name' might be an
            # abstractproperty (the pluggable requires plugin implementations
            # to provide a name) so we don't set the name in this case
            if 'name' in cls.__dict__ and isinstance(cls.name, str):
                plugin_name = cls.name
            else:
                plugin_name = decamelcase(cls.__name__)
                if 'name' not in cls.__dict__:
                    cls.name = plugin_name

            cls._plugin_name = plugin_name

        for base_cls in cls.__bases__:
            if not issubclass(base_cls, Pluggable):
                continue

            for plugin in registry.values():
                if plugin.name == plugin_name:
                    warnings.warn(
                        f'a {cls._pluggable.__name__} by the name '
                        f'{plugin_name} has already been declared: '
                        f'{plugin.__module__}.{plugin.__qualname__}; it will '
                        f'be replaced by {cls.__module__}.{cls.__qualname__}',
                        DNADNAWarning)
                    break

            if not isinstance(cls.schema, (str, dict)):
                raise ValueError(
                    f'{cls.__name__}.schema must be the name of a schema or a '
                    f'schema instance as a dict')

            registry[plugin_name] = cls

            cls.plugin_registered()

            if cls._pluggable is cls:
                pluggable_name = Pluggable._plugin_name
            else:
                pluggable_name = cls._pluggable._plugin_name

            def is_builtin_plugin(cls):
                # Is this a plugin from a built-in module (part of the
                # dnadna package) excluding dnadna.examples which are treated
                # as normal plugins
                mod = cls.__module__
                return (mod.startswith('dnadna.') and
                        not mod.startswith('dnadna.examples.'))

            if is_builtin_plugin(cls) or cls._registry_log is None:
                # Just immediately log the plugin's registry to the DEBUG log;
                # this is useful for logging built-in plugins
                log.debug(
                    f'loaded built-in plugin {pluggable_name}:{plugin_name} '
                    f'({cls})')
            else:
                cls._registry_log.append(
                        f'{pluggable_name}:{plugin_name} ({cls})')

            # Save the plugin in the global plugin cache
            if not is_builtin_plugin(cls):
                if cls._provider is None:
                    provider = cls.__module__
                else:
                    provider = cls._provider
                cls.provider = provider
                _plugins_cache[cls.provider].add(cls)
            else:
                cls.provider = None

            return  # don't look for any more Pluggables in the bases

    @classmethod
    def plugin_registered(cls):
        """
        An optional method plugins/pluggables can implement which is called
        after the plugin has been registered by the plugin system, and may
        perform arbitrary side-effects.
        """

    @classmethod
    def get_plugins(cls):
        """
        Return all plugins registered with this pluggable.

        Returns an iterator of tuples consisting of each plugin's name
        along with the plugin class itself.
        """

        for name, plugin in cls._registry.items():
            yield (name, plugin)

    @classmethod
    def get_plugin(cls, name):
        """
        Return the plugin by the given name.

        This can be specified in two different ways: The exact name of the
        class or the plugin's `Pluggable.name`.

        Examples
        --------

        >>> from dnadna.utils.plugins import Pluggable
        >>> class MyPluggable(Pluggable):
        ...     pass
        ...
        >>> class MyPlugin(MyPluggable):
        ...     pass
        ...
        >>> MyPluggable.get_plugin('MyPlugin')
        <class 'dnadna.utils.plugins.MyPlugin'>
        >>> MyPluggable.get_plugin('my_plugin')
        <class 'dnadna.utils.plugins.MyPlugin'>

        If this method is called on `Pluggable` itself, it returns the
        pluggable of that name:

        >>> Pluggable.get_plugin('MyPluggable')
        <class 'dnadna.utils.plugins.MyPluggable'>
        >>> Pluggable.get_plugin('my_pluggable')
        <class 'dnadna.utils.plugins.MyPluggable'>
        >>> del Pluggable._registry['my_pluggable']  # cleanup
        """

        for plugin_name, plugin in cls.get_plugins():
            if plugin_name == name or plugin.__name__ == name:
                return plugin
        else:
            if cls._pluggable is not None:
                pluggable = cls._pluggable.__name__
            else:
                pluggable = Pluggable.__name__

            raise ValueError(f'no {pluggable} named {name} found')

    @classmethod
    def get_schema(cls):
        r"""
        For internal use by DNADNA's schema reference resolver for
        ``dnadna-plugin:`` URIs.

        Returns a dict of JSON Schema definitions describing the available
        plugins.

        Individual `Pluggable` subclasses may provide their own implementation
        to provide additional Pluggable-specific definitions for use in parts
        of the DNADNA schemas.

        Examples
        --------

        Just for testing, we make sure the existing Pluggable registry is
        clear, and save the old one:

        >>> from dnadna.utils.plugins import Pluggable
        >>> old_registry = Pluggable._registry
        >>> Pluggable._registry = {}

        Define a new pluggable and instantiate one of its plugins.  The
        pluggable has its own ``get_schema()`` which provides a way to validate
        configuration for its plugins:

        >>> class MyPluggable(Pluggable):
        ...     @classmethod
        ...     def get_schema(cls):
        ...         if cls is MyPluggable:
        ...             # return a oneOf for the schemas of all the plugins
        ...             # to MyPluggable
        ...             return {
        ...                 'oneOf': [
        ...                     {'$ref': f'dnadna-plugin:{cls.name}:{plugin_name}'}
        ...                     for plugin_name, _ in cls.get_plugins()
        ...                  ]}
        ...         # Return the schema for just this plugin; it combines the
        ...         # config schema with an additional required 'name' property
        ...         return {
        ...             'allOf': [{
        ...                 'properties': {
        ...                     'name': {
        ...                         'type': 'string',
        ...                         'enum': [cls.name, cls.__name__]
        ...                      }
        ...                  },
        ...                  'required': ['name'],
        ...              },
        ...              plugin.schema]
        ...         }
        ...

        Now we implement a plugin of ``MyPluggable`` that has its own
        ``schema``:

        >>> class MyPlugin(MyPluggable):
        ...     schema = {
        ...         'properties': {'param1': {'type': 'integer'}},
        ...         'required': ['param1']
        ...     }
        ...     def __init__(self, param1):
        ...         self.param1 = param1
        ...

        Calling just `Pluggable.get_schema()` returns definitions related to
        all ``Pluggable``\s.  In particular, it has one definition per
        ``Pluggable`` which lists the names of all known plugins for that
        ``Pluggable``:

        >>> Pluggable.get_schema()
        {'type': 'string', 'enum': ['my_pluggable', 'MyPluggable'],
        'definitions': {'my_pluggable': {'type': 'string', 'enum':
        ['my_plugin', 'MyPlugin']}}}

        We can also get the pluggable-specific schema definitions defined for
        ``MyPluggable`` by either calling
        ``MyPluggable.get_schema()`` directly, or:

        >>> pluggable = Pluggable.get_plugin('my_pluggable')
        >>> schema = pluggable.get_schema()
        >>> schema
        {'oneOf': [{'$ref': 'dnadna-plugin:my_pluggable:my_plugin'}]}

        Furthermore, the full schema provided by ``MyPlugin`` looks like:

        >>> plugin = pluggable.get_plugin('my_plugin')
        >>> plugin.get_schema()
        {'allOf': [{'properties':
        {'name': {'type': 'string', 'enum': ['my_plugin', 'MyPlugin']}},
        'required': ['name']},
        {'properties': {'param1': {'type': 'integer'}},
        'required': ['param1']}]}

        Here we can create a simple schema that accepts configuration for a
        single ``MyPlugin`` for its ``transform`` property.  If you look at the
        implementation of `~dnadna.transforms.Transform.get_schema` you can get
        a sense of what motivates this example:

        >>> my_pluggables = {'oneOf': [plugin.get_schema()
        ...                            for _, plugin in MyPluggable.get_plugins()]
        ...                 }
        >>> schema = {
        ...     'properties': {
        ...         'transform': {'$ref': '#/definitions/my_pluggables'}
        ...     },
        ...     'definitions': {'my_pluggables': my_pluggables}
        ... }
        ...

        The following config should pass validation against this schema:

        >>> config = {
        ...     'transform': {
        ...         'name': 'my_plugin',
        ...         'param1': 1
        ...     }
        ... }
        >>> import jsonschema
        >>> jsonschema.validate(config, schema)

        This config does not pass validation because there is no "transform"
        named 'my_plugin2':

        >>> config = {
        ...     'transform': {
        ...         'name': 'my_plugin2',
        ...         'param1': 1
        ...     }
        ... }
        >>> jsonschema.validate(config, schema)
        Traceback (most recent call last):
        ...
        jsonschema.exceptions.ValidationError: 'my_plugin2' is not one of ['my_plugin', 'MyPlugin']
        ...

        The above example showed programmatically creating a JSON Schema
        document using the return value from ``MyPluggable.get_schema()``, but
        when using the `~dnadna.utils.config.ConfigValidator` class, a ``$ref``
        resolver for the custom ``dnadna-plugin:`` URI scheme is provided.
        This can be used in schemas loaded by DNADNA to directly access
        definitions provided by plugins:

        >>> from dnadna.utils.config import ConfigValidator
        >>> schema = {
        ...     'properties': {
        ...         'transform': {
        ...             '$ref': 'dnadna-plugin:my_pluggable'
        ...         }
        ...     }
        ... }
        ...
        >>> validator = ConfigValidator(schema)
        >>> config = {
        ...     'transform': {
        ...         'name': 'my_plugin',
        ...         'param1': 1
        ...     }
        ... }
        >>> validator.validate(config)
        >>> config = {
        ...     'transform': {
        ...         'name': 'my_plugin2',
        ...         'param1': 1
        ...     }
        ... }
        >>> validator.validate(config)
        Traceback (most recent call last):
        ...
        dnadna.utils.config.ConfigError: error in config at 'transform.name':
        'my_plugin2' is not one of ['my_plugin', 'MyPlugin']

        >>> Pluggable._registry = old_registry  # cleanup
        """

        # The default implementation does something different depending on
        # the class it's called on:
        #
        # * On Pluggable itself it generates a schema for the name of a
        #   pluggable.  It also generates a definitions list for schemas
        #   matching the name of a sepecific pluggable (e.g.
        #   #/definitions/my_pluggable gives the names of all MyPluggables)
        #
        # * On a specific Pluggable it generates a schema for the name of a
        #   plugin registered to that pluggable.
        #
        # * On a specific plugin it simply returns that plugin's schema
        #   if any.
        #
        # This method may be overridden at any level, by a pluggable, or a
        # plugin, to extend this behavior.
        return cls._get_schema(cls)

    @staticmethod
    def _get_schema(cls):
        if cls is not Pluggable and cls is not cls._pluggable:
            # It is a a plugin; just return its config schema by default
            return cls.schema

        name_enum = []
        schema = {'type': 'string', 'enum': name_enum}

        for plugin_name, plugin in cls.get_plugins():
            # Allow both the canonical plugin_name and the plugin's class
            # name
            name_enum.append(plugin_name)
            name_enum.append(plugin.__name__)
            if cls is Pluggable:
                definitions = schema.setdefault('definitions', {})
                # Call the default Pluggable.get_schema here instead of
                # the cls.get_schema in case it is overridden by the class
                definitions[plugin_name] = Pluggable._get_schema(plugin)

        return schema

    @classmethod
    @contextmanager
    def _loading(cls, provider=None):
        """
        Context manager which sets plugin registry loading mode.

        Instead of logging plugin registry directly to the logger, it adds
        log messages to the list returned by this context manager, which
        can be used to defer logging of registered plugins; this is used
        to implement logging in `load_plugins`.

        It also sets the "provider" (the plugin module that provided the
        plugin) which is also saved on each plugin, which can be used for
        introspection later (e.g. to find out what plugin modules are needed
        in order to provide the functionality of that plugin).
        """

        try:
            Pluggable._registry_log = []
            Pluggable._provider = provider
            yield Pluggable._registry_log
        finally:
            Pluggable._registry_log = None
            Pluggable._provider = None


def gen_name_params_schema(cls, ignored_positional_args=[]):
    """
    Helper function used by some pluggables to generate their plugin schema.

    Notably used by `~dnadna.nets.Network` and `~dnadna.optim.Optimizer`, both
    of which are specified in the config file in a format like::

        name: 'name_of_plugin'
        params:
            param1: value1
            param2: value2

    This function generates a schema in this format.
    """

    schemas = []
    all_names = []
    for plugin_name, plugin in sorted(cls.get_plugins(), key=lambda p: p[0]):
        # Determine whether or not the network *requires* any parameters to
        # be initialized.  If it doesn't take any parameters or if all the
        # parameters have defaults, then the 'params' property is not
        # strictly required.  This also accounts for the 'special' param
        # names in _computed_params
        params = list(signature(plugin).parameters.values())
        required_params = set(param.name for param in params
                              if param.default is param.empty)
        required = ['name']
        if (len(params) > 0 and
                required_params.difference(ignored_positional_args)):
            required.append('params')

        # Either the "plugin_name" spelling or the class name "PluginName"
        # spelling are allowed
        names = [plugin_name, plugin.__name__]
        all_names.append(names)

        schemas.append({
            'properties': {
                'name': {
                    'enum': names,
                },
                'params': ({'$ref': plugin.schema + '.yml'}
                           if isinstance(plugin.schema, str)
                           else plugin.schema)
            },
            'required': required
        })

    # A custom error message for when the user does not provided one of the
    # supported names.
    all_names = ['{}/{}'.format(*name_pair) for name_pair in all_names]
    error_msg = f'must be one of {", ".join(all_names)}'

    return {
        'type': 'object',
        'oneOf': schemas,
        'errorMsg': {'enum': error_msg}
    }
