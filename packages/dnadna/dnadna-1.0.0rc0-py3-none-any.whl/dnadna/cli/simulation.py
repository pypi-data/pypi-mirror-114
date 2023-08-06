"""Simulation command-line interface."""


import logging
import os
import os.path as pth
import sys
import textwrap

from .. import __version__
from ..utils.cli import Command, CommandWithPlugins
from ..utils.config import save_dict_annotated, Config
from ..utils.misc import desphinxify, first_paragraph, indent


DEFAULT_SIMULATOR_PLUGINS = ['dnadna.examples.one_event']


log = logging.getLogger(__name__)


class SimulationInitCommand(CommandWithPlugins):
    """
    Initialize a new simulation.

    Outputs a default simulation config file which may be modified before
    running the simulation.
    """

    default_plugins = DEFAULT_SIMULATOR_PLUGINS

    @classmethod
    def create_argument_parser(cls, namespace=None, **kwargs):
        from ..simulator import Simulator

        simulators = sorted(name for name, _ in Simulator.get_plugins())
        parser = super().create_argument_parser(namespace=namespace, **kwargs)
        parser.add_argument('name', metavar='NAME', type=str,
                nargs='?',
                help='name to give the dataset being simulated; the simulation '
                     'data will be created in a directory with the same name '
                     'as the module, under the current directory (or the '
                     'root directory given in the last (optional) argument')

        parser.add_argument('simulator', type=str, nargs='?',
                            default='one_event', choices=simulators,
                help='the name of the simulator to run; additional '
                     'simulators can be loaded by passing the name or '
                     'filesystem path of a Python module containing '
                     'additional simulator classes; use --help-simulators '
                     'to list available simulators')

        parser.add_argument("simulations_root", metavar='SIMULATIONS-ROOT',
                default='.', type=str, nargs='?',
                help='root directory for simulations (default: %(default)s)')

        # TODO: After selecting a simulator, the selected simulator class could
        # in principle extend the command-line interface to supply additional
        # arguments, but we'll omit that functionality until/unless someone
        # wants to have it.

        return parser

    @classmethod
    def run(cls, args):
        from ..simulator import Simulator

        simulator_name = args.simulator
        simulator_cls = Simulator.get_plugin(simulator_name)
        config = simulator_cls.config_default

        # Don't accidentally modify the original default config object
        config = config.copy()

        if args.name:
            config['dataset_name'] = args.name

        dataset_name = config['dataset_name']

        # New filename based on the model name
        filename_format = simulator_cls.config_filename_format
        config_filename = filename_format.format(dataset_name=dataset_name)
        config['simulator_name'] = simulator_name

        if simulator_cls.provider is not None:
            config['plugins'] = [simulator_cls.provider]

        config['dnadna_version'] = __version__

        # Merge with the default dataset config in case there are any other
        # properties missing
        config = Config(config, Config.from_default('dataset'))

        simulations_root = pth.normpath(args.simulations_root)
        simulation_dir = pth.join(simulations_root, dataset_name)
        os.makedirs(simulation_dir, exist_ok=True)
        config_path = pth.normpath(
                pth.join(simulation_dir, config_filename))
        print(f'Writing sample simulation config to {config_path} ...',
              file=sys.stderr)
        save_dict_annotated(config, config_path, schema='simulation',
                            indent=4, sort_keys=False)
        print('Edit the config file as needed, then run this simulation '
              'with the command:', file=sys.stderr)
        print(file=sys.stderr)
        print(indent(f'dnadna simulation run {config_path}'), file=sys.stderr)
        return


class SimulationRunCommand(Command):
    """
    Run a simulation specified by a simulation config file.

    You can use ``dnadna simulation init`` to create a default simulation
    config file and output directory for the simulation.
    """

    logging = True

    @classmethod
    def create_argument_parser(cls, namespace=None, **kwargs):
        parser = super().create_argument_parser(namespace=namespace, **kwargs)
        parser.add_argument("--scenario-id", default=0, type=int)
        parser.add_argument("--scenarios-to-simulate", default=None, type=int)
        parser.add_argument("--overwrite", action='store_true',
            help='overwrite an existing simulation, in particular overwriting '
                 'the scenario params table, if it already exists; this does '
                 'not delete existing scenario data, so if there is a chance '
                 'of confusion, manually delete the scenario directories '
                 'first')
        parser.add_argument("--backup", action='store_true',
            help='back up existing simulation data before overwriting it; '
                 'implies --overwrite')
        parser.add_argument("--n-cpus", default=1, type=int)
        parser.add_argument("--verbose", action='store_true',
                        help='increase output verbosity from the simulator')
        parser.add_argument('config',  # TODO: Add a File type
            help='path to the simulation config file for the simulation '
                 'to run')
        return parser

    @classmethod
    def run(cls, args):
        from ..simulator import Simulator

        simulator = Simulator.from_config_file(args.config)

        log.info(
            f'Running {simulator.simulator_name} simulator with '
            f'n_scenarios={simulator.n_scenarios} and '
            f'n_replicates={simulator.n_replicates}')

        # Only display the progress bar if stderr is a TTY
        simulator.run_simulation(
            scenario_id=args.scenario_id,
            n_scenarios=args.scenarios_to_simulate,
            n_cpus=args.n_cpus,
            overwrite_existing=args.overwrite or args.backup,
            backup_existing=args.backup,
            progress_bar=sys.stderr.isatty(),
            verbose=args.verbose)

        log.info('Simulation complete!')
        log.info('Initialize model training with the command:')
        log.info('')
        log.info(indent(f'dnadna init --simulation-config={args.config}'))


class SimulationCommand(CommandWithPlugins):
    """Run a registered simulation."""

    default_plugins = DEFAULT_SIMULATOR_PLUGINS

    subcommands = {
        'init': SimulationInitCommand,
        'run': SimulationRunCommand
    }

    @classmethod
    def create_argument_parser(cls, namespace=None, **kwargs):
        parser = super().create_argument_parser(namespace=namespace, **kwargs)
        parser.add_argument("--help-simulators", action='store_true',
                help='print list of available simulators and exit')
        return parser

    @classmethod
    def run(cls, args):
        if args.help_simulators:
            cls.list_simulators()

    @staticmethod
    def list_simulators():
        from ..simulator import Simulator

        for name, cls in Simulator.get_plugins():
            print(name, cls, sep=': ')
            doc = desphinxify(first_paragraph(cls.__doc__ or ''))
            print(indent('\n'.join(textwrap.wrap(doc))))
        sys.exit()
