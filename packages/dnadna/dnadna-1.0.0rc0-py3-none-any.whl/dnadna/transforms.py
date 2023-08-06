"""Data transforms that can be applied during training."""


import abc
import multiprocessing
import warnings
from contextlib import nullcontext
from inspect import signature

import numpy as np
import torch

from . import DNADNAWarning
from .utils.plugins import Pluggable


class TransformException(Exception):
    """
    Exception raised when applying a `Transform` to an input.

    Parameters
    ----------

    transform : `dnadna.transforms.Transform`
        The transform that caused the exception.
    """

    def __init__(self, transform):
        self.transform = transform


class InvalidSNPSample(Exception):
    """
    Exception raised when a sample doesn't meet the minimum requirements for
    the dataset.

    Used by `ValidateSnp`.
    """

    def __init__(self, msg, sample=None):
        super().__init__(msg)
        self.sample = sample


class Compose:
    """
    Pseudo-transform that composes multiple transforms by applying them in
    order one after the other.
    """

    def __init__(self, transforms):
        self.transforms = transforms

    def __repr__(self):
        return f'{self.__class__.__name__}({self.transforms!r})'

    def __call__(self, data):
        for transform in self.transforms:
            try:
                data = transform(data)
            except Exception as exc:
                raise TransformException(transform) from exc

        return data


class Transform(Pluggable, metaclass=abc.ABCMeta):
    r"""
    Dataset transform.

    When loading `~dnadna.snp_sample.SNPSample`\s from the dataset, these
    transforms are applied to the samples to modify either the position or SNP
    matrix arrays, or both.

    To implement a transform you must provide its ``__call__`` method, which
    takes as input a tuple consisting of the `~dnadna.snp_sample.SNPSample`
    being loaded from the dataset, as well as a the parameters being trained
    as a `~dnadna.params.LearnedParams`, and the parameter values associated
    with the sample's scenario, as loaded from the Pandas `~pandas.DataFrame`.
    """

    @abc.abstractmethod
    def __call__(self, inputs):
        """
        Execute the transform on the given inputs.

        All transforms take a single argument so that they can easily be
        pipelined.
        """

    def __repr__(self):
        """
        Represent a Transform instance.

        Examples
        --------

        >>> subsample = Subsample(size=[100, 200])
        >>> subsample
        Subsample(size=[100, 200], keep_polymorphic_only=True)

        >>> subsample = Subsample(size=[100, 200], keep_polymorphic_only=False)
        >>> subsample
        Subsample(size=[100, 200], keep_polymorphic_only=False)
        """

        parameters = []
        for parameter in signature(self.__class__).parameters:
            try:
                value = repr(getattr(self, parameter))
            except AttributeError:
                warnings.warn(
                    f'Transform input parameters should be assigned to '
                    f'attributes of the same name, but '
                    f'{self.__class__.__name__} does not have a {parameter} '
                    f'attribute.', DNADNAWarning)
                value = '?'
            parameters.append(f'{parameter}={value}')
        return f'{self.__class__.__name__}({", ".join(parameters)})'

    @classmethod
    def get_schema(cls):
        """
        Provide a schema for validating a single transform in a list of
        transforms in the config file (see the :ref:`training config schema
        <schema-training>`) for example usage).
        """

        if cls is not Transform:
            # Simple return the schema for the individual transform, if any
            return cls.schema

        # transforms that do not take any arguments can be given as a string
        # that is just the transform name
        name_only_transforms = []

        # Other transforms must be dicts containing the transform's name, and
        # any other parameters of the transform (which cannot be 'name')
        schemas = []

        for plugin_name, plugin in cls.get_plugins():
            init_params = signature(plugin).parameters
            schema = plugin.schema

            if not init_params:
                name_only_transforms.append(plugin_name)
                name_only_transforms.append(plugin.__name__)
            elif len(init_params) == 1:
                # For transforms that only have one init parameter we can
                # allow "transform_name: param_value" without specifiying
                # the param name
                param_name = list(init_params)[0]
                param_schema = plugin.schema.get('properties', {}).get(
                        param_name, {})
                schema = {'oneOf': [schema, param_schema]}

            schema = {
                'properties': {
                    plugin_name: schema,
                    plugin.__name__: schema
                },
                'maxProperties': 1,
                'minProperties': 1,
                'additionalProperties': False
            }
            # TODO: We could use type annotations to automatically generate
            # default config schemas for transforms, or even for networks.

            schemas.append(schema)

        return {'oneOf': [{'type': 'string', 'enum': name_only_transforms}] +
                         schemas}


