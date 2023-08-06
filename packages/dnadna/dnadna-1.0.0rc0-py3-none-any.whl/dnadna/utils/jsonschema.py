"""Utilities for extending JSON-Schema validation of config files."""


import copy
import os
import os.path as pth
import pathlib
from collections import ChainMap
from collections.abc import Mapping
from datetime import datetime
from urllib.parse import splittype, urlsplit, urljoin
from urllib.request import url2pathname

import jsonschema
from jsonschema.exceptions import best_match, relevance

from .. import BUILTIN_PLUGINS
from .plugins import Pluggable, load_plugins
from .serializers import DictSerializer


SCHEMA_SUPPORTED_VERSIONS = [
    jsonschema.Draft6Validator,
    jsonschema.Draft7Validator
]


SCHEMA_DIRS = [pathlib.Path(pth.dirname(pth.dirname(__file__))) / 'schemas']
"""Paths to built-in schemas."""


ERRORMSG_SCHEMA_BASE = {
    'oneOf': [
        {
            'type': 'string',
            'description':
                'a single error message to return for any error in validating '
                'the associated property',
            'minLength': 1,
            'format': 'errorMsg'
        }, {
            'type': 'object',
            'description':
                'a mapping from JSON-Schema validators (e.g. "type", '
                '"minLength", etc.) to the error message to use when a '
                'property fails that specific validator, e.g., a special '
                'message may be provided when a string fails to validate '
                'against "minLength" as opposed to "pattern"; the value '
                '"default" may be used as a fallback message to use for other '
                'validators not listed',
            'properties': {
                # Additional properties will be filled out by
                # make_config_schema depending on the metaschema we're
                # extending
                'default': {
                    'type': 'string',
                    'minLength': 1,
                    'format': 'errorMsg'
                }
            }
        }
    ]
}


def make_config_meta_schema(meta_schema):
    """
    Given an existing JSON-Schema meta-schema, it is extended by adding support
    for the ``"errorMsg"`` property, which provides custom error messages to
    return to users when a property in the schema fails validation.

    See `dnadna.utils.config.ConfigValidator.validate` for a worked example.
    """

    errormsg_schema = copy.deepcopy(ERRORMSG_SCHEMA_BASE)
    for prop in meta_schema.get('properties', {}):
        # Fill out the allowed properties for the object form of errorMsg
        # (the second choice in the oneOf array)
        errormsg_schema['oneOf'][1]['properties'][prop] = {
            'type': 'string',
            'minLength': 1,
            'format': 'errorMsg'
        }

    meta_schema = copy.deepcopy(meta_schema)
    meta_schema['properties']['errorMsg'] = errormsg_schema
    return meta_schema


class CustomValidationError(jsonschema.ValidationError):
    """
    Extends `jsonschema.ValidationError` for use with custom "errorMsg"
    errors.

    Because "errorMsg" supports some template variables in the error message,
    this stores the template and implements ``self.message`` as a property
    which renders the template.
    """

    @property
    def message(self):
        errormsg = self.__dict__['message']
        prop = '.'.join(str(p) for p in self.path)
        return errormsg.format(property=prop,
                               value=self.instance,
                               validator=self.validator,
                               validator_value=self.validator_value)

    @message.setter
    def message(self, value):
        self.__dict__['message'] = value


