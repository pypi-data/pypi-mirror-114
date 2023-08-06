"""
Top-level implementation of the ``dnadna`` command-line interface.

Some individual sub-commands are implemented in other modules; the sub-command
CLIs are then unified under a single command.
"""

from .init import InitCommand
from .predict import PredictCommand
from .preprocess import PreprocessCommand
from .simulation import SimulationCommand
from .sumstats import SumStatsCommand
from .train import TrainCommand
from .. import __version__
from ..utils.cli import CommandWithPlugins
from ..utils.decorators import format_docstring


@format_docstring(version=__version__)
class DnadnaCommand(CommandWithPlugins):
    """
    dnadna version {version} top-level command.

    See dnadna <sub-command> --help for help on individual sub-commands.
    """

    subcommands = {
        'init': InitCommand,
        'preprocess': PreprocessCommand,
        'train': TrainCommand,
        'predict': PredictCommand,
        'sumstats': SumStatsCommand,
        'simulation': SimulationCommand
    }

    @classmethod
    def create_argument_parser(cls, namespace=None, **kwargs):
        # The top-level dnadna command doesn't take any special arguments
        # so just create a basic ArgumentParser with help support
        parser = super().create_argument_parser(namespace=namespace, **kwargs)
        parser.add_argument('-V', '--version', action='store_true',
                help='show the dnadna version and exit')
        return parser

    @classmethod
    def run(cls, args):
        if args.version:
            cls.exit_error(__version__, exit_code=0)