def keep_polymorphic_only(sample):
    """
    Remove sites that are no longer polymorphic in sample.

    Both the SNP matrix and position vector are filtered.
    If position is encoded as distance, distances between SNPs are adjusted.

    Parameters
    ----------

    sample : SNPSample
        sample to filter
    """

    snp_2_keep = ~(sample.snp[0, :] == sample.snp).all(dim=0)
    if snp_2_keep.sum() == sample.n_snp:
        # No column is constant, nothing to filter
        return sample

    orig_distance = sample.full_pos_format['distance']
    if orig_distance:
        # convert positions from distance to absolute values
        # before filtering out SNPs
        transform = ReformatPosition(distance=False)
        sample, _, _ = transform((sample, None, None))
    sub_snp = sample.snp[:, snp_2_keep]
    sub_pos = sample.pos[snp_2_keep]
    sample = sample.copy_with(snp=sub_snp, pos=sub_pos, validate=False)
    if sample.full_pos_format['distance'] != orig_distance:
        # convert back position to the original format
        transform = ReformatPosition(distance=orig_distance)
        sample, _, _ = transform((sample, None, None))

    return sample


class Crop(Transform):
    """
    Crop the SNP matrix and position array to a maximum size.

    Parameters
    ----------

    max_snp : int, optional
        crop the number of SNPs to at most ``max_snp``
    max_indiv : int, optional
        crop the number of individuals to at most ``max_indiv``
    keep_polymorphic_only : bool
        if true, SNPs that are not polymorphic are removed
    """

    schema = {
        'type': 'object',
        'description':
            "Crop the SNP matrix and position array to a maximum size",
        'properties': {
             'max_snp': {
                 'description':
                     'Maximum number of SNPs to crop dataset outputs to. '
                     'Set this to less-than-or-equal to '
                     'preprocessing.min_snp to ensure that all samples have '
                     'the same number of SNPs, as some nets require a fixed '
                     'number of SNPs.',
                 'type': ['integer', 'null'],
                 'minimum': 1,
                 'default': None
             },
             'max_indiv': {
                 'description':
                     'Maximum number of individuals to crop dataset outputs '
                     'to, set this to less-than-or-equal to '
                     'preprocessing.min_indiv to ensure that all samples '
                     'have the same number of individuals, as some nets '
                     'require a fixed number of individuals.',
                 'type': ['integer', 'null'],
                 'minimum': 1,
                 'default': None
             },
             'keep_polymorphic_only': {
                 'description':
                     'After subsampling or cropping the individuals dimension of '
                     'a SNP matrix, if some sites are no longer polymorphic they '
                     'will be removed if keep_polymorphic_only=True ',
                 'type': ['boolean'],
                 'default': True
             }
        }
    }

    def __init__(self, max_snp=None, max_indiv=None, keep_polymorphic_only=True):
        self.max_snp = max_snp
        self.max_indiv = max_indiv
        self.keep_polymorphic_only = keep_polymorphic_only

    def __call__(self, data):
        sample, lp, scen = data
        snp, pos = sample.snp, sample.pos

        if self.max_indiv is not None:
            # It might be a little more efficient to slice by rows first
            snp = snp[:self.max_indiv]
        if self.keep_polymorphic_only:
            # filter out columns that are not variable anymore
            # important to do it after cropping individuals
            # and before cropping SNPs
            sample = keep_polymorphic_only(sample.copy_with(snp=snp, pos=pos,
                                                            validate=False))
            snp, pos = sample.snp, sample.pos

        if self.max_snp is not None:
            snp, pos = snp[:, :self.max_snp], pos[:self.max_snp]

        sample = sample.copy_with(snp=snp, pos=pos)
        return (sample, lp, scen)


class SnpFormat(Transform):
    """
    This transform specifies in what format the SNP matrix and position arrays
    are combined to form the input to the network.

    Currently this can be one of:

    * concat: the position array and the SNP matrix are concatenated vertically
      with the position array becoming the first row of the tensor (this is
      the default, even if this transform is not used explicitly).

    * product: the SNP matrix is multiplied by the position array, so that
      each active site has the value of its position, rather than just ``1``.
    """

    schema = {
        'type': 'object',
        'description':
            "when loading SNPs from a dataset, specify whether to "
            "concatenate the positions array to the SNP matrix or to "
            "multiply them together (uses 'concat' by default)",
        'properties': {
            'format': {
                'type': 'string',
                'enum': ['concat', 'product']
            }
        }
    }

    def __init__(self, format='concat'):
        self.format = format

    def __call__(self, data):
        sample, lp, scen = data
        if sample.tensor_format != self.format:
            sample = sample.copy_with(tensor_format=self.format)

        return (sample, lp, scen)


