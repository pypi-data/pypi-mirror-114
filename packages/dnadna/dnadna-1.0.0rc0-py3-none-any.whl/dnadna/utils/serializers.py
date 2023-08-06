"""
Implements generic utilities for serialization/deserialization of native
Python objects to/from file formats to which they can be serialized.
"""


import abc
import collections
import json
import os.path as pth
import pathlib
from collections.abc import Sequence, Set as SetABC
from contextlib import nullcontext
from functools import partial, wraps
from typing import List, Set

import yaml

from .decorators import classproperty
from .yaml import YAMLDumper


__all__ = ['GenericSerializer', 'DictSerializer', 'JSONSerializer',
           'YAMLSerializer']


# TODO: Make serializers into a Pluggable
class GenericSerializer(metaclass=abc.ABCMeta):
    """
    Base class for serializers/deserializers for a specific object type or
    types.

    A `classmethod` ``match_filename()`` is used to match a given file (based
    on its filename) to a given serializer.  File-like objects are also
    supported but they must have either a ``.name`` or ``.filename`` attribute
    in order to guess the correct implementation to use.

    This class should be subclassed for serializers of specific object types.
    Subclasses should define values for the `~GenericSerializer.types` and
    `~GenericSerializer.extensions` attributes at a minimum.

    If one object type supports multiple serialization formats, it is good
    practice to create a base class which instantiates the ``types`` attribute,
    and then further base classes for each supported format.  See for example
    the `DictSerializer` base class, and its format-specific subclasses
    `JSONSerializer` and `YAMLSerializer`.  While the format-specific
    serializers may be used directly, a `dict` object can be loaded or saved
    using the `DictSerializer` class directly, since it will automatically
    guess the correct format to use based on the filename.

    .. todo::

        For open file-like objects we could also support checking the format
        by peeking at the file contents and matching against a file signature
        (e.g. ``137 80 78 71 13 10 26 10`` for PNG files).
    """

    @abc.abstractproperty
    def types(self) -> Set[type]:
        """
        Python types that can be serialized by subclasses of this serializer.
        """

    # NOTE: This is implemented without using a decorator, since otherwise
    # pytest will not locate the doctest.
    @classmethod
    def _extensions(cls):
        """
        Filename extensions recognized by this serializer.

        .. note::

            Dotted extensions must include the dot, i.e. ``[".json"]``.  This
            is otherwise not assumed since it could support filename suffixes
            that do not include a dot (although in practice most do of course).

        Examples
        --------

        >>> from dnadna.utils.serializers import DictSerializer
        >>> DictSerializer.extensions
        ['.json', '.yaml', '.yml']
        """

        # The default implementation returns a sorted list of all extensions
        # supported by all sub-classes.
        extensions = set()

        cls_stack = [cls]
        while cls_stack:
            cls = cls_stack.pop()
            if isinstance(cls.__dict__.get('extensions'), (Sequence, SetABC)):
                extensions.update(cls.extensions)

            for subcls in cls.__subclasses__():
                cls_stack.append(subcls)

        return sorted(extensions)

    @classproperty
    @abc.abstractmethod
    def extensions(cls) -> List[str]:
        return cls._extensions()

    language = None
    """
    Name of the language/format saved/loaded by this serializer.  This is used
    primarily for introspection purposes, such as applying proper code
    highlighting to a file.

    Generally not applicable for binary file formats which do not have a
    useful textual display.
    """

    binary = False
    """
    If True, files are read and written in binary mode by this serializer.
    """

    def __init_subclass__(cls):
        """
        Automatically wrap load and save methods defined on subclasses with
        additional functionality.
        """

        for method_name in ['load', 'save']:
            if method_name not in cls.__dict__:
                continue

            method = cls.__dict__[method_name]
            if not isinstance(method, classmethod):
                raise TypeError(
                    f'{cls.__name__}.{method_name} must be a classmethod')

            make_wrapper = getattr(cls, f'_make_{method_name}_wrapper')
            setattr(cls, method_name, make_wrapper(method.__func__))

    @classmethod
    def _make_load_wrapper(cls, func):
        """Creates the automatic wrapper around the ``load`` method."""

        mode = 'r' + ('b' if cls.binary else '')

        @classmethod
        @wraps(func)
        @filename_or_obj(arg=1, mode=mode)
        def load(cls, filename, **kwargs):
            return cls._check_type(func(cls, filename, **kwargs), 'load')

        return load

    @classmethod
    def _make_save_wrapper(cls, func):
        """Creates the automatic wrapper around the ``save`` method."""

        mode = 'w' + ('b' if cls.binary else '')

        @classmethod
        @wraps(func)
        @filename_or_obj(arg=2, mode=mode)
        def save(cls, obj, filename, **kwargs):
            return func(cls, cls._check_type(obj, 'save'), filename, **kwargs)

        return save

    @classmethod
    def _check_type(cls, obj, method):
        """
        Checks the given ``obj`` against the types supported by ``cls.types``.

        Returns ``obj`` if it passes the test, or raises a `ValueError`
        otherwise.

        Examples
        --------

        >>> from dnadna.utils.serializers import GenericSerializer
        >>> class MySerializer(GenericSerializer):
        ...     types = set([dict, set])
        >>> MySerializer._check_type({}, 'load')
        {}
        >>> MySerializer._check_type(set(), 'load')
        set()
        >>> MySerializer._check_type([], 'load')
        Traceback (most recent call last):
        ...
        ValueError: object [] returned by MySerializer.load is not one of the
        allowed types specified by MySerializer.types = set([dict, set])
        >>> MySerializer._check_type([], 'save')
        Traceback (most recent call last):
        ...
        ValueError: object [] passed to MySerializer.save is not one of the
        allowed types specified by MySerializer.types = set([dict, set])
        """

        for type_ in cls.types:
            if isinstance(obj, type_):
                return obj
        else:
            if method == 'load':
                action = 'returned by'
            elif method == 'save':
                action = 'passed to'
            else:
                raise RuntimeError(
                    "method argument must be either 'load' or 'save'")

            types = 'set([{}])'.format(
                    ', '.join(sorted(_format_type(t) for t in cls.types)))

            raise ValueError(
                f'object {obj} {action} {cls.__name__}.{method} is not one of '
                f'the allowed types specified by {cls.__name__}.types = '
                f'{types}')

    @classmethod
    def serializer_for(cls, filename):
        """
        Given a filename, return the first `GenericSerializer` subclass that
        handles this file, based on the result of its
        `~GenericSerializer.match_filename` method.

        Examples
        --------

        Here we use `DictSerializer` as a concrete example:

        >>> from dnadna.utils.config import DictSerializer
        >>> DictSerializer.serializer_for('foo.json')
        <class 'dnadna.utils.serializers.JSONSerializer'>
        >>> DictSerializer.serializer_for('bar.yaml')
        <class 'dnadna.utils.serializers.YAMLSerializer'>
        >>> DictSerializer.serializer_for('unknown')
        Traceback (most recent call last):
        ...
        NotImplementedError: no known serializer for the given filename:
        "unknown"
        """

        for subcls in cls.__subclasses__():
            if subcls.match_filename(filename):
                return subcls

        raise NotImplementedError(
            f'no known serializer for the given filename: "{filename}"')

    @staticmethod
    def to_filename(filename_or_obj):
        """
        Utility function for use with the `filename_or_obj` decorator.

        If ``filename_or_obj`` is already a `str` or `pathlib.Path`, return it.
        Otherwise it checks some heuristics for possible filename attributes on
        file-like objects.  If all else fails it still returns the original
        file-like object.
        """

        if isinstance(filename_or_obj, (str, pathlib.Path)):
            return filename_or_obj
        elif hasattr(filename_or_obj, 'filename'):
            return filename_or_obj.filename
        elif hasattr(filename_or_obj, 'name'):
            return filename_or_obj.name
        else:
            return filename_or_obj

    @classmethod
    def match_filename(cls, filename):
        """
        Given a filename, return True if the file is handled by a given
        `GenericSerializer` subclass.

        The default implementation matches the filename against the class's
        `~GenericSerializer.extensions` list.
        """

        filename = cls.to_filename(filename)
        if not isinstance(filename, (str, pathlib.Path)):
            # Can't work on something without a filename
            return False

        return pth.splitext(filename)[1] in cls.extensions

    @abc.abstractclassmethod
    def load(cls, filename, **kwargs):
        """
        Read the file given by filename and return its deserialized contents.

        Additional keyword arguments are passed to individual subclass loaders
        depending on the file type, and may not be meaningful unless loading a
        file in a specific, known serialization format.

        Subclasses should override this method to implement the details of
        deserializing specific file formats.

        .. note::

            Subclasses which implement this method should ensure that it is
            decorated as a `classmethod`.  The method will also be
            automatically wrapped in the `filename_or_obj` decorator, which
            checks whether the ``filename`` argument is a filename or file-like
            object.  It is also wrapped in a type-checker which ensures the
            returned object is one of the types supported by the serializer.

        .. todo::

            Perhaps ``**kwargs`` should be processed to only pass the relevant
            keyword arguments supported by the deserializer that will be used.
        """

        try:
            serializer = cls.serializer_for(filename)
        except NotImplementedError:
            raise NotImplementedError(
                f'no known deserializer for the given filename: "{filename}"')

        return serializer.load(filename, **kwargs)

    @abc.abstractclassmethod
    def save(cls, obj, filename, **kwargs):
        """
        Serialize the given object to the given filename.

        The serialization format is determined automatically by the filename.

        Additional keyword arguments are passed to individual subclass's save
        methods depending on the file type, and their meaning depends on the
        target serialization format.

        Subclasses should override this method to implement the details of
        serializing specific file formats.

        .. note::

            Subclasses which implement this method should ensure that it is
            decorated as a `classmethod`.  The method will also be
            automatically wrapped in the `filename_or_obj` decorator, which
            checks whether the ``filename`` argument is a filename or file-like
            object.  It is also wrapped in a type-checker which ensures the
            passed object is one of the types supported by the serializer.

        .. todo::

            Perhaps ``**kwargs`` should be processed to only pass the relevant
            keyword arguments supported by the serializer that will be used.
        """

        return cls.serializer_for(filename).save(obj, filename, **kwargs)


