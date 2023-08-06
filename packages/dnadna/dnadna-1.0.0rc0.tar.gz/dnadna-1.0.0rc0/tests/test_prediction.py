"""Additional tests of the `dnadna.prediction` module."""


from unittest.mock import MagicMock

import torch

from dnadna.prediction import Predictor
from dnadna.utils.config import Config


def test_predict_with_classification_params():
    """
    Test that the output of `dnadnda.prediction.Predictor.predict` is correct
    when there are classification parameters in the mix.
    """

    # A fake (partial) training config sufficient to configure some params
    # that a network was trained on.
    config = Config({
        'network': {
            'name': 'CustomCNN'
        },
        'learned_params': {
            'position': {'type': 'regression'},
            'selection': {
                'type': 'classification',
                'classes': ['yes', 'no']
            }
        }
    })

    # A mock network which when called will return a fake prediction
    net = MagicMock(return_value=torch.tensor([[0.123, 0.1, 0.9]]))

    # For the purposes of this test (using a mock net) it doesn't matter what
    # the values of the SNP are
    snp = torch.tensor([[0.1, 0.2], [0, 1], [1, 0]])

    predictor = Predictor(config, net, validate=False)
    prediction = predictor.predict(snp, sample_meta=(1, 2),
            extra_cols=('scenario_idx', 'replicate_idx'))
    prediction_cls = predictor.prediction_cls(extra_cols=('scenario_idx',
        'replicate_idx'))
    print(prediction)
    assert isinstance(prediction, prediction_cls)
    assert prediction._fields == ('scenario_idx', 'replicate_idx',
            'position', 'selection_yes', 'selection_no', 'selection')
    # softmax((0.1, 0.9)) = (0.3100255, 0.6899744)
    assert prediction == (1, 2, 0.123, 0.3100255, 0.6899744, 'no')