class Subsample(Transform):
    """
    Subsample SNP matrix of size (n, k), with n individuals and k SNPs and
    return a matrix of size (m, l), with m individuals and m < n and l SNPs
    with l <= k because columns without SNP anymore are not kept.

    Parameters
    ----------
    size : int, tuple, list
        Number of individuals to keep. If tuple/list, random value of
        individuals within the range defined by the tuple values.
    keep_polymorphic_only : bool
        if true, SNPs that are not polymorphic are removed
    """

    schema = {
        'type': 'object',
        'description':
            'take random subsamples of the SNP matrix; the argument is a pair '
            '(min, max) of integers giving the range for random sizes of the '
            'subsamples, or a single integer giving a fixed size for the '
            'subsamples. Use keep_polymorphic_only=False to keep non polymorphic sites'
            'after subsampling, otherwise they are removed',
        'properties': {
            'size': {
                'oneOf': [{
                    'type': 'array',
                    'minItems': 2,
                    'maxItems': 2,
                    'items': {'type': 'integer', 'minimum': 1}
                }, {
                    'type': 'integer',
                    'minimum': 1
                }]
            },
            'keep_polymorphic_only': {
                'description':
                    'After subsampling or cropping the individuals dimension of '
                    'a SNP matrix, if some sites are no longer polymorphic they '
                    'will be removed if keep_polymorphic_only=True ',
                'type': ['boolean'],
                'default': True
            }
        }
    }

    def __init__(self, size, keep_polymorphic_only=True):
        self.size = size
        self.keep_polymorphic_only = keep_polymorphic_only

    def __call__(self, data):
        snp, lp, scen = data
        if isinstance(self.size, (tuple, list)):
            size = np.random.randint(*self.size)
        else:
            size = self.size

        idx = np.random.choice(snp.n_indiv, size, replace=False)
        sample = snp.copy_with(snp=snp.snp[idx, :], pos=snp.pos, validate=False)
        if self.keep_polymorphic_only:
            sample = keep_polymorphic_only(sample)
        return (sample, lp, scen)


class Rotate(Transform):
    """
    Given a sequence, return a random rotation of it along the SNP axis.

    Args:
        None
    """

    schema = {
        'description':
            'apply a random rotation along the SNP axis of a sequence'
    }

    def __call__(self, data):
        snp, lp, scen = data
        shift_index = np.random.randint(0, snp.n_snp)
        rot_snp = np.roll(snp.snp, shift_index, axis=1)
        rot_pos = np.roll(snp.pos, shift_index, axis=0)
        shift = rot_pos[0]

        # If any regression parameters are tied to position, we must apply
        # the position shift to them as well
        # TODO: Should position normalization (i.e. relative_position()
        # also be applied in this case?
        if lp is not None and scen is not None:
            reg_params = lp.regression_params.items()
            for param_name, param in reg_params:
                if param['tied_to_position'] and scen[param_name] >= 0:
                    scen[param_name] = (scen[param_name] - shift) % 1

        return (snp.copy_with(snp=rot_snp, pos=rot_pos, validate=False),
                lp, scen)


