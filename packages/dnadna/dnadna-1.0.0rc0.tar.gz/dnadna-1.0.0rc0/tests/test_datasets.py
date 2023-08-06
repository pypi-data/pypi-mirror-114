import hashlib
import os
import os.path as pth
from contextlib import nullcontext
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import torch
from torch.utils.data import DataLoader

from dnadna import DNADNAWarning
from dnadna.datasets import (DictSNPSource, NpzSNPSource, DNADataset,
        DNATrainingDataset)
from dnadna.examples import one_event
from dnadna.params import LearnedParams
from dnadna.snp_sample import SNPSample
from dnadna.transforms import ValidateSnp
from dnadna.utils.misc import zero_pad_format


@pytest.fixture(scope='module')
def dummy_simulation(tmp_path_factory):
    """
    Fixture returning a function which produces a directory of dummy
    simulations in NPZ format.

    The idea is that the contents of the data are irrelevant, just the format.
    """

    tmpdir = tmp_path_factory.mktemp('dummy_simulations')

    def _make_dummy_simulation(n_scenarios=15, n_replicates=15,
                               keys=('SNP', 'POS'), n_indiv=10, n_snp=10,
                               dataset_name=None, filename_format=None):
        simulation_key = ((n_scenarios, n_replicates) + tuple(keys) +
            (n_indiv, n_snp, dataset_name, filename_format))
        simulation_hash = hashlib.md5(str(simulation_key).encode('utf8'))
        simulation_dirname = simulation_hash.hexdigest()
        simulation_dir = tmpdir / simulation_dirname

        if simulation_dir.exists():
            return simulation_dir

        config = one_event.DEFAULT_ONE_EVENT_CONFIG

        if dataset_name is None:
            dataset_name = config['dataset_name']

        if filename_format is None:
            filename_format = config['data_source']['filename_format']

        filename_format = zero_pad_format(filename_format,
                scenario=n_scenarios, replicate=n_replicates)

        # Generate the fake simulation
        # TODO: Use SNPSample for this once it's able to write to files
        # NOTE: Use of an identity matrix here is arbitrary.
        snp = np.identity(max(n_indiv, n_snp))[:n_indiv, :n_snp]
        pos = np.arange(n_snp)
        data = {keys[0]: snp, keys[1]: pos}

        for s_idx, r_idx in product(range(n_scenarios), range(n_replicates)):
            filename = filename_format.format(dataset_name=dataset_name,
                    scenario=s_idx, replicate=r_idx)
            filepath = simulation_dir / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(simulation_dir / filename, **data)

        return simulation_dir

    return _make_dummy_simulation


def test_dummy_simulation(dummy_simulation):
    """Test the dummy_simulation fixture itself."""

    simulation_dir = dummy_simulation()
    file_count = 0
    # There should be 225 .npz files
    for curdir, dirs, files in os.walk(simulation_dir):
        file_count += len([f for f in files if f.endswith('.npz')])

    assert file_count == 15 ** 2

    # Try opening a few files that should exist
    samples = [(0, 0), (5, 7), (14, 14)]
    pos = np.arange(10)

    for s_idx, r_idx in samples:
        filename = f'scenario_{s_idx:02}/one_event_{s_idx:02}_{r_idx:02}.npz'

        with np.load(simulation_dir / filename) as npz_data:
            assert (npz_data['POS'] == pos).all()
            assert (npz_data['SNP'] == np.identity(10)).all()


def test_npz_snp_source(dummy_simulation):
    """
    Basic test of `dnadna.datasets.NpzSNPSource`.

    Includes guessing of filename padding.
    """
    simulation_dir = dummy_simulation()

    npz_snp_source = NpzSNPSource(simulation_dir,
            one_event.DEFAULT_ONE_EVENT_CONFIG['dataset_name'])

    # See the note in dummy_simulation on how position arrays are used to
    # identify that the correct file was loaded
    # NOTE: On Windows the default integer type for Numpy is still 32-bit for
    # some reason, while on Linux it defaults to 64-bit.  So we use from_numpy
    # here to ensure it uses the same dtype Numpy would use
    pos = torch.from_numpy(np.arange(10))

    # Just test that a few sample files can be loaded
    for scenario, replicate in [(0, 0), (5, 7), (14, 14)]:
        snp = npz_snp_source[scenario, replicate]
        assert isinstance(snp, SNPSample)
        assert (snp.snp == torch.eye(10, dtype=torch.uint8)).all()
        assert (snp.pos == pos).all()


