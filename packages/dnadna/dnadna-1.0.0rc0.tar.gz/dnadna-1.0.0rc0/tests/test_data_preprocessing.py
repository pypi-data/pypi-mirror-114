"""Additional tests for data preprocessing."""

import copy
import logging

import numpy as np
import pandas as pd
import pytest

from dnadna.data_preprocessing import DataPreprocessor
from dnadna.datasets import DNADataset
from dnadna.utils.config import Config, ConfigError
from dnadna.utils.testing import DummySource


def test_random_seed(cached_preprocessor):
    """
    Test that two preprocessing runs in a row on the same data with the same
    random seed produce the same pre-processed scenario params.
    """

    def preprocess():
        config = copy.deepcopy(cached_preprocessor.config)
        config['preprocessing']['seed'] = 0
        preprocessor = DataPreprocessor(config,
                dataset=cached_preprocessor.dataset)
        return preprocessor.preprocess_scenario_params()

    results1 = preprocess()
    results2 = preprocess()

    config1 = results1[1].copy(True)
    config2 = results2[1].copy(True)
    # drop datetime from the results since they necessarily won't compare equal
    del config1['preprocessing_datetime']
    del config2['preprocessing_datetime']

    # compare the config results
    assert config1 == config2

    # compare the pre-processed scenario params
    assert (results1[0] == results2[0]).all().all()


def test_preprocessing_performance(cached_preprocessor, monkeypatch):
    """
    Regression test for
    https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/47

    This ensures that the full SNP data is never loaded during preprocessing
    (in the future this requirement may change, but currently it should be
    unnecessary).
    """

    def fake_get_data(self):
        raise RuntimeError('this function should not be called')

    monkeypatch.setattr('dnadna.snp_sample.NpzSNPConverter.get_data',
                        fake_get_data)

    preprocessor = cached_preprocessor
    assert preprocessor.dataset.source.lazy  # the default
    preprocessor.preprocess_scenario_params()


def test_validate_config(caplog):
    """
    Test validation of preprocessing config files.

    Regression test for https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/102
    """

    # The minimum necessary bits to create a DataPreprocessor
    fake_dataset = DNADataset(Config.from_default('dataset'),
                              source=DummySource(),
                              scenario_params=pd.DataFrame())
    config = Config.from_default('preprocessing').copy(True)
    preprocessor = DataPreprocessor(config, dataset=fake_dataset)

    # The defaults for dataset_splits should be "just right"
    preprocessor.validate_config(config)

    # Make it so the splits don't add up to 1
    # Chosen so that they sum to a nice floating point value
    config['dataset_splits'] = {
        'training': 0.25,
        'validation': 0.25,
        'test': 0.25
    }

    with caplog.at_level(logging.WARNING):
        preprocessor.validate_config(config)

    assert config['dataset_splits'] == {
        'training': 0.25,
        'validation': 0.25,
        'test': 0.25,
        'unused': 0.25
    }

    for rec in caplog.records:
        assert 'dataset_splits must sum to 1.0' in rec.message

    # Make it so they add to over 1
    config['dataset_splits'] = {
        'training': 0.2,
        'validation': 0.4,
        'test': 0.5
    }

    with pytest.raises(ConfigError) as exc:
        preprocessor.validate_config(config)

    assert ('dataset_splits must sum to 1.0; the given splits sum to 1.1'
            in str(exc.value))


def test_drop_unused_scenarios():
    """
    When dataset_splits does not add up to 1.0, this means some subset of the
    scenarios will be unused.

    In this case the (randomly selected) unused scenarios should be dropped
    from the output scenario params table.

    Regression test for
    https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/103
    """

    # A fake scenario params table with 100 scenarios in it
    sp = pd.DataFrame({
        'scenario_idx': np.arange(100),
        'param1': np.zeros(100),
        'param2': np.zeros(100),
        'n_replicates': np.repeat(1, 100)}).set_index('scenario_idx')

    # The minimum necessary bits to create a DataPreprocessor
    fake_dataset = DNADataset(Config.from_default('dataset'),
                              source=DummySource(),
                              scenario_params=sp)
    config = Config.from_default('preprocessing').copy(True)

    # Splits that do not add up to 1.
    config['dataset_splits'] = {
        'training': 0.25,
        'validation': 0.25,
        'test': 0.25
    }

    preprocessor = DataPreprocessor(config, dataset=fake_dataset)
    preprocessed_sp, _ = preprocessor.preprocess_scenario_params()
    assert 'splits' in preprocessed_sp
    splits = preprocessed_sp['splits']
    assert len(splits) == 75   # not 100, since we dropped some
    assert len(splits[splits == 'training']) == 25
    assert len(splits[splits == 'validation']) == 25
    assert len(splits[splits == 'test']) == 25
