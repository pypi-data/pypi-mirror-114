"""
An example :ref:`msprime <msprime:sec_intro>`-based simulator with demographic
parameters for a model with one population change event.
"""


import textwrap

import msprime
import numpy as np
import pandas as pd

from .. import __version__  # noqa: F401
from ..simulator import Simulator
from ..snp_sample import SNPSample
from ..utils.config import Config


__all__ = ['OneEventSimulator']


ONE_EVENT_CONFIG_SCHEMA = {
    'properties': {
        'dataset_name': {'default': 'one_event'},
        'n_scenarios':  {'default': 20000},  # noqa: E241
        'n_samples':    {'default': 50},  # noqa: E241
        'n_replicates': {'default': 100},
        'scenario_params_path': {
            'default': 'one_event_params.csv'
        },
        'data_source': {
            'default': {'format': 'dnadna'}
        },
        'position_format': {
            'normalized': True
        },
        # TODO: Provide descriptions for the additional properties added to
        # this schema.
        'tmax': {
            'type': 'integer',
            'default': 100000
        },
        'tmin': {
            'type': 'integer',
            'default': 2000
        },
        'generation_time': {
            'type': 'integer',
            'default': 25
        },
        'recombination_rate': {
            'type': 'number',
            'default': 1e-8
        },
        'mutation_rate': {
            'type': 'number',
            'default': 1e-8
        },
        'n_min': {
            'type': 'number',
            'default': np.log10(5000)
        },
        'max': {
            'type': 'number',
            'default': np.log10(50000)
        }
    }
}
"""
Schema for configuring the `OneEventSimulator`.  It is based on the the
generic ``dnadna/schemas/simulation.yml`` schema but adds additional
configuration options.
"""


# TODO: Generate this directly from the schema instead
DEFAULT_ONE_EVENT_CONFIG = Config({
    'simulator_name': 'one_event',
    'dataset_name': 'one_event',
    'scenario_params_path': 'one_event_params.csv',
    'n_scenarios': 20000,
    'n_replicates': 100,
    'n_samples': 50,
    'segment_length': 2e6,
    'tmax': 100000,
    'tmin': 2000,
    'generation_time': 25,
    'recombination_rate': 1e-8,
    'mutation_rate': 1e-8,
    'n_min': np.log10(5000),
    'n_max': np.log10(50000)
}, Config.from_default('dataset'))


DEFAULT_ONE_EVENT_PREPROCESSING_CONFIG = Config({
    'model_root': '.',
    'model_name': 'one_event',
    'dataset_splits': {
        'training': 0.70,
        'validation': 0.30
    },
    'preprocessing': {
        'min_snp': 500,
    },
    'learned_params': {
        'event_time': {
            'type': 'regression',
            'log_transform': True,
            'loss_func': 'MSE'
        },
        'recent_size': {
            'type': 'regression',
            'log_transform': True,
            'loss_func': 'MSE'

        },
        'event_size': {
            'type': 'regression',
            'log_transform': True,
            'loss_func': 'MSE'
        }
    }
})


DEFAULT_ONE_EVENT_TRAINING_CONFIG = Config({
    'dataset_transforms': [
        {'crop': {'max_snp': 500}}
    ],
    'n_epochs': 5,
    'batch_size': 20,
    'evaluation_interval': 10,
    'loader_num_workers': 4
})