def test_dna_dataset_without_scenario_params(dummy_simulation):
    """
    Test the ``scenario_params=None`` mode of `dnadna.dataset.DNADataset`.
    """

    # Make a dummy simulation with 3 scenarios and 4 replicates per scenario,
    # so there should be 12 simulations in the full dataset; these numbers
    # were just picked at arbitrary for testing purposes
    simulation_dir = dummy_simulation(n_scenarios=3, n_replicates=4,
                                      dataset_name='dummy')

    source = NpzSNPSource(simulation_dir, 'dummy')

    # iterating over the data source should return the product of all scenario
    # indices with all replicate indices
    assert sorted(source) == list(product(range(3), range(4)))

    # Create a DNADataset from this source with no scenario_params and check
    # that all items and returned when iterating over it
    dataset = DNADataset(validate=False, source=source)
    assert len(list(dataset)) == 12


def test_dna_training_dataset(dummy_simulation):
    """
    Basic test of `dnadna.dataset.DNATrainingDataset`.

    Tests loading samples from a few indices, and the data set size.
    """

    # TODO: Most of this setup code can be moved into a utility function or
    # fixture for reuse in other tests of DNATrainingDataset.
    n_scenarios = 10
    n_replicates = 10

    config = one_event.DEFAULT_ONE_EVENT_CONFIG
    dataset_name = config['dataset_name']

    # Arbitrary subset of parameters to output from the Dataset
    params = {p: {'type': 'regression'} for p in
              ['recombination_rate', 'mutation_rate', 'event_size']}

    simulation_dir = dummy_simulation(n_scenarios, n_replicates)

    # Don't generate a full simulation; just used to create some dummy
    # scenario parameters
    simulator = one_event.OneEventSimulator({
        'n_scenarios': n_scenarios, 'n_replicates': n_replicates})
    scenario_params = simulator.generate_scenario_params()

    source = NpzSNPSource(simulation_dir, dataset_name)
    learned_params = LearnedParams(params, scenario_params)
    dataset = DNATrainingDataset(validate=False, source=source,
                                 learned_params=learned_params)

    # Fake SNP matrix and positions to test against
    snp = torch.eye(10, dtype=torch.uint8)

    # NOTE: On Windows the default integer type for Numpy is still 32-bit
    # for some reason, while on Linux it defaults to 64-bit.
    # So we use from_numpy here to ensure it uses the same dtype Numpy
    # would use
    pos = torch.from_numpy(np.arange(10))

    assert len(dataset) == 100

    # Test a handful of indices:
    for idx in [0, 42, 99]:
        # We have 10 scenarios with 10 replicates each and no missing samples,
        # so this invariant should hold:
        expected_scenario_idx = idx // 10
        expected_replicate_idx = idx % 10

        expected_sample = torch.cat((pos.unsqueeze(0), snp.to(pos.dtype)))
        expected_scenario_params = scenario_params.loc[expected_scenario_idx]

        # NOTE: the LearnedParams ulimately determines the parameter *order*
        # so make sure to use LearnedParams.param_names here
        expected_scenario_param_values = \
                expected_scenario_params[learned_params.param_names].values
        expected_target = \
                torch.tensor(expected_scenario_param_values)

        scenario_idx, replicate_idx, sample, target = dataset[idx]

        assert scenario_idx == expected_scenario_idx
        assert replicate_idx == expected_replicate_idx
        assert bool((sample.tensor == expected_sample).all())
        assert bool((target == expected_target).all())


