"""Config file, serialization, and schema handling."""


import collections
import copy
import os
import os.path as pth
import pathlib
from collections.abc import Mapping, KeysView, ValuesView, ItemsView
from itertools import chain

import jsonschema

from .. import DEFAULTS_DIR
from .decorators import cached_classproperty, lru_cache_with_dict
from .jsonschema import make_config_validator, normpath, SCHEMA_DIRS
from .serializers import DictSerializer, JSONSerializer, YAMLSerializer
from .yaml import CommentedMapping, CommentedYAMLDumper


__all__ = [
    'load_dict', 'save_dict', 'save_dict_annotated', 'normpath',
    'Config', 'ConfigError', 'ConfigMixIn'
]


def load_dict(filename, **kwargs):
    """
    Loads a nested JSON-like data structure from a given filename.

    May support multiple serialization formats, determined primarily by the
    filename extension.  Currently supports:

        * JSON (``.json``)
        * YAML (``.yml`` or ``.yaml``)
    """

    return DictSerializer.load(filename, **kwargs)


def save_dict(obj, filename, **kwargs):
    """
    Serializes a nested JSON-like data structure to a given filename.

    The serialization format is determined by the filename.

    May support multiple serialization formats, determined primarily by the
    filename extension.  Currently supports:

        * JSON (``.json``)
        * YAML (``.yml`` or ``.yaml``)
    """

    DictSerializer.save(obj, filename, **kwargs)


def save_dict_annotated(obj, filename, schema=None, validate=False,
                        serializer=YAMLSerializer, **kwargs):
    """
    Serializes a (possibly nested) `dict` to YAML, after (optionally)
    validating it against the given ``schema``, and producing comments from the
    title/description keywords in the schema.

    Parameters
    ----------
    obj : dict, `Config`
        The dict-like object to save.
    filename : str, `pathlib.Path`, file-like
        A filename or `pathlib.Path`, or open file-like object to which to
        stream the output.
    schema : str or dict, optional
        A schema given either as the name of a schema in the schema registry,
        or a full schema object given as a dict.  If omitted, this is
        equivalent to `save_dict` to a YAML file, and no annotation is added.
    validate : bool, optional
        Validate the given object against the schema before writing it
        (default: False).  This can be used in case the object is not already
        known to be valid against the schema.
    serializer : `~dnadna.utils.serializers.DictSerializer`, optional
        Specify the `~dnadna.utils.serializers.DictSerializer` to use; normally
        this should be the `~dnadna.utils.serializers.YAMLSerializer` since
        it's the only one (currently) which supports
        comments.

    Examples
    --------

    >>> from io import StringIO
    >>> from dnadna.utils.config import save_dict_annotated
    >>> schema = {
    ...     'description': 'file description',
    ...     'properties': {
    ...         'a': {'type': 'string', 'title': 'a',
    ...               'description': 'a description'},
    ...         'b': {'type': 'integer', 'description': 'b description'},
    ...         'c': {
    ...             'type': 'object',
    ...             'description': 'c description',
    ...             'properties': {
    ...                 'd': {'description': 'd description'},
    ...                 'e': {'description': 'e description'}
    ...             }
    ...         },
    ...         'f': {'description': 'f description'}
    ...     }
    ... }
    ...
    >>> d = {'a': 'foo', 'b': 2, 'c': {'d': 4, 'e': 5}, 'f': 6}
    >>> out = StringIO()
    >>> save_dict_annotated(d, out, schema=schema, validate=True, indent=4)
    >>> print(out.getvalue())
    # file description
    # a
    #
    # a description
    a: foo
    # b description
    b: 2
    # c description
    c:
        # d description
        d: 4
        # e description
        e: 5
    # f description
    f: 6
    """

    if schema is None:
        return serializer.save(obj, filename, **kwargs)

    if not isinstance(schema, dict):
        schema = Config.schemas[schema]

    validator = Config._schema_validator_for(schema)
    if validate:
        # TODO: This probably shouldn't be so dependent on internal details of
        # the `Config` class; perhaps schema validation can be moved out to an
        # independent routine
        # Deep-copy the original object since the schema validator *can* modify
        # it in-place
        obj = copy.deepcopy(obj)
        validator.validate(obj)

    # If the filename is not a YAML file, also do not annotate; JSON files
    # cannot be commented
    if (isinstance(filename, (str, pathlib.Path)) and
            serializer.language != 'yaml'):
        return serializer.save(obj, filename, **kwargs)

    # Build a CommentedMapping with comments extracted from the schema
    def get_comment(schema):
        # Technically if a schema contains a $ref property, the ref'd schema is
        # supposed to completely override any other properties in the schema.
        # However, if we have a schema with some description properties *and*
        # a ref, we try getting the description properties from the base schema
        # first, then from the ref'd schema.
        # You can see an example where this can be useful in the training.yml
        # schema for the 'network' property.
        comment = None

        if 'description' in schema:
            comment = schema.get('description')
            if 'title' in schema:
                if comment:
                    comment = schema['title'] + '\n\n' + comment
                else:
                    comment = schema['title']

        ref = schema.get('$ref')
        if comment is None and ref:
            # Try the ref'd schema
            with validator.resolver.resolving(ref) as schema:
                return get_comment(schema)

        return comment

    comment = get_comment(schema)
    comments = {}
    path = []

    # TODO: Improve support getting comments from sub-schemas in
    # allOf/anyOf/oneOf keywords; right now we ignore the semantics of
    # allOf/anyOf/oneOf and just take the comment from the first sub-schema
    # that contains a property.
    # In order to do this right we would have to actually validate the config
    # against each sub-schema to determine the one that would match, and take
    # the property description from that sub-schema.
    #
    # Perhaps it would be better to actually implement a special schema
    # validator that also extracts comments as it goes.
    def get_comments_recursive(schema):
        for key in ('allOf', 'anyOf', 'oneOf'):
            for subschema in schema.get(key, []):
                get_comments_recursive(subschema)

        ref = schema.get('$ref')
        if ref:
            # resolve references
            with validator.resolver.resolving(ref) as schema:
                get_comments_recursive(schema)
                return

        for prop, subschema in schema.get('properties', {}).items():
            path.append(prop)
            comment = get_comment(subschema)
            if comment is not None:
                comments.setdefault(tuple(path), comment)

            get_comments_recursive(subschema)
            path.pop()

    get_comments_recursive(schema)

    commented_obj = CommentedMapping(obj, comment=comment, comments=comments)
    serializer.save(commented_obj, filename, Dumper=CommentedYAMLDumper,
                    **kwargs)