class ReformatPosition(Transform):
    """
    Changes the format of the input position array.

    It can change from normalized/unnormalized positions, and can convert
    between distance and absolute position formats.

    When initializing this transform it is only necessary to specify those
    parameters that you explicitly want to convert.

    .. warning::

        This transform should be applied before any other transforms (e.g.
        rotate) which can modify the position orders, since this transform
        assumes positions are all in increasing order.

    Parameters
    ----------
    distance : bool, optional
        If True, change positions to distances or vice-versa; if left
        unspecified the current position format is kept.
    normalized : bool, optional
        If True, unnormalized positions are converted to normalized positions
        and vice-versa; if left unspecified the current normalization is kept.
        The ``chromosome_size`` argument is also required when changing the
        normalization, unless the ``chromosome_size`` is already specified on
        the inputs.
    chromosome_size : int, optional
        Length of the chromosome; required when transforming from normalized to
        unnormalized positions.  If left unspecified, but the input
        `~dnadna.snp_sample.SNPSample` has a ``chromosome_size`` in its
        ``pos_format``, that it will be used.
    circular : bool, optional
        Chromosome should be treated as circular when performing the
        transformation.  Normally the input's circularity is kept.
    initial_position : int or float, optional
        A position to use as the initial position when converting from circular
        positions.

    Examples
    --------
    >>> from dnadna.snp_sample import SNPSample
    >>> from dnadna.transforms import ReformatPosition
    >>> import numpy as np

    Initial example with unnormalized absolute positions and chromosome_size =
    1000:

    >>> sample = SNPSample(np.eye(4), [5, 460, 900, 952],
    ...                    pos_format={'normalized': False, 'distance': False,
    ...                                'chromosome_size': 1000})
    >>> xf = ReformatPosition(normalized=True)
    >>> xf((sample, None, None))[0]
    SNPSample(
        snp=tensor(...),
        pos=tensor([0.0050, 0.4600, 0.9000, 0.9520], dtype=torch.float64),
        pos_format={'normalized': True, 'distance': False,
                    'chromosome_size': 1000}
    )
    >>> xf = ReformatPosition(distance=True)
    >>> xf((sample, None, None))[0]
    SNPSample(
        snp=tensor(...),
        pos=tensor([  5, 455, 440,  52]),
        pos_format={'normalized': False, 'distance': True,
                    'chromosome_size': 1000}
    )
    >>> xf = ReformatPosition(distance=True, normalized=True)
    >>> dist_norm = xf((sample, None, None))[0]
    >>> dist_norm
    SNPSample(
        snp=tensor(...),
        pos=tensor([0.0050, 0.4550, 0.4400, 0.0520], dtype=torch.float64),
        pos_format={'normalized': True, 'distance': True,
                    'chromosome_size': 1000}
    )

    Convert from normalized distances back to unnormalized positions:

    >>> xf = ReformatPosition(distance=False, normalized=False)
    >>> xf((dist_norm, None, None))[0]
    SNPSample(
        snp=tensor(...),
        pos=tensor([  5, 460, 900, 952]),
        pos_format={'normalized': False, 'distance': False,
                    'chromosome_size': 1000}
    )

    Convert from normalized linear distances to circular distances:

    >>> xf = ReformatPosition(circular=True, initial_position=0.005)
    >>> xf((dist_norm, None, None))[0]
    SNPSample(
        snp=tensor(...),
        pos=tensor([0.0530, 0.4550, 0.4400, 0.0520], dtype=torch.float64),
        pos_format={'normalized': True, 'distance': True,
                    'chromosome_size': 1000, 'circular': True,
                    'initial_position': 0.005}
    )

    Convert from positions to circular distances:

    >>> xf = ReformatPosition(distance=True, circular=True)
    >>> xf((sample, None, None))[0]
    SNPSample(
        snp=tensor(...),
        pos=tensor([  53, 455, 440,  52]),
        pos_format={'normalized': False, 'distance': True,
                    'chromosome_size': 1000, 'circular': True,
                    'initial_position': 5}
    )
    >>> xf = ReformatPosition(distance=True, normalized=True, circular=True)
    >>> circ_norm = xf((sample, None, None))[0]
    >>> circ_norm
    SNPSample(
        snp=tensor(...),
        pos=tensor([0.0530, 0.4550, 0.4400, 0.0520], dtype=torch.float64),
        pos_format={'normalized': True, 'distance': True,
                    'chromosome_size': 1000, 'circular': True,
                    'initial_position': 0.005}
    )

    Test converting some circular distances, first from circular to
    non-circular:

    >>> xf = ReformatPosition(circular=False)
    >>> xf((circ_norm, None, None))[0]
    SNPSample(
        snp=tensor(...),
        pos=tensor([0.0050, 0.4550, 0.4400, 0.0520], dtype=torch.float64),
        pos_format={'normalized': True, 'distance': True,
                    'chromosome_size': 1000, 'circular': False,
                    'initial_position': 0.005}
    )
    """

    # NOTE: basic provisional schema for this transform; it does not fully
    # restrict normalization configs that don't make sense.
    schema = {
        'type': 'object',
        'description': 'renormalize the position array',
        'definitions': {
            'optional-boolean': {
                'type': ['boolean', 'null'],
                'default': None
            }
        },
        'properties': {
            'distance': {'$ref': '#/definitions/optional-boolean'},
            'normalized': {'$ref': '#/definitions/optional-boolean'},
            'circular': {'$ref': '#/definitions/optional-boolean'},
            'chromosome_size': {
                'type': ['integer', 'null'],
                'minimum': 1,
                'default': None
            },
            # TODO: We could place stronger requirements on initial_position
            # depending on the renormalization type, (distance->position or
            # vice-versa and whether or not circular is used)
            'initial_position': {
                'type': ['integer', 'number', 'null'],
                'default': None
            }
        }
    }

    def __init__(self, distance=None, normalized=None, circular=None,
                 chromosome_size=None, initial_position=None):
        self.distance = distance
        self.normalized = normalized
        self.circular = circular
        self.chromosome_size = chromosome_size
        self.initial_position = initial_position

    def __call__(self, data):
        snp, lp, scen = data
        input_pos_format = snp.full_pos_format
        new_pos_format = {}
        chromosome_size = input_pos_format.get('chromosome_size',
                                               self.chromosome_size)
        initial_position = input_pos_format.get('initial_position',
                                                self.initial_position)

        pos = snp.pos

        # Normalize/de-normalize first; this makes it easier to specify
        # normalization when converting to/from distances
        if (self.normalized is not None and
                self.normalized != input_pos_format['normalized']):
            if chromosome_size is None:
                raise TypeError(
                    f'{self.__class__.__name__}: chromosome_size must be '
                    f'specified when requesting normalization/de-normalization')

            if self.normalized:
                norm_method = self._normalize
            else:
                norm_method = self._denormalize

            pos = norm_method(pos, chromosome_size)
            if initial_position is not None:
                initial_position = norm_method(initial_position,
                                               chromosome_size)

            new_pos_format['normalized'] = self.normalized
            normalized = self.normalized
        else:
            # Normalization is same as the input format
            normalized = input_pos_format['normalized']

        if (self.distance is not None and
                self.distance != input_pos_format['distance']):

            if self.distance:
                # Should the output be circular distances?
                circular = (self.circular if self.circular is not None
                                          else input_pos_format['circular'])
                if circular:
                    new_pos_format['circular'] = True
                    initial_position = pos[0].item()

                pos = self._position_to_distance(pos,
                        normalized=normalized,
                        circular=circular, chromosome_size=chromosome_size)
            else:
                # Are the inputs circular distances?
                circular = input_pos_format['circular']
                pos = self._distance_to_position(pos, normalized=normalized,
                        circular=circular, initial_position=initial_position)

            new_pos_format['distance'] = self.distance
            if self.circular is not None:
                # We are now in absolute positions, so 'circular' should be
                # set to whatever was specified in the transform, even though
                # there is no particular difference between circular and
                # non-circular positions
                new_pos_format['circular'] = self.circular
            distance = self.distance
        else:
            distance = input_pos_format['distance']

        if (self.circular is not None and
                self.circular != input_pos_format['circular'] and
                distance == input_pos_format['distance'] == True):  # noqa: E712
            # Special case for converting between circular and non-circular
            # distances
            if self.circular:
                pos = self._linear_to_circular_distance(pos,
                        normalized=normalized, chromosome_size=chromosome_size)
            else:
                if initial_position is None:
                    raise TypeError(
                        f'{self.__class__.__name__}: initial_position must be '
                        f'specified for converting circular distances to '
                        f'linear distances')
                pos = self._circular_to_linear_distance(pos, initial_position)

            new_pos_format['circular'] = self.circular

        # Don't save chromosome_size unless converting to normalized
        if self.normalized:
            new_pos_format['chromosome_size'] = chromosome_size

        if initial_position is not None:
            new_pos_format['initial_position'] = initial_position

        output_pos_format = snp.pos_format.copy()
        output_pos_format.update(new_pos_format)
        return (snp.copy_with(pos=pos, pos_format=output_pos_format,
                              validate=False), lp, scen)

    def _position_to_distance(self, pos, normalized=False,
                              circular=False, chromosome_size=None):
        # Sanity check
        if not normalized and circular and chromosome_size is None:
            raise TypeError(
                f'{self.__class__.__name__}: chromosome_size must be '
                f'specified when converting un-normalized positions '
                f'to circular distances')
        dist = torch.empty_like(pos)
        dist[1:] = pos[1:] - pos[:-1]
        if circular:
            dist[0] = pos[0] - pos[-1]
            if normalized:
                dist = dist % 1
            else:
                dist = dist % chromosome_size
        else:
            dist[0] = pos[0]
        return dist

    def _distance_to_position(self, pos, normalized=False, circular=False,
                              chromosome_size=None, initial_position=None):
        if circular:
            if initial_position is None:
                raise TypeError(
                    f'{self.__class__.__name__}: initial_position must be '
                    f'specified when converting circular distances to '
                    f'positions')
            # Copy the original position array before modifying it
            pos = pos.detach().clone()
            pos[0] = initial_position

        return pos.cumsum(0)

    def _normalize(self, pos, chromosome_size):
        if isinstance(pos, torch.Tensor):
            pos = pos.double()

        return pos / chromosome_size

    def _denormalize(self, pos, chromosome_size):
        # Use round() to round to nearest int so that small rounding errors
        # don't result in truncation
        pos = pos * chromosome_size
        if isinstance(pos, torch.Tensor):
            return pos.round().long()
        else:
            return round(pos)

    def _linear_to_circular_distance(self, pos, normalized=False,
                                     chromosome_size=None):
        if not normalized and chromosome_size is None:
            raise TypeError(
                f'{self.__class__.__name__}: chromosome_size must be '
                f'specified when converting non-normalized distances '
                f'to circular distances')

        out = pos.detach().clone()
        pos_sum = pos.sum()
        if normalized:
            out[0] = (pos[0] - pos_sum) % 1
        else:
            out[0] = (pos[0] - pos_sum) % chromosome_size

        return out

    def _circular_to_linear_distance(self, pos, initial_position):
        out = pos.detach().clone()
        # That's all it is; initial_position should have already been
        # normalized/de-normalized by this point
        out[0] = initial_position
        return out


