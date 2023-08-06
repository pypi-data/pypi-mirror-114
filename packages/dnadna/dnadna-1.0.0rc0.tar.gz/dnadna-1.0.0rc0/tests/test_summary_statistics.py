"""Tests of the `dnadna.summary_statistics` module."""


import numpy as np
import pandas as pd
import pytest

from dnadna.datasets import DictSNPSource
from dnadna.simulation import Simulation
from dnadna.summary_statistics import SummaryStatistics, SumStats


def test_sumstats_run(tmp_path, cached_simulation):
    """
    Test that `SummaryStatistics.run` outputs the expected files.

    This is not a sophisticated test and does not check any of the statistical
    results; it is merely to check that the function is outputting the expected
    files to the expected paths.

    Regression test for bug introduced by
    https://gitlab.inria.fr/ml_genetics/private/dnadna/-/commit/64dabe654e59108e476dfce497a5e9a3638df053
    """

    # TODO: This setup code is mostly duplicated between tests in this module;
    # consider adding a common setup fixture
    simulation_config, scenario_params, scenarios = cached_simulation

    # set the simulation data root to the temp directory so summary stats are
    # written there
    simulation_config['data_root'] = str(tmp_path)

    source = DictSNPSource(scenarios)
    simulation = Simulation(simulation_config, source=source,
                            scenario_params=scenario_params)
    sumstats = SummaryStatistics(simulation_config, simulation=simulation)

    # limit the run to 2 replicates per scenario just to speed it up
    sumstats.run(n_replicates=2)

    # now load all the stats files and make sure they exist and are at least
    # non-empty
    seen_scenarios = 0
    for scenario_idx, stats in sumstats.load_all():
        for stat_name in stats._fields:
            stat = getattr(stats, stat_name)
            assert isinstance(stat, pd.DataFrame)
            # Also at least check that it's not completely empty; testing that
            # the actual values of the statistics are meaningful is left to
            # other tests
            assert len(stat) > 0
        seen_scenarios += 1

    assert seen_scenarios == len(scenario_params)


@pytest.mark.parametrize('sel_options', [{'window': 100}, {'window': 0}])
def test_compute_load_one_scenario(tmp_path, cached_simulation, sel_options):
    """
    Compute summary statistics for a single scenario, then load the computed
    statistics and perform some basic tests (specifically regression tests on
    bugs that have been fixed in development).
    """

    simulation_config, scenario_params, scenarios = cached_simulation
    source = DictSNPSource(scenarios)
    simulation_config.setdefault('summary_statistics', {})['sel_options'] = \
            sel_options
    simulation = Simulation(simulation_config, source=source,
                            scenario_params=scenario_params)
    sumstats = SummaryStatistics(simulation_config, simulation=simulation)

    # Compute statistics for few "random" samplings of simulations
    scenario_idxs = [0, 7, 14]
    for scenario_idx in scenario_idxs:
        stats = sumstats.compute_scenario(scenario_idx)
        filename_format = tmp_path / '{scenario_idx}_{type}.csv'
        stats.to_csv(str(filename_format),
                     format_fields={'scenario_idx': scenario_idx})

        # Load the statistics
        sfs, ld, sel = SumStats.from_csv(str(filename_format),
                format_fields={'scenario_idx': scenario_idx})

        assert isinstance(sfs, pd.DataFrame)
        assert isinstance(ld, pd.DataFrame)
        assert isinstance(sel, pd.DataFrame)

        # Load an arbitrary sample replicate from the data source against which
        # to compare some basic stats
        sample = source[scenario_idx, 0]

        # SFS (non-folded) should have 1 minus the number of individuals in
        # length (one entry for each n_indiv grouping) except 0
        assert len(sfs) == sample.n_indiv - 1

        # LD (non-circular) should have 1 minus the number of distance bins,
        # the default being 19 (TODO: why?)
        assert len(ld) == 18

        # For windowed selection statistics, the number of rows is 1 + the
        # bin count given by window; for non-windowed it is expected to be
        # the max number of SNPs across all replicates in the scenario
        window = sel_options.get('window')
        if window:
            assert len(sel) == window + 1
        else:
            n_replicates = \
                int(scenario_params.loc[scenario_idx]['n_replicates'])
            max_snp = max(source[scenario_idx, replicate_idx].n_snp
                          for replicate_idx in range(n_replicates))
            assert len(sel) == max_snp

        # A few other checks for issues that had bugs during development
        # Check that the dtypes of these columns were correctly determined:
        assert sel['label'].dtype == np.dtype(object)
        assert np.all(sel['label'] == '')
        assert sel['tajimasd_sem'].dtype == np.float64
