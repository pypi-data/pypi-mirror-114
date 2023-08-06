# -*- coding: utf-8 -*-
"""
Utilities for loading data from data sets, including support for different data
set formats:

* Classes for reading different dataset formats.  Datasets are collections of
  SNP files for multiple scenarios, possibly with multiple replicates per
  scenario:

    * The `NpzSNPSource` class reads a data set of multiple parameter scenarios
      with (possibly) multiple replicates per scenario, stored in NPZ_ files in
      a particular filesystem layout, known as the :ref:`DNADNA Format
      <dataset-formats-dnadna>`. This is the default data set format understood
      by DNADNA.

    * The `DictSNPSource` class reads a JSON-based data set format which is
      less efficient both in terms of storage compactness and
      parsing/serializing, that allows plain-text storage of SNP data.
      Currently this is used primarily in testing.

* The `DNATrainingDataset` and its simpler base class `DNADataset` are
  implementations of a PyTorch `~torch.utils.data.Dataset` used for loading SNP
  data (in the form of `SNPSamples <dnadna.snp_sample.SNPSample>` along with
  their associated scenario parameters, for both training sets and validation
  sets during model training.  This works independently of what the dataset
  format is (the dataset format is implemented as an ``SNPSource`` such as the
  two listed above, which is an abstract interface for arbitrary dataset
  formats).  (TODO: There is currently no ``SNPSource`` base class, but one
  should be implemented in order to help define the interface.)

.. _NPZ: https://numpy.org/devdocs/reference/generated/numpy.savez.html#numpy.savez
"""

# TODO: I fear that the design of the classes in this module have gotten overly
# confusing as different needs for it have developed over time.  I think that
# it should be redesigned from the ground-up, but that will have to wait if so.


import abc
import errno
import os
import posixpath as pth
import pathlib
import pprint
import re
import warnings
from collections.abc import Set, Sequence
from inspect import signature

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

from . import DNADNAWarning
from .params import LearnedParams
from .utils.config import load_dict, Config, ConfigMixIn
from .utils.misc import parse_format, format_to_re, reformat_format
from .utils.plugins import Pluggable
from .snp_sample import SNPSample
from .transforms import Compose, Transform, TransformException


class MissingSNPSample(Exception):
    """
    Exception raised when a specified sample is not found in an SNP source.
    """

    def __init__(self, scenario, replicate, path, reason=None):
        self.scenario = scenario
        self.replicate = replicate
        self.path = path
        self.reason = reason

    def __str__(self):
        msg = (f'could not load scenario {self.scenario} replicate '
               f'{self.replicate}')
        if self.path:
            msg += f' from "{self.path}"'
        if self.reason is not None:
            msg += f': {self.reason!r}'
        return msg


class SNPSource(Pluggable, metaclass=abc.ABCMeta):
    r"""
    A "SNPSource" is a class for loading `~dnadna.snp_sample.SNPSample` objects
    from some data source.

    Subclasses of this class represent different data *formats* from which
    samples can be loaded.

    This is in a way "lower-level" than `DNADataset`.  `DNADataset` is an
    abstraction that loads SNPSamples from a data source, possibly performs
    some transforms on them, and returns them.  From the point of view of
    `DNADataset` the actual on-disk format from which the samples are read is
    abstracted out to `SNPSource`.

    In fact it may not even be an "on-disk" format; for example one could
    implement a `SNPSource` plugin that loads samples from an S3 bucket.

    The "main" implementation of `SNPSource` is `NpzSNPSource` which loads
    samples organized on disk in the :ref:`"dnadna" format
    <dataset-formats-dnadna>`.  The other built-in implementations include:

        * `FileListSNPSource` -- a simple format that simply reads a list
          of `SNPSample`\s from a list of filenames; this is used primarily
          by the ``dnadna predict`` command for reading in a list of files on
          which to make predictions.

        * `DictSNPSource` -- used primarily for testing, it can read samples
          from a JSON-compatible dict format; see its documentation for more
          details.
    """

    @classmethod
    def from_config_file(cls, filename, validate=True, **kwargs):
        """
        Like `~SNPSource.from_config` but given a filename instead of a
        `~dnadna.utils.config.Config` object.

        The additional keyword arguments are passed to the dict serializer, and
        the config is validated against the :ref:`dataset schema
        <schema-dataset>`.
        """

        kwargs.setdefault('schema', 'dataset')
        config = Config.from_file(filename, validate=validate, **kwargs)
        # if validate=True was given we have already validated the config
        # if validate=False was given we don't want to validate the config in
        # from_config either
        return cls.from_config(config, validate=False)

    @classmethod
    def from_config(cls, config, validate=True):
        """
        Instantiate an `SNPSource` from dataset `~dnadna.utils.config.Config`
        matching the :ref:`dataset schema <schema-dataset>`.

        Although configuration specific to a given `SNPSource` subclass may
        have its own format-specific schema, these are still passed the full
        dataset config, which may contain additional properties (such as
        ``data_root``) that might be useful to a given format.

        Subclasses should implement this method in order to specify how to
        instantiate it from a config file; otherwise it cannot be used as a
        configurable plugin.
        """
        raise NotImplementedError(
            f'loading a {cls.__name__} from a config file is not currently '
            f'implemented')

    @abc.abstractmethod
    def __getitem__(self, scenario_replicate):
        """
        Subclasses must implement a ``__getitem__`` which takes a
        ``(scenario_idx, replicate_idx)`` tuple and reads and returns the
        `~dnadna.snp_sample.SNPSample` in the dataset associated with that
        index pair.
        """

    @abc.abstractmethod
    def __iter__(self):
        """
        Iterate over all samples found in the data source and return their
        associated ``(scenario_idx, replicate_idx)`` tuple.

        To load all samples in the data source this can be used like::

            for scenario_idx, replicate_idx in source:
                sample = source[scenario_idx, replicate_idx]

        For optimization reasons it only iterates over the ``(scenario_idx,
        replicate_idx)`` pairs, but does not return the samples themselves.
        """

    @abc.abstractmethod
    def __contains__(self, scenario_replicate):
        """
        Return whether the given ``(scenario_idx, replicate_idx)`` pair
        represents a sample that can be found in the data source.
        """


