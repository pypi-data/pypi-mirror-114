import copy
import os.path as pth

from ..utils.cli import CommandWithPlugins, str_or_int


class TrainCommand(CommandWithPlugins):
    """
    Train a model on a simulation using a specified pre-processed training
    config.
    """

    logging = True
    # Override the default help message for --log-file
    logfile_format = '{model_name}_{run_name}_training.log'
    logging_args = copy.deepcopy(CommandWithPlugins.logging_args)
    logging_args['--log-file']['help'] += (
        f'; by default logs to {logfile_format} in the run directory')

    @classmethod
    def create_argument_parser(cls, namespace=None, **kwargs):
        parser = super().create_argument_parser(namespace=namespace, **kwargs)
        parser.add_argument('-r', '--run-id', type=str_or_int,
                help='run ID to give to this training run (used to initialize '
                     'the output directory for the training run); may be '
                     'either a string or an integer; if unspecified, the '
                     'next unused integer ID is determined automatically')
        parser.add_argument('--overwrite',
                            help="overwrite run (otherwise, create a new run)",
                            action="store_true")
        parser.add_argument('config',
            help='path to the training config file to use for this training '
                 'run')

        return parser

    @classmethod
    def run(cls, args):
        from ..training import ModelTrainer

        model_trainer = ModelTrainer.from_config_file(
                args.config, progress_bar=True)

        run_id, run_name, run_dir = model_trainer.get_run_info(args.run_id)
        # Configure the default logfile if it was not specified by the user
        if args.log_file is None:
            filename = cls.logfile_format.format(
                    run_name=run_name, model_name=model_trainer.model_name)
            filename = pth.join(run_dir, filename)
            cls.configure_log_file(filename, args.log_level)
            # Make sure the run directory exists since it's where the log file
            # will be written
            model_trainer.ensure_run_dir(run_id, args.overwrite)

        model_trainer.run_training(run_id=run_id, overwrite=args.overwrite)
