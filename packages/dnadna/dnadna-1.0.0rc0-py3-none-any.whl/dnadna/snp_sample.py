"""
Implements the `~dnadna.snp_sample.SNPSample` class, a generic container for
DNADNA's SNP data, consisting of the SNP matrix itself and the SNP positions
array.  It includes built-in methods for reading SNP data from different file
formats, as well as writing it out to different formats.

* Classes for reading and writing `SNPSample` objects to/from different file
  formats and data representations.  These are generally not used directly, but
  rather through methods on the `SNPSample` class itself using the
  ``SNPSample.to/from_<format>`` methods.  The available formats can be listed
  like:

  >>> from dnadna.snp_sample import SNPSample
  >>> SNPSample.converter_formats
  ['dict', 'npz']

  * `DictSNPConverter` - converts `SNPSample` to/from a JSON-serializable
    `dict`-based format.

  * `NpzSNPConverter` - serializes and deserializes an `SNPSample` to/from an
    NPZ file.

  Additional converters can be registered simply by defining subclasses of
  `SNPConverter` (make sure the modules the classes are in are actually
  imported).
"""


import abc
import os.path as pth
import pathlib
import types
import zipfile
from itertools import chain

import numpy as np
import torch

from .utils.decorators import (cached_classproperty, cached_property,
        classproperty)
from .utils.misc import flatten, indent
from .utils.serializers import GenericSerializer
from .utils.tensor import to_tensor


class _SNPSampleMeta(type):
    """Metaclass for `SNPSample` implementing some automatic functionality."""

    def __getattr__(cls, attr):
        """
        Implements automatic generation of SNPSample.to/from_<format>
        methods.
        """

        formats = {c.format: c for c in SNPConverter.converters
                   if isinstance(c.format, str)}

        if '_' in attr:
            method, format = attr.split('_', 1)
            if method not in ['to', 'from'] or format not in formats:
                raise AttributeError(attr)

            return getattr(formats[format], 'convert_' + method)

        raise AttributeError(attr)

    @property
    def format_methods(cls):
        formats = [c.format for c in SNPConverter.converters
                   if isinstance(c.format, str)]

        return list(flatten([f'to_{format}', f'from_{format}']
                             for format in formats))

    def __dir__(cls):
        return sorted(super().__dir__() + cls.format_methods)