def filename_or_obj(func=None, *, arg=0, mode='r'):
    """
    Decorator for functions which take as one of its arguments either a
    filename or an already open file-like object.

    If given a filename as a string or `pathlib.Path`, it opens the file
    (optionally with the given ``mode``) and closes the file when the wrapped
    function exits.

    If given an object of any either type (which is assumed to be duck-typeable
    as a file object), the object is not closed when the wrapped function
    exits; this is assumed to be the responsibility of the caller.

    By default, the ``file_or_obj`` argument is assumed to be the first
    positional argument of the wrapper function, but the optional ``arg``
    argument to the decorate can accept either the index of a positional
    argument, or an argument name.  Thus for most method types, ``arg`` should
    be ``1`` or greater to skip the ``self`` argument.

    .. todo::

        Add a usage example for this decorator.
    """

    if func is None:
        return partial(filename_or_obj, arg=arg, mode=mode)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if isinstance(arg, int):
            args = arg_source = list(args)
        elif isinstance(arg, str):
            arg_source = kwargs

        file_or_obj = arg_source[arg]

        if isinstance(file_or_obj, (str, pathlib.Path)):
            fileobj = ctx = open(file_or_obj, mode=mode)
        else:
            ctx = nullcontext(file_or_obj)
            fileobj = file_or_obj

        arg_source[arg] = fileobj

        with ctx:
            return func(*args, **kwargs)

    return wrapper


