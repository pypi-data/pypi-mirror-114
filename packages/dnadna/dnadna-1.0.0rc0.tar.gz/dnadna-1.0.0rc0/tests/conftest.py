"""Configure pytest, in particular by loading fixtures used by the tests."""


import os

import pytest

from dnadna.utils.testing import cached_simulation, cached_preprocessor  # noqa: F401


@pytest.fixture
def change_test_dir(request, tmp_path):
    os.chdir(tmp_path)
    yield
    os.chdir(request.config.invocation_dir)