class NpzSNPSource(SNPSource):
    """
    SNP source that reads simulation data as `SNPSamples
    <dnadna.snp_sample.SNPSample>` stored on disk in DNADNA's native
    :ref:`"dnadna" format <dataset-formats-dnadna>`.

    Each simulation is stored in a NumPy NPZ_ file containing two arrays,
    by default keyed by ``'SNP'`` for the SNP matrix, and ``'POS'`` for the
    positions array.

    There is one ``.npz`` file for each replicate of each scenario, laid out
    in a filesystem format.  The exact layout and filename can be specified
    by the ``filename_format`` argument to this class's constructor, but the
    default layout is as specified in
    `NpzSNPSource.DEFAULT_NPZ_FILENAME_FORMAT`, which is also the documented
    format assumed by the "dnadna" format.

    .. _NPZ: https://numpy.org/devdocs/reference/generated/numpy.savez.html#numpy.savez

    Parameters
    ----------
    root_dir : str, pathlib.Path
        The root directory of the DNADNA dataset.  All filenames generated
        from the ``filename_format`` are appended to this directory.
    dataset_name : str
        The name of the dataset--same as that specified in the simulation
        config for this dataset.
    filename_format : str, optional
        A string in :ref:`Python format string syntax <python:formatstrings>`
        specifying the format for filenames of individual simulations in this
        dataset.  The format string can contain 3 replacement fields:
        ``{dataset_name}`` which is filled in with the model name given by the
        ``dataset_name`` parameter above, ``{scenario}`` which is filled with
        the scenario index, and ``{replicate}`` which is filled with the
        replicate index.  If the scenario and replicate indices are zero-padded
        in the filenames, the amount of zero-padding may be explicitly
        specified by writing the format string like ``{scenario:05}`` (for
        scenario indices padded up to 5 zeros).  However, if no-zero padding is
        specified in the format string, the appropriate amount of zero-padding
        is automatically guessed by filenames actually present in the dataset.
        Therefore the default ``filename_format``,
        `NpzSNPSource.DEFAULT_NPZ_FILENAME_FORMAT` can be used regardless of
        the amount of zero-padding used in a given dataset.
    keys : tuple, optional
        A 2-tuple of ``(snp_key, pos_key)`` giving the keywords for the SNP
        matrix and the position array in the NPZ file.  The default
        ``('SNP', 'POS')`` is the default for the "dnadna" format, but
        different names may be specified for these arrays.
    position_format : dict, optional
        The format of the position arrays in the dataset (currently all samples
        in the dataset are assumed to have the same position formats).
        Corresponds to the ``pos_format`` argument to
        `~dnadna.snp_sample.SNPSample`.
    lazy : bool, optional
        By default data is lazy-loaded, so that it is not read from disk until
        needed.  Use ``lazy=False`` to ensure that the data is immediately
        loaded into memory.

    Examples
    --------
    >>> import numpy as np
    >>> from dnadna.datasets import NpzSNPSource
    >>> from dnadna.snp_sample import SNPSample
    >>> tmp = getfixture('tmp_path')  # pytest-specific

    Make a few random SNP and position arrays:

    >>> dataset = {}
    >>> filename_format = 'my_model_{scenario:03}_{replicate:03}.npz'
    >>> for scenario_idx, replicate_idx in zip(range(2), range(2)):
    ...     snp = (np.random.random((10, 10)) >= 0.5).astype('uint8')
    ...     pos = np.sort(np.random.random(10))
    ...     sample = SNPSample(snp, pos)
    ...     filename = tmp / filename_format.format(
    ...         scenario=scenario_idx, replicate=replicate_idx)
    ...     sample.to_npz(filename)
    ...     dataset[(scenario_idx, replicate_idx)] = sample

    Instantiate the `NpzSNPSource` and load a couple samples:

    >>> source = NpzSNPSource(tmp, 'my_model', filename_format=filename_format)
    >>> source[0, 0]
    SNPSample(
        snp=tensor([[...],
                    ...
                    [...]], dtype=torch.uint8),
        pos=tensor([...], dtype=torch.float64),
        pos_format={'normalized': True},
        path=...Path('...my_model_000_000.npz')
    )
    >>> source[0, 0] == dataset[0, 0]
    True
    >>> source[1, 1] == dataset[1, 1]
    True
    >>> source[2, 0]
    Traceback (most recent call last):
    ...
    dnadna.datasets.MissingSNPSample: could not load scenario 2 replicate 0
    from "...my_model_002_000.npz": FileNotFoundError(2, 'No file matching or
    similar to')
    """

    name = 'dnadna'

    DEFAULT_NPZ_FILENAME_FORMAT = \
            'scenario_{scenario}/{dataset_name}_{scenario}_{replicate}.npz'
    """
    Default format string for filenames relative to the ``root_dir`` of
    an `NpzSNPSource`.

    This is the default filesystem layout for the :ref:`DNADNA format
    <dataset-formats-dnadna>`.  Each scenario has its own directory named
    ``scenario_<scenario_idx>`` where the ``scenario_idx`` is typically
    zero-padded the correct amount for the total number of scenarios in the
    dataset.

    Each simulation file in a scenario has the filename
    ``<model-name>_<scenario_idx>_<replicate_idx>.npz`` where both
    ``scenario_idx`` and ``replicate_idx`` are again zero-padded an appropriate
    amount.

    In a simulation config with the option ``{"data_source": {"format":
    "dnadna"}}``, this default filename format can be overridden with the
    ``{"data_source": {"filename_format": "..."}}`` option.
    """

    def __init__(self, root_dir, dataset_name, filename_format=None,
                 keys=('SNP', 'POS'), position_format=None, lazy=True):
        self.root_dir = pathlib.Path(root_dir)
        self.dataset_name = dataset_name

        # Normalize path separators to UNIX style
        self.filename_format = (filename_format or
                self.DEFAULT_NPZ_FILENAME_FORMAT).replace('\\', '/')

        # Create a regular expression against which files in this dataset
        # must match
        self.filename_re = re.compile('^' + format_to_re(
            self.filename_format,
            dataset_name=r'\w+',
            scenario=(r'(?P<scenario>0*\d+)', r'0*\d+'),
            replicate=(r'(?P<replicate>0*\d+)', r'0*\d+')) + '$')

        self.keys = keys
        self.position_format = position_format
        self.lazy = lazy

        parsed_format = parse_format(self.filename_format)

        if (all(not f[0] for f in parsed_format.get('scenario', [])) and
                all(not f[0] for f in parsed_format.get('replicate', []))):
            # There is no format spec specified for either scenario or
            # replicate fields in the filename format: This indicates that we
            # should "guess" the zero-padding of that field, if any.
            #
            # Otherwise, if a format spec is given for any of those fields we
            # assume all bets are off and use the user-specified format exactly
            self._guessed_format = None
        else:
            self._guessed_format = filename_format

    @classmethod
    def from_config(cls, config, validate=True):
        """
        Instantiate an `NpzSNPSource` from a simulation
        `~dnadna.utils.config.Config` matching the :ref:`simulation schema
        <schema-simulation>`.
        """

        config = Config(config, schema='dataset', validate=validate)

        # These extra checks are not necessary if the config was validated
        # against the schema, but we add them for extra care in case it wasn't
        data_source = config.get('data_source')
        if not data_source:
            raise ValueError(
                f'{cls.__name__}.from_config must be passed a config object '
                f'containing a data_source key')

        if data_source.get('format') != 'dnadna':
            raise ValueError(
                f'{cls.__name__}.from_config must be passed a config object '
                f'with the "dnadna" format in its data source; got:\n'
                f'{pprint.pformat(data_source)}')

        return cls(config['data_root'], config['dataset_name'],
                   filename_format=data_source.get('filename_format'),
                   keys=data_source.get('keys'),
                   position_format=data_source.get('position_format'))

    def __getitem__(self, scenario_replicate):
        scenario, replicate = scenario_replicate
        filename = None
        try:
            # Try to open the file, so that if it does not exist a
            # FileNotFoundError is still raised even if self.lazy=True
            filename = self._get_filename(scenario, replicate)
            with open(filename, 'rb') as fobj:
                return SNPSample.from_npz(fobj, keys=self.keys,
                                          pos_format=self.position_format,
                                          lazy=self.lazy)
        except Exception as exc:
            # As in FileNotFoundError
            filename = getattr(exc, 'filename', filename)
            raise MissingSNPSample(scenario, replicate, filename, reason=exc)

    def __iter__(self):
        """
        Iterate over all files found in the data source and return their
        associated ``(scenario_idx, replicate_idx)`` tuple.

        Note: This does *not* necessarily return all files in lexicographic
        order, as it depends on the order in which `os.walk` returns files.
        """

        for scenario_idx, replicate_idx, _ in self._iter_dataset_files():
            yield (scenario_idx, replicate_idx)

    def __contains__(self, scenario_replicate):
        """
        Returns True if the sample specified by scenario and replicate number
        exists in the data source, and False otherwise.

        This can be used to check for existence without fully loading the data.

        Examples
        --------

        >>> from dnadna.datasets import NpzSNPSource
        >>> from dnadna.snp_sample import SNPSample
        >>> tmp = getfixture('tmp_path')  # pytest-specific

        Create a dummy sample file:

        >>> filename = NpzSNPSource.DEFAULT_NPZ_FILENAME_FORMAT.format(
        ...     dataset_name='MyModel', scenario=0, replicate=0)
        >>> (tmp / filename).parent.mkdir()
        >>> SNPSample([[1, 0], [1, 0]], [0, 1]).to_npz(tmp / filename)

        Check that it exists, and that some other arbitrary sample doesn't:

        >>> snp_source = NpzSNPSource(tmp, 'MyModel')
        >>> (0, 0) in snp_source
        True
        >>> (42, 66) in snp_source
        False
        """

        scenario, replicate = scenario_replicate
        try:
            self._get_filename(scenario, replicate)
        except FileNotFoundError:
            return False
        else:
            return True

    def _iter_dataset_files(self, scenario_format=r'\d+',
                            replicate_format=r'\d+'):
        """
        Iterate recursively over all filenames in the simulation data root
        directory and match them against the filename format for the data
        source.

        The ``scenario_format`` and ``replicate_format`` arguments are used
        by the ``_guess_filename`` method to filter for files matching specific
        scenario/replicate indices.

        Yields tuples of ``(scenario_idx, replicate_idx, filename)``.
        """

        # TODO: This routine might be useful for more than just NPZ files, but
        # as it is the only SNPSource type for now it lives here.

        # First split the filename format into directory components; this
        # allows avoiding recursing into non-matching sub-directories during
        # os.walk()
        format_parts = self.filename_format.split(pth.sep)

        # Convert these to tuples with a named group for the first match;
        # see the docs for format_to_re
        scenario_format = (f'(?P<scenario>{scenario_format})', scenario_format)
        replicate_format = (f'(?P<replicate>{replicate_format})',
                            replicate_format)

        part_res = [
            re.compile(format_to_re(
                format_part, dataset_name=r'\w+',
                scenario=scenario_format, replicate=replicate_format))
            for format_part in format_parts]

        for curdir, dirnames, filenames in os.walk(self.root_dir):
            # Omit the root_dir from curdir
            curdir = curdir[(len(str(self.root_dir)) + 1):]

            depth = 0 if not curdir else curdir.count(pth.sep) + 1
            if depth == len(format_parts) - 1:
                # No need to recurse any deeper
                del dirnames[:]
                for filename in sorted(filenames):
                    m = part_res[-1].match(filename)
                    if m:
                        # If we find any files matching the format we take the
                        # first one we find; the rest are assumed to follow the
                        # same pattern--if not this an error in the data.
                        # Perhaps later we could add an option for more
                        # flexibility on this, but it would also be necessarily
                        # slower.
                        filename = pth.join(curdir, filename)
                        scenario_idx = int(m.group('scenario'))
                        replicate_idx = int(m.group('replicate'))
                        yield (scenario_idx, replicate_idx, filename)
            else:
                # Do not recurse into subdirectories at the current
                # depth that do not match the format
                part_re = part_res[depth]
                dirnames[:] = [d for d in dirnames if part_re.match(d)]
                dirnames.sort()

    def _get_filename(self, scenario, replicate):
        """Get the filename for the given scenario and replicate numbers."""

        # First check whether the file exists using the given filename format
        # (e.g. if zero-padding is not used at all); in this case the question
        # of whether or not zero-padding is used at all by the dataset is
        # inconclusive
        if self._guessed_format is not None:
            filename_fmt = self._guessed_format
        else:
            filename_fmt = self.filename_format

        filename = filename_fmt.format(
                dataset_name=self.dataset_name,
                scenario=scenario,
                replicate=replicate)

        # Micro-optimization: joining paths with pathlib is *slow*, and it adds
        # up over ~millions of files; using string concatenation here can save
        # several minutes of processing time over a long training run
        # filename = self.root_dir / filename
        filename = str(self.root_dir) + os.sep + filename

        if pth.isfile(filename):
            return filename
        elif self._guessed_format:
            # We have already tried the guessed format so bail out early
            raise FileNotFoundError(errno.ENOENT,
                'No file matching or similar to', filename)
        else:
            # Try guessing the filename format (e.g. if it uses zero padding)
            return self._guess_filename(scenario, replicate)

    def _guess_filename(self, scenario, replicate):
        """
        Using a sample scenario index and replicate index (which are assumed to
        exist in the data set) attempt to guess the real filename without
        knowing how much zero-padding is used in those fields (if any).

        If no appropriate matching file is found then the file is assumed not
        to exist at all, so a `FileNotFound` exception is raised.
        """

        # This creates a regular expression for filenames that have zero-padded
        # scenario indices and replicate indices.  In order to detect
        # zero-padding there must be at least one file in which a number starts
        # with zero but contains non-zero digits (i.e. we ignore numerals like
        # '0')

        filename_iter = self._iter_dataset_files(
                scenario_format=f'0*{scenario}',
                replicate_format=f'0*{replicate}')

        try:
            # If any files match it should be the only one returned by the
            # iterator
            _, _, matching_filename = next(filename_iter)
        except StopIteration:
            raise FileNotFoundError(errno.ENOENT,
                'No file matching or similar to',
                self.filename_format.format(
                    dataset_name=self.dataset_name, scenario=scenario,
                    replicate=replicate))

        # Now build a regexp over the entire filename format
        format_re = re.compile(format_to_re(
            self.filename_format,
            dataset_name=r'\w+',
            scenario=(rf'(?P<scenario>0*{scenario})', rf'0*{scenario}'),
            replicate=(rf'(?P<replicate>0*{replicate})',
                       rf'0*{replicate}')))

        # Use it to extract the scenario and replicate fields to determine the
        # zero-padding use for them; it should already be assumed to match if
        # we made it here
        match = format_re.match(matching_filename)
        s_idx = match.group('scenario')
        r_idx = match.group('replicate')
        s_padding = 0
        r_padding = 0

        if len(s_idx) > 1 and s_idx[0] == '0':
            # Ensure that the index is actually zero-padded; if not
            # then this data set does not use zero-padding for the
            # index
            s_padding = len(s_idx)

        if len(r_idx) > 1 and r_idx[0] == '0':
            r_padding = len(r_idx)

        if s_padding and r_padding:
            # If neither number in the filename contained zero padding we
            # cannot accurately guess whether or not zero padding is used;
            # this will be checked again with a later filename.
            self._guessed_format = reformat_format(self.filename_format,
                    format_replacements={'scenario': f'0{s_padding}',
                                         'replicate': f'0{r_padding}'})

        return self.root_dir / matching_filename


