"""Tests for the default config files."""


import os
import os.path as pth

import pytest

import dnadna
from dnadna.utils.config import Config


DEFAULT_CONFIGS = [f for f in os.listdir(dnadna.DEFAULTS_DIR)
                   if f.endswith('.yml')]


@pytest.mark.parametrize('config', DEFAULT_CONFIGS)
def test_default_config_valid(config):
    """
    Tests a default config file against the appropriate schema.

    Right now the schema to use for each default is the same as the file name.
    If that ever changes for some reason we'll need a different mechanism to
    specify the schema).
    """

    schema = pth.splitext(config)[0]
    Config.from_default(config, schema=schema, validate=True)
