import os.path as pth

from ..utils.cli import Command
from ..utils.misc import capture_stdio


def _gpus_list(gpus=None):
    """
    An int or comma-separated list of ints giving GPU numbers.

    Used for parsing the --gpus flag.
    """

    if isinstance(gpus, str):
        if gpus.strip() == '*':
            gpus = True
        else:
            gpus = [int(x.strip()) for x in gpus.split(',')]

    return gpus


class PredictCommand(Command):
    """
    Make parameter predictions on existing SNP data using an already trained
    model.
    """

    logging = True

    @classmethod
    def create_argument_parser(cls, namespace=None, **kwargs):
        parser = super().create_argument_parser(namespace=namespace, **kwargs)
        parser.add_argument('model', metavar='MODEL',
                help='path to either a model trained by dnadna with a .pth '
                     'extension, or the preprocessed training config file '
                     'which produced that model')
        parser.add_argument('dataset', metavar='INPUT', nargs='+',
                help='one or more files containing SNP matrices in one of '
                     'the supported formats, or a dataset config file, in '
                     'which case all files in the dataset are processed')
        parser.add_argument('-o', '--output', default=None,
                help='output file for predictions; outputs to standard '
                     'output by default')
        parser.add_argument('-p', '--preprocess', action='store_true',
                help='run preprocessing checks over each loaded scenario '
                     'and skip those that do not pass the check; otherwise '
                     'all scenarios are assumed to conform to the '
                     'requirements of the model')
        parser.add_argument('-g', '--gpus', type=_gpus_list, default=False,
                help='use any available GPUs to evaluate the model; --gpus=* '
                     'uses all available GPUs, or you can select one or more '
                     'specific GPUs to use in a comma-separated list like '
                     '--gpus=1,3')
        parser.add_argument('-w', '--loader-num-workers', type=int, default=0,
                help='number of worker process to use when loading the '
                     'prediction dataset; may help speed up prediction on '
                     'large datasets')
        parser.add_argument('--checkpoint', default='best',
                help='when passing a training run config file, specifies '
                     'which checkpoint from which to load the network (e.g. '
                     'best or last_epoch')
        parser.add_argument('--progress-bar', action='store_true',
                help='display a progress bar while evaluating predictions; '
                     'this is only useful when processing a large number of '
                     'files')
        return parser

    @classmethod
    def run(cls, args):
        from ..prediction import Predictor
        from ..snp_sample import SNPSerializer
        from ..utils.serializers import DictSerializer

        # Check if the model argument looks like a config file; if so the
        # model will be loaded using this config file instead of directly from
        # the model file
        _, ext = pth.splitext(args.model)
        if ext in DictSerializer.extensions:
            predictor = Predictor.from_config_file(args.model,
                                                   checkpoint=args.checkpoint)
        else:
            # Otherwise it is assumed to be a model file
            predictor = Predictor.from_net_file(args.model)

        # Check if the first datset argument looks like a dataset config file;
        # if so the data to run prediction on will come from the dataset,
        # otherwise the list of filenames will be checked to see if they are
        # known SNP files
        _, ext = pth.splitext(args.dataset[0])
        if ext in DictSerializer.extensions:
            if len(args.dataset) > 1:
                cls.exit_error(
                    f'when using a dataset config file as the input, only one '
                    f'input file is supported (the inputs are read from the '
                    f'dataset config file "{args.dataset[0]})')

            input_kwargs = {'dataset_config': args.dataset[0]}
        else:
            for filename in args.dataset:
                _, ext = pth.splitext(filename)
                if ext not in SNPSerializer.extensions:
                    exts = ', '.join(SNPSerializer.extensions)
                    cls.exit_error(
                        f'"{filename}" does not have one of the supported '
                        f'file types for SNP data ({exts})')

            input_kwargs = {'filenames': args.dataset}

        # Prevent possibly confusing (to users) warning message from PyTorch's
        # C++ code regarding unavailabilty of NNPACK; see
        # https://gitlab.inria.fr/ml_genetics/private/dnadna/-/merge_requests/94#note_524257
        with capture_stdio(stderr_file='/dev/null'):
            # We can go through the code path that initializes NNPACK simply by
            # evaluating a trivial 1-D convolution; we do this while sending
            # stderr to /dev/null so the warning is squelched.
            import torch
            from torch.nn import Conv1d
            c = Conv1d(1, 1, 1)
            c(torch.zeros([1, 1, 1]))

        predictor.run_prediction(
                output=args.output,
                preprocess=args.preprocess,
                gpus=args.gpus,
                loader_num_workers=args.loader_num_workers,
                progress_bar=args.progress_bar,
                **input_kwargs)