class DictSNPSource(SNPSource):
    """
    SNP source that reads from a JSON-like data structure consisting of a dict
    with ``(simulation, replicate)`` pairs for keys, and `SNPSamples
    <dnadna.snp_sample.SNPSample>` in JSON-compatible format for values (see
    `~dnadna.snp_sample.DictSNPConverter.to_dict`).

    Currently used just by the test suite, but may be useful in other contexts
    as well (e.g. serialization of simulations).

    Parameters
    ----------
    scenarios : dict
        `dict` with ``(simulate, replicate)`` tuple keys, and values in the
        format output by `~dnadna.converters.DictSNPConverter.to_dict`, or
        the values may also be `~dnadna.snp_sample.SNPSample` instances
        (useful for testing).
    position_format : dict, optional
        Position format dict corresponding to the ``pos_format`` argument to
        `~dnadna.snp_sample.SNPSample` (currently all samples in the dataset
        are assumed to have the same position formats).
    filename : str, optional
        If the ``scenarios`` dict was read from a file (e.g. a JSON or YAML
        file) this can be set to the filename; this is used just as a
        convenience when reporting errors.
    lazy : bool, optional
        By default data is lazy-loaded, so that it is not converted from the
        dict format until needed.  Use ``lazy=False`` to ensure that the data
        is immediately converted.

    Examples
    --------
    >>> from dnadna.datasets import DictSNPSource
    >>> from dnadna.snp_sample import SNPSample
    >>> sample = SNPSample([[0, 1], [1, 0]], [0.1, 0.2])
    >>> source = DictSNPSource({(0, 0): sample.to_dict()},
    ...                        filename='scenario_0_0.json')
    >>> source.scenarios
    {(0, 0): {'SNP': ['01', '10'], 'POS': [0.1, 0.2]}}
    >>> (0, 0) in source
    True
    >>> source[0, 0]
    SNPSample(
        snp=tensor([[0, 1],
                    [1, 0]], dtype=torch.uint8),
        pos=tensor([0.1000, 0.2000], dtype=torch.float64),
        pos_format={'normalized': True},
        path='scenario_0_0.json'
    )

    If the requested sample doesn't exist in the dataset a `MissingSNPSample`
    exception is raised:

    >>> (0, 1) in source
    False
    >>> source[0, 1]
    Traceback (most recent call last):
    ...
    dnadna.datasets.MissingSNPSample: could not load scenario 0 replicate 1
    from "scenario_0_0.json": KeyError((0, 1))
    """

    name = 'dict'

    def __init__(self, scenarios, position_format=None, filename=None,
                 lazy=True):
        self.scenarios = scenarios
        self.position_format = position_format
        self.filename = filename
        self.lazy = lazy

    @classmethod
    def from_file(cls, filename, **kwargs):
        return cls(load_dict(filename, **kwargs), filename=filename)

    def __getitem__(self, scenario_replicate):
        scenario, replicate = scenario_replicate
        try:
            snp = self.scenarios[scenario, replicate]
            if isinstance(snp, SNPSample):
                pass
            elif isinstance(snp, dict):
                snp = SNPSample.from_dict(snp, pos_format=self.position_format,
                                          path=self.filename, lazy=self.lazy)
            else:
                raise ValueError(
                        f"SNP instances in {self.__class__.__name__} must "
                        f"be of type SNPSample or dict; got "
                        f"{type(snp).__name__} for scenario {scenario} "
                        f"replicate {replicate}")

            return snp
        except Exception as exc:
            raise MissingSNPSample(scenario, replicate, self.filename,
                                   reason=exc)

    def __iter__(self):
        """
        Iterate over all files found in the data source and return their
        associated ``(scenario_idx, replicate_idx)`` tuple.
        """

        return iter(self.scenarios.keys())

    def __contains__(self, scenario_replicate):
        """
        Returns True if the sample specified by scenario and replicate number
        exists in the data source, and False otherwise.

        This can be used to check for existence without fully loading the data.
        """

        return scenario_replicate in self.scenarios


