#!/usr/bin/env python
"""
A minimal ``setup.py`` is still required when using setuptools.

See ``setup.cfg`` for package configuration.
"""

from setuptools import setup
setup(use_scm_version={
    'write_to': 'dnadna/_version.py',
    'local_scheme': 'node-and-timestamp'
})