class OneEventSimulator(Simulator):
    # Inherit the module's docstring.
    __doc__ = __doc__ + textwrap.dedent("""

    The following attributes are available via the `.Config` object for this
    class:

    Attributes
    ----------

    n_scenarios : int
        number of scenarios to simulate by random draw
    n_samples : int
        number of segment drawn from the population
    n_replicates : int
        number of replicates to generate from the same scenario (i.e. a set
        of demographic parameters)
    segment_length : int
         length of each segment, in bp
    tmax : int
        oldest time possible for the start of the event
    tmin : int
        earliest time possible for the start of the event
    recombination_rate : float
        per generation per bp recombination rate
    mutation_rate : float
        per generation per bp mutation rate
    n_min : int
        minimum size of a population
    n_max : int
        maximum size of a population
    generation_time : int
         length of a generation
    """)

    name = 'one_event'
    schema = ONE_EVENT_CONFIG_SCHEMA
    config_default = DEFAULT_ONE_EVENT_CONFIG
    preprocessing_config_default = DEFAULT_ONE_EVENT_PREPROCESSING_CONFIG
    training_config_default = DEFAULT_ONE_EVENT_TRAINING_CONFIG

    def generate_scenario_params(self):
        """
        Generate demographic parameters for a model with one event.

        See the `OneEventSimulator` top-level documentation for the list of
        available attributes loaded from the config file.
        """

        scenario_params = pd.DataFrame(columns=[
            'scenario_idx', 'mutation_rate', 'recombination_rate', 'event_time',
            'recent_size', 'event_size', 'n_replicates'])

        scenario_params['scenario_idx'] = np.arange(self.n_scenarios)
        scenario_params = scenario_params.set_index('scenario_idx')
        scenario_params['mutation_rate'] = \
                np.full(self.n_scenarios, self.mutation_rate)
        scenario_params['recombination_rate'] = \
                np.full(self.n_scenarios, self.recombination_rate)
        scenario_params['event_time'] = np.random.uniform(
            self.tmin / self.generation_time,
            self.tmax / self.generation_time,
            size=self.n_scenarios).astype(int)
        scenario_params['recent_size'] = (10 ** (np.random.uniform(
            low=self.n_min, high=self.n_max,
            size=self.n_scenarios))).astype(int)

        pop_size = []
        for recent_size in scenario_params['recent_size']:
            pop_size.append(10 ** self.n_min - 1)
            while (pop_size[-1] > 10 ** self.n_max or
                    pop_size[-1] < 10 ** self.n_min):
                pop_size[-1] = recent_size * 10 ** (np.random.uniform(-1, 1))

        scenario_params['event_size'] = np.array(pop_size).astype(int)
        scenario_params['n_replicates'] = \
                np.full(self.n_scenarios, self.n_replicates)
        scenario_params['n_samples'] = np.full(self.n_scenarios, self.n_samples)
        scenario_params['segment_length'] = \
                np.full(self.n_scenarios, self.segment_length).astype(int)

        return scenario_params

    def simulate_scenario(self, scenario, verbose=False):
        """
        Simulate scenarios containing only one event from a pandas
        `~pandas.DataFrame` of simulation parameters.
        """

        s = scenario

        demographic_events = [msprime.PopulationParametersChange(
            time=s.event_time, growth_rate=0, initial_size=s.event_size)]

        population_configurations = [msprime.PopulationConfiguration(
            sample_size=s.n_samples, initial_size=s.recent_size)]

        if verbose:
            msprime.DemographyDebugger(
                population_configurations=population_configurations,
                demographic_events=demographic_events).print_history()

        tree_sequence = msprime.simulate(
            length=s.segment_length,
            population_configurations=population_configurations,
            demographic_events=demographic_events,
            recombination_rate=s.recombination_rate,
            mutation_rate=s.mutation_rate,
            num_replicates=s.n_replicates,
            random_seed=self.seed)

        for rep_idx, rep in enumerate(tree_sequence):
            positions = np.array([
                variant.site.position for variant in rep.variants()
            ])
            # TODO: The following lines generate relative, unscaled positions
            # instead; however much of the current code assumes positions are
            # absolute normalized to [0.0, 1.0); later we will support other
            # normalizations, and this code could be modified as well to
            # include a normalization option.
            #  positions = np.array(positions) - np.array([0] + positions[:-1])
            #  positions = positions.astype(int)

            # Normalize positions to the range [0.0, 1.0)
            positions /= rep.sequence_length
            snps = rep.genotype_matrix().T.astype(np.uint8)
            samp = SNPSample(snp=snps, pos=positions,
                             pos_format={'normalized': True})
            yield (s.Index, rep_idx, samp)