class FileListSNPSource:
    """
    SNP source that returns scenarios from a fixed list of arbitrary files.

    Because the concepts of "scenarios" and "replicates" are not necessary
    applicable to an arbitrary list of files, each file is considered a single
    scenario of one replicate (e.g. ``source[3, 0]`` returns the contents of
    the fourth file in the list.
    """

    # TODO: Some file types may contain multiple replicates in a single file.
    # E.g. when we add support for ms files, a single ms file can contain
    # multiple replicates, as can the JSON SNP format.  In such a case, the
    # functionality of this class might change, though we need a way to specify
    # when a file type can contain multiple SNPs

    def __init__(self, filenames):
        self.filenames = filenames

    def __getitem__(self, scenario_replicate):
        scenario, replicate = scenario_replicate
        filename = None
        try:
            if replicate != 0:
                raise ValueError(
                    f'scenario {scenario} replicate {replicate} does not '
                    f'exist')
            filename = self.filenames[scenario]
            return SNPSample.from_file(filename)
        except Exception as exc:
            raise MissingSNPSample(scenario, replicate, filename,
                                   reason=exc)

    def __iter__(self):
        """
        Iterate over all files found in the data source and return their
        associated ``(scenario_idx, replicate_idx)`` tuple.
        """

        for scenario in range(len(self.filenames)):
            yield (scenario, 0)

    def __contains__(self, scenario_replicate):
        """
        Returns True if the sample specified by scenario and replicate number
        exists in the data source, and False otherwise.

        This can be used to check for existence without fully loading the data.
        """

        scenario, replicate = scenario_replicate
        if replicate != 0:
            return False

        try:
            return pth.exists(self.filenames[scenario])
        except IndexError:
            return False