class ValidateSnp(Transform):
    """
    A special transform that does not actually modify the data, but merely
    performs certain verifications on it.

    If verification fails the data sample will be excluded from batches
    returned by the data loader.

    Currently there is only one verification supported, which is to verify
    that all SNPs have the same shape (same number of SNPs and individuals).

    This can be combined e.g. with `Crop` to first crop the SNP sizes to
    a maximum size, then verify that they are of a consistent shape with
    previous SNPs in the dataset.

    Parameters
    ----------

    uniform_shape : bool, optional
        Check whether all SNP samples in the dataset have the same shape
        (same number of SNPs and individuals).
    """

    schema = {
        'type': 'object',
        'description':
            'validate the SNP resulting from previous transforms (if any); '
            'does not modify the data, but will cause it to be excluded from '
            'the batch if validation fails',
        'properties': {
            'uniform_shape': {
                'type': 'boolean',
                'default': True
            }
        }
    }

    def __init__(self, uniform_shape=True):
        self.uniform_shape = uniform_shape
        if self.uniform_shape:
            # Keep track of the dimensions of each data sample for ensuring
            # that they are uniform (if uniform_shape=True)
            # We must use a shared array so this can be synchronized when using
            # a multi-process DataLoader
            self._snp_shape = multiprocessing.Array('q', [0, 0])

    def __call__(self, data):
        if self.uniform_shape:
            self._validate_uniform_shape(data)
        return data

    def _validate_uniform_shape(self, data):
        sample, _, _ = data

        if hasattr(self._snp_shape, 'get_lock'):
            ctx = self._snp_shape.get_lock
        else:
            # it is no longer a shared value
            ctx = nullcontext

        with ctx():
            shape = tuple(self._snp_shape[:])
            if any(dim == 0 for dim in sample.shape):
                raise InvalidSNPSample(
                    'sample contains empty data (zero SNPs and/or individuals)',
                    sample=sample)
            elif shape == (0, 0):
                # The shared shape has not been initialized, so initialize it
                # to sync its value with the other processes
                self._snp_shape[:] = shape = sample.shape
            elif sample.shape != shape:
                if shape[1] != sample.n_snp:
                    raise InvalidSNPSample(
                        f'sample has {sample.n_snp} SNPs, which differs from '
                        f'the rest of the dataset ({shape[1]} SNPs)',
                        sample=sample)
                else:
                    raise InvalidSNPSample(
                        f'sample has {sample.n_indiv} individuals, which '
                        f'differs from the rest of the dataset ({shape[0]} '
                        f'individuals)', sample=sample)

        # after the synchronized self._snp_shape has been read once its value
        # is never set again (since for a uniform dataset we just assume the
        # first sample read sets the expected shape for all samples) so we no
        # longer need synchronization on this
        self._snp_shape = tuple(shape)
