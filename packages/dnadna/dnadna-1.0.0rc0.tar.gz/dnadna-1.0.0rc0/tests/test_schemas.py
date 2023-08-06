"""
Tests of file format schemas, for correctness of the schema itself, as well as
test of files against the schema.
"""

import copy
import os
import os.path as pth
from itertools import product

import jsonschema
import pytest

from dnadna.examples.one_event import DEFAULT_ONE_EVENT_CONFIG
from dnadna.utils.config import ConfigError, Config, load_dict
from dnadna.utils.jsonschema import (make_config_meta_schema, SCHEMA_DIRS,
        SCHEMA_SUPPORTED_VERSIONS)
from dnadna.utils.misc import parse_format


SCHEMAS = {f: d for d in SCHEMA_DIRS
                for f in os.listdir(d) if f.endswith('.yml')}


@pytest.mark.parametrize('schema,validator',
                         product(SCHEMAS, SCHEMA_SUPPORTED_VERSIONS))
def test_schemas_valid(schema, validator):
    """
    Test that all schemas in the ``dnadna/schemas`` directory are valid
    Draft-06 (minimum) or Draft-07 JSON Schemas.
    """

    # add a format checker for the "errorMsg" custom format used for error
    # messages--this checks that all errorMsgs contain only the supported
    # template variables
    format_checker = jsonschema.FormatChecker()

    @format_checker.checks('errorMsg', AssertionError)
    def errormsg(value):
        template_vars = set([
            'property', 'value', 'validator', 'validator_value'])
        assert isinstance(value, str) and len(value) >= 1
        assert set(parse_format(value)).issubset(template_vars)
        return True

    # extend the validator to also check our extended meta-schema with support
    # for errorMsg
    class TestValidator(validator):
        META_SCHEMA = make_config_meta_schema(validator.META_SCHEMA)

        def __init__(self, *args, **kwargs):
            # We have to extend __init__ because the default implementation
            # of validator.check_schema doesn't allow passing a
            # format_checker
            super().__init__(*args, **kwargs)
            self.format_checker = format_checker

    # NOTE: We leave the full directory name out of the 'schema' parameter for
    # cleaner output when running `pytest -v`; instead join the filename with
    # the SCHEMA_DIR here.
    schema = load_dict(pth.join(SCHEMAS[schema], schema))
    assert TestValidator.check_schema(schema) is None


def test_training_schema_validation_errors():
    """
    Regression test for different (improved) error messages for invalid
    learned_params in a training config, based on the examples in
    https://gitlab.inria.fr/ml_genetics/private/dnadna/-/merge_requests/49#note_418849
    """

    # .copy() makes it forget its filename, which makes the asserts below
    # a bit simpler
    config = Config.from_default('training').copy(folded=True)

    # no learned_params
    try:
        del config['learned_params']
    except KeyError:
        pass

    with pytest.raises(ConfigError) as exc:
        config.validate(schema='training')

    assert "'learned_params' is a required property" in str(exc.value)

    # parameter is the wrong type
    config['learned_params'] = {'selection': None}

    with pytest.raises(ConfigError) as exc:
        config.validate(schema='training')

    assert ("'learned_params.selection': must be an object like:"
            in str(exc.value))

    # missing classes for classification param
    config['learned_params']['selection'] = {'type': 'classification'}

    with pytest.raises(ConfigError) as exc:
        config.validate(schema='training')

    assert ("'learned_params.selection': 'classes' is a required property"
            in str(exc.value))


@pytest.mark.parametrize('empty_learned_params', [[], {}])
def test_empty_learned_params(empty_learned_params):
    """
    Demonstrates that a useful error message is given if learned_params is
    empty.
    """

    # .copy() makes it forget its filename, which makes the assert below
    # a bit simpler
    config = Config.from_default('training').copy(folded=True)
    config['learned_params'] = empty_learned_params

    with pytest.raises(ConfigError) as exc:
        config.validate(schema='training')

    assert ("'learned_params': at least one parameter must be declared in "
            "learned_params" in str(exc.value))


def test_simulation_schema_inheritance():
    """
    This simulation.yml schema is a superset of the dataset.yml schema.

    Ensure that a simulation config is also valid as a dataset config.
    """

    config = Config(copy.deepcopy(DEFAULT_ONE_EVENT_CONFIG))

    # First ensure it passes the simulation schema--this should be trivial
    # since if it didn't we'd be in bigger trouble.
    config.validate('simulation')

    # Confirm that it is also a valid dataset
    config.validate('dataset')