class ConfigValidatorMixin:
    """
    Mix-in class to combine with `jsonschema.IValidator` classes to add new
    functionality provided by `make_config_validator`.

    The new validator has additional options for controlling how to resolve
    relative filenames in the schema and how to handle the ``default`` property
    in schemas.

    It also allows specifying a default format checker.

    See the implementation in `~dnadna.utils.config.ConfigValidator` class for
    more details and example usage.
    """

    format_checker = None

    def __init__(self, schema, *args, resolve_plugins=True,
                 resolve_defaults=True, resolve_filenames=True,
                 posixify_filenames=False, **kwargs):
        self._resolve_plugins = resolve_plugins
        kwargs.setdefault('format_checker', self.format_checker)
        kwargs.setdefault('resolver', self.get_resolver_for(schema))
        super().__init__(schema, *args, **kwargs)
        self._resolve_defaults = resolve_defaults
        self._resolve_filenames = resolve_filenames
        self._posixify_filenames = posixify_filenames
        self._schema_stack = [self.schema]

    def iter_errors(self, instance, _schema=None):
        pop_schema_stack = False
        if isinstance(_schema, dict) and '$ref' not in _schema:
            self._schema_stack.append(_schema)
            pop_schema_stack = True

        err_occurred = False
        orig_instance = instance

        if isinstance(orig_instance, (dict, Mapping)):
            # This is to work around a bug with applying default values from
            # schemas, when that schema is a sub-schema in a oneOf/anyOf schema
            # composition.
            #
            # Only defaults from the correct/matching sub-schema should be
            # applied.  If an error occurs in a sub-schema, then it is not
            # applicable.
            #
            # To work around this we must first make a copy of the original
            # instance, and then only apply any updates made to that instance
            # if there were no errors.  I don't think this is a perfect
            # workaround, but it solves the test case in the test
            # test_config_validation_defaults_nested_in_one_of() in
            # tests/test_utils.py
            orig_instance = copy.deepcopy(orig_instance)

        try:
            for error in super().iter_errors(instance, _schema=_schema):
                err_occurred = True
                if not isinstance(error, CustomValidationError):
                    errormsg = self._find_applicable_errormsg(error)
                    if errormsg is not None:
                        error = CustomValidationError.create_from(error)
                        error.message = errormsg
                yield error
        finally:
            if pop_schema_stack:
                self._schema_stack.pop()

            if err_occurred and orig_instance is not instance:
                # If an error occurred, clear any updates made to the instance
                # and replace it with its original values.
                if isinstance(instance, ChainMap):
                    # Special case for ChainMaps: doing a clear/update results
                    # in nested ChainMaps: It's better to clear and update the
                    # first map since this is the one that gets modified if any
                    # of the instance's values were modified (or new keys
                    # added)
                    instance.maps[0].clear()
                    instance.maps[0].update(orig_instance.maps[0])
                else:
                    # The general approach for dict to restore the same dict
                    # object to a previous value
                    instance.clear()
                    instance.update(orig_instance)

    def descend(self, instance, schema, path=None, schema_path=None):
        # This is to work around a bug/oversight (?) in jsonschema that
        # context errors in a oneOf/anyOf do not have their full paths filled
        # out
        for error in super().descend(instance, schema, path=path,
                schema_path=schema_path):
            for cerr in error.context:
                if path is not None:
                    cerr.path.appendleft(path)
                if schema_path is not None:
                    cerr.schema_path.appendleft(schema_path)
            yield error

    def validate(self, *args, **kwargs):
        """
        Passes all errors through `jsonschema.exceptions.best_match` with a
        custom heuristic (see `relevance_with_const_select`) to raise the most
        relevant validation error.
        """

        error = best_match(self.iter_errors(*args, **kwargs),
                           key=self.relevance_with_const_select)
        if error is None:
            return

        raise error

    @staticmethod
    def relevance_with_const_select(error):
        """
        This implements a custom heuristic for choose the best-match error
        with `jsonschema.exceptions.best_match`.

        It prioritizes `CustomValidatonError`\\s over other errors, so that
        a schema with custom ``errorMsg`` properties can decide through that
        means which errors are most important.  This can be especially useful
        when using ``errorMsg`` in a ``oneOf`` suite, where the custom error
        is perhaps more important than default reason given for why none of the
        sub-schemas matched.  Here's an example::

            >>> schema = {
            ...     'oneOf': [{
            ...         'type': 'object',
            ...         'minProperties': 1,
            ...         'errorMsg': {
            ...             'minProperties': 'must have at least 1 entry'
            ...         }
            ...    }, {
            ...        'type': 'array',
            ...        'minItems': 1,
            ...        'errorMsg': {
            ...            'minItems': 'must have at least 1 entry'
            ...        }
            ...    }]
            ... }

        This schema matches either an array or an object, which in either case
        must have a least one property (in the object case) or item (in the
        array case).  Without this custom relevance function, ``best_match``
        will just choose one of the errors from one of the ``oneOf`` schemas
        which caused it not to match.  In this case it happens to select the
        type error from the first sub-schema::

            >>> from jsonschema.exceptions import best_match
            >>> from dnadna.utils.jsonschema import make_config_validator
            >>> Validator = make_config_validator()
            >>> validator = Validator(schema)
            >>> errors = validator.iter_errors([])  # try an empty list
            >>> best_match(errors)
            <ValidationError: "[] is not of type 'object'">

        Using this custom error ranking algorithm, the `CustomValidationError`
        will be preferred::

            >>> errors = validator.iter_errors([])  # try an empty list
            >>> best_match(errors,
            ...            key=ConfigValidatorMixin.relevance_with_const_select)
            <CustomValidationError: 'must have at least 1 entry'>

        Otherwise it's the same as the default heuristic with extra support for
        a common pattern where ``oneOf`` combined with ``const`` or ``enum`` is
        used to select from a list of sub-schemas based on the value of a
        single property.

        For example::

            >>> schema = {
            ...     'required': ['type'],
            ...     'oneOf': [{
            ...         'properties': {
            ...             'type': {'const': 'regression'},
            ...         }
            ...     }, {
            ...         'properties': {
            ...             'type': {'const': 'classification'},
            ...             'classes': {'type': 'integer'},
            ...         },
            ...         'required': ['classes']
            ...     }]
            ... }
            ...

        The first schema in the `oneOf` list will match if and only if
        the document contains ``{'type': 'regression'}`` and the second will
        match if and only if ``{'type': 'classification'}`` with no ambiguity.

        In this case, when ``type`` matches a specific sub-schema, the more
        interesting error will be errors that occur within the sub-schema.
        But the default heuristics are such that it will think the ``type``
        error is more interesting.  For example::

            >>> import jsonschema
            >>> jsonschema.validate({'type': 'classification'}, schema)
            Traceback (most recent call last):
            ...
            jsonschema.exceptions.ValidationError: 'regression' was expected
            ...

        Here the error that matched the heuristic happens to be the the one
        that caused the first sub-schema to be skipped over, because
        ``properties.type.const`` did not match.  But actual reason an error
        was raised at all was because the second sub-schema didn't match either
        due to the required ``'classes'`` property being missing.  Under this
        use case, that would be the more interesting error.  This heuristic
        solves that.  In order to demonstrate this, we have to call
        ``best_match`` directly, since `jsonschema.validate` doesn't have an
        option to pass down a different heuristic key::

            >>> from dnadna.utils.jsonschema import ConfigValidatorMixin
            >>> validator = jsonschema.Draft7Validator(schema)
            >>> errors = validator.iter_errors({'type': 'classification'})
            >>> raise best_match(errors,
            ...           key=ConfigValidatorMixin.relevance_with_const_select)
            Traceback (most recent call last):
            ...
            jsonschema.exceptions.ValidationError: 'classes' is a required property
            ...

        This also supports a similar pattern (used by several plugins) where
        instead of ``const`` being used to select a specific sub-schema,
        ``enum`` is used with a unique list of values (in fact ``const`` is
        just a special case of ``enum`` with only one value).  For example::

            >>> schema = {
            ...     'required': ['name'],
            ...     'oneOf': [{
            ...         'properties': {
            ...             'name': {'enum': ['my-plugin', 'MyPlugin']},
            ...         }
            ...     }, {
            ...         'properties': {
            ...             'name': {'enum': ['my-plugin2', 'MyPlugin2']},
            ...             'x': {'type': 'integer'},
            ...         },
            ...         'required': ['x']
            ...     }]
            ... }
            ...
            >>> validator = jsonschema.Draft7Validator(schema)
            >>> errors = validator.iter_errors({'name': 'my-plugin2'})
            >>> raise best_match(errors,
            ...           key=ConfigValidatorMixin.relevance_with_const_select)
            Traceback (most recent call last):
            ...
            jsonschema.exceptions.ValidationError: 'x' is a required property
            ...
        """

        # How it works: the default heuristic used "relevance" returns a tuple
        # of integers that are used to rank errors
        # When looping over the 'context' errors of a oneOf error, the
        # error with the lowest ranking wins (see the docstring of best_match
        # for explanation)
        #
        # In this case we just extend that tuple with one more value which
        # always contains 1 *if* the error's parent is a oneOf and the error's
        # validator is 'const'.  So this assumes somewhat implicitly that this
        # oneOf+const select pattern is in use (most of the time the most
        # likely reason to use const in a oneOf sub-schema)
        rank = relevance(error)

        # Also add True/False depending on whether the error is a
        # CustomValidationError, so that these are weighted more heavily
        # (remember, False is ranked higher in this case)
        rank = (not isinstance(error, CustomValidationError),) + rank

        if (error.parent and error.parent.validator == 'oneOf' and
                error.validator in ('const', 'enum')):
            # It looks like we are using the oneOf+const pattern
            return (True,) + rank
        else:
            return (False,) + rank

    def _find_applicable_errormsg(self, error):
        # Walk up the current chain of schemas until we find one with an
        # errorMsg
        # If the errorMsg is a string, or a dict with a 'default' key, it
        # applies to all errors at or below that sub-schema, otherwise if it
        # is a dict it only applies if the relevant validator is in found in
        # the dict
        schema_path = list(error.schema_path)
        for schema in self._schema_stack[::-1]:
            for validator in schema_path[::-1]:
                errormsg = schema.get('errorMsg')
                if isinstance(errormsg, dict):
                    errormsg = errormsg.get(validator, errormsg.get('default'))

                if errormsg is not None:
                    return errormsg

        # No custom error message found anywhere on the schema path
        return None

    @staticmethod
    def _resolver_builtin_schemas_base():
        return 'file:///{}/'.format(SCHEMA_DIRS[0].as_posix())

    @classmethod
    def _resolver_fallback_handler(cls, uri):
        # This is kind of a hack needed in order to allow fallback to file:///
        # resolution when inside the scope of a dnadna-plugin: reference.
        # The problem this is solving is that when jsonschema *resolves*
        # a URI to a schema it enters a new "scope" based on that URI (this is
        # useful for resolving relative URIs relative to a schema's path)
        #
        # Unfortunately, when entering a schema fom a dnadna-plugin: URI,
        # relative filenames are no longer relevant, so if inside a
        # dnadna-plugin: schema we see {"$ref": "training.yml"} for example,
        # the resolver does not know how to join the path "training.yml" to the
        # dnadna-plugin reference, and falls back on just tring to handle the
        # "URI" "training.yml" by itself, which is in fact no longer a valid
        # URI.
        #
        # In this case its scheme is '' so we can actually register a handler
        # for the '' scheme, and assume in cases like this that it refers to a
        # file relative to the dnadna schema paths, as is the case for the
        # default scope of this resolver.
        base = cls._resolver_builtin_schemas_base()
        return cls._resolver_file_handler(urljoin(base, uri))

    # TODO: reference resolver for local files in the dnadna/schemas
    # This should be improved to allow more flexible schema resolution
    # but this suffices for the built-in schemas
    @staticmethod
    def _resolver_file_handler(uri):
        """
        Custom ``file://`` handler for RefResolver that can load schemas from YAML
        or JSON.

        Slightly hackish, but supported workaround to the larger issue discussed at
        https://github.com/Julian/jsonschema/issues/420
        """

        filename = url2pathname(splittype(uri)[1])
        return DictSerializer.load(filename)

    def _resolver_dnadna_plugin_handler(self, uri):
        """
        Custom handler for ``dnadna-plugin:`` URIs.

        See also `~dnadna.utils.plugins.Pluggable.get_schema` for example
        usage.

        The format for these URIs is
        ``dnadna-plugin:[pluggable-name][:plugin-name][#fragment]``.

        If ``pluggable-name`` and ``plugin-name`` are ommitted, then the
        top-level schema is that provided by `Pluggable.get_schema`, whereas a
        URI like ``dnadna-plugin:transform`` returns a schema from
        `Transform.get_schema`, and so on.

        If ``resolve_plugins=False`` was passed to the validator's constructor,
        no plugins are loaded and the plugin resolves to an empty schema.
        """

        if not self._resolve_plugins:
            return {}

        parts = urlsplit(uri)
        if parts.scheme != 'dnadna-plugin':
            raise ValueError(
                f'this resolver only handles dnadna-plugin: URIs; got {uri}')

        fmt = 'dnadna-plugin:[pluggable-name][:plugin-name][#fragment]'

        if parts.netloc:
            raise ValueError(
                f'dnadna-plugin: URIs do not have a netloc component (i.e. '
                f'they should not have // after the colon); they must be in '
                f'the format {fmt}')

        path = parts.path.split(':', 1)

        # Ensure all built-in pluggables have been loaded
        load_plugins(BUILTIN_PLUGINS)

        if len(path) == 1 and not path[0].strip():
            # empty path, so it is the top-level definitions
            schema = Pluggable.get_schema()
        elif len(path) == 1:
            schema = Pluggable.get_plugin(path[0]).get_schema()
        elif len(path) == 2:
            plugin = Pluggable.get_plugin(path[0]).get_plugin(path[1])
            schema = plugin.get_schema()
        else:
            raise ValueError(
                f'invalid dnadna-plugin: URI; must be in the format {fmt}')

        return schema

    def get_resolver_for(self, schema):
        """
        Return a RefResolver that can handle relative references to other
        schemas installed in main schemas directory.

        This is somewhat inflexible at the moment but is all we need currently.
        """

        # Passing the current schema as the 'referrer' argument to RefResolver
        # is necessary to ensure URL fragments (e.g.  "$ref":
        # "#definitions/...) are resolved properly after other references are
        # resolved
        handlers = {
            '': self._resolver_fallback_handler,
            'file': self._resolver_file_handler,
            'dnadna-plugin': self._resolver_dnadna_plugin_handler
        }
        return jsonschema.RefResolver(
                self._resolver_builtin_schemas_base(),
                schema, handlers=handlers)