class SNPSample(metaclass=_SNPSampleMeta):
    """
    Class representing a single SNP sample from a population.

    Consists of an boolean array of shape ``(n, m)`` where ``n`` is the
    number of individuals in the sample and ``m`` is the number of SNPs, along
    with a 1-D array of shape ``(m,)`` of SNP positions in the nucleotide.

    For now positions are assumed to be normalized to the range ``[0.0, 1.0]``
    of absolute positions.

    .. todo::

        Other normalizations are possible, so we may want a way of specifying
        how the input positions have been normalized, and either automatically
        re-normalize them or keep them as-is.

    The SNP and pos arrays can be given in any type that can be easily
    converted to a `torch.Tensor`.

    Parameters
    ----------
    snp : `list`, `numpy.ndarray`, `torch.Tensor`, optional
        The SNP matrix.  Must be provided unless a ``loader`` is provided.
    pos : `list`, `numpy.ndarray`, `torch.Tensor`, optional
        The positions array.  Must be provided unless a ``loader`` is provided.
    pos_format : `dict`, optional
        A `dict` specifying how the positions are formatted.  It can currently
        contain up to 4 keys (see the ``position_format`` property in the
        :ref:`dataset schema <schema-dataset>`).  If not specified, the
        default assumption is ``{'distance': False, 'circular': False,
        'normalized': False}``, though it will be inferred whether or not the
        positions are normalized if not otherwise specified.
    path : object, optional
        The path from which this `SNPSample` was loaded.  Typically this will
        be a filesystem path as a `str` or `pathlib.Path`, but it may be
        anything depending on how the `SNPSample` as loaded.  This is included
        for informational purposes only.
    copy : bool, optional
        If `True` the data underlying ``snp`` and ``pos`` arguments are always
        copied.  If `False` (default) a copy will be avoided *if possible*, but
        may still be necessary (e.g. when converting a Python `list` to
        `torch.Tensor`, or when the dtype needs to be converted).
    loader : `SNPLoader`, optional
        If provided, the ``snp`` and/or ``pos`` arguments may be omitted.  A
        loader allows lazy-loading of SNP matrix data on-demand.  See the
        documentation for `SNPLoader`.
    validate : bool, optional
        Validate the formats of the SNP and position tensors.  This can be
        disabled for efficiency if you are sure they are already in the correct
        format.  When ``validate=False`` make sure also to supply a correct
        ``pos_format`` argument (default: True).

    Examples
    --------

    >>> from dnadna.snp_sample import SNPSample
    >>> snp = [[1, 0, 0, 1], [0, 1, 1, 0]]
    >>> pos = [0.2, 0.4, 0.6, 0.8]
    >>> samp = SNPSample(snp, pos)
    >>> samp.snp
    tensor([[1, 0, 0, 1],
            [0, 1, 1, 0]], dtype=torch.uint8)
    >>> samp.pos
    tensor([0.2000, 0.4000, 0.6000, 0.8000], dtype=torch.float64)

    The SNP and position arrays can be combined into a single array in one of
    two formats, ``.product`` which takes the product of the two arrays, with
    the position array multiplied along the individuals axis:

    >>> samp.product
    tensor([[0.2000, 0.0000, 0.0000, 0.8000],
            [0.0000, 0.4000, 0.6000, 0.0000]], dtype=torch.float64)

    Or the two arrays can be simply concatenated into a ``(n + 1, m)`` array,
    with the first row containing the positions and the remaining rows
    containing the SNPs:

    >>> samp.concat
    tensor([[0.2000, 0.4000, 0.6000, 0.8000],
            [1.0000, 0.0000, 0.0000, 1.0000],
            [0.0000, 1.0000, 1.0000, 0.0000]], dtype=torch.float64)

    Or just ``.tensor`` returns one or the other depending on the value of the
    ``.tensor_format`` attribute:

    >>> bool((samp.concat == samp.tensor).all())
    True
    >>> samp2 = SNPSample(samp.snp, samp.pos, tensor_format='product')
    >>> bool((samp2.product == samp2.tensor).all())
    True

    The optional ``path`` element (`None` by default) can give a data
    source-specific path from which the sample was read (typically a
    filename):

    >>> SNPSample(snp, pos, path='one_event/scenario_000/one_event_000_0.npz')
    SNPSample(
        snp=tensor([[1, 0, 0, 1],
                    [0, 1, 1, 0]], dtype=torch.uint8),
        pos=tensor([0.2000, 0.4000, 0.6000, 0.8000], dtype=torch.float64),
        pos_format={'normalized': True},
        path='one_event/scenario_000/one_event_000_0.npz'
    )
    """

    DEFAULT_POS_FORMAT = {
        'distance': False,
        'normalized': False,
        'circular': False
    }
    TENSOR_FORMATS = ('concat', 'product')
    DEFAULT_TENSOR_FORMAT = 'concat'

    def __init__(self, snp=None, pos=None, pos_format=None, tensor_format=None,
                 path=None, copy=False, loader=None, validate=True):
        # TODO: Do we want to be able to specify the dtype for the positions?
        # How will we determine that?
        if loader is None and (snp is None or pos is None):
            raise TypeError(
                'both the snp and pos arguments must be provided if a loader'
                'is not provided')

        if snp is not None:
            snp = to_tensor(snp, dtype=torch.uint8, copy=copy)

        if pos is not None:
            pos = to_tensor(pos, copy=copy)

            if pos.dim() > 1:
                # On a 1x1 tensor torch.squeeze() actually makes it
                # 0-dimensional which we don't want
                pos = pos.squeeze()

        if validate and snp is not None and pos is not None:
            # Validate them now, otherwise we wait until all the data is loaded
            # from the loader
            pos_format = self._validate(snp, pos, pos_format)

        self._snp = snp
        self._pos = pos
        self._pos_format = pos_format
        self._path = path
        self._tensor_format = tensor_format or self.DEFAULT_TENSOR_FORMAT
        self._loader = loader

        assert self._tensor_format in self.TENSOR_FORMATS, (
                f'tensor_format must be one of {self.TENSOR_FORMATS}')

    def __dir__(self):
        return sorted(super().__dir__() + self.__class__.format_methods)

    @property
    def snp(self):
        """The SNP matrix."""

        if self._snp is None:
            # This will only be called if the snp argument was not provided
            # upon initialization
            self._snp = self._data[0]

        return self._snp

    @property
    def pos(self):
        """The positions array."""

        if self._pos is None:
            self._pos = self._data[1]

        return self._pos

    @cached_property
    def shape(self):
        """The number of SNPs and number of individuals as a tuple."""

        if self._snp is not None:
            return (self._snp.shape[0], self._snp.shape[1])
        else:
            return self._loader.get_shape()

    @property
    def n_snp(self):
        """The number of SNPs in the sample."""

        return self.shape[1]

    @property
    def n_indiv(self):
        """The number of individuals in the sample."""

        return self.shape[0]

    @property
    def tensor(self):
        """
        Either `SNPSample.concat` or `SNPSample.product` depending on the value
        of `SNPSample.tensor_format`.
        """

        return getattr(self, self.tensor_format)

    @property
    def product(self):
        """
        The product of the ``pos`` array with the ``snp`` array.

        The result has the same dtype as the ``pos`` array.
        """

        return self.snp.to(self.pos.dtype).mul_(self.pos)

    @property
    def concat(self):
        """
        The concatenation of the ``pos`` array with the ``snp`` array.

        The result has the same dtype as the ``pos`` array.
        """

        return torch.cat((self.pos.unsqueeze(0), self.snp.to(self.pos.dtype)))

    @property
    def pos_format(self):
        """
        A `dict` specifying how the positions are formatted.

        It can currently contain up to 4 keys (see the ``position_format``
        property in the :ref:`dataset schema <schema-dataset>`).  If not
        specified, the default assumption is ``{'distance': False, 'circular':
        False, 'normalized': False}``, though it will be inferred whether or
        not the positions are normalized if not otherwise specified.
        """

        if self._pos_format is None:
            return self.DEFAULT_POS_FORMAT.copy()
        else:
            return self._pos_format

    @property
    def full_pos_format(self):
        """
        Return the user-provided ``pos_format`` merged with the default value.
        """

        full_pos_format = self.DEFAULT_POS_FORMAT.copy()
        full_pos_format.update(self.pos_format)
        return full_pos_format

    @property
    def tensor_format(self):
        """
        The default format for `SNPSample.tensor` on this `SNPSample`.

        If ``'concat'``, it is equivalent to `SNPSample.concat`, and if
        ``'product'`` it is equivalent to `SNPSample.product` (default:
        ``'concat'``).
        """

        return self._tensor_format

    @property
    def path(self):
        """
        The path from which this `SNPSample` was loaded.

        Typically this will be a filesystem path as a `str` or `pathlib.Path`,
        but it may be anything depending on how the `SNPSample` as loaded.
        This is included for informational purposes only.
        """

        return self._path

    @property
    def loader(self):
        """The `SNPLoader` used for lazy-loading this `SNPSample`, if any."""

        return self._loader

    @classmethod
    def from_file(cls, filename_or_obj, **kwargs):
        """
        Read an `SNPSample` from a file using one of the known `SNPSerializer`
        types.  The serialization format will be determined by the filename.

        In the case of file-like objects it must have a ``.name`` or
        ``.filename`` attribute in order to guess the format.

        .. todo::

            It would be a good idea to use actual file format analysis to
            determine the file type instead of just rely on the filename; for
            now this is simpler and all that's needed in most cases.

        For a usage example, see `SNPSample.to_file`.
        """

        return SNPSerializer.load(filename_or_obj, **kwargs)

    def to_file(self, filename_or_obj, **kwargs):
        """
        Serialize the `SNPSample` to a file or file-like object.

        The appropriate serializer will be determined by the filename, as in
        `SNPSample.from_file`.

        Examples
        --------

        >>> import io
        >>> from dnadna.snp_sample import SNPSample
        >>> out = io.BytesIO()

        A filename ending with ``.npz`` indicates the NPZ-based DNADNA format:

        >>> out.name = 'out.npz'
        >>> snp = SNPSample([[0, 1], [0, 0]], [0.1, 0.2])
        >>> snp.to_file(out)
        >>> _ = out.seek(0)
        >>> snp2 = SNPSample.from_file(out)
        >>> snp == snp2
        True
        """

        return SNPSerializer.save(self, filename_or_obj, **kwargs)

    @classproperty
    def converter_formats(cls):
        """
        List the names of all converter formats available for `SNPSample`.

        For each format in this list, there is are associated
        ``SNPSample.to_<format>`` and ``SNPSample.from_<format>`` methods
        available (where the latter is a `classmethod`).

        Examples
        --------

        >>> from dnadna.snp_sample import SNPSample
        >>> SNPSample.converter_formats
        ['dict', 'npz']
        >>> SNPSample.from_dict
        <bound method DictSNPConverter.from_dict of
        <class 'dnadna.snp_sample.DictSNPConverter'>>
        >>> snp = SNPSample([[1, 0], [0, 1]], [0, 1])
        <bound method DictSNPConverter.to_dict of SNPSample(
            snp=tensor([[1, 0, 1],
                        [0, 1, 0],
                        [0, 1, 0]], dtype=torch.uint8),
            pos=tensor([1, 2, 3],
            tensor_format='concat')
        )>

        As you can see in the above examples, the converter methods are
        actually defined on the `DictSNPConverter` class, but they are made
        available directly as methods on `SNPSample`.

        See also `dir` of `SNPSample` for a list of methods:

        >>> dir(SNPSample)
        [...from_dict, from_npz, ..., to_dict, to_npz...]
        """

        return SNPConverter.formats

    @cached_property
    def _data(self):
        """
        Returns the SNP matrix and pos arrays from the loader if they were not
        already set.
        """

        snp, pos = self._loader.get_data()
        self._pos_format = self._validate(snp, pos, self._pos_format)
        return snp, pos

    def __getattr__(self, attr):
        """
        Implement lookup of the ``from/to_<format>`` methods on `SNPSample`
        instances.

        This just goes directly through the metaclass for this, but we also
        have to implement it at the instance level.  For plain functions we
        must still bind them to the instance.

        Tests
        -----

        Regression test: Ensure that if a property which is defined on the
        class bubbles up an `AttributeError`, then an `AttributeError` is still
        raised for that property as opposed to a more obscure error.

        >>> from dnadna.snp_sample import SNPSample
        >>> class BrokenSNPSample(SNPSample):
        ...     @property
        ...     def snp(self):
        ...         return self._does_not_exist
        ...
        >>> s = BrokenSNPSample([[0, 1], [1, 0]], [0, 1])
        >>> s.snp
        Traceback (most recent call last):
        ...
        AttributeError: snp
        """

        method = type(self.__class__).__getattr__(self.__class__, attr)

        if not hasattr(method, '__self__'):
            # It is not yet a bound method
            method = types.MethodType(method, self)

        return method

    def __repr__(self):
        cls_name = self.__class__.__name__

        # NOTE: Ensure that self.snp and self.pos are loaded before
        # formatting pos_format, since self.pos_format can be set when
        # lazy-loading self.snp or self.pos
        snp = indent(repr(self.snp), 8, first=False)
        pos = indent(repr(self.pos), 8, first=False)
        pos_format = (f',\n    pos_format={self.pos_format}'
                      if self.full_pos_format != self.DEFAULT_POS_FORMAT
                      else '')
        tensor_format = (f',\n    tensor_format={self.tensor_format}'
                         if self.tensor_format != self.DEFAULT_TENSOR_FORMAT
                         else '')
        path = f',\n    path={self.path!r}' if self.path is not None else ''
        return (f'{cls_name}(\n'
                f'    snp={snp},\n'
                f'    pos={pos}'
                f'{pos_format}{tensor_format}{path}\n)')

    def __eq__(self, other):
        """
        Two `SNPSample`s are equal if their SNP and position arrays are equal.

        This does not take into account other possible isomorphisms.

        Examples
        --------

        >>> from dnadna.snp_sample import SNPSample
        >>> sample1 = SNPSample([[1, 0], [0, 1]], [0.2, 0.4])
        >>> sample2 = SNPSample([[1, 1], [1, 0]], [0.3, 0.5])
        >>> sample1 == sample1
        True
        >>> sample1 == sample2
        False
        """

        if not isinstance(other, SNPSample):
            return False

        return bool((self.pos == other.pos).all() and
                    (self.snp == other.snp).all())

    def copy(self):
        """
        Creates a copy of this `SNPSample`, including copying the ``snp`` and
        ``pos`` tensors.
        """

        return self.copy_with(copy=True)

    def copy_with(self, snp=None, pos=None, pos_format=None,
                  tensor_format=None, path=None, copy=False,
                  validate=None):
        """
        Creates a copy of this `SNPSample` instance with any of the fields
        replaced.

        If ``copy=True`` the storage for the ``snp`` and ``pos`` tensors is
        also copied; otherwise the same storage is referenced in the new
        `SNPSample`.
        """

        # Only re-validate if any of the SNP/pos matrices have changed or the
        # position format has changed
        if validate is None:
            validate = (snp is not None or pos is not None or
                        pos_format is not None)

        return self.__class__(
            snp if snp is not None else self.snp,
            pos if pos is not None else self.pos,
            pos_format if pos_format is not None else self.pos_format.copy(),
            tensor_format if tensor_format is not None else self.tensor_format,
            path if path is not None else self.path,
            copy=copy,
            validate=validate
        )

    def _validate(self, snp, pos, pos_format=None):
        """
        Determine the position format and check that it's consistent with
        the given positions array.

        If the ``'normalized'`` keyword is not otherwise specified we can
        infer it by the data (i.e. if all values are < 1).

        Examples
        --------

        Several possible errors can be raised if the positions are not in a
        consistent format.  By default, positions are assumed to be
        non-normalized, non-circular absolute positions:

        >>> from dnadna.snp_sample import SNPSample
        >>> sample = SNPSample([[0, 1, 0], [1, 0, 1]], [1, 2, 3])
        >>> sample
        SNPSample(
            snp=tensor([[0, 1, 0],
                        [1, 0, 1]], dtype=torch.uint8),
            pos=tensor([1, 2, 3])
        )

        If the positions are not in the default format this is displayed
        explicitly:

        >>> sample = SNPSample([[0, 1, 0], [1, 0, 1]], [0.1, 0.2, 0.3],
        ...                    pos_format={'distance': True,
        ...                                'normalized': True})
        >>> sample
        SNPSample(
            snp=tensor([[0, 1, 0],
                        [1, 0, 1]], dtype=torch.uint8),
            pos=tensor([0.1000, 0.2000, 0.3000], dtype=torch.float64),
            pos_format={'distance': True, 'normalized': True}
        )

        If the positions are normalized this will be inferred:

        >>> sample = SNPSample([[0, 1, 0], [1, 0, 1]], [0.1, 0.2, 0.3])
        >>> sample
        SNPSample(
            snp=tensor([[0, 1, 0],
                        [1, 0, 1]], dtype=torch.uint8),
            pos=tensor([0.1000, 0.2000, 0.3000], dtype=torch.float64),
            pos_format={'normalized': True}
        )

        If we specify ``normalized=False`` but the positions are clearly
        normalized (or vice-versa) this will result in a `ValueError`:

        >>> sample = SNPSample([[0, 1, 0], [1, 0, 1]], [0.1, 0.2, 0.3],
        ...                    pos_format={'normalized': False})
        Traceback (most recent call last):
        ...
        ValueError: specified normalized=False in pos_format even though
        the positions appear to be normalized
        """

        assert snp.dim() == 2, (
                'snp must by a 2-D array of shape (n, m) where n is the '
                'number of individuals in the sample and m the number of '
                'SNPs')
        assert pos.shape[0] == snp.shape[1], (
                f'the size of the pos array ({pos.shape[0]}) must be the '
                f'same as the number of SNPs in the snp array '
                f'({snp.shape[1]})')

        if pos_format is None:
            pos_format = {}

        normalized = bool((pos <= 1.0).all())

        if 'normalized' in pos_format:
            if pos_format['normalized'] and not normalized:
                raise ValueError(
                    'specified normalized=True in pos_format even though the '
                    'positions appear to not be normalized')
            elif not pos_format['normalized'] and normalized:
                raise ValueError(
                    'specified normalized=False in pos_format even though the '
                    'positions appear to be normalized')
        else:
            # Set this in case it was not otherwise specified
            pos_format['normalized'] = normalized

        if (pos < 0).any():
            raise ValueError('positions/distances must be non-negative')

        return pos_format


