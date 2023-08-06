"""
This directory contains some example config files that are used for generating
the example configurations output by commands like ``dnadna init`` and ``dnadna
preprocess``.

Currently they do not contain all the required properties (it might be a good
idea if they did).  Rather, when they are loaded with
`~dnadna.utils.config.Config.from_default` the associated schemas are used to
fill in default values for the remaining properties.

If this module is imported like ``import dnadna.defaults`` each default config
is available as ``DEFAULT_<NAME>_CONFIG`` where ``<NAME>`` is the name of the
file without the ``.yml``.  For example ``DEFAULT_DATASET_CONFIG``.
"""


import glob
import os.path as pth

from ..utils.config import Config


for filename in glob.glob(pth.join(pth.dirname(__file__), '*.yml')):
    name = pth.splitext(pth.basename(filename))[0]
    varname = f'DEFAULT_{name.upper()}_CONFIG'
    locals()[varname] = Config.from_default(name)


# cleanup
del filename, name, varname
