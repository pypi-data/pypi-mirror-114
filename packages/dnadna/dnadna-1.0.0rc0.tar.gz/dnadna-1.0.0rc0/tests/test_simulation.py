"""Tests of the ``dnada.simulation`` module."""


import copy
import glob
import pathlib

import numpy as np
import pandas
import pytest

from dnadna.cli.simulation import SimulationInitCommand, SimulationRunCommand
from dnadna.examples import one_event
from dnadna.simulator import Simulator
from dnadna.utils.config import Config, ConfigError


def test_simulator_missing_simulator_name():
    """
    Test instantiating a `Simulator` without a simulator_name in the
    config.
    """

    with pytest.raises(ConfigError) as excinfo:
        Simulator()

    assert ('simulation config does not have a "simulator_name" key' in
            str(excinfo.value))
    assert ("currently registered simulators are: 'one_event'" in
            str(excinfo.value))


def test_simulator_unknown_simulator_name():
    """
    Test instantiating a `Simulator` with a simulator_name that is not
    registered.
    """

    with pytest.raises(ConfigError) as excinfo:
        Simulator({'simulator_name': 'garbage'})

    assert ("unknown simulator 'garbage'" in
            str(excinfo.value))
    assert ("currently registered simulators are: 'one_event'" in
            str(excinfo.value))


def test_simulation_main(tmp_path, monkeypatch):
    """
    A dummy test to demonstrate that dnadna.simulation.main produces output
    without crashing.
    """
    n_scenarios = 2
    n_replicates = 2
    config = one_event.DEFAULT_ONE_EVENT_CONFIG
    dataset_name = config['dataset_name']

    # Some of the real defaults are too large for testing purposes so change
    # them to just a few:
    monkeypatch.setitem(config, 'n_scenarios', n_scenarios)
    monkeypatch.setitem(config, 'n_replicates', n_replicates)

    # Set the seed so that the test is reproducible
    monkeypatch.setitem(config, 'seed', 2)

    # Initialize a new simulation configuration and data directory
    argv = ['--debug', dataset_name, 'one_event', str(tmp_path)]
    assert SimulationInitCommand.main(argv, raise_exceptions=True) is None

    # These file and directory names are hard-coded defaults, currently.
    dataset_dir = tmp_path / dataset_name

    # Check that the simulation parameters JSON file was created
    config_filename = \
            Simulator.config_filename_format.format(dataset_name=dataset_name)
    config_path = dataset_dir / config_filename
    assert config_path.is_file()

    # Load the file and validate it against the simulation schema
    Config.from_file(config_path, schema='simulation', validate=True)

    # Now run the simulation with the 'dnadna simulation run' command
    argv = ['--debug', str(config_path)]
    assert SimulationRunCommand.main(argv, raise_exceptions=True) is None

    # Check that the randomly generated scenario parameters table was created
    scenario_params_path = (dataset_dir / config['scenario_params_path'])
    assert scenario_params_path.is_file()

    # Just test for now that it's a valid CSV file that can be read by Pandas
    assert isinstance(pandas.read_csv(scenario_params_path), pandas.DataFrame)

    def check_scenarios(path=dataset_dir, check_load=True):
        for scenario_idx in range(n_scenarios):
            for replicate_idx in range(n_replicates):
                # Just check that each file can be loaded.  Later we can check
                # specific things about the files if there is interest to (it
                # may not be necessary if we build more unit tests) TODO: It
                # might be nice to have the format of this file hierarchy
                # encoded precisely in a function.
                filename_format = config['data_source']['filename_format']
                filename = filename_format.format(dataset_name=dataset_name,
                        scenario=scenario_idx, replicate=replicate_idx)
                scenario_path = (path / filename)
                assert scenario_path.is_file()
                if check_load:
                    assert isinstance(np.load(scenario_path),
                                      np.lib.npyio.NpzFile)

    check_scenarios()

    # Test that an existing simulation cannot be overwritten by default
    with pytest.raises(FileExistsError,
                       match='existing scenario params file.*'):
        SimulationRunCommand.main(argv, raise_exceptions=True)

    # Run again but with --backup
    argv.insert(1, '--backup')
    assert SimulationRunCommand.main(argv, raise_exceptions=True) is None
    check_scenarios()
    # Also check the backup
    backups = glob.glob(str(dataset_dir / f'{dataset_name}-backup.*'))
    assert len(backups) == 1
    check_scenarios(path=pathlib.Path(backups[0]), check_load=False)


def test_simulator_config_validation_known_simulator():
    """
    Test validating a simulation config with ``simulator_name`` referencing
    a known Simulator plugin (in this case OneEventSimulator).
    """

    config = Config(copy.deepcopy(one_event.DEFAULT_ONE_EVENT_CONFIG))
    config.validate(schema='simulation')

    # If we set one of the values in the config to something invalid for the
    # OneEventSimulator's config schema ensure that validation fails (to ensure
    # the OneEventSimulator schema is in fact being validated)
    config['tmax'] = 'blah blah'
    with pytest.raises(ConfigError) as exc:
        config.validate(schema='simulation')

    assert str(exc.value) == (
            "error in config at 'tmax': 'blah blah' is not of type 'integer'")


def test_simulator_config_validation_unknown_simulator():
    """
    Test validation a simulation config with ``simulator_name`` referencing
    an unknown simulator.

    In this case validation should pass so long as the rest of the simulation
    config is correct.
    """

    config = Config(copy.deepcopy(one_event.DEFAULT_ONE_EVENT_CONFIG))
    config['simulator_name'] = 'my-custom-simulator-not-from-dnadna'
    config.validate(schema='simulation')

    # If we set one of the values in the config to something invalid for the
    # OneEventSimulator's config schema, validation should still pass because
    # we don't have a schema for 'my-custom-simulator-not-from-dnadna' and
    # don't know how to interpret any additional properties
    config['tmax'] = 'blah blah'
    config.validate(schema='simulation')
