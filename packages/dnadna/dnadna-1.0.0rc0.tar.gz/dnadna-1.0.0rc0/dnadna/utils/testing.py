"""Shared utilities for test suite."""


import copy
import io
import os
import sys

import pytest
import torch
from filelock import FileLock

from ..cli import DnadnaCommand
from ..data_preprocessing import DataPreprocessor
from ..datasets import DictSNPSource
from ..simulation import Simulation
from ..snp_sample import SNPSample
from ..examples import one_event


# For use when parametrizing tests on whether or not to use CUDA.
# Don't bother testing with use_cude=True unless CUDA is actually available
if torch.cuda.is_available():
    USE_CUDA = (False, True)
else:
    USE_CUDA = (False,)


TEST_SIMULATION_CACHE_KEY = 'dnadna/tests/test_simulation'

# Some of the real defaults are too large for testing purposes so change them
# to just a few:
# TODO: Perhaps make these arguments to cached_simulation so different
# simulations of different sizes can be used for different tests
TEST_SIMULATION_CONFIG = one_event.DEFAULT_ONE_EVENT_CONFIG.copy(True)
TEST_SIMULATION_CONFIG.update({
    'n_scenarios': 15,
    'n_replicates': 10,
    'segment_length': 1e5,
    'seed': 2  # For reproducibility between tests
})


class DummySource:
    """
    Fake data source that does not return any real data.

    Used to test functions that don't require actually loading data from a real
    data source.  However, some functions do require the appearance of a real
    data source.  This source just returns fake `SNPSamples` of the requested
    size.
    """

    def __init__(self, n_snp=1, n_indiv=1):
        self.n_snp = n_snp
        self.n_indiv = n_indiv

    def __getitem__(self, idx):
        return SNPSample(torch.zeros(self.n_indiv, self.n_snp),
                         torch.arange(self.n_snp))

    def __contains__(self, item):
        return True


@pytest.fixture
def cached_simulation(cache, monkeypatch, change_test_dir):
    # Ensure the cache dir exists and set up a place to create the file lock
    # for this cache key
    lockdir = cache.makedir('locks')
    lockfile = lockdir / (TEST_SIMULATION_CACHE_KEY + '.lock')
    os.makedirs(lockfile.dirname, exist_ok=True)

    lock = FileLock(lockfile)

    def cached_simulate_scenarios(self, *args, **kwargs):
        scenarios = cache.get(TEST_SIMULATION_CACHE_KEY, None)
        for key, data in scenarios.items():
            s_idx, r_idx = map(int, key.split(':'))
            yield s_idx, r_idx, SNPSample.from_dict(data)

    # I believe both of these need to be patched
    monkeypatch.setattr(one_event, 'DEFAULT_ONE_EVENT_CONFIG',
                        TEST_SIMULATION_CONFIG)
    monkeypatch.setattr(one_event.OneEventSimulator, 'config_default',
                        TEST_SIMULATION_CONFIG)

    with lock:
        simulator = one_event.OneEventSimulator(TEST_SIMULATION_CONFIG)
        scenario_params = simulator.generate_scenario_params()
        scenarios = cache.get(TEST_SIMULATION_CACHE_KEY, None)

        if scenarios is None:
            scenarios_gen = simulator.simulate_scenarios(scenario_params)
            scenarios = {(s_idx, r_idx): sample.to_dict()
                         for s_idx, r_idx, sample in scenarios_gen}
            # Data is stored in the cache as JSON (it may be possible to supply
            # other cache data formats but I don't know how right now).
            # Samples are stored by their (scenario_idx, replicate_idx) pairs,
            # but this is not allowed by JSON, so instead we key them by
            # "<scenario_idx>:<replicate_idx>" strings:
            cache_scenarios = {f'{s_idx}:{r_idx}': sample
                               for (s_idx, r_idx), sample in scenarios.items()}
            cache.set(TEST_SIMULATION_CACHE_KEY, cache_scenarios)
        else:
            # Deserialize the keys back to tuples
            scenarios = {tuple(map(int, k.split(':'))): v
                         for k, v in scenarios.items()}

    # Patch OneEventSimulator.simulate_scenarios to use the cache from now
    # on within the test in which this fixture is used
    monkeypatch.setattr(one_event.OneEventSimulator,
                        'simulate_scenarios',
                        cached_simulate_scenarios)

    # Return a copy of this so individual tests can modify this without
    # stepping on each other's toes
    config = copy.deepcopy(TEST_SIMULATION_CONFIG)
    return config, scenario_params, scenarios


@pytest.fixture
def cached_preprocessor(cached_simulation):
    """
    Companion to `cached_simulation`.

    Prepares the cached simulation for a training run by setting up and
    returning a `~dnadna.data_preprocessing.DataPreprocessor` configured
    with an appropriate training config.
    """

    simulation_config, scenario_params, scenarios = cached_simulation
    preprocessing_config = \
            one_event.DEFAULT_ONE_EVENT_PREPROCESSING_CONFIG.copy(True)
    training_config = one_event.DEFAULT_ONE_EVENT_TRAINING_CONFIG.copy(True)

    preprocessing_config['dataset'] = simulation_config
    preprocessing_config['dataset_splits'] = {
        'training': 2.0 / 3,
        'validation': 1.0 / 3
    }
    preprocessing_config['preprocessing'].update({
        'min_snp': 100,
        'seed': 0  # for reproducibility of tests
    })

    training_config['dataset'] = simulation_config
    training_config['dataset_transforms'][0]['crop']['max_snp'] = 100
    training_config['n_epochs'] = 1
    # Set the seed so it is consistent between test runs, for historical
    # reasons it is set to 2 (see
    # https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/109)
    training_config['seed'] = 2

    source = DictSNPSource(scenarios)
    simulation = Simulation(simulation_config, source=source,
                            scenario_params=scenario_params)
    return DataPreprocessor(preprocessing_config, dataset=simulation)


def run_main(argv, exitcode=0, capture=False,
             sys_executable=sys.executable, cmd=DnadnaCommand):
    """
    Run the main method of a given class with the given argv, including argv[0]
    for the expected command name.

    Doctests don't capture stderr by default, so also redirect stderr to stdout
    for testing error messages.

    If ``capture=True`` the stdout/err is captured and returned as a string
    instead of printed.
    """

    old_argv0 = sys.argv[0]
    old_stdio = (sys.stdout, sys.stderr)
    old_sys_executable = sys.executable

    try:
        sys.argv[0] = argv[0]
        if capture:
            sys.stdout = io.StringIO()

        sys.stderr = sys.stdout
        # This can replace the default sys.executable in case it's something
        # strange; some tests require this
        sys.executable = sys_executable
        cmd.main(argv[1:])
        if capture:
            return sys.stdout.getvalue()
    except SystemExit as exc:
        assert exc.code == exitcode
        if capture:
            return sys.stdout.getvalue()
    finally:
        sys.executable = old_sys_executable
        sys.stdout, sys.stderr = old_stdio
        sys.argv[0] = old_argv0