class DictSerializer(GenericSerializer):
    """
    Base class for serializers/deserializers of JSON-like nested dictionary
    data structures.

    A `classmethod` ``match_filename()`` is used to match a give file (based on
    its filename) to a given serializer.
    """

    types = set([dict, collections.abc.Mapping])
    """
    Types supported by `DictSerializer` (just `dict` and
    `collections.abc.Mapping` for now).
    """

    language = None
    """
    Name of the language / format saved/loaded by this serializer.  This is
    used primarily for introspection purposes, such as applying proper code
    highlighting to a file.
    """


class JSONSerializer(DictSerializer):
    extensions = ['.json']
    language = 'json'

    @classmethod
    def load(cls, filename_or_obj, **kwargs):
        return json.load(filename_or_obj, **kwargs)

    @classmethod
    def save(cls, obj, filename_or_obj, **kwargs):
        json.dump(obj, filename_or_obj, **kwargs)


class YAMLSerializer(DictSerializer):
    extensions = ['.yml', '.yaml']
    language = 'yaml'

    @classmethod
    def load(cls, filename_or_obj, **kwargs):
        return yaml.safe_load(filename_or_obj, **kwargs)

    # TODO: Consider adding built-in support for saving commented YAML files à
    # la save_dict_annotated
    @classmethod
    def save(cls, obj, filename_or_obj, **kwargs):
        kwargs.setdefault('Dumper', YAMLDumper)
        yaml.dump(obj, filename_or_obj, **kwargs)


def _format_type(cls):
    """
    Formats a type/class as a string based on its name and module.

    Examples
    --------

    >>> from dnadna.utils.serializers import _format_type, GenericSerializer
    >>> _format_type(dict)
    'dict'
    >>> _format_type(GenericSerializer)
    'dnadna.utils.serializers.GenericSerializer'
    """

    if cls.__module__ == 'builtins':
        return cls.__qualname__
    else:
        return f'{cls.__module__}.{cls.__qualname__}'