def nonuniform_dataset(nonuniformity='snp', n_scenarios=1,
                       validate_uniform_shape=True):
    """
    Helper function to create a ``DNATrainingDataset`` containing some
    ``SNPSamples`` that are non-uniform in shape.

    The ``nonuniformity`` argument cant be either ``'snp'``, ``'indiv'``, or
    ``'both'``.
    """

    if validate_uniform_shape:
        transforms = [ValidateSnp(uniform_shape=True)]
    else:
        transforms = None

    # create a small dataset with a couple non-uniform SNPs.  Non-uniform here
    # meaning some of the SNPs do not have the same dimensions, either in
    # number of SNPs or number of individuals; first we test non-uniformity in
    # SNP sites
    data = {}

    for s_idx in range(n_scenarios):
        r_idx = 0
        data[(s_idx, r_idx)] = SNPSample([[0, 0], [0, 1]], [0.1, 0.2])
        r_idx += 1
        if nonuniformity in ('snp', 'both'):
            data[(s_idx, r_idx)] = SNPSample(
                [[0, 0, 0], [0, 1, 0]],
                [0.1, 0.2, 0.3]
            )
            r_idx += 1

        if nonuniformity in ('indiv', 'both'):
            data[(s_idx, r_idx)] = SNPSample(
                [[0, 0], [0, 1], [1, 0]],
                [0.1, 0.2]
            )
            r_idx += 1

    source = DictSNPSource(data)

    # Minimal valid LearnedParams; perhaps there should be a shortcut for
    # this, including supporting zero parameters (only useful for testing)
    params = {'param1': {'type': 'regression'}}
    scenario_params = pd.DataFrame({
        'scenario_idx': list(range(n_scenarios)),
        'param1': [0.0] * n_scenarios,
        'n_replicates': [r_idx] * n_scenarios
    })
    learned_params = LearnedParams(params, scenario_params)
    dataset = DNATrainingDataset(validate=False, source=source,
                                 learned_params=learned_params,
                                 transforms=transforms)
    return source, dataset


def test_invalid_uniform_dataset():
    """
    Regression test for issue #32

    Test that the correct exceptions are raised for non-uniform datasets when
    uniform datasets are expected.
    """

    source, dataset = nonuniform_dataset()

    # Loading the first data sample should work (it doesn't check for
    # non-uniformity until it has at least one datum to compare against)
    assert torch.allclose(source[0, 0].concat, dataset[0][2].tensor)

    with pytest.warns(DNADNAWarning,
            match=r'.*sample has 3 SNPs, which differs from the rest of the '
                  r'dataset \(2 SNPs\).*'):
        dataset[1]

    # Similar test, but with different number of individuals:
    source, dataset = nonuniform_dataset(nonuniformity='indiv')
    assert torch.allclose(source[0, 0].concat, dataset[0][2].tensor)

    with pytest.warns(DNADNAWarning,
            match=r'.*sample has 3 individuals, which differs from the '
                  r'rest of the dataset \(2 individuals\).*'):
        dataset[1]

    # Finally, assert that no errors are raised if verifying
    # uniform_shape=False (equivalent to not passing any transforms)
    source, dataset = nonuniform_dataset(nonuniformity='both',
                                         validate_uniform_shape=False)
    for replicate_idx, datum in enumerate(dataset):
        assert torch.allclose(source[0, replicate_idx].concat, datum[2].tensor)


