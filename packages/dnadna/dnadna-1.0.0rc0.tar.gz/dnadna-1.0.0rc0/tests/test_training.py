"""Tests of the `dnadna.training` module."""


from itertools import product

import pandas as pd
import pytest
import torch
from pytest import approx

from dnadna.data_preprocessing import DataPreprocessor
from dnadna.datasets import DNADataset, DNATrainingDataset
from dnadna.nets import Network
from dnadna.params import LearnedParams
from dnadna.training import ModelTrainer
from dnadna.utils.config import Config
from dnadna.utils.testing import USE_CUDA, DummySource


@pytest.mark.parametrize('network,use_cuda',
                         product(['MLP', 'CustomCNN',
                                  ('SPIDNA', {
                                      'n_features': 3,
                                      'n_blocks': 2
                                  })],
                                 USE_CUDA))
def test_random_seed(cached_preprocessor, network, use_cuda):
    """
    Test that two training runs in a row on the same data with the same random
    seed produce the same output for best loss.
    """

    preprocessor = cached_preprocessor
    preprocessed_scenario_params, processed_config = \
            preprocessor.preprocess_scenario_params()

    # Still necessary to make a deep copy of the original generated config, or
    # else this can mess up other tests that use it (since it's cached).
    processed_config = processed_config.copy(True)

    if isinstance(network, tuple):
        net_name, net_params = network
    else:
        net_name = network
        net_params = None

    # Test parameters
    processed_config['network']['name'] = net_name
    if net_params is not None:
        processed_config['network']['params'] = net_params
    processed_config['use_cuda'] = use_cuda
    processed_config['seed'] = 0  # for reproducibility of tests

    def train():
        source = preprocessor.dataset.source
        dataset = DNATrainingDataset(
                processed_config, source=source,
                scenario_params=preprocessed_scenario_params)
        trainer = ModelTrainer(processed_config)
        trainer.prepare(
                dataset=dataset,
                preprocessed_scenario_params=preprocessed_scenario_params)
        return trainer.train()  # returns best loss

    # Run training twice from scratch and compare results
    loss1 = train()
    loss2 = train()

    if use_cuda:
        # When using CUDA there are some sources of floating point variation
        # that cannot be easily controlled for, so as long as the values are
        # "close enough" the test passes
        # See https://gitlab.inria.fr/ml_genetics/private/dnadna/issues/9
        assert loss1 == approx(loss2, rel=1e-2)
    else:
        assert loss1 == loss2


