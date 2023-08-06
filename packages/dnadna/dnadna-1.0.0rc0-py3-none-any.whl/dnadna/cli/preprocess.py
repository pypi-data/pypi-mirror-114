import copy
import os.path as pth

from ..utils.cli import Command


class PreprocessCommand(Command):
    """Prepare a training run from an existing model training configuration."""

    logging = True
    # Override the default help message for --log-file
    logfile_format = '{model_name}_preprocessing.log'
    logging_args = copy.deepcopy(Command.logging_args)
    logging_args['--log-file']['help'] += (
        f'; by default logs to {logfile_format} in the run directory')

    @classmethod
    def create_argument_parser(cls, namespace=None, **kwargs):
        parser = super().create_argument_parser(namespace=namespace, **kwargs)
        parser.add_argument('config',
                            help='path to the preprocessing config file')

        return parser

    @classmethod
    def run(cls, args):
        from ..data_preprocessing import DataPreprocessor
        preprocessor = DataPreprocessor.from_config_file(
                args.config)

        # Configure the default logfile if it was not specified by the user
        if args.log_file is None:
            filename = cls.logfile_format.format(
                    model_name=preprocessor.model_name)
            filename = pth.join(preprocessor.model_root, filename)
            cls.configure_log_file(filename, args.log_level)

        preprocessor.run_preprocessing(progress_bar=True)