class SNPLoader(metaclass=abc.ABCMeta):
    """
    Base class for SNP loaders.

    A loader is used for lazy-loading of SNP data.  While the `SNPConverter`
    classes are converting `SNPSample` objects to/from different formats (e.g.
    different file formats), a *loader* simply provides methods for getting the
    SNP matrix and position array data on-demand.

    An `SNPLoader` must at minimum implement the `SNPLoader.get_data` method
    which returns a tuple of `torch.Tensor` objects for the SNP matrix and
    position arrays respectively.

    It may optionally implement an `SNPLoader.get_shape` which returns a tuple
    ``(n_indiv, n_snp)``--the number of SNPs and the number of individuals in
    the sample.  This can be used as an optimization to get the dimensions of a
    sample without loading the full data.
    """

    @abc.abstractmethod
    def get_data(self):
        """
        Returns the SNP matrix and position array of an SNP sample as a tuple
        of `torch.Tensor`.

        Must be implemented by subclasses.
        """

    def get_shape(self):
        """
        Returns the dimensions of an `SNPSample` as a tuple of ``(n_indiv,
        n_snp)``.

        The default implementation simply calls `SNPLoader.get_data` and
        returns the dimensions of the tensors.  However, this may be overridden
        by subclasses to provide a more efficient implementation, e.g. that
        does not require loading the full data if there is metadata available
        to provide this information.
        """

        snp, _ = self.get_data()
        return tuple(snp.shape)