class TestLossComputations:
    """Various tests related to calculating losses from nets."""

    @pytest.mark.parametrize('use_cuda', USE_CUDA)
    def test_compute_loss_metrics_regression(self, use_cuda):
        """
        Test ``ModelTrainer._compute_loss_metrics`` on two regression
        parameters only.
        """

        param_config = {
            'x': {'type': 'regression', 'loss_func': 'MSE'},
            'y': {'type': 'regression', 'loss_func': 'MSE'}
        }

        # Fake parameter values for a couple batches
        param_values = {
            'x': [0.0, 1.0],
            'y': [2.0, 3.0],
        }

        trainer = self._make_dummy_trainer(param_config, param_values, use_cuda)

        targets = torch.cat((
            torch.tensor(param_values['x']).unsqueeze(1),
            torch.tensor(param_values['y']).unsqueeze(1)), 1)

        # Check that we're arranging the targets correctly
        assert bool((targets == torch.tensor([
            [0.0, 2.0],
            [1.0, 3.0]
        ])).all())

        targets = targets.to(trainer.device)

        # Fake outputs from a hypothetical net, chosen so that the
        # MSE losses will be 0.01 for both parameters
        outputs = torch.tensor([
            [0.1, 1.8],
            [0.9, 2.8]
        ]).to(trainer.device).requires_grad_()

        # TODO: Test also with validation=True
        losses, errors = trainer._compute_loss_metrics(outputs, targets)
        losses, errors = losses.to('cpu'), errors.to('cpu')
        assert torch.allclose(losses, torch.tensor([0.01, 0.04]))
        assert torch.allclose(errors, torch.tensor([0.01, 0.04]))

    @pytest.mark.parametrize('use_cuda', USE_CUDA)
    def test_compute_loss_metrics_regression_and_classification(self, use_cuda):
        """
        Test ``ModelTrainer._compute_loss_metrics`` with both a regression
        parameter and a classification parameter on three categories.
        """

        param_config = {
            'x': {'type': 'regression', 'loss_func': 'MSE'},
            'c': {'type': 'classification', 'loss_func': 'cross entropy',
                  'classes': 3}
        }

        # Fake parameter values for a couple batches
        param_values = {
            'x': [0.0, 1.0],
            'c': [0, 2]
        }

        trainer = self._make_dummy_trainer(param_config, param_values, use_cuda)

        targets = torch.cat((
            torch.tensor(param_values['x']).unsqueeze(1),
            torch.tensor(param_values['c']).unsqueeze(1).float()), 1)

        # Check that we're arranging the targets correctly
        assert bool((targets == torch.tensor([
            [0.0, 0.0],  # x, c
            [1.0, 2.0]   # x, c
        ])).all())

        targets = targets.to(trainer.device)

        # Fake outputs from a hypothetical net, chosen so that the
        # MSE loss for 'x' will be 0.01, and a hard-coded value pre-determined
        # numerically so that cross-entropy loss will also be close to 0.01
        outputs = torch.tensor([
            [0.1, 5.293529352935294, 0.0, 0.0],
            [0.9, 0.0, 0.0, 5.293529352935294]
        ]).to(trainer.device).requires_grad_()

        # TODO: Test also with validation=True
        losses, errors = trainer._compute_loss_metrics(outputs, targets)
        losses, errors = losses.to('cpu'), errors.to('cpu')

        # NOTE: Classification parameter losses are weighted by the inverse of
        # their number of classes, or 1/3 in this case; see
        # LearnedParams.loss_weights
        assert torch.allclose(losses, torch.tensor([0.01, 0.0033]), atol=1e-4)
        assert torch.allclose(errors, torch.tensor([0.01, 0.0]))

    @pytest.mark.parametrize('use_cuda', USE_CUDA)
    def test_compute_loss_metrics_one_param_monobatch(self, use_cuda):
        """
        Regression test for issue #34.

        Test that ``ModelTrainer._compute_loss_metrics`` works when there is
        only one parameter and ``batch_size = 1``.
        """

        param_config = {
            'x': {'type': 'regression', 'loss_func': 'MSE'},
        }

        # Fake parameter values; we have to provide at least two values because
        # the DataPreprocessor in _make_dummy_trainer expects at least one
        # training and one validation scenario--when we perform the test we
        # will create a slice with only one value (batch_size = 1)
        param_values = {'x': [1.0, 1.0]}

        trainer = self._make_dummy_trainer(param_config, param_values, use_cuda)
        targets = torch.tensor(param_values['x'][:1]).unsqueeze(0)
        targets = targets.to(trainer.device)
        outputs = torch.tensor([[0.9]]).to(trainer.device).requires_grad_()

        losses, errors = trainer._compute_loss_metrics(outputs, targets)
        losses, errors = losses.to('cpu'), errors.to('cpu')

        assert torch.allclose(losses, torch.tensor([0.01]))
        assert torch.allclose(errors, torch.tensor([0.01]))

    def test_net_with_arbitrary_kwargs(self):
        """
        Test initialization of a network which accepts arbitrary ``**kwargs``
        in its ``__init__``.

        Regression test for
        https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/51
        """

        trainer = self._make_dummy_trainer()

        # Register a network
        class TestNetWithArbitraryKwargs(Network):
            def __init__(self, n_snp, n_indiv, n_outputs, **kwargs):
                self.n_snp = n_snp
                self.n_indiv = n_indiv
                self.n_outputs = n_outputs
                self.kwargs = kwargs

            def forward(self, x):
                pass

        trainer.network = {
            'name': 'TestNetWithArbitraryKwargs',
            'params': {'a': 1, 'b': 2, 'c': 3}
        }
        net, _ = trainer._prepare_net()

        assert net.n_snp == 1  # this and the next value are due to DummySource
        assert net.n_indiv == 1
        assert net.n_outputs == 1

        # any additional network params are passed as **kwargs
        assert net.kwargs == {'a': 1, 'b': 2, 'c': 3}

    @staticmethod
    def _make_dummy_trainer(param_config=None, param_values=None,
                            use_cuda=False):
        """
        Creates a `~dnadna.training.ModelTrainer` for testing methods of that
        class.

        Parameters
        ----------
        param_config : dict
            learned_parameters configuration
        param_values : dict
            map param names to lists of target values for each parameter
        use_cuda : bool
            whether or not to enable CUDA support for the test
        """

        # For tests where we don'g care about the params, just make a
        # trivial default parameter with a couple values
        if param_config is None:
            param_config = {'x': {'type': 'regression'}}

        if param_values is None:
            param_values = {param: [0.0, 1.0] for param in param_config}

        training_config = Config.from_default('training',
                schema='training').copy(True)
        dataset_config = Config.from_default('dataset',
                schema='dataset').copy(True)

        # Note: The new defaults for the 'crop' transform using
        # keep_polymorphic_only=True seems to break some of the tests that use
        # this as the test SNPs are very small and basic.  For these tests just
        # remove all default transforms for now.
        training_config['dataset_transforms'] = []

        scenario_params = pd.DataFrame(param_values)
        scenario_params['n_replicates'] = [1] * len(scenario_params)

        # dummy simulation and simulation config
        training_config['dataset'] = dataset_config
        learned_params = LearnedParams(param_config, scenario_params)
        dummy_dataset = DNADataset(dataset_config, source=DummySource(),
                                   scenario_params=scenario_params)

        # modify the original training config with two fake regression
        # parameters, and use a more basic net
        training_config['network']['name'] = 'MLP'
        training_config['learned_params'] = param_config
        training_config['use_cuda'] = use_cuda
        # Set the seed so it is consistent between test runs, for historical
        # reasons it is set to 2 (see
        # https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/109)
        training_config['seed'] = 2

        preprocessor = DataPreprocessor(training_config,
                                        dataset=dummy_dataset)
        preprocessed_scenario_params, processed_config = \
                preprocessor.preprocess_scenario_params()

        # Force all scenarios to be in the training set for the purposes of
        # this test.
        preprocessed_scenario_params['splits'] = \
                ['training'] * len(scenario_params)

        # It doesn't matter what the simulation configuration is because we are
        # only using fake data to pass directly to
        # ModelTrainer._compute_loss_metrics, so the data loader doesn't enter
        # into this test
        dummy_dataset = DNATrainingDataset(
                training_config, source=DummySource(),
                learned_params=learned_params,
                scenario_params=preprocessed_scenario_params)
        trainer = ModelTrainer(processed_config)
        trainer.prepare(
                dataset=dummy_dataset,
                preprocessed_scenario_params=preprocessed_scenario_params)

        return trainer