def load_dict_from_json(filepath):
    """
    Load a JSON file as a `dict`.

    Shortcut for `~dnadna.utils.serializers.JSONSerializer.load`.

    Parameters
    ==========

    filepath : str
        filepath to the json file
    """
    return JSONSerializer.load(filepath)


def save_dict_in_json(filepath, params):
    """Save a dictionary into a json file.

    Parameters
    ==========
    filepath : str
        filepath of the json file
    params : dict
        dictionary containing the overall parameters used for the simulation
        (e.g. path to the data folder, number of epoch...)
    """
    return JSONSerializer.save(params, filepath, indent=4)


# The default implements of KeysView, ValuesView, and ItemsView have annoying
# reprs that only show the repr of the underlying Mapping, rather than showing
# just the keys/values/items respectively.
class _KeysView(KeysView):
    def __repr__(self):
        return f'{self.__class__.__name__.strip("_")}({list(self)!r})'


class _ValuesView(ValuesView):
    def __repr__(self):
        return f'{self.__class__.__name__}.strip("_")({list(self.values())!r})'


class _ItemsView(ItemsView):
    def __repr__(self):
        return f'{self.__class__.__name__}.strip("_")({list(self.items())!r})'


class DeepChainMap(collections.ChainMap):
    """
    Like `collections.ChainMap`, but also automatically applies chaining
    recursively to nested dictionaries.

    For example, if two dictionaries in a `DeepChainMap` ``dc`` each contain
    the key ``'c'`` holding a dictionary, then ``dc['c']`` returns a
    `DeepChainMap` of those dictionaries.  This follows the tree recursively
    until and unless the key ``c`` in one of the parent maps does not refer to
    a dictionary--this can have the effect of "clobbering" dicts higher up in
    the tree.  It is also possible to prevent recursion at a specific key by
    providing overrides.

    Parameters
    ----------

    maps : list
        The sequence of mappings to chain together
    overrides : list, optional
        List of tuples giving the path to a key whose value should be
        overridden entirely by the mapping before it in the maps sequence.
        This is only relevant when the value is a dict: Rather than merging
        the two dicts into a `DeepChainMap`, the first dict overrides the value
        of the second.

    Attributes
    ----------

    maps : list
        The sequence of mappings that is walked when looking up keys in a
        `DeepChainMap`.  The key is looked up first in ``.maps[0]`` and then so
        on until found, or until the sequence is exhausted.

    overrides : list
        List of paths into the mapping in the format ``(key, subkey, ...)``
        providing which keys should be overridden by values earlier in the maps
        list (see examples).

    Examples
    --------

    >>> from dnadna.utils.config import DeepChainMap

    Simple case; this is no different from a regular `collections.ChainMap`:

    >>> d = DeepChainMap({'a': 1, 'b': 2}, {'b': 3, 'd': 4})
    >>> dict(d)
    {'a': 1, 'b': 2, 'd': 4}

    But when some of the maps contain nested maps at the same key, those are
    now also chained.  Compare with regular `collections.ChainMap`, in which
    the left-most dict under ``'b'`` completely clobbers the dict in the
    right-hand ``'b'``:

    >>> from collections import ChainMap
    >>> left = {'a': 1, 'b': {'c': 2, 'd': 3}}
    >>> right = {'a': 2, 'b': {'c': 4, 'f': 5}, 'g': 6}
    >>> c = ChainMap(left, right)
    >>> dict(c)
    {'a': 1, 'b': {'c': 2, 'd': 3}, 'g': 6}

    With `DeepChainMap` the dicts under ``'b'`` are chained as well.  The
    `DeepChainMap.dict` method can be used to recursively convert all nested
    dicts to a plain `dict`:

    >>> d = DeepChainMap(left, right)
    >>> d.dict()
    {'a': 1, 'b': {'c': 2, 'd': 3, 'f': 5}, 'g': 6}

    As mentioned above, nested chaining only continues so long as the dict in
    the chain also contains a dict a the same key; a non-dict value can in a
    sense "interrupt" the chain:

    >>> d = DeepChainMap({'a': {'b': 2}}, {'a': {'c': 3}}, {'a': 5},
    ...                  {'a': {'d': 4}})
    >>> d.dict()
    {'a': {'b': 2, 'c': 3}}

    You can see that the right-most ``{'a': {'d': 4}}`` is ignored since just
    before it ``{'a': 5}`` does not have a dict at ``'a'``.  However, if
    ``'a'`` is *missing* at some point along the chain that is not a
    problem--the nested mapping continues to the next map in the chain:

    >>> d = DeepChainMap({'a': {'b': 2}}, {'a': {'c': 3}}, {},
    ...                  {'a': {'d': 4}})
    >>> d.dict()
    {'a': {'b': 2, 'c': 3, 'd': 4}}

    You can also "interrupt" the chaining for dict values by providing the
    ``overrides`` argument; this is an advanced usage.  In the first case
    ``d['a']['b']`` is merged from both dicts:

    >>> d = DeepChainMap({'a': {'b': {'c': 2}}, 'w': 'w'},
    ...                  {'a': {'b': {'d': 3}}, 'x': 'x'})
    >>> d.dict()
    {'a': {'b': {'c': 2, 'd': 3}}, 'w': 'w', 'x': 'x'}

    But by passing ``overrides=('a', 'b')`` merging stops short at ``d['a']``:

    >>> d = DeepChainMap({'a': {'b': {'c': 2}, 'w': 'w'}},
    ...                  {'a': {'b': {'d': 3}, 'x': 'x'}},
    ...                  overrides=[('a', 'b')])
    >>> d.dict()
    {'a': {'b': {'c': 2}, 'w': 'w', 'x': 'x'}}

    Here you can see that the dicts keyed by ``['a']['b']`` were not merged,
    and only the first one was kept.


    """

    def __init__(self, *maps, overrides=set()):
        super().__init__(*maps)
        self.overrides = overrides
        # override path
        self._overrides = set(ovr[0] for ovr in overrides if len(ovr) == 1)

    def __iter__(self):
        """
        Improved ``__iter__`` over `~collections.ChainMap`.

        The base implementation returns keys in inverse depth order; that is,
        keys that first appear in roots of the mapping tree will appear first
        in the iteration order.

        This makes it so that keys that appear first in leaf nodes are listed
        first in the iteration order.  For example:

        >>> from collections import ChainMap
        >>> a = {'a': 1, 'b': 2}
        >>> b = {'a': 3, 'c': 4, 'd': 5}
        >>> cm = ChainMap(a, b)
        >>> list(cm)
        ['a', 'c', 'd', 'b']

        With `DeepChainMap` it is inverted so that keys in the left-most/leaf
        mappings are returned first:

        >>> from dnadna.utils.config import DeepChainMap
        >>> dcm = DeepChainMap(a, b)
        >>> list(dcm)
        ['a', 'b', 'c', 'd']

        Note that when iterating over values/items the values still come from
        the leaf mappings as expected:

        >>> list(dcm.items())
        [('a', 1), ('b', 2), ('c', 4), ('d', 5)]
        """

        seen = set()  # set of already seen keys
        # This ensures that the order of the keys in `d` is in order of
        # self.maps
        for m in self.maps:
            for k in m:
                if k not in seen:
                    yield k
                    seen.add(k)

    def __getitem__(self, key):
        chained_values = []

        for m in self.maps:
            try:
                chained_values.append(m[key])
            except KeyError:
                continue

        if not chained_values:
            raise KeyError(key)

        first = chained_values[0]

        # Note: Although instances of dict are also instances of Mapping,
        # isinstance(x, dict) is much faster than isinstance(x, Mapping), and
        # dict being the most common case we explicitly check for it first.
        if not isinstance(first, (dict, Mapping)) or key in self._overrides:
            return first

        nested = []

        for m in chained_values:
            if isinstance(m, (dict, Mapping)):
                nested.append(m)
            else:
                break

        overrides = [ovr[1:] for ovr in self.overrides if len(ovr) > 1]
        return self.__class__(*nested, overrides=overrides)

    def get_owner(self, key):
        """
        Given a key, return the first nested map that contains that key.

        Examples
        --------

        >>> from dnadna.utils.config import DeepChainMap
        >>> cm = DeepChainMap({'a': 1, 'b': 2}, {'b': 3, 'c': 4})
        >>> cm.get_owner('b')
        {'a': 1, 'b': 2}
        >>> cm.get_owner('c')
        {'b': 3, 'c': 4}
        """

        for m in self.maps:
            if key in m:
                return m

    def copy(self, folded=False):
        """
        New DeepChainMap or subclass with a new copy of maps[0] and refs to
        maps[1:].

        If ``folded=True``, however, it returns a copy with all maps folded
        in so that there is only one map in the resulting copy; that is, it is
        equivalent to ``DeepChainMap(chain_map.dict())``.
        """

        if folded:
            return self.__class__(self.dict())
        else:
            return super().copy()

    def dict(self, cls=dict):
        """
        Recursively convert self and all nested mappings to a plain `dict`, or
        the type specified by the ``cls`` argument.
        """

        def to_dict(d):
            d = cls(d)
            for k, v in d.items():
                if isinstance(v, (dict, Mapping)):
                    d[k] = to_dict(v)

            return d

        return to_dict(self)

    # Override .keys(), .values(), and .items() to return more debug-friendly
    # View objects
    def keys(self):
        return _KeysView(self)

    def values(self):
        return _ValuesView(self)

    def items(self):
        return _ItemsView(self)

    def _max_depth(self, depth=0):
        """
        Utility function for returning the highest tree depth in a tree of
        nested DeepChainMaps.
        """

        depth += 1
        return max((m._max_depth(depth) for m in self.maps
                    if isinstance(m, collections.ChainMap)), default=depth)