class SNPConverter(metaclass=abc.ABCMeta):
    """
    Base class for converters between `SNPSample` and other objects
    representing SNPs.

    Similar interface to `~dnadna.utils.serializers.GenericSerializer`
    except the inputs and outputs need not be files.  In the case
    of `SNPSerializer` they are files, but see `DictSNPConverter` for
    a counter-example.
    """

    @abc.abstractproperty
    def format(self):
        """
        Name of the format this implements (which may be different from the
        filename extension(s).  This is used to generate ``to/from_<format>``
        methods on `SNPSample`.
        """

    @abc.abstractclassmethod
    def convert_from(cls, obj, *args, **kwargs):
        """Convert the given object to an `SNPSample`."""

    @abc.abstractmethod
    def convert_to(self, *args, **kwargs):
        """
        Convert the given `SNPSample` to the desired output
        type.

        .. note::

            The way these classes are used is such that they are never
            instantiated, but are instead containers for methods on the
            `SNPSample` class itself (see ``_SNPSampleMeta`` in the source
            code).

            This is because when the ``.convert_to()`` method is called,
            ``self`` is not an instance of an `SNPConverter`, but rather it is
            an instance of `SNPSample`.
        """

    def __init_subclass__(cls):
        """
        Every time a new `SNPConverter` subclass comes online we must
        invalidate the cache for `SNPConverter.converters`.
        """

        SNPConverter.__dict__['converters'].invalidate(SNPConverter)

    @cached_classproperty
    def converters(cls):
        """
        List of all converter classes.

        This is cached to speed up in the future, but it relies on recursively
        evaluating all its ``__subclasses__()``.  Therefore if any new
        subclasses are defined we need to invalidate the cache each time (see
        ``SNPConverter.__init_subclass__``).

        Examples
        --------

        Test that this invalidation actually occurs when defining a new
        subclass:

        >>> from dnadna.snp_sample import SNPConverter
        >>> SNPConverter.formats
        ['dict', 'npz']
        >>> class MyConverter(SNPConverter):
        ...     # note: it's not strictly necessary to define the to/from
        ...     #methods
        ...     format = 'my_format'
        >>> SNPConverter.formats
        ['dict', 'my_format', 'npz']

        There is, however, no way to "unregister" formats under this mechanism,
        but in practice that would be rare.  We just have to delete the
        subclass and then manually perform the cache invalidation e.g. by
        manually calling ``__init_subclass__`` in order to clean up:

        >>> n_subclasses = len(SNPConverter.__subclasses__())
        >>> del MyConverter
        >>> SNPConverter.__init_subclass__()

        Note: It's not enough just to ``del MyConverter``.  Apparently
        ``type.__subclasses__`` can still holds on to weak references (possibly
        as a `weakref.WeakSet`?) so there is a risk of resurrecting the deleted
        class if we try to rebuild the cache.  Run a few rounds of garbage
        collection to really make sure it's gone:

        >>> import gc
        >>> while len(SNPConverter.__subclasses__()) > n_subclasses - 1:
        ...     _ = gc.collect()
        >>> SNPConverter.formats
        ['dict', 'npz']
        """

        # Note: type.__subclasses__() only returns immediate subclasses, but we
        # want to be able to check over all derived subclasses of SNPConverter
        def subclasses_recursive(cls):
            return chain([cls], flatten(subclasses_recursive(subcls)
                                        for subcls in cls.__subclasses__()))

        return list(subclasses_recursive(cls))

    def _formats(cls):
        """
        Returns just the format names of all registered non-abstract
        converters.

        Examples
        --------

        >>> from dnadna.snp_sample import SNPConverter
        >>> SNPConverter.formats
        ['dict', 'npz']
        """

        return sorted(c.format for c in cls.converters
                      if isinstance(c.format, str))

    # NOTE: This is implemented without using a decorator, since otherwise
    # pytest will not locate the doctest.
    formats = classproperty(_formats)


