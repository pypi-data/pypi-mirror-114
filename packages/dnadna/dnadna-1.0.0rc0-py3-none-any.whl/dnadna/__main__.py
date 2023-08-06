"""
``__main__`` module for running the dnadna package as a module; e.g.::

    $ python -m dnadna

"""


import sys

from dnadna.cli import DnadnaCommand


sys.exit(DnadnaCommand.main())