@pytest.mark.parametrize('num_workers', (0, 2))
def test_invalid_uniform_dataloader(num_workers):
    """
    Regression test for #33, which is a follow-up to #32.

    Ensure that when an ``InvalidSNPSample`` is encountered when iterating over
    a ``DataLoader`` containing an invalid non-uniform dataset that the correct
    exception is raised.
    """

    _, dataset = nonuniform_dataset(nonuniformity='both', n_scenarios=10)
    loader = DataLoader(dataset=dataset,
                        batch_size=1,
                        num_workers=num_workers,
                        collate_fn=DNATrainingDataset.collate_batch)

    # Attempting to iterate over the loader should result in an
    # InvalidSNPSample error eventually
    # Note: In the multi-processing case the warning will occur in the worker
    # process so we won't capture it here.
    if num_workers > 0:
        ctx = nullcontext()
    else:
        ctx = pytest.warns(DNADNAWarning, match=r'.*InvalidSNPSample.*')

    with ctx:
        all_data = list(loader)
        assert len(all_data) == 30  # 3 replicates * 10 scenarios

    # Check that if the dataset is created with uniform=False the loader can be
    # fully iterated over
    source, dataset = nonuniform_dataset(nonuniformity='both',
                                         validate_uniform_shape=False)
    loader = DataLoader(dataset=dataset,
                        batch_size=1,
                        num_workers=num_workers,
                        collate_fn=DNATrainingDataset.collate_batch)

    for r_idx, datum in enumerate(loader):
        s_idx, snp = datum[:2]
        s_idx = int(s_idx)
        assert torch.allclose(source[s_idx, r_idx].concat.float(), snp)


@pytest.mark.parametrize('zero_pad', (False, True))
def test_non_zero_padded_dataset(tmp_path, monkeypatch, zero_pad):
    """
    Regression test for !33.

    This ensures that when the filenames in a dataset do not use zero-padding
    on the scenario or replicate index that this is correctly detected.
    """

    # monkeypatch os.walk so that directories are returned in order of highest
    # length--one of the sources of this bug was that I assumed os.walk would
    # always iterate in lexicographic order, e.g. with the smallest scenario
    # number first, but this is not guaranteed.  To reproduce the bug it is
    # sufficient to start with the longest directory names first.
    os_walk = os.walk

    def longest_dir_first_os_walk(*args):
        def sort_key(ent):
            return (len(ent[0]), ent[0])

        return sorted(os_walk(*args), key=sort_key, reverse=True)

    monkeypatch.setattr(os, 'walk', longest_dir_first_os_walk)

    base_filename_fmt = pth.join('scenario_{scenario}',
                                 'scenario_{scenario}_{replicate}.npz')

    if zero_pad:
        filename_fmt = zero_pad_format(base_filename_fmt, scenario=15,
                                       replicate=15)
    else:
        filename_fmt = base_filename_fmt

    for s_idx, r_idx in product(range(15), range(15)):
        filename = filename_fmt.format(scenario=s_idx, replicate=r_idx)
        filepath = tmp_path / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.touch()

    source = NpzSNPSource(tmp_path, '', filename_format=base_filename_fmt)
    expected = tmp_path / filename_fmt.format(scenario=0, replicate=0)
    assert Path(source._get_filename(0, 0)) == expected

    # Reset _guessed_format each time to make sure it guesses correctly in each
    # case
    source._guessed_format = None
    expected = tmp_path / filename_fmt.format(scenario=0, replicate=14)
    assert Path(source._get_filename(0, 14)) == expected

    source._guessed_format = None
    expected = tmp_path / filename_fmt.format(scenario=1, replicate=1)
    assert Path(source._get_filename(1, 1)) == expected

    source._guessed_format = None
    expected = tmp_path / filename_fmt.format(scenario=13, replicate=1)
    assert Path(source._get_filename(13, 1)) == expected
    # Regression test: there was a bug where if the first filename one which
    # guess_format was run did not contain zero-padding (because the number is
    # large enough to use all the digits) then the guess would not work
    # correctly and generating the filename of subsequent smaller
    # scenario/replicate numbers would fail
    expected = tmp_path / filename_fmt.format(scenario=1, replicate=1)
    assert Path(source._get_filename(1, 1)) == expected

    # Same regression test but with the roles of scenario and replicate index
    # reversed
    source._guessed_format = None
    expected = tmp_path / filename_fmt.format(scenario=1, replicate=13)
    assert Path(source._get_filename(1, 13)) == expected
    expected = tmp_path / filename_fmt.format(scenario=1, replicate=1)
    assert Path(source._get_filename(1, 1)) == expected