def make_config_validator(validator_cls=jsonschema.Draft7Validator,
                          get_path=None):
    """
    Creates a `jsonschema.IValidator` class based on the given
    ``validator_cls`` (`jsonschema.Draft7Validator` by default) which supports
    special functionality for DNADNA `.Config` objects, though it can be adapted
    to other types.

    See the `~dnadna.utils.config.ConfigValidator` class for more details and
    example usage.
    """
    # Note: We can't simply provide a format checker, or override the 'format'
    # property validator as they are only passed the value of the string
    # instance, and are not given an opportunity to modify its value.  In order
    # to *modify* the instance in-place we need to handle this at a higher
    # level where we have access to the full dict instance.
    validate_properties = validator_cls.VALIDATORS['properties']

    def resolve_filename(instance, prop, subschema, get_path=None,
                         posixify=False):
        errors = []

        # Handle format: filename
        format_ = subschema.get('format')
        if (subschema.get('type') == 'string' and
                format_ in ('filename', 'filename!')):
            filename = instance.get(prop)
            if isinstance(filename, str):
                if callable(get_path):
                    path = get_path(instance, prop)
                else:
                    path = '.'
                # If neither the filename nor its default are a string to
                # begin with we ignore it for now and deal with it later
                # when we do error checking
                filename = normpath(filename, relto=path, _posixify=posixify)

                if format_[-1] == '!' and not pth.exists(filename):
                    errors.append(
                        jsonschema.ValidationError(
                            f'property {prop} of {instance} must be an '
                            f'existing file, but {filename} does not exist'
                        )
                    )
                else:
                    instance[prop] = filename

        return errors

    def validate_config_properties(validator, properties, instance, schema):
        errors = []

        if validator._resolve_filenames:
            posixify = validator._posixify_filenames
            for prop, subschema in properties.items():
                errors += resolve_filename(instance, prop, subschema,
                                           get_path, posixify)

        # Now run the default properties validator
        errors += list(validate_properties(validator, properties, instance,
                                           schema))

        # If there are no errors then the instance matches this schema or
        # sub-schema (in the case of a oneOf/allOf/anyOf); now we assign any
        # defaults so that defaults are only added from a schema that this
        # instance actually matches.  Then, if defaults were added we re-run
        # validation on the properties to ensure that the defaults are also
        # valid.
        if not errors and validator._resolve_defaults:
            added_defaults = False
            for prop, subschema in properties.items():
                # Fill missing props with their defaults
                if (isinstance(instance, (dict, Mapping)) and
                        'default' in subschema and prop not in instance):
                    instance[prop] = subschema['default']
                    added_defaults = True

            if added_defaults:
                # We only need to re-validate if any defaults were actually
                # assigned
                errors = validate_properties(validator, properties, instance,
                                             schema)

        for error in errors:
            yield error

    # Create the format checker; filename and filename! are already handled
    # specially in validate_config_properties since it requires special support
    # for resolving relative filenames.  Other, simpler formats are checked
    # here
    format_checker = copy.deepcopy(jsonschema.draft7_format_checker)

    @format_checker.checks('python-module', raises=(ImportError,))
    def check_python_module(instance):
        if isinstance(instance, str):
            __import__(instance)

        return True

    validator_cls = jsonschema.validators.extend(
            validator_cls, {'properties': validate_config_properties})

    # Add the mix-in class
    validator_cls = type(f'DNA{validator_cls.__name__}',
                         (ConfigValidatorMixin, validator_cls),
                         {'format_checker': format_checker})

    # Create the extended meta-schema with support for errorMsg
    validator_cls.META_SCHEMA = \
            make_config_meta_schema(validator_cls.META_SCHEMA)

    # Support arbitrary Mapping types for 'object' in addition to dict; this
    # will inclue Config objects
    validator_cls.TYPE_CHECKER = validator_cls.TYPE_CHECKER.redefine('object',
            lambda tc, obj: isinstance(obj, (dict, Mapping)))
    return validator_cls