class DNADataset(Dataset, ConfigMixIn):
    """
    Simplified base class for DNADNA datasets which simply maps an integer
    index to an `~dnadna.snp_sample.SNPSample` instance from the simulation
    dataset.

    This has two modes of operation: One where a ``scenario_params`` table is
    given as a `pandas.DataFrame` in the format described for the :ref:`DNADNA
    Format <dataset-formats-dnadna>`.  In this case, all the scenarios and
    replicates described in that table are returned (where they exist), and for
    each item in the dataset a ``(scenario_idx, replicate_idx, snp_sample,
    scenario_params)`` tuple is returned.

    In the second mode of operation, ``scenario_params`` is not given, and the
    data sources are simply looped over directly.  In this case a 4-tuple of
    ``(scenario_idx, replicate_idx, snp_sample, None)`` is returned for each
    item.

    The `DNATrainingDataset` is the more complete implementation which can
    perform additional transformations on the data when used in model training,
    and which keeps separate training and validation sets.

    Given a ``scenario_set=<scenario_idx>`` argument, only the data in a single
    scenario are returned; this may also be a list/set of scenario indices to
    consider.
    """

    config_schema = 'dataset'

    def __init__(self, config={}, validate=True, source=None,
                 scenario_params=None, scenario_set=None, cached_set=None):
        super().__init__(config, validate=validate)

        if source is None:
            # Load the data_source from the config
            data_source = config.get('data_source')
            if not data_source:
                raise ValueError(
                    f'{self.__class__.__name__} must be passed a config '
                    f'object containing a data_source key')
            format = data_source.get('format', 'dnadna')
            source_cls = SNPSource.get_plugin(format)
            source = source_cls.from_config(config, validate=False)

        self.source = source

        if scenario_params is None:
            # Load the scenario params DataFrame from the scenario_param_path
            scenario_params_path = config.get('scenario_params_path')
            if scenario_params_path is not None:
                scenario_params = pd.read_csv(scenario_params_path,
                                              sep=None,  # autodetect separator
                                              engine='python')  # for sep=None

                try:
                    if scenario_params.index.name != 'scenario_idx':
                        scenario_params.set_index('scenario_idx', inplace=True)
                except KeyError:
                    raise ValueError(
                        f"a column scenario_idx must exist in your scenario "
                        f"params table; the column is missing from "
                        f"{scenario_params_path}")

        self.scenario_params = scenario_params

        if scenario_set is not None:
            if not isinstance(scenario_set, (Set, Sequence)):
                scenario_set = [scenario_set]

        self.scenario_set = scenario_set
        self.cached_set = cached_set
        self._indices = {}
        self._sample_iter = None

    @classmethod
    def from_config_file(cls, filename, *args, validate=True, source=None,
                         scenario_params=None, scenario_set=None, **kwargs):
        """
        Load the `~dnanda.utils.config.Config` from a file.

        Additional ``kwargs`` are passed to `~.Config.from_file`.

        The additional keyword arguments are passed to the dict serializer, and
        the config is validated against the :ref:`dataset schema
        <schema-dataset>`.
        """

        config = Config.from_file(filename, schema=cls.config_schema,
                                  validate=validate, **kwargs)
        # if validate=True was given we have already validated the config
        # if validate=False was given we don't want to validate the config in
        # from_config either
        return cls(config, validate=False, source=source,
                   scenario_params=scenario_params, scenario_set=scenario_set)

    def __len__(self):
        """
        Return the total length of the data set, accounting for missing samples
        if ``self.ignore_missing == True``.

        This must iterate over all samples in order to count.
        """

        self._cache_all_indices()
        return len(self._indices)

    def __getitem__(self, index):
        scenario_idx, replicate_idx = self._get_index(index)
        scenario_params = None
        cache = False
        if self.cached_set and index in self.cached_set:
            value = self.cached_set[index]
            if value is None:
                cache = True
            else:
                return value

        try:
            snp_sample = self.source[scenario_idx, replicate_idx]
        except Exception as exc:
            if self.config.get('ignore_missing', False):
                # Just produce a warning for the missing sample
                warnings.warn(
                    f'missing sample scenario {scenario_idx} replicate '
                    f'{replicate_idx} in the dataset: {exc}; returning None',
                    DNADNAWarning)
                snp_sample = None
            else:
                raise

        if self.scenario_params is not None:
            scenario_params = self.scenario_params.loc[scenario_idx]

        value = (scenario_idx, replicate_idx, snp_sample, scenario_params)
        if cache:
            self.cached_set[index] = value

        return value

    def __getstate__(self):
        """
        Datasets are sometimes pickled for the purposes of multiprocessing.

        ``self._sample_iter`` cannot be pickled, if set, since it is a
        generator, so we exclude it from the Dataset state, and make allowances
        to ensure it can be 'resumed' where it left off if ``self._indices`` is
        non-empty.
        """

        state = self.__dict__.copy()
        state['_sample_iter'] = None
        return state

    @property
    def cached_set(self):
        """Indices whose samples should be cached in memory."""

        return self.__dict__.setdefault('_cached_set', {})

    @cached_set.setter
    def cached_set(self, value):
        # Initialize the internal _cached_set dict with keys from the set of
        # indices to be cached
        if value is None:
            self._cached_set = {}
        else:
            self._cached_set = dict.fromkeys(value)

    def _cache_next_index(self):
        if self._sample_iter is None:
            self._sample_iter = self._iter_samples()

        next_idx, value = next(self._sample_iter)
        self._indices[next_idx] = value
        return next_idx, value

    def _cache_all_indices(self):
        """Ensure all indices have been checked and cached."""

        while True:
            try:
                self._cache_next_index()
            except StopIteration:
                break

    def _get_index(self, index):
        """
        Get the ``(scenario_idx, replicate_idx)`` for a given integer index.

        This is looked up in ``self._indices`` first, and if not found, we
        lazily iterate through ``self._sample_iter`` to get the next index.
        """

        if index in self._indices:
            return self._indices[index]

        while True:
            try:
                next_idx, value = self._cache_next_index()
                if next_idx == index:
                    return value
            except StopIteration:
                # We've exhausted all available samples, so the given index does
                # not exist
                raise IndexError(
                        f'{self.__class__.__name__} index out of range')

    def _iter_scenario_replicates(self):
        """
        Return the scenario index, and replicate index for each scenario
        replicate in the dataset.
        """

        if self.scenario_params is not None:
            # iterate over all scenario indicies and replicate indices given by
            # the scenario_params table
            def iter_scenarios():
                for scenario in self.scenario_params.itertuples():
                    scenario_idx = scenario.Index
                    for replicate_idx in range(int(scenario.n_replicates)):
                        yield (scenario_idx, replicate_idx)
        else:
            # otherwise, the data source itself tells us what
            # scenarios/replicates it has
            def iter_scenarios():
                return iter(self.source)

        for scenario_idx, replicate_idx in iter_scenarios():
            if self.scenario_set and scenario_idx not in self.scenario_set:
                continue

            yield (scenario_idx, replicate_idx)

    def _iter_samples(self):
        """
        Iterates over each replicate for each scenario in dataset in order.

        This wraps `DNADatset._iter_scenario_replicates` to perform additional
        checks, such as whether the simulation exists, and finally assigns a
        single index number to each simulation.

        For each scenario_idx/replicate_idx pair it checks if that sample is
        actually available in the given data source.  If not an error is
        raised, unless ``self.ignore_missing == True``.
        """

        idx = 0
        for idx_pair in self._iter_scenario_replicates():
            # Skip indices that have already been produced; this can be the
            # case after restoring from a pickle
            if idx in self._indices:
                idx += 1
                continue

            if not self.config.get('ignore_missing', False):
                # Missing samples will not be allowed, so we check now if
                # the file exists in the source
                if idx_pair not in self.source:
                    # Look up the missing sample in the source and raise
                    # whatever execption the source would raise in case of a
                    # missing sample (e.g. FileNotFoundError, etc.)
                    self.source[idx_pair]

            yield (idx, idx_pair)
            idx += 1