class ConfigError(ValueError):
    def __init__(self, config, msg, suffix='', path=()):
        super().__init__(msg, suffix, path)
        self.config = config

    def __str__(self):
        msg, suffix, path = self.args[:3]

        if isinstance(self.config, Config) and self.config.filename:
            prefix = f'error in "{self.config.filename}"'
        else:
            prefix = 'error in config'

        if path:
            prefix += f" at '{'.'.join(str(p) for p in path)}'"

        msg = f'{prefix}: {msg}'

        if suffix:
            msg += '; ' + suffix

        return msg


class Config(DeepChainMap):
    """
    Represents the configuration for one of DNADNA's components, such as
    simulation and training configuration.

    This is a specialized subclass of `DeepChainMap`, with extra bells and
    whistles, in particular validating the configuration against a
    `JSON Schema`_ using a specialized schema validator with enhanced
    functionality over the default `jsonschema.validate` functionality.
    See `ConfigValidator` for examples of the extra functionality
    provided by the custom schema validator used by `Config`.

    Another special feature of `Config` is to link multiple config files
    together with a special "inherit" property: If the value of a keyword
    in the config is a `dict` containing the "inherit" key, the value of that
    dict is loaded directly from the file pointed to by "inherit".  Any
    additional keys in the dict containing "inherit" override/extend the dict
    loaded from the inherit.  See the Examples section below for explicit
    examples.

    Parameters
    ----------
    *args:
        One or more `dict` or other *mapping* types from which to instantiate
        the `Config`.  In normal usage only one `dict` should be passed.  The
        support for multiple positional arguments is in order to supported the
        underlying `DeepChainMap` functionality.  The reason `DeepChainMap` is
        used is to support the "inherit" functionality.  Each inherited
        `Config` is added to the tree of `DeepChainMap.maps`.
    overrides : list, optional
        Same as in `DeepChainMap`.
    validate : bool or dict, optional
        Validate the given config.  This checks two things: It validates that
        all inherits were successfully resolved.  If a ``schema`` was
        specified, it then also validates the config against that schema
        (default: `False`).  If a non-empty `dict` is given instead, validation
        is enabled, and the dict is passed as keyword arguments to the
        `ConfigValidator` class to control its behavior.  This is used
        primarily for implementation purposes.
    schema : str or dict, optional
        The JSON Schema against which to validate the config.  This can either
        be the name of one of the built-in schemas (see `Config.schemas`) or it
        can be a full JSON Schema object represented as a `dict`.
    filename : str or pathlib.Path, optional
        If the `Config` was read from a file (e.g. as with `Config.from_file`)
        this argument can be used to store the name of the file the config was
        read from.  This should normally not be used directly, as it is
        normally set when using `Config.from_file`
    resolve_inherits : bool or dict, optional
        If `True`, make sure all "inherit" keywords in the given config are
        resolved to their true values, by loading the inherited config
        files. If ``resolve_inherits`` is a non-empty `dict` this has the
        same effect is `True`, except the dict is passed as keyword arguments
        to the `load_dict` call that is used to read inherited config files.
        This argument is primarily for internal use and testing, and should not
        be used directly without knowing what you're doing.

    Examples
    --------
    >>> from dnadna.utils.config import Config

    Under the simplest usage, a `Config` is just a simple wrapper for a `dict`:

    >>> config = Config({'a': 1, 'b': 'c'})
    >>> config['a']
    1
    >>> config['b']
    'c'

    However, when a ``schema`` is provided and ``validate=True``, the wrapped
    dict is validated against that schema.  If validation succeeds, then the
    `Config` object is quietly instantiated with success:

    >>> schema = {'properties': {'a': {'type': 'integer'}}}
    >>> config = Config({'a': 1, 'b': 'c'}, validate=True, schema=schema)

    But when validation fails, instantiating the `Config` will fail with a
    `jsonschema.ValidationError <jsonschema.exceptions.ValidationError>`
    exception:

    >>> config = Config({'a': 'b', 'c': 'd'}, validate=True, schema=schema)
    Traceback (most recent call last):
    ...
    dnadna.utils.config.ConfigError: error in config at 'a': 'b' is not of type 'integer'

    Validation can also be delayed.  If a schema was provided but
    ``validate=False``, a later call to `Config.validate` will validate the
    instantiated `Config` against that schema:

    >>> config = Config({'a': 'b', 'c': 'd'}, schema=schema)
    >>> config['a']  # successfully created despite violating the schema
    'b'
    >>> config.validate()  # validates against the previously provided schema
    Traceback (most recent call last):
    ...
    dnadna.utils.config.ConfigError: error in config at 'a': 'b' is not of
    type 'integer'

    It is also possible to validate against one of the many built-in schemas
    given by:

    >>> sorted(Config.schemas)
    ['dataset', 'dataset_formats/dnadna', 'definitions', 'nets/...', ...,
    'param-set', ..., 'training', 'training-run']

    For example:

    >>> from dnadna.examples.one_event import DEFAULT_ONE_EVENT_CONFIG
    >>> config = Config(DEFAULT_ONE_EVENT_CONFIG.copy(), schema='simulation')
    >>> config.validate() is None
    True

    You can also view the full values of these schemas, like:

    >>> Config.schemas['simulation']
    {'$schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'description': 'JSON Schema (YAML-formatted) for basic properties of a
    simulation...',
    ...}

    Now we discuss inherits, which is a slightly complicated subject.  The
    most basic usage is having a key in the config dictionary like
    ``"key": {"inherit": "/path/to/inherited/file"}``.  In this case the
    value associated with ``"key"`` is replaced with the contents of the
    inherited file:

    >>> from dnadna.utils.config import save_dict
    >>> tmp = getfixture('tmp_path')  # pytest specific
    >>> inherited = tmp / 'inherited.json'
    >>> save_dict({'foo': 'bar', 'baz': 'qux'}, inherited)
    >>> d = {'key': {'inherit': str(inherited)}}

    In the original dict, the value of the ``'key'`` key is just as we
    specified:

    >>> d['key']
    {'inherit': '...inherited.json'}

    But when we instantiate `Config` from this, the value for ``'key'`` will
    be transparently replaced with the contents of ``inherited.json``:

    >>> config = Config(d, resolve_inherits=True)
    >>> config['key']
    Config({'foo': 'bar', 'baz': 'qux'})

    Inherits can also be nested, so if file A inherits from file B, and file B
    also contains inherits, the inherits in file B are resolved first, and so
    on.  Demonstrating this is left as an exercise to the reader.

    If a dict contains the ``'inherit'`` keyword, as well as other keys, first
    the inherit is resolved, but then the other keys in the dict override the
    inherited dict.  This is made possible by the use of `DeepChainMap`:

    >>> d = {'key': {
    ...         'inherit': str(inherited),
    ...         'baz': 'quizling',
    ...         'fred': 'barney',
    ...     }}
    >>> config = Config(d, resolve_inherits=True)
    >>> config['key']
    Config({'baz': 'quizling', 'fred': 'barney', 'foo': 'bar'})

    In the previous examples we used absolute filename paths with
    ``'inherit'``, but it may also contain a relative path.  If it contains a
    relative path there are two possibilities:  If the parent config does not
    have a ``.filename``, then relative paths are simply resolved relative to
    the current working directory.  This is not terribly useful because it
    might resolve to a different file depending on what directory you're
    currently working in.  More useful is that when the parent file *does* have
    a ``.filename``, then relative paths are considered relative to the
    directory containing the parent file.

    For example, let's put a parent and child file in the same directory:

    >>> parent_filename = tmp / 'parent.json'
    >>> child_filename = tmp / 'child.json'
    >>> save_dict({'a': 1}, child_filename)
    >>> save_dict({'foo': {'inherit': 'child.json'}, 'b': 2}, parent_filename)

    As noted, both files are in the same directory:

    >>> parent_filename.parent == child_filename.parent
    True

    So we could specify just ``{'inherit': 'child.json'}``, meaning inherit
    from the file ``child.json`` in the same directory as me:

    >>> parent = Config.from_file(parent_filename)
    >>> parent
    Config({'foo': {'a': 1}, 'b': 2})
    >>> parent['foo']
    Config({'a': 1})

    This feature is particularly useful when there are multiple config files
    in a rigid directory structure, where one file is always going to be in
    the same position in the file hierarchy relative to the files it inherits
    from.  So the relationship between the files is maintained even if the
    root of the directory structure is moved, e.g. between different machines.

    .. _JSON Schema: https://json-schema.org/understanding-json-schema/
    """

    filename = None
    _schemas = None

    def __init__(self, *args, overrides=[], validate=False, schema=None,
                 filename=None, resolve_inherits=False):
        if filename is not None:
            filename = pathlib.Path(normpath(filename))

        # Only applicable when instantiating from a single dict containing
        # inherits; the multiple-argument format is for supporting chained
        # mappings after inherits have already been resolved
        if resolve_inherits and len(args) == 1:
            if isinstance(resolve_inherits, dict):
                resolve_kwargs = resolve_inherits
            else:
                resolve_kwargs = {}

            args = [self.resolve_inherits(args[0], filename,
                                          **resolve_kwargs)]

        # Prevent deep nesting of Configs.  When passed only one map,
        # if it is already a ChainMap just copy its maps.
        # In the more general case flatten all the maps into a single
        # list.  However, we can only do this for Configs with an empty
        # filename, otherwise information about what file the config (or
        # inherited config) was loaded from is lost.
        if (len(args) == 1 and isinstance(args[0], Config)):
            if filename is None:
                filename = args[0].filename
            args = args[0].maps
        elif args:
            args = chain(*(m.maps
                           if isinstance(m, Config) and m.filename is None
                           else [m] for m in args))

        super().__init__(*args, overrides=overrides)
        self._schema = schema
        self.filename = filename
        if validate:
            if isinstance(validate, dict):
                validator_kwargs = validate
            else:
                validator_kwargs = {}
            self.validate(schema=schema, **validator_kwargs)

    @classmethod
    def from_file(cls, filename, validate=True, schema=None,
                  resolve_inherits=True, **kwargs):
        """
        Read the `Config` from a supported JSON-like file, currently either a
        JSON or YAML file.

        Parameters
        ----------
        filename : str or pathlib.Path
            The filename to read from; currently should have either a
            ``.json``, ``.yml``, or ``.yaml`` extension in order to determine
            the correctly determine the file format.  Other formats implemented
            by additional subclasses of
            `~dnadna.utils.serializers.DictSerializer` may by supported in the
            future.
        validate : bool or dict, optional
            Same as the ``validate`` option to the standard `Config`
            constructor (default: `True`).
        schema : str or dict, optional
            Same as the ``schema`` option to the standard `Config`
            constructor.
        resolve_inherits : bool or dict, optional
            Same as the ``resolve_inherits`` option to the standard `Config`
            constructor.
        **kwargs:
            Additional keyword arguments are passed to the underlying
            `load_dict` call.

        Examples
        --------
        >>> from dnadna.utils.config import Config, save_dict
        >>> tmp = getfixture('tmp_path')  # pytest specific
        >>> filename = tmp / 'config.json'
        >>> save_dict({'a': 1}, filename)
        >>> schema = {'properties': {'a': {'type': 'integer'}}}
        >>> config = Config.from_file(filename, schema=schema)
        >>> config['a']
        1
        >>> str(config.filename)
        '...config.json'
        >>> schema['properties']['a']['type'] = 'string'
        >>> Config.from_file(filename, schema=schema)
        Traceback (most recent call last):
        ...
        dnadna.utils.config.ConfigError: error in ".../config.json" at 'a':
        1 is not of type 'string'
        """

        config = load_dict(filename, **kwargs)
        filename = normpath(DictSerializer.to_filename(filename))
        if resolve_inherits:
            config = cls.resolve_inherits(config, filename, **kwargs)
        return cls(config, validate=validate, schema=schema, filename=filename,
                   resolve_inherits=False)

    # TODO: I would like it if config files could specify in them the default
    # schema against which they should validate.  There is no one standard for
    # this, though different proposals have been discussed, e.g. by repurposing
    # the $schema property in data documents:
    # https://github.com/json-schema-org/understanding-json-schema/issues/50
    @classmethod
    @lru_cache_with_dict()
    def from_default(cls, name, validate=True, schema=None,
                     resolve_inherits=True, **kwargs):
        """
        Load one of the default config files from `dnadna.DEFAULTS_DIR`.

        The filename extension may be omitted, so that
        ``Config.from_default('simulation')`` is the same as
        ``Config.from_default('simulation.yml')``; as such that directory
        should not contain any conflicting filenames.

        Remaining keyword arguments are the same as those to `Config`, with the
        exception that the ``schema`` argument may only be a string, since the
        use of `~functools.lru_cache` means all arguments must be *hashable*.

        By default, the default config file is validated against the schema of
        the same name.  For example, the ``Config.from_default('dataset')``
        validates against the ``'dataset'`` schema if it exists.

        Examples
        --------
        >>> from dnadna.utils.config import Config
        >>> Config.from_default('dataset', schema='dataset')
        Config({'data_root': '.', 'dataset_name': 'generic', ...})
        """

        # For now the only files we have in here are .yml
        if name.endswith('.yml'):
            filename = name
            name = pth.splitext(name)[0]
        else:
            filename = name + '.yml'

        if schema is None and name in cls.schemas:
            schema = name

        if validate:
            if not isinstance(validate, dict):
                validate = {}
            # Normally the ConfigValidator has the possibility to modify the
            # config object inplace, but for the default configs we want them,
            # in general, to be "pristine" and unmodified, so we disable the
            # options that would otherwise cause them to be modified, with the
            # exception of filling in default values
            validate.setdefault('resolve_plugins', False)
            validate.setdefault('resolve_filenames', False)
            validate.setdefault('resolve_defaults', True)

        return cls.from_file(pth.join(DEFAULTS_DIR, filename),
                validate=validate, schema=schema,
                resolve_inherits=resolve_inherits, **kwargs)

    @cached_classproperty
    def schemas(cls):
        """
        `dict` mapping the names of built-in schemas to their values.

        Built-in schemas are loaded from any ``.json``, ``.yml``, or ``.yaml``
        files in the directories listed in
        `~dnadna.utils.jsonschema.SCHEMA_DIRS`.

        Schemas in sub-directories of paths in
        `~dnadna.utils.jsonschema.SCHEMA_DIRS` have their subdirectory path
        prepended to the name with ``/``.
        """

        schemas = {}

        for schema_dir in SCHEMA_DIRS:
            for curdir, dirs, files in os.walk(schema_dir):
                for filename in files:
                    base, ext = pth.splitext(filename)
                    dirname = curdir[len(str(schema_dir)) + 1:]
                    name = base
                    if dirname:
                        name = dirname + '/' + base
                    try:
                        schemas[name] = load_dict(pth.join(curdir, filename))
                    except NotImplementedError:
                        # Not a format recognized by the dict serializer
                        continue

        return schemas

    def __getitem__(self, key):
        """
        Propagate the `Config.filename` attribute when accessing nested dicts
        in a `Config`.

        Because `DeepChainedMap.__getitem__` returns a new instance of the
        parent dict's class when accessing a nested dict, we need to propagate
        this attribute if we want to track which `Config` the nested dict came
        from.

        Examples
        --------

        >>> from dnadna.utils.config import Config, DeepChainMap
        >>> c = Config({'a': {'b': 2, 'c': 3}}, filename='foo.json')

        If we just use the base class's ``__getitem__``, accessing ``c['a']``
        returns a new `Config` instance without the ``.filename`` attribute
        set:

        >>> a = DeepChainMap.__getitem__(c, 'a')
        >>> a
        Config({'b': 2, 'c': 3})
        >>> a.filename is None
        True

        This implementation, however, propagates the source file of the nested
        dict as well:

        >>> a = c['a']
        >>> a
        Config({'b': 2, 'c': 3})
        >>> str(a.filename)
        '...foo.json'

        """

        value = super().__getitem__(key)
        if isinstance(value, Config) and value.filename is None:
            value.filename = self.filename

        return value

    def __repr__(self):
        return f'{self.__class__.__name__}({self.dict()})'

    def copy(self, folded=False):
        """
        New `Config` or subclass with a new copy of maps[0] and refs to
        maps[1:].

        If ``folded=True``, however, it returns a copy with all maps folded
        in so that there is only one map in the resulting copy; that is, it is
        equivalent to ``Config(chain_map.dict())``.

        Also copies the filename.
        """

        new = super().copy(folded=folded)
        new.filename = self.filename
        return new

    def to_file(self, filename=None, **kwargs):
        """
        Save the `Config` to the file given by ``filename``.

        If the `Config` was read from a file and has a non-empty ``.filename``
        attribute, it will be written back to the same file by default.

        Additional ``kwargs`` depend on the file format and are passed to the
        appropriate `.DictSerializer` depending on the filename.

        This is equivalent to calling `.save_dict` with ``self``.
        """

        if filename is None:
            if self.filename is not None:
                filename = self.filename
            else:
                raise ValueError(
                    'Config does not have a filename; a filename argument '
                    'must be provided')

        save_dict(self.dict(), filename, **kwargs)

    def validate(self, schema=None, **validator_kwargs):
        """
        Ensure that the configuration is valid:

        * All keys should be strings (for JSON-compatibility).

        * There should not be any 'inherit' keywords: 'inherit' is only used in
          configurations loaded from files, and should have been resolved during
          loading.

        * Finally, if a JSON *schema* is given, validate the config against
          that schema.  The schema may either be a full JSON Schema given as
          a `dict`, or a key into the `Config.schemas` registry.
        """

        if schema is None:
            schema = self._schema

        def validate_keys(d, path=()):
            if 'inherit' in d:
                raise ConfigError(self,
                        'invalid "inherit" keyword found in the config; '
                        'the "inherit" keyword should only be present in '
                        'configs loaded directly from files',
                        path=path)

            for k, v in d.items():
                if not isinstance(k, str):
                    raise ConfigError(self,
                            f'invalid key {k}',
                            'config keys must be strings', path=path)

                if isinstance(v, (dict, Mapping)):
                    validate_keys(v, path=(path + (k,)))

        validate_keys(self)

        if schema is not None:
            if not isinstance(schema, dict):
                schema = self.schemas[schema]

            validator = self._schema_validator_for(schema, validator_kwargs)
            validator.validate(self)

    @classmethod
    def resolve_inherits(cls, config, filename, **kwargs):
        if filename is None:
            config_dir = os.getcwd()
        else:
            config_dir = pth.dirname(filename)

        def resolve_inherits(d, path=()):
            # NOTE: It's important to resolve the inheritence in depth-first
            # order so as to maintain the correct topology
            for k, v in d.items():
                if isinstance(v, (dict, Mapping)):
                    d[k] = resolve_inherits(v, path=(path + (k,)))

            try:
                d = cls._resolve_inherit(d, config_dir, **kwargs)
            except ConfigError as exc:
                raise ConfigError(config, *exc.args[:2], path=path)

            return d

        return resolve_inherits(config)

    @classmethod
    def _resolve_inherit(cls, d, config_dir='', **kwargs):
        """Helper method for `Config.from_file`."""

        if 'inherit' not in d:
            return d

        inherit = d['inherit']
        del d['inherit']

        if isinstance(inherit, str):
            inherit = [inherit]
        elif not isinstance(inherit, list):
            raise ConfigError(d, 'invalid "inherit" keyword found',
                              'it must be either a string or a list')

        # ChainMap prioritizes the left-most map, while our 'inherit' keyword
        # prioritizes the right-most; so we reverse inherit
        parents = tuple(
                cls.from_file(normpath(f, relto=config_dir), **kwargs)
                for f in inherit[::-1])

        return cls(d, *parents)

    def unresolve_inherits(self, config_dir=None, only=None):
        """
        A sort of inversion of `Config.resolve_inherits`.

        This walks through all the chained mappings in this `Config`, and for
        any that have a non-empty ``.filename``, it is removed from the chained
        mappings and replaced with an entry in an ``inherit`` property for the
        top-level mapping.

        This returns a *new* `Config` with all the relevant replacements made.

        Examples
        --------

        >>> from dnadna.utils.config import save_dict
        >>> tmp = getfixture('tmp_path')  # pytest specific
        >>> inherited = tmp / 'inherited.json'
        >>> save_dict({'foo': 'bar', 'baz': 'qux'}, inherited)
        >>> c = Config({'key': {'inherit': str(inherited)}},
        ...            resolve_inherits=True)
        ...
        >>> c
        Config({'key': {'foo': 'bar', 'baz': 'qux'}})
        >>> c2 = c.unresolve_inherits()
        >>> c2
        Config({'key': {'inherit': '...inherited.json'}})
        """

        def unresolve_inherits(config):
            config = self._unresolve_inherit(config, config_dir=config_dir,
                                             only=only)
            for k, v in config.items():
                if isinstance(v, Config):
                    # When using Config.__getitem__, if the value is also a
                    # Config it automatically inherits its filename from the
                    # current Config (unless it was loaded from a different
                    # file to begin with).  So make sure the value's filename
                    # is not the same as the current config's filename
                    if (v.filename and config.filename and
                            v.filename == config.filename):
                        continue

                    config[k] = self._unresolve_inherit(
                        v, config_dir=config_dir, only=only)

            return config

        return unresolve_inherits(self)

    @classmethod
    def _unresolve_inherit(cls, config, config_dir=None, only=None):
        new_maps = []
        inherit = []

        for m in config.maps:
            if not isinstance(m, Config) or not m.filename:
                new_maps.append(m)
                continue

            if only:
                if m in only:
                    inherit.append(str(m.filename))
                else:
                    new_maps.append(m)
            else:
                inherit.append(str(m.filename))

        if config_dir:
            # For inherited configs in the same directory or a subdirectory
            # thereof as the current config's directory, replace the filenames
            # with a simple relative filename.  Otherwise make no such
            # simplifications.
            for idx, path in enumerate(inherit):
                if str(path).startswith(config_dir):
                    inherit[idx] = pth.relpath(path, config_dir)

        if inherit:
            if len(inherit) == 1:
                inherit = inherit[0]
            else:
                inherit = inherit[::-1]

            new_maps.append({'inherit': inherit})

        return cls(*new_maps, filename=config.filename)

    @classmethod
    def _schema_validator_for(cls, schema, validator_kwargs=None):
        if validator_kwargs is None:
            validator_kwargs = {}

        return ConfigValidator(schema, **validator_kwargs)