def normpath(path, relto='.', _posixify=False):
    """
    Converts the given path to an absolute path.

    If it is a relative path, the path to which it is relative can be specified
    with the ``relto`` argument (if ``relto`` is a relative path then the final
    path is relative to the current working directory as with any
    `os.path.abspath` call).

    Examples
    --------

    >>> import os
    >>> import os.path as pth
    >>> from dnadna.utils.jsonschema import normpath
    >>> tmp = getfixture('tmpdir')  # pytest specific
    >>> _ = tmp.join('a').mkdir()
    >>> with tmp.join('a').as_cwd():
    ...     normpath('b', _posixify=True)
    ...     normpath('c', 'b', _posixify=True)
    ...     # should ignore relto given absolute path
    ...     normpath('/c', 'asdf', _posixify=True)
    '/.../a/b'
    '/.../a/b/c'
    '/c'
    """

    if not pth.isabs(path):
        path = pth.join(relto, path)

    path = pth.abspath(path)

    if _posixify:
        # "private" option used currently only for testing: makes a Windows
        # path beginning with a drive letter look like a POSIX path by dropping
        # the drive letter and switching the slash directions
        path = pth.splitdrive(path)[1].replace(os.sep, '/')

    return path


def timestamp(dt=None):
    """
    Returns a UTC datetime formatted according to the format expected by
    the JSON Schema "date-time" format.

    See
    https://json-schema.org/understanding-json-schema/reference/string.html#dates-and-times

    Examples
    --------

    >>> from dnadna.utils.jsonschema import timestamp
    >>> from datetime import datetime
    >>> dt = datetime(2021, 4, 8, 11, 11, 27)  # assumed UTC
    >>> timestamp(dt)
    '2021-04-08T11:11:27+00:00'
    """

    if dt is None:
        dt = datetime.utcnow()

    return dt.isoformat() + '+00:00'