class DictSNPConverter(SNPConverter, SNPLoader):
    """
    Converts `SNPSamples <SNPSample>` to/from a
    JSON-compatible dict format.

    Also acts as an `SNPLoader` for lazy-loading when
    `DictSNPConverter.from_dict` is passed ``lazy=True`` (the default).

    See `DictSNPConverter.convert_to` for a description of the data format.
    """

    format = 'dict'

    def __init__(self, data, keys=('SNP', 'POS')):
        self.data = data
        self.keys = keys

    def get_data(self):
        return self._from_dict(self.data, self.keys)

    @classmethod
    def from_dict(cls, data, keys=('SNP', 'POS'), pos_format=None, path=None,
                  lazy=True):
        """
        Convert a JSON-compatible data structure to an `SNPSample`.

        See `DictSNPConverter.convert_to` for a description of the data format.

        Examples
        --------

        >>> from dnadna.snp_sample import SNPSample
        >>> import numpy as np

        Random SNP and position arrays:

        >>> snp = (np.random.random((10, 10)) >= 0.5).astype('uint8')
        >>> pos = np.sort(np.random.random(10))
        >>> sample = SNPSample(snp, pos)
        >>> sample2 = SNPSample.from_dict(sample.to_dict())
        >>> sample == sample2
        True
        """

        if lazy:
            return SNPSample(pos_format=pos_format, path=path,
                    loader=cls(data, keys))

        snp, pos = cls._from_dict(data, keys)
        return SNPSample(snp=snp, pos=pos, pos_format=pos_format, path=path)

    def to_dict(self, keys=('SNP', 'POS')):
        """
        Convert the `SNPSample` to a JSON-compatible representation.

        This format is similar to the NPZ format in that the SNP matrix and
        position arrays are output to properties given by the ``keys``
        argument, which defaults to ``('SNP', 'POS')``.

        The position array is written as a JSON array of floats.  The SNP
        matrix is written in a compact representation consisting of an array of
        SNPs, with each SNP represented as a *string* of ``1`` s and ``0`` s.

        Examples
        --------

        >>> from dnadna.snp_sample import SNPSample
        >>> snp = [[1, 0, 1], [0, 1, 0], [1, 1, 0]]
        >>> pos = np.array([0.1, 0.2, 0.3], dtype=np.float64)
        >>> sample = SNPSample(snp, pos)
        >>> sample.to_dict()
        {'SNP': ['101', '010', '110'], 'POS': [0.1, 0.2, 0.3]}
        """

        snp_bytes = self.snp.numpy().astype('S1')

        return {
            keys[0]: [s.tobytes().decode('ascii') for s in snp_bytes],
            keys[1]: self.pos.tolist()
        }

    @staticmethod
    def _from_dict(data, keys=('SNP, POS')):
        """Convert the dict structure to `torch.Tensor`."""

        # Convert the SNP matrix to a NumPy array first, since NumPy will
        # convert strings containing digits to numbers
        snp = np.array([list(s) for s in data[keys[0]]], dtype=np.uint8)
        snp = to_tensor(snp, dtype=torch.uint8)
        # Assume maximum available precision; if need be we can add an option
        # later to specify dtype/precision for the positions.
        pos = to_tensor(data[keys[1]], dtype=torch.float64)
        return snp, pos

    # Note: We do this so that the actual methods have more the more
    # descriptive names from_dict and to_dict, otherwise the only good way to
    # make a Python function with a different name/signature is to mess around
    # with exec or code types.
    #
    # This pattern should be repeated in other SNPConverters (though it is not
    # required).
    convert_from = from_dict
    convert_to = to_dict