class ConfigMixIn:
    """
    Mix-in for classes that accept a `Config` object to provide part of their
    attribute namespace.  Makes top-level keys in the `Config` object
    accessible as attributes on instances of the class.

    Includes optional validation of the `Config` against a schema by setting
    the ``config_schema`` class attribute.

    The ``config_schema`` attribute may be either the name of a built-in
    schema, or a JSON Schema object (see `Config.validate`).

    If ``config_default`` is provided, it provides default values for the
    config which can be overridden.

    Examples
    --------

    >>> from dnadna.utils.config import Config, ConfigMixIn
    >>> class MyClass(ConfigMixIn):
    ...     config_schema = {
    ...         'properties': {'a': {'type': 'integer'}}
    ...     }
    ...
    ...     def __init__(self, config, foo=1, validate=True):
    ...         super().__init__(config, validate=validate)
    ...         self.foo = foo
    ...
    >>> config = Config({'a': 1, 'b': 'b'})
    >>> inst = MyClass(config)
    >>> inst.a
    1
    >>> inst.b
    'b'

    Assignment to attributes that are keys in the `Config` also update the
    underlying `Config`.  Such updates are ''not'' validated against the
    schema:

    >>> inst.b = 'c'
    >>> inst.b
    'c'
    >>> inst.config['b']
    'c'

    Validation is performed upon instantiation unless passed ``validate=False``:

    >>> config = Config({'a': 'a', 'b': 'b'})
    >>> inst = MyClass(config)
    Traceback (most recent call last):
    ...
    dnadna.utils.config.ConfigError: error in config at 'a': 'a' is not of
    type 'integer'

    Note, if validation is disabled, then there is no guarantee the object
    will work properly if the config is invalid.
    """

    config_attr = 'config'
    """
    The name of the attribute in which instances of this class store its
    `Config`.  Typically this is just the ``.config`` attribute.
    """

    config_default = {}
    """Default value for the `Config` of instances of this class."""

    config_schema = None
    """
    The schema against which this class should validate its config
    `Config` by default.

    May be either the name of one of the built-in schemas (see
    `Config.schemas`) or a full schema object.
    """

    def __init__(self, config={}, validate=True):
        # It is necessary to perform a copy() here since Config objects have
        # some functionality that make in-place modifications to the underlying
        # dict, so we don't want to accidentally modify if the default.
        filename = config.filename if isinstance(config, Config) else None
        default_config = Config(copy.deepcopy(self.config_default),
                                filename=filename)

        if not isinstance(config, Config):
            config = Config(config)

        default_config.update(config)
        config = default_config

        if validate:
            self.validate_config(config)

        setattr(self, self.config_attr, config)

    @classmethod
    def from_config_file(cls, filename, validate=True, **kwargs):
        """
        Instantiate from a config file.

        This method must be overridden if the subclass takes additional
        ``__init__`` arguments besides ``config`` and ``validate``.
        """

        config = Config.from_file(filename, validate=False, **kwargs)
        return cls(config=config, validate=validate)

    def __getattr__(self, attr):
        """Convenience access for config options via attribute access."""

        if not (attr.startswith('_') or attr == self.config_attr):
            try:
                return getattr(self, self.config_attr)[attr]
            except KeyError:
                raise AttributeError(attr)

        return super().__getattr__(attr)

    def __setattr__(self, attr, value):
        """
        Update self.config if assigning to an attribute that is already found
        in the config; otherwise proceed normally.

        To add new config values that are not already keys in ``self.config``,
        then assign those new values to ``self.config`` directly.
        """

        if attr != self.config_attr and not attr.startswith('_'):
            config = getattr(self, self.config_attr, None)

            if config is not None and attr in config:
                config[attr] = value
                return

        super().__setattr__(attr, value)

    def validate_config(self, config):
        """
        Validate the config file with which this class was initialized.

        By default it validates the config file against the associated
        `ConfigMixin.config_schema` schema, but this method may be overridden
        to add additional semantic validation to the config file that is not
        possible through the schema alone.
        """

        config.validate(schema=self.config_schema)