class DatasetTransformationMixIn(DNADataset):
    """
    Partially implemented `~torch.utils.data.Dataset` which accepts parameters
    for transforming the SNP data returned from the data source.

    Parameters
    ----------

    transforms : `list`
        `list` giving transform names or transform descriptions (a transform
        name plus its parameters) as specified in the ``dataset_transforms``
        property in the training config file.  See also ref:`schema-training`.
        May also contain instances of `~dnadna.transforms.Transform`.
    param_set : `.ParamSet`
        `.ParamsSet` object representing all the details of the parameters
        to learn in training, including the values of those parameters for the
        training and validation sets (the pre-processed scenario params);
        information about the parameters can be used by some transforms.

    Additional positional and keyword arguments are passed to
    ``super().__init__()`` so that this can be used as a mix-in with arbitrary
    `DNADataset` subclasses.
    """

    def __init__(self, config, transforms=None, param_set=None, **kwargs):
        super().__init__(config, **kwargs)
        self.transforms = transforms
        self.param_set = param_set

        # TODO: This is required to be present for training, but this fact
        # isn't made very explicit except in the code.  It might be good to
        # explicitly validate the format of preprocessed_scenario_params
        # somehow.
        if self.scenario_params is not None:
            self.splits = self.scenario_params.get('splits')
        else:
            self.splits = None

        # These are only filled if a splits series is given (the splits column
        # from the pre-processed scenario params)
        self._split_scenario_sets = {
            'training': set(),
            'validation': set(),
            'test': set()
        }
        self._cache_validation_set = self.config.get('cache_validation_set',
                                                     False)

    @property
    def training_set(self):
        """Set of indices to use for training."""
        self._cache_all_indices()
        return frozenset(self._split_scenario_sets['training'])

    @property
    def validation_set(self):
        """Set of indices to use for validation."""
        self._cache_all_indices()
        return frozenset(self._split_scenario_sets['validation'])

    @property
    def test_set(self):
        """Set of indices to use for testing."""
        self._cache_all_indices()
        return frozenset(self._split_scenario_sets['test'])

    def __getitem__(self, index):
        item = super().__getitem__(index)
        scenario_idx, replicate_idx, sample, scenario = item

        # Here is another case where `sample` can be `None` if
        # `ignore_missing=True` and the sample failed to be loaded; in this
        # case we just return immediately since the rest of this function deals
        # with the sample
        if sample is None:
            return item

        if scenario is not None and self.param_set is not None:
            # Limit the scenario Series to just the parameter values
            scenario = \
                scenario.loc[self.param_set.param_names].astype(np.float64)

        transforms = None

        if self.transforms:
            if isinstance(self.transforms, dict):
                # Per-dataset split transforms
                for split, scenarios in self._split_scenario_sets.items():
                    if scenario_idx in scenarios:
                        transforms = self.transforms.get(split)
            else:
                transforms = self.transforms

        if transforms is not None:
            transform_args = (sample, self.param_set, scenario)
            try:
                sample, _, scenario = transforms(transform_args)
            except TransformException as exc:
                warnings.warn(
                    f'an exception occurred evaluating {exc.transform} on '
                    f'scenario {scenario_idx} replicate {replicate_idx}: '
                    f'{exc.__cause__!r}; it will be excluded from the batch',
                    DNADNAWarning)

                # Exclude this sample by returning None
                return scenario_idx, replicate_idx, None, scenario

        # Return target parameter values as double-precision floats, so that
        # precision does not need to be thrown away until necessary.
        # TODO: Perhaps make this an option for the DNATrainingDataset, whether
        # it returns single- or double-precision floats, since sometimes it
        # might reduce overhead to use single-precision only
        if scenario is not None:
            target = torch.from_numpy(scenario.to_numpy())
        else:
            target = None

        return scenario_idx, replicate_idx, sample, target

    @property
    def transforms(self):
        """
        The composed set of transforms to apply to the dataset.

        Either `dnadna.transforms.Compose` or a dict mapping dataset splits
        ("training", "validation", "test") to their corresponding
        `~dnadna.transforms.Compose` of transforms.
        """

        return self._transforms

    @transforms.setter
    def transforms(self, transforms):
        if transforms is None:
            self._transforms = None
            return

        if isinstance(transforms, list):
            xfs = self._compose_transforms(transforms)
        else:
            xfs = {k: self._compose_transforms(v)
                   for k, v in transforms.items()}

        self._transforms = xfs

    def _compose_transforms(self, transforms):
        """
        Given a list of transforms from a config, initialize each transform and
        return a composition of them in the form of a
        `dnadna.transforms.Compose`.
        """

        xfs = []
        for transform in transforms:
            try:
                if isinstance(transform, str):
                    # Transform with no arguments given as just the name
                    transform_cls = Transform.get_plugin(transform)
                    transform = transform_cls()
                elif isinstance(transform, dict):
                    # It should be a single item dict mapping the transform
                    # name to its parameter(s)
                    name, params = next(iter(transform.items()))
                    transform_cls = Transform.get_plugin(name)
                    if not isinstance(params, dict):
                        # The transform takes a single argument, and was passed
                        # a single argument here
                        transform = transform_cls(params)
                    else:
                        sig = signature(transform_cls)
                        transform_params = list(sig.parameters)
                        # if the transform takes a single argument and that
                        # argument's name is not in the passed in params, then
                        # we may guess that the transform's first argument is
                        # itself a dict
                        if (len(transform_params) == 1 and
                                transform_params[0] not in params):
                            transform = transform_cls(params)
                        else:
                            transform = transform_cls(**params)
                elif isinstance(transform, Transform):
                    pass
                else:
                    raise ValueError(f'invalid transform: {transform}')
            except KeyError as exc:
                raise ValueError(f'unknown transform: {exc.args[0]}')

            xfs.append(transform)

        if xfs:
            xfs = Compose(xfs)
        else:
            xfs = None

        return xfs

    @staticmethod
    def collate_batch(batch):
        """
        Specifies how multiple scenario samples are collated into batches.

        Each batch element is a single element as returned by
        ``DNATrainingDataset.__getitem__``: ``(scenario_idx, replicate_idx,
        snp_sample, target)``.

        For input samples and targets are collated into batches "vertically",
        so that the size of the first dimension represents the number of items
        in a batch.

        Examples
        --------

        >>> import torch
        >>> from dnadna.datasets import DNATrainingDataset
        >>> from dnadna.snp_sample import SNPSample
        >>> fake_snps = [torch.rand(3, 3 + i) for i in range(5)]
        >>> fake_snps = [SNPSample(s[1:], s[0]) for s in fake_snps]
        >>> fake_params = [torch.rand(4, dtype=torch.float64) for _ in range(5)]
        >>> fake_batch = list(zip(range(5), [0] * 5, fake_snps, fake_params))
        >>> collated_batch = DNATrainingDataset.collate_batch(fake_batch)
        >>> scenario_idxs, inputs, targets = collated_batch
        >>> bool((torch.arange(5) == scenario_idxs).all())
        True
        >>> inputs.shape  # last dim should be num SNPs in largest fake SNP
        torch.Size([5, 3, 7])
        >>> bool((inputs[0,:3,:3] == fake_snps[0].tensor).all())
        True
        >>> bool((inputs[0,3:,3:] == -1).all())
        True
        >>> bool((inputs[-1] == fake_snps[-1].tensor).all())
        True
        >>> targets.shape
        torch.Size([5, 4])
        >>> [bool((fake_params[bat].float() == targets[bat]).all())
        ...  for bat in range(targets.shape[0])]
        [True, True, True, True, True]
        """

        # filter any missing samples out of the batch
        batch = list(filter(lambda it: it[2] is not None, batch))

        # we have to consider the possibility of an empty batch (which could
        # happen if batch_size=1 and the sample was missing)
        if not batch:
            return None

        scen_idxs, _, samples, targets = zip(*batch)

        # add padding so that all input SNPs are the same size and shape
        # (though should all have the same number of rows, but may have
        # different number of SNPs (columns)
        # the value -1 is used for padded regions
        # TODO: Question: Must nets explicitly account for this padding, and if
        # so, how?  ReLU?
        # NOTE: This extra step of filling unevenly-sized matrices with -1
        # is unnecessary if we are using a dataset with uniform=True, so
        # there should be an option to skip this step entirely.  For now we
        # just check if all inputs are the same size
        inputs = [s.tensor for s in samples]
        example_shape = inputs[0].shape
        if any(inp.shape != example_shape for inp in inputs):
            max_ind_batch = np.max([inp.shape[0] for inp in inputs])
            max_snp_batch = np.max([inp.shape[1] for inp in inputs])
            new_inputs_shape = (len(batch), max_ind_batch, max_snp_batch)
            new_inputs = torch.full(new_inputs_shape, -1, dtype=torch.float)
            for idx, inp in enumerate(inputs):
                # NOTE: I feel like there should be a more efficient way to fill an
                # N-D tensor for a sequence of (N - 1)-D tensors, but at the moment
                # I can't find it; to revisit
                new_inputs[idx, :inp.shape[0], :inp.shape[1]] = inp
        else:
            # Just stack the inputs
            new_inputs = torch.stack(inputs).float()

        # Concatenate targets and ensure they are converted to single-precision
        # floats for passing to GPU devices
        # NOTE: targets can be all None if the Dataset was initialized without
        # scenario_params
        if targets[0] is not None:
            n_parameters = len(targets[0])
            targets = torch.cat(targets).reshape(-1, n_parameters).float()

        return [torch.tensor(scen_idxs, dtype=torch.long), new_inputs, targets]

    def _iter_samples(self):
        """
        Iterates over each replicate for each scenario in
        ``self.learned_params.scenario_params`` in order.

        For each scenario_idx/replicate_idx pair it checks if that sample is
        actually available in the given data source.  If not an error is
        raised, unless ``self.ignore_missing == True``.
        """

        for idx, (scenario_idx, replicate_idx) in super()._iter_samples():
            # Add indices to the training and validation sets; by the time this
            # code is reached the index is known to refer to a valid simulation
            # in the dataset
            if self.splits is not None:
                split = self.splits.loc[scenario_idx]

                # NOTE: This code could easily be generalized to support more
                # than just hard-coded split names, but right now we always
                # have just training/validation/test
                if split in self._split_scenario_sets:
                    self._split_scenario_sets[split].add(idx)

                # TODO: Perhaps allow caching of other dataset splits as well;
                # right now it's just supported for validation as a special
                # case.
                if split == 'validation':
                    if self._cache_validation_set:
                        # Prime the cache for this index; the cache mechanism
                        # will only cache indices for which there is an
                        # explicit key already in the cache dict
                        self.cached_set[idx] = None

            yield idx, (scenario_idx, replicate_idx)


