"""
Base implementation for `~dnadna.simulator.Simulator` classes.

This can be used to implement new population genetics simulators, or to wrap
existing simulators in a common interface used by DNADNA, as well as to adapt
existing simulation data (without recomputing it) to the DNADNA interface.
"""


import abc
import collections
import functools
import logging
import os
import os.path as pth
import multiprocessing
import re
import time

import numpy as np
import pandas as pd
import tqdm

from .datasets import NpzSNPSource
from .utils.config import Config, ConfigMixIn, ConfigError
from .utils.misc import format_to_re, zero_pad_format
from .utils.plugins import load_plugins, Pluggable


log = logging.getLogger(__name__)


class Simulator(ConfigMixIn, Pluggable, metaclass=abc.ABCMeta):
    """
    Base class for implementing simulators for use with the DNADNA training
    system.

    None of the other components in DNADNA directly depend on using this
    interface, so its primary purpose is as a convenience, and example for how
    to implement a basic SNP data simulator.

    It can be used either as the base class for a novel simulator (see
    the `dnadna.examples.one_event` module for a concrete example); it can also
    be use to wrap existing simulation code under a common API.  Furthermore,
    it can be used as a *converter*, to input existing simulation data, and
    translate it to the format expected by DNADNA's other tools.
    """

    name = abc.abstractproperty()
    """
    The name of the simulator, used primarily to select this simulator from
    the command-line.  If multiple simulators with the same name are loaded
    simultaneously, only the last-loaded will be used (and a warning is issued).
    """

    config_schema = 'simulation'
    """
    The name of the schema or a `dict` containing a schema against which to
    validate the configuration for this simulator.  Custom simulators can
    override or extend the base 'simulation' schema.
    """

    config_default = Config.from_default('dataset')
    """
    A `dict` containing a default sample configuration for this simulator; the
    sample configuration need not be fully functional, but it can be used to
    initialize a template config file for the simulation.
    """

    config_filename_format = '{dataset_name}_simulation_config.yml'
    """
    Format string for the default config filename; it is passed the
    ``dataset_name`` from the config as a template variable.
    """

    preprocessing_config_default = Config()
    """
    Simulators may extend the default preprocessing configuration file with
    additional settings optimized for the simulator.
    """

    training_config_default = Config()
    """
    Simulators may extend the default training configuration file with
    additional settings optimized for the simulator.
    """

    def __new__(cls, config={}, validate=True, **kwargs):
        if cls is not Simulator:
            # Instantiating a subclass
            return super().__new__(cls)

        simulator_cls = cls.class_from_config(config)
        return simulator_cls(config=config, validate=True, **kwargs)

    def __init__(self, config={}, validate=True):
        super().__init__(config, validate=validate)

        if 'seed' in self.config:
            np.random.seed(self.config['seed'])

    @classmethod
    def get_schema(cls):
        """
        Returns the schema extensions for simulator plugins.

        Simulation configs are validated against the base :ref:`simulation
        schema <schema-simulation>` plus any simulator-specific schemas
        provided by `Simulator` plugins.
        """

        if cls is not Simulator:
            return cls.schema

        simulators = []
        simulator_names = []
        for plugin_name, plugin in cls.get_plugins():
            names = [plugin_name, plugin.__name__]
            simulators.append({
                'allOf': [{
                    'properties': {
                        'simulator_name': {
                            'type': 'string',
                            'enum': names
                        }
                    },
                    'required': ['simulator_name']
                }, plugin.schema]
            })
            simulator_names.extend(names)

        # A simulation config only needs to match the config schema for a
        # DNADNA Simulator if the Simulator plugin is loaded.  If
        # simulator_name is some other arbitrary or custom value, it can
        # be ignored.
        simulators.append({
            'properties': {
                'simulator_name': {
                    'type': 'string',
                    'not': {'enum': simulator_names}
                }
            }
        })

        return {'oneOf': simulators}

    @classmethod
    def class_from_config(cls, config):
        """
        Load the appropriate Simulator subclass determined from the config and
        optionally validate the config against a Simulator-specific config
        schema.
        """

        plugins = config.get('plugins', [])
        load_plugins(plugins)

        try:
            simulator_name = config['simulator_name']
        except KeyError:
            simulators = ', '.join(f'{s!r}' for s, _ in cls.get_plugins())
            raise ConfigError(config,
                f'simulation config does not have a "simulator_name" key; '
                f'this is required to load the correct Simulator class; '
                f'currently registered simulators are: {simulators}; '
                f'additional simulators can be loaded via plugin modules')

        try:
            simulator_cls = cls.get_plugin(simulator_name)
        except ValueError:
            simulators = ', '.join(f'{s!r}' for s, _ in cls.get_plugins())
            raise ConfigError(config,
                f'unknown simulator {simulator_name!r}: a subclass '
                f'of Simulator with this name must be registered via a plugin; '
                f'currently registered simulators are: {simulators}')

        return simulator_cls

    @abc.abstractmethod
    def generate_scenario_params(self):
        """
        Generate and return the `pandas.DataFrame` containing scenario
        parameters for this simulation.

        The scenario parameters table (or scenario params for short) is a
        `pandas.DataFrame` containing at a minimum: an `pandas.Index` named
        ``'scenario_idx'`` which gives an integer label to each scenario in the
        table, and a column named ``'n_replicates'`` giving the number of
        replicates for each scenario.  A "replicate" is a copy of a scenario,
        generated using the same scenario parameters, but containing
        potentially different data (i.e. with different randomization).  If a
        simulation does not use scenario replicates, this the value in this
        column can simply be set to ``1`` for each scenario.

        Beyond this, the scenario parameters may contain any number of columns
        giving the known values of parameters that were used to generate the
        simulation, such as "mutation rate" or "recombination rate", among many
        others.  See `dnadna.examples.one_event` for an example.

        Its only argument is ``self``, so all information needed to generate
        the scenario params should be provided to the simulator via its
        ``__init__`` method, especially via the simulator config file.

        This method may either implement the task of generating scenario
        parameters for the simulation; or if this is a wrapper class for an
        existing simulation, it may simply return the parameters of that
        simulation, possibly reorganized into the correct format.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def simulate_scenario(self, scenario, verbose=False):
        """
        Simulate a single scenario, given as a named tuple from the simulation
        params table as returned by `pandas.DataFrame.itertuples`.  Returns a
        an iterator over replicates in the scenario.

        The items returned from this method should be a 3-tuple in the format
        ``(scenario_idx, rep_idx, SNPSample(snp=SNPs, pos=positions)``, where
        ``scenario_idx`` is the index into the scenario params table for the
        parameters that were used to produce this simulation; ``rep_idx`` is
        the replicate index, in the case where multiple replicates are
        generated for each scenario, if not it can just be ``0``; the final
        element is an `.SNPSample` instance containing the SNP matrix and
        positions array generated by the simulator.

        This method is called from `Simulator.simulate_scenarios`, which loops
        over all rows in the simulation params and calls this method for each
        scenario, possibly parallelized if parallelization is enabled.  For
        finer control over simulation flow control,
        `Simulator.simulate_scenarios` may also be overridden by a subclass.
        """

        raise NotImplementedError

    def load_scenario_params(self, scenario_id=0, n_scenarios=None,
                             load_existing=False, save=False):
        """
        Returns a `pandas.DataFrame` containing the simulation parameters
        table, either by reading it from a file (currently only CSV supported)
        given by ``self.scenario_params_path``, or by generating it by calling
        `Simulator.generate_scenario_params`.

        Parameters
        ----------
        scenario_id : int, optional
            The ID number of the initial scenario to return (default: 0, i.e.
            return all parameter scenarios).
        n_scenarios : int, optional
            The number of scenarios (started from ``scenario_id`` to return);
            by default returns all scenarios in the scenario params table
            starting from ``scenario_id``.
        load_existing : bool, optional
            If the scenario params file given by the config already exists,
            load the existing one instead of regenerating it.
        save : bool, optional
            If the scenario params file does not already exist in the filename
            given by ``self.scenario_params_path``, it is generated by calling
            `Simulator.generate_scenario_params`.  If ``save=True`` the
            generated file is also saved to that path.  Otherwise it is not
            saved, and the `pandas.DataFrame` is simply returned.
        """
        if load_existing and pth.exists(self.scenario_params_path):
            log.info(f'Loading existing scenario params file '
                     f'{self.scenario_params_path}')
            skiprows = list(range(1, scenario_id + 1))
            scenario_params = pd.read_csv(self.scenario_params_path,
                                          index_col='scenario_idx',
                                          skiprows=skiprows,
                                          nrows=n_scenarios)
        else:
            log.info('Generating new scenario params table')
            scenario_params = self.generate_scenario_params()
            end = None if n_scenarios is None else scenario_id + n_scenarios
            scenario_slice = slice(scenario_id, end)
            scenario_params = scenario_params[scenario_slice]

            if save:
                log.info(
                    f'Saving generated scenario params file to '
                    f'{self.scenario_params_path}')
                os.makedirs(pth.dirname(self.scenario_params_path),
                            exist_ok=True)
                scenario_params.to_csv(self.scenario_params_path,
                                       index_label='scenario_idx')

        return scenario_params

    def simulate_scenarios(self, scenario_params, n_cpus=1, verbose=False):
        """
        Return an iterator over simulated SNPs given a scenario params table
        (see `Simulator.load_scenario_params` for the format of this table).

        This method should iterate over all scenarios in the simulation
        (possibly generating the simulation as well, or reading it from an
        existing simulation), which are then each passed to
        `Simulator.simulate_scenario` for each scenario.

        The items returned from the iterator should be a 3-tuple in the format
        ``(scenario_idx, rep_idx, SNPSample(snp=SNPs, pos=positions)``, where
        ``scenario_idx`` is the index into the scenario params table for the
        parameters that were used to produce this simulation; ``rep_idx`` is
        the replicate index, in the case where multiple replicates are
        generated for each scenario, if not it can just be ``0``; the final
        element is an `.SNPSample` instance containing the SNP matrix and
        positions array generated by the simulator.

        Parameters
        ----------
        scenario_params : `pandas.DataFrame`
            The scenario params table for the scenarios to simulate.
        n_cpus : int, optional
            If ``1``, scenarios are simulated in serial; for ``n_cpus > 1`` a
            process pool of size ``n_cpus`` is used.  If ``n_cpus = 0`` or
            `None`, use the default number of CPUs used by
            `multiprocessing.pool.Pool`.
        """

        if n_cpus < 1:
            n_cpus = None

        tuple_name = 'Scenario'

        if n_cpus == 1:
            func = functools.partial(self.simulate_scenario, verbose=verbose)

            def iter_scenarios():
                for scenario in scenario_params.itertuples(name=tuple_name):
                    yield func(scenario)
        else:
            func = functools.partial(self._simulate_scenario_wrapper,
                    tuple_name, list(scenario_params.columns), verbose=verbose)

            def iter_scenarios():
                it = scenario_params.itertuples(name=None)
                with multiprocessing.Pool(n_cpus) as pool:
                    for scenario in pool.imap_unordered(func, it):
                        yield scenario

        for scenario in iter_scenarios():
            for replicate in scenario:
                yield replicate

    def run_simulation(self, scenario_id=0, n_scenarios=None, n_cpus=1,
                       load_existing_scenario_params=False,
                       save_scenario_params=True,
                       overwrite_existing=False,
                       backup_existing=True,
                       progress_bar=False,
                       verbose=False):

        if not load_existing_scenario_params:
            if self._check_existing():
                if overwrite_existing:
                    action = 'backed up' if backup_existing else 'overwritten'
                    log.warning(
                        f'Existing scenario params file '
                        f'{self.scenario_params_path} and associated '
                        f'simulation data will be {action}')
                    self._backup_or_delete(backup_existing)
                else:
                    raise FileExistsError(
                        f'existing scenario params file '
                        f'{self.scenario_params_path} will not be '
                        f'overwritten; re-run with the --backup flag if you '
                        f'want to keep a backup of the existing data, or with '
                        f'the --overwrite flag if you want to delete it')

        scenario_params = self.load_scenario_params(
                scenario_id=scenario_id, n_scenarios=n_scenarios,
                load_existing=load_existing_scenario_params,
                save=save_scenario_params)

        # NOTE: Currently one simulation file format is supported, the
        # "DNADNA" format, so for now it is assumed here:
        filename_format = self.data_source['filename_format']

        filename_format = zero_pad_format(filename_format,
                scenario=len(scenario_params))

        it = self.simulate_scenarios(scenario_params, n_cpus=n_cpus,
                                     verbose=verbose)
        bar = tqdm.tqdm(it, total=scenario_params['n_replicates'].sum(),
                        unit='sample', disable=(not progress_bar))

        prev_sample = None

        for s_idx, r_idx, sample in bar:
            if s_idx != prev_sample:
                # Update the filename format, since in principle each sample
                # can have a different number of replicates
                prev_sample = s_idx
                n_replicates = scenario_params.n_replicates[s_idx]
                filename_format = zero_pad_format(filename_format,
                        replicate=n_replicates)

            filename = filename_format.format(
                    dataset_name=self.dataset_name,
                    scenario=s_idx,
                    replicate=r_idx)

            # The filename template may contain directories as well
            dirname = pth.join(self.data_root, pth.dirname(filename))
            if dirname and not os.path.exists(dirname):
                os.mkdir(dirname)

            sample.to_npz(pth.join(self.data_root, filename))

    def _simulate_scenario_wrapper(self, tuple_name, column_names, scenario,
                                   verbose=False):
        """
        Wrapper for `Simulator.simulate_scenario` which returns all replicates
        in a scenario as a list, rather than a generator, for use with
        multiprocessing.

        It also converts from a plain tuple back to named tuple, since
        namedtuples can't easily be pickled.
        """

        # reconstruct the namedtuple
        scenario_tuple = collections.namedtuple(
                tuple_name, ['Index'] + column_names, rename=True)
        scenario = scenario_tuple(*scenario)
        return list(self.simulate_scenario(scenario, verbose=verbose))

    def _check_existing(self):
        """
        Returns True if it looks like a partial run of this simulation already
        exists in the same ``data_root`` directory.

        Checks for both the scenario params file of the same name as given in
        the config, as well as any scenario files/directories (at least one)
        matching the filename format.
        """

        if pth.exists(self.scenario_params_path):
            return True

        # Look for just the first path component of the filename format
        first_part = self.data_source['filename_format'].split(os.sep, 1)[0]
        format_re = format_to_re(first_part, dataset_name=self.dataset_name,
                                 scenario=r'\d+', replicate=r'\d+') + '$'
        for path in os.listdir(self.data_root):
            if re.search(format_re, path):
                return True

    def _backup_or_delete(self, backup=True):
        """
        Backup or delete existing simulation data to a new subdirectory.

        If ``backup=False`` the files that would have been backed up are simply
        deleted.

        This will prevent overwriting it if a simulation is run multiple times
        within the same directory.
        """

        # TODO: This only works if the dataset is using the "dnadna format"
        # (the only format currently explicitly used by Simulator).  In the
        # future this can be a feature specific to a dataset format.
        assert self.data_source['format'] == 'dnadna', (
            'automatic backup of existing simulation datasets is only '
            'supported for the "dnadna" format; unfortunately this means '
            'you will have to manually clean up the existing data if you '
            'do not want it to be overwritten or mixed up with new simulation '
            'data')

        # Determine the backup directory name.  It will come from the current
        # datetime, plus a .N extension if even that directory already exists
        ts = int(time.time())
        backup_dir_base = pth.join(self.data_root,
                                   f'{self.dataset_name}-backup.{ts}')
        backup_dir = backup_dir_base
        idx = 0

        while pth.exists(backup_dir):
            backup_dir = backup_dir_base + f'.{idx}'

        if backup:
            log.warning(
                f'The existing scenario params file {self.scenario_params_path} '
                f'and all existing simulation data (.npz files) will be backed '
                f'up to {backup_dir}; you can remove this directory manually if '
                f'you no longer require its contents')

            os.makedirs(backup_dir)

        def backup_or_delete(src):
            if not pth.isabs(src):
                src = pth.join(self.data_root, src)

            if not backup:
                os.unlink(src)
            else:
                dst = pth.join(backup_dir, src[len(self.data_root) + 1:])

                os.makedirs(pth.dirname(dst), exist_ok=True)
                os.rename(src, dst)

            # If the directory containing the file is empty, remove that
            # directory too.
            dirname = pth.dirname(src)
            if pth.isdir(dirname) and not os.listdir(dirname):
                os.rmdir(dirname)

        # Back up the scenario params file to the backup directory
        if backup:
            log.info('Backing up old scenario params')
        backup_or_delete(self.scenario_params_path)

        # Reuse the machinery from this class for iterating over files in a
        # dnadna format directory; this would be a useful method to generalize
        # for other data format "source" classes, but that API is still to be
        # worked out further...
        source = NpzSNPSource.from_config(self.config, validate=False)
        # Back up all existing files matching the filename format from the
        # config file (files that do not match the format are left alone,
        # assuming they will not conflict with later attempts to read the data
        # set.  Users are responsible for cleanup of any additional junk files.
        if backup:
            log.info('Backing up old scenario data')
        for _, _, filename in source._iter_dataset_files():
            backup_or_delete(filename)

        if backup:
            log.info('Backup complete')