def _get_config_key_path(config, key):
    """
    Returns the full path to the directory containing the file ``key`` came
    from in a `Config`.

    If the filename is empty or does not exist, then the current working
    directory is assumed by default.

    This is used by `~dnadna.utils.jsonschema.make_config_validator` to provide
    a `Config`-specific implementation of this routine.
    """

    owner = config.get_owner(key)

    if isinstance(owner, Config) and owner.filename is not None:
        return pth.dirname(owner.filename)
    elif config.filename is not None:
        return pth.dirname(config.filename)
    else:
        return '.'


class ConfigValidator(make_config_validator(get_path=_get_config_key_path)):
    """
    A `jsonschema.IValidator` class which supports special validation
    functionality for DNADNA `Config` objects::

    * Recognizes `Config` objects as JSON ``object`` s.

    * Adds new string formats:

        * ``filename``: When a `Config` is loaded from a file, any values in
          the `Config` that are recognized by the specified JSON schema as
          representing a filename are automatically resolved to absolute paths
          relative to the config file's location.  If the filename is already
          an absolute filename it is left alone.  If the config does not have
          an associated filename, relative paths are treated as relative to the
          current working directory.

        * ``filename!``: Same as ``filename`` without the ``!``, but a schema
          validation error is raised if the resulting filename does not exist
          on the filesystem.

        * ``python-module``: The name of a Python module/package that should
          be importable via the standard import system (e.g. ``import
          dnadna``).  If an `ImportError` is raised when trying to import this
          module a schema validation error is raised.

    * If the schema specifies defaults for any properties, those default values
      are filled into the `Config` if it is otherwise missing values for those
      properties.

    * If the schema specifies an ``"errorMsg"`` property, custom error
      messages for validation errors can be provided and shown to users.  See
      `ConfigValidator.validate` for examples.

    Examples
    --------

    >>> from dnadna.utils.config import ConfigValidator, Config
    >>> schema = {
    ...     'type': 'object',
    ...     'properties': {
    ...         'abspath': {'type': 'string', 'format': 'filename'},
    ...         'relpath': {'type': 'string', 'format': 'filename'},
    ...         'nonpath': {'type': 'string'},
    ...         'has_default_1': {'type': 'string', 'default': 'a'},
    ...         'has_default_2': {'type': 'string', 'default': 'b'}
    ...     }
    ... }
    >>> validator = ConfigValidator(schema, posixify_filenames=True)
    >>> config = Config({
    ...     'abspath': '/bar/baz/qux',
    ...     'relpath': 'fred',
    ...     'nonpath': 'barney',
    ...     'has_default_2': 'c'  # override the default
    ... }, filename='/foo/bar/config.json')
    >>> validator.validate(config) is None
    True
    >>> config
    Config({'abspath': '/bar/baz/qux', 'relpath': '/foo/bar/fred',
        'nonpath': 'barney', 'has_default_2': 'c', 'has_default_1': 'a'})
    """

    def validate(self, config, *args, **kwargs):
        """
        Validate the config against the schema and raise a `ConfigError` if
        validation fails.

        This can be enhanced by an extension to JSON-Schema, the
        ``"errorMsg"`` property which can be added to schemas.  All
        JSON-Schema validation errors have a default error message which, while
        technically correct, may not tell the full story to the user.
        For example::

            >>> from dnadna.utils.config import ConfigValidator
            >>> schema = {
            ...     'type': 'object',
            ...     'properties': {
            ...         'loss_weight': {
            ...             'type': 'number',
            ...             'minimum': 0,
            ...             'maximum': 1
            ...         }
            ...     }
            ... }
            ...
            >>> validator = ConfigValidator(schema)
            >>> validator.validate({'loss_weight': 2.0})
            Traceback (most recent call last):
            ...
            dnadna.utils.config.ConfigError: error in config at 'loss_weight':
            2.0 is greater than the maximum of 1

        However, if the schema has an ``"errorMsg"`` for ``"loss_weight"`` we
        can give a more descriptive error.  The value of ``"errorMsg"`` may
        also include the following template variables:

            * ``{property}`` the name of the property being validated
            * ``{value}`` the value of the property being validated
            * ``{validator}`` the name of the validation being performed (e.g.
              ``'minimum'``
            * ``{validator_value}`` the value associated with the validator
              (e.g. ``1`` for ``"minimum": 1``)

        Let's try adding a more descriptive error message for validation errors
        on ``"loss_weight"``::

            >>> schema = {
            ...     'type': 'object',
            ...     'properties': {
            ...         'loss_weight': {
            ...             'type': 'number',
            ...             'minimum': 0,
            ...             'maximum': 1,
            ...             'errorMsg':
            ...                 '{property} must be a floating point value '
            ...                 'between 0.0 and 1.0 inclusive (got {value})'
            ...         }
            ...     }
            ... }
            ...
            >>> validator = ConfigValidator(schema)
            >>> validator.validate({'loss_weight': 2.0})
            Traceback (most recent call last):
            ...
            dnadna.utils.config.ConfigError: error in config at 'loss_weight':
            loss_weight must be a floating point value between 0.0 and 1.0
            inclusive (got 2.0)

        .. note::

            In the above example it would have just as easy to explicitly write
            ``loss_weight`` in the error message instead of the template
            variable ``{property}``, but the latter case is more reusable (e.g.
            in definitions) and was used in this example just for illustration
            purposes

        The ``"errorMsg"`` property may also be an object/dict, mapping the
        names of validators to error messages specific to a validator.
        If it contains the validator ``"default"``, the default message is
        used as a fallback for any other validators that do not have a specific
        error message.  For example, the following schema requires an array
        of at least one unique string.  It provides a custom error message for
        ``minItems``, but not for the other properties::

            >>> schema = {
            ...     'type': 'array',
            ...     'items': {'type': 'string'},
            ...     'minItems': 1,
            ...     'uniqueItems': True,
            ...     'errorMsg': {
            ...         'default':
            ...             'must be an array of at least 1 unique string',
            ...         'minItems':
            ...             'array was empty (it must have at least 1 item)'
            ...     }
            ... }
            ...
            >>> validator = ConfigValidator(schema)
            >>> validator.validate([1, 2])
            Traceback (most recent call last):
            ...
            dnadna.utils.config.ConfigError: error in config at '0': must be an
            array of at least 1 unique string
            >>> validator.validate(['a', 'a'])
            Traceback (most recent call last):
            ...
            dnadna.utils.config.ConfigError: error in config: must be an array
            of at least 1 unique string
            >>> validator.validate([])
            Traceback (most recent call last):
            ...
            dnadna.utils.config.ConfigError: error in config: array was empty
            (it must have at least 1 item)
            >>> validator.validate(['a', 'b', 'c'])
        """

        try:
            return super().validate(config, *args, **kwargs)
        except jsonschema.ValidationError as exc:
            # if the error came from a sub-schema in a one/all/anyOf then the
            # full path must also include the parent schema path; this can
            # get a little confusing depending on the nesting, but in general
            # the longest path is always the best one it seems
            parent = exc
            path = ()
            while parent is not None:
                if len(parent.path) > len(path):
                    path = tuple(parent.path)
                parent = parent.parent
            raise ConfigError(config, exc.message, path=path)