class DNATrainingDataset(DatasetTransformationMixIn):
    config_schema = 'training'

    def __init__(self, config={}, validate=True, source=None,
                 scenario_params=None, transforms=None, learned_params=None):
        """
        Parameters
        ----------
        source : `.SNPSource`, optional
            The `.SNPSource` from which the data is loaded.  Overrides the
            value from the config, if given.
        scenario_params : `pandas.DataFrame`, optional
            Optionally override the scenario params table; if not given it is
            taken from the ``learned_params.scenario_params``.
        learned_params : `.LearnedParams`
            `.LearnedParams` object representing all the details of the
            parameters to learn in training, including the values of those
            parameters for the training and validation sets (the pre-processed
            scenario params).  Overrides the value from the config, if given.
        """

        if transforms is None:
            transforms = config.get('dataset_transforms')

        if scenario_params is None and learned_params is not None:
            # get scenario_params from learned_params
            scenario_params = learned_params.scenario_params

        if validate:
            # Validate the config against the 'training' schema before passing
            # it to the base class (which uses the 'dataset' schema)
            config.validate()

        super().__init__(config.get('dataset', {}), validate=False,
                         source=source, scenario_params=scenario_params,
                         transforms=transforms)

        if learned_params is None:
            learned_params = config.get('learned_params')
            if learned_params is None:
                raise ValueError(
                    f'{self.__class__.__name__} must be passed a config '
                    f'object object containing a learned_params key')

            learned_params = LearnedParams(learned_params,
                                           self.scenario_params,
                                           validate=False)

        self.param_set = self.learned_params = learned_params

    @classmethod
    def from_config_file(cls, filename, validate=True, source=None,
                         scenario_params=None, transforms=None,
                         learned_params=None, **kwargs):
        """
        Load the `~dnanda.utils.config.Config` from a file.

        Additional ``kwargs`` are passed to `~.Config.from_file`.

        The additional keyword arguments are passed to the dict serializer, and
        the config is validated against the :ref:`training schema
        <schema-training>`.
        """

        config = Config.from_file(filename, schema=cls.config_schema,
                                  validate=validate, **kwargs)
        # if validate=True was given we have already validated the config
        # if validate=False was given we don't want to validate the config in
        # from_config either
        return cls(config, validate=False, source=source,
                   scenario_params=scenario_params, transforms=transforms,
                   learned_params=learned_params)
