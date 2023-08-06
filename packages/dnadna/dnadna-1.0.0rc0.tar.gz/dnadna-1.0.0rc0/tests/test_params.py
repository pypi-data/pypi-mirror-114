"""Test learned parameter management."""


import os.path as pth

import jsonschema
import pandas as pd

import dnadna
from dnadna.params import LearnedParams
from dnadna.utils.config import load_dict


class TestSchema:
    """
    Tests of the ``param-set.yml`` schema.

    This is a slightly complex schema that is worth testing for correctness in
    some cases.
    """

    @classmethod
    def setup_class(cls):
        cls.schema_dir = pth.join(pth.dirname(dnadna.__file__), 'schemas')
        cls.schema_file = pth.join(cls.schema_dir, 'param-set.yml')
        cls.schema = load_dict(cls.schema_file)

    @classmethod
    def valid(cls, obj):
        try:
            return jsonschema.validate(obj, cls.schema) is None
        except jsonschema.ValidationError:
            return False

    def test_type(self):
        """
        Test that a parameter's type can only be 'regression' or
        'classification', and that the 'classes' property is required and
        allowed if and only if the type is 'classification'.
        """

        # Params must have a type of 'regression' or 'classification'
        assert not self.valid({'param': {}})
        assert not self.valid({'param': {'type': 'x'}})

        assert self.valid({'reg_param': {'type': 'regression'}})

        assert not self.valid({
            'reg_param': {
                'type': 'regression',
                'classes': 2
            }
        })

        assert not self.valid({'class_param': {'type': 'classification'}})

        # Test different valid formats for classes
        for classes in [1, 2, ['a'], ['a', 'b'], ['a', 1]]:
            assert self.valid({
                'class_param': {
                    'type': 'classification',
                    'classes': classes
                }
            })

        # Test invalid format for classes
        assert not self.valid({
            'class_param': {
                'type': 'classification',
                'classes': 'a'
            }
        })

        # Only regression params can have log_transform
        for log_transform in (True, False):
            assert not self.valid({
                'class_param': {
                    'type': 'classification',
                    'log_transform': log_transform
                }
            })

            assert self.valid({
                'reg_param': {
                    'type': 'regression',
                    'log_transform': log_transform
                }
            })

    def test_validate_regression_param(self):
        """
        Ensure that a typical regression parameter passes schema validation.

        This is a regression test, as it was found to previously fail at
        runtime.
        """

        learned_params = {
            'recent_size': {
                'type': 'regression',
                'loss_func': 'MSE',
                'loss_weight': 1.0,
                'log_transform': True
            }
        }

        assert self.valid(learned_params)


def test_param_ordering_by_scenario_params():
    """
    Ensure that, if no other ordering is specified in the config (by giving
    an explicit ordered mapping), the order parameters are taken from the
    scenario params table.

    Regression test for #46.
    """

    # param3 is an extra param that we're not learning
    scenario_params = pd.DataFrame({
        'param1': [0], 'param2': [0], 'param3': [0]
    }, columns=['param1', 'param2', 'param3'])

    # Config using a dict for the params, in this case although Python 3.6+
    # dicts *are* ordered, the ordering is not explicitly guaranteed by the
    # serialization format (YAML or JSON) so we take the order from the
    # scenario_params
    config = {
        'param2': {'type': 'regression'},
        'param1': {'type': 'classification', 'classes': 2}
    }
    lp = LearnedParams(config, scenario_params)
    assert lp.param_names == ['param1', 'param2']

    # Now the config is given with an ordered mapping with explicit ordering
    # to the parameters inherent in the data structure
    config = [{k: v} for k, v in config.items()]
    lp = LearnedParams(config, scenario_params)
    assert lp.param_names == ['param2', 'param1']
