import os
import os.path as pth
import pathlib
import sys

from ..simulator import Simulator
from ..utils.cli import Command
from ..utils.config import Config, save_dict_annotated
from ..utils.misc import indent
from ..utils.plugins import load_plugins


DEFAULT_DATASET_CONFIG_FILENAME_FORMAT = '{model_name}_dataset_config.yml'
DEFAULT_PREPROCESSING_CONFIG_FILENAME_FORMAT = \
        '{model_name}_preprocessing_config.yml'


class InitCommand(Command):
    """Initialize a new model training configuration and directory structure."""

    default_plugins = ['dnadna.examples.one_event']

    @classmethod
    def create_argument_parser(cls, namespace=None, **kwargs):
        parser = super().create_argument_parser(namespace=namespace, **kwargs)
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--simulation-config',
                help="path to the simulation config file for the simulation "
                     "on which this model will be trained; if omitted, a "
                     "default simulation config will be appended to the "
                     "training config")
        group.add_argument('--dataset-config',
                help="path to the dataset config file for the dataset "
                     "on which this model will be trained; if omitted, a "
                     "default dataset config will be appended to the "
                     "training config")
        parser.add_argument('-m', '--model-name',
                help="name for the model / simulation we'll be training if "
                     "different from the dataset_name in the simulation config")
        parser.add_argument('models_root', metavar='MODELS-ROOT', default='.',
                nargs='?',
                help="root directory for trained models (default: "
                     "%(default)s)")

        return parser

    @classmethod
    def run(cls, args):
        preprocessing_config = Config.from_default('preprocessing')

        if args.simulation_config:
            # Ensure the file exists and validates the schema
            dataset_config = Config.from_file(args.simulation_config,
                                              schema='dataset',
                                              validate=True)
            simulator_name = dataset_config.get('simulator_name')
            if simulator_name:
                # Load any plugins mentioned in the simulation config
                load_plugins(dataset_config.get('plugins', []))
                # See if simulator_name is a known simulator, and get its
                # default preprocessing config
                try:
                    # NOTE: overrides = learned_params is special-cased here
                    # since the default preprocessing config file has some
                    # dummy learned_params that a simulator-specific
                    # preprocessing config may want to override.
                    simulator_cls = Simulator.get_plugin(simulator_name)
                    preprocessing_config = Config(
                        simulator_cls.preprocessing_config_default,
                        preprocessing_config,
                        overrides=[('learned_params',)])
                except ValueError:
                    pass
        elif args.dataset_config:
            dataset_config = Config.from_file(args.dataset_config,
                                              schema='dataset',
                                              validate=True)
        else:
            # Just use the default dataset_config
            dataset_config = Config.from_default('dataset')

        if args.model_name:
            model_name = args.model_name
        else:
            # take the model name from the dataset name
            model_name = dataset_config['dataset_name']

        # Put the model_name into the preprocessing_config
        preprocessing_config['model_name'] = model_name

        model_dir = pathlib.Path(args.models_root) / model_name

        os.makedirs(model_dir, exist_ok=True)

        def write_config(config, schema, filename_format):
            filename = filename_format.format(model_name=model_name)
            path = pth.normpath(model_dir / filename)
            print(f'Writing sample {schema} config to {path} ...',
                  file=sys.stderr)
            save_dict_annotated(config, path, schema=schema, indent=4,
                                sort_keys=False)
            config.filename = path
            return config

        if not (args.simulation_config or args.dataset_config):
            # Generate a default dataset config file
            write_config(dataset_config, 'dataset',
                         DEFAULT_DATASET_CONFIG_FILENAME_FORMAT)

        # Set the preprocessing config to inherit from the dataset config
        # file, rather than include it verbatim
        preprocessing_config = preprocessing_config.copy(folded=True)
        preprocessing_config['dataset'] = {
            'inherit': pth.relpath(dataset_config.filename, model_dir)
        }

        preprocessing_config = write_config(
            preprocessing_config,
            'preprocessing',
            DEFAULT_PREPROCESSING_CONFIG_FILENAME_FORMAT)
        print('Edit the dataset and/or preprocessing config files as needed, '
              'then run preprocessing with the command:', file=sys.stderr)
        print(file=sys.stderr)
        print(indent(f'dnadna preprocess {preprocessing_config.filename}'),
              file=sys.stderr)
