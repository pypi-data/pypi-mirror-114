"""Top-level dnadna package."""


import os.path as pth

from .version import get_version


__version__ = get_version()


DEFAULTS_DIR = pth.join(pth.dirname(__file__), 'defaults')
"""
Directory in which to find default config files.

.. todo::

    Maybe this should be extended to allow a list of directories to search.

"""


BUILTIN_PLUGINS = [
    'dnadna.nets',
    'dnadna.optim',
    'dnadna.simulator',
    'dnadna.transforms'
]
"""
List all internal modules that provide a `Pluggable` class.

These modules must be imported when providing dynamic plugin discovery by
pluggable interface name (e.g. listing all network names, including networks
provided by third-party plugins).
"""


class DNADNAWarning(UserWarning):
    """Warning class for all warnings from DNADNA."""


# clean up module namespace
del pth, get_version