class SNPSerializer(GenericSerializer):
    """Base class for `SNPSample` serializers."""

    types = set([SNPSample])


class NpzSNPConverter(SNPSerializer, SNPConverter, SNPLoader):
    """
    Serialize `SNPSamples <SNPSample>` to/from NPZ_ files.

    Provides ``SNPSample.to/from_npz`` methods.

    Also acts as an `SNPLoader` for lazy-loading when
    `NpzSNPConverter.from_npz` is passed ``lazy=True`` (the default).
    """

    format = 'npz'
    extensions = ['.npz']
    binary = True

    def __init__(self, filename, keys=('SNP', 'POS')):
        self.filename = filename
        self.keys = keys

    def get_data(self):
        return self._from_npz(self.filename, keys=self.keys)

    def get_shape(self):
        """
        For NPZ files it is possible to get the array shapes by reading the
        metadata without extracting the entire array.

        It should be sufficient to find just the metadata for the SNP matrix.

        Examples
        --------

        >>> from dnadna.snp_sample import SNPSample, NpzSNPConverter
        >>> import io
        >>> out = io.BytesIO()
        >>> snp = SNPSample([[1, 0], [0, 1], [1, 1]], [2, 3])
        >>> snp.to_npz(out)
        >>> out.seek(0)
        0
        >>> conv = NpzSNPConverter(out)
        >>> conv.get_shape()
        (3, 2)
        """

        snp_filename = self.keys[0] + '.npy'

        with zipfile.ZipFile(self.filename) as archive:
            with archive.open(snp_filename) as fobj:
                version = np.lib.format.read_magic(fobj)
                version = '_'.join(str(v) for v in version)
                func_name = f'read_array_header_{version}'
                func = getattr(np.lib.format, func_name)
                shape, _, _ = func(fobj)
                return tuple(shape)

    @classmethod
    def load(cls, filename_or_obj, keys=('SNP', 'POS'), pos_format=None,
             lazy=True):
        """
        Implements the `~dnadna.utils.serializers.GenericSerializer`
        interface for loading data from an NPZ file.
        """

        filename = cls.to_filename(filename_or_obj)
        if isinstance(filename, (str, pathlib.Path)) and pth.exists(filename):
            # If a filename can be extracted from filename_or_obj, then use
            # that filename as the path to the SNP
            # Otherwise it might be some file-like object (e.g. an io.BytesIO)
            # that does not have a filename
            filename = pth.abspath(filename)
            path = pathlib.Path(filename)
            loader = cls(filename, keys)
        else:
            path = None
            loader = cls(filename_or_obj, keys)

        if lazy:
            return SNPSample(pos_format=pos_format, path=path, loader=loader)

        snp, pos = cls._from_npz(filename, keys)
        return SNPSample(snp=snp, pos=pos, pos_format=pos_format,
                         path=pathlib.Path(cls.to_filename(filename)))

    @classmethod
    def save(cls, obj, filename, keys=('SNP', 'POS'), compressed=True):
        """
        Implements the `~dnadna.utils.serializers.GenericSerializer`
        interface for saving data to an NPZ file.
        """
        savez = np.savez_compressed if compressed else np.savez
        data = {keys[0]: obj.snp.numpy(), keys[1]: obj.pos.numpy()}
        savez(filename, **data)

    @classmethod
    def from_npz(cls, filename, keys=('SNP', 'POS'), pos_format=None,
                 lazy=True):
        """
        Read a `SNPSample` from a NumPy NPZ_ file.

        An NPZ file can contain multiple arrays, each keyed by an array name.
        For SNP samples it is assumed that a given NPZ file contains at least a
        SNP matrix array and a position array.  The argument keys (default
        ``('SNP', 'POS')``) should be a 2-tuple giving the array names to look
        for in the SNP file for the SNP matrix and the positions respectively.

        Examples
        --------

        >>> import numpy as np
        >>> from dnadna.snp_sample import SNPSample
        >>> tmp = getfixture('tmp_path')  # pytest-specific

        Random SNP and position arrays:

        >>> snp = (np.random.random((10, 10)) >= 0.5).astype('uint8')
        >>> pos = np.sort(np.random.random(10))
        >>> np.savez(tmp / 'test.npz', SNP=snp, POS=pos)
        >>> sample = SNPSample.from_npz(tmp / 'test.npz')
        >>> (sample.snp.numpy() == snp).all()
        True
        >>> (sample.pos.numpy() == pos).all()
        True

        .. _NPZ: https://numpy.org/devdocs/reference/generated/numpy.savez.html#numpy.savez
        """

        return cls.load(filename, keys=keys, pos_format=pos_format, lazy=lazy)

    def to_npz(self, filename, keys=('SNP', 'POS'), compressed=True):
        """
        Write a `SNPSample` to a NumPy NPZ_ file.

        An NPZ file can contain multiple arrays, each keyed by an array name.
        See also `NpzSNPConverter.load` for the converse.  The ``keys=('SNP',
        'POS')`` argument can be overridden to save with different names for
        the SNP and position arrays.

        If ``compressed=True`` (default) the NPZ archive is written with zip
        compression.

        .. _NPZ: https://numpy.org/devdocs/reference/generated/numpy.savez.html#numpy.savez

        Examples
        --------

        >>> import numpy as np
        >>> from dnadna.snp_sample import SNPSample
        >>> tmp = getfixture('tmp_path')  # pytest-specific

        Random SNP and position arrays:

        >>> snp = (np.random.random((10, 10)) >= 0.5).astype('uint8')
        >>> pos = np.sort(np.random.random(10))
        >>> sample = SNPSample(snp, pos)
        >>> sample.to_npz(tmp / 'test.npz')
        >>> sample == SNPSample.from_npz(tmp / 'test.npz')
        True
        """

        # Because of how convert_to works, `self` here is an SNPSample
        # instance, not an NpzSNPConverter instance, so we must use the class
        # explicitly for the .save() method
        return NpzSNPConverter.save(self, filename, keys=keys,
                compressed=compressed)

    convert_from = from_npz
    convert_to = to_npz

    @staticmethod
    def _from_npz(filename, keys=('SNP', 'POS')):
        """Load the raw snp and pos tensors."""

        with np.load(filename) as npz_data:
            snp = to_tensor(npz_data[keys[0]], dtype=torch.uint8)
            pos = to_tensor(npz_data[keys[1]])
            return snp, pos
