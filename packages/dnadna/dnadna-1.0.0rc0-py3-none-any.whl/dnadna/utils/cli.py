"""Utilities for generating the command-line interface."""


import abc
import argparse
import inspect
import logging
import os.path as pth
import shutil
import sys
import textwrap
import traceback

try:
    import coloredlogs
except ImportError:
    coloredlogs = None

from .misc import unique, stdio_redirect_tqdm
from .plugins import load_plugins


log = logging.getLogger(__name__)


# Log filter for filtering out uninteresting messages from other libraries
class DNADNAFilter(logging.Filter):
    def __init__(self, my_level):
        super().__init__(__package__.split('.')[0])  # dnadna
        if isinstance(my_level, str):
            my_level = logging.getLevelName(my_level)

        self.my_level = my_level

    def filter(self, record):
        if (self.my_level is not None and (record.levelno > self.my_level or
                self.my_level <= logging.DEBUG)):
            return True

        # The default Filter logs out messages that are not from the
        # 'dnadna' logger
        return super().filter(record)


class Command(metaclass=abc.ABCMeta):
    """
    Simple mix-in class for classes that provide a command-line interface,
    with support for sub-commands.

    This takes inspiration from cliff_, but much simpler.

    .. _cliff: https://docs.openstack.org/cliff/latest/index.html
    """

    subcommands = {}
    logging = False
    logging_args = {
        '--log-level': {
            'default': 'INFO',
            'metavar': 'LEVEL',
            'choices': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            'help': 'amount of log detail (default: INFO)'
        },
        '--log-file': {
            'metavar': 'FILENAME',
            'type': argparse.FileType('a'),
            'help': 'filename to write the log to (in addition to stdout)'
        },
        '--log-nc': {
            'action': 'store_true',
            'help': 'disable terminal colors in log output (install the '
                    'coloredlogs package to enable colors in log output)'
        }
    }
    """Command line arguments used to configure logging."""

    logging_config = {
        'format': '%(asctime)s; %(levelname)8s;  %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
    }
    """
    Additional options (passed to `logging.basicConfig`) to configure the
    logger for this command.
    """

    @classmethod
    @abc.abstractmethod
    def run(cls, args):
        """
        Sub-classes must provide a ``run()`` method which provides the "main"
        function of the command.  ``run()`` is called by this class's
        ``main()`` method which provides just a thin wrapper around it.
        """

        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create_argument_parser(cls, namespace=None, **kwargs):
        """
        Initializes a base `argparse.ArgumentParser` using any given
        ``kwargs``.  Subclasses should call this instead of
        `argparse.ArgumentParser` directly in order to properly handle
        sub-commands.
        """

        if 'prog' not in kwargs and namespace is not None:
            prog = getattr(namespace, 'prog_name', None)
            command = getattr(namespace, 'command', [])
            if prog and command:
                prog = prog + ' ' + command[0]

            if prog is not None:
                namespace.prog_name = kwargs['prog'] = prog

        descr = inspect.getdoc(cls)
        kwargs.setdefault('description', descr)

        if cls.subcommands:
            epilog = cls._format_subcommand_help()
            kwargs.setdefault('epilog', epilog)
            kwargs.setdefault('formatter_class', argparse.RawTextHelpFormatter)

        parser = argparse.ArgumentParser(**kwargs)
        parser.set_defaults(prog_name=parser.prog)

        # Add logging configuration, if enabled
        if cls.logging and cls.logging_args:
            group = parser.add_argument_group('logging')
            for argname, argparams in cls.logging_args.items():
                group.add_argument(argname, **argparams)

        if cls.subcommands:
            # Add to the default usage message to indicate addition
            # subcommands may follow
            parser.usage = parser.format_usage().replace('usage: ', '').\
                    rstrip() + ' [COMMAND]\n'
            parser.add_argument('command', nargs=argparse.REMAINDER,
                                choices=list(cls.subcommands),
                                help=argparse.SUPPRESS)

        return parser

    @staticmethod
    def preparse_args(argv=None, namespace=None):
        """
        Base argument parser handling just a few standard arguments.
        """
        preparser = argparse.ArgumentParser(add_help=False)
        preparser.add_argument("--debug", action="store_true",
                               help=argparse.SUPPRESS)
        preparser.add_argument("--pdb", action="store_true",
                               help=argparse.SUPPRESS)
        return preparser.parse_known_args(argv, namespace=namespace)

    @classmethod
    def configure_logging(cls, args):
        """
        Configure command logging facilities using the CLI arguments given
        by `Command.logging_args`.
        """

        if args.debug:
            # In --debug mode force the log level to DEBUG
            log_level = 'DEBUG'
        else:
            # Fallback to INFO if it's missing somehow
            log_level = getattr(args, 'log_level', 'INFO')

        # args.log_file might not exist if we are in debug mode but running
        # a command that does not normally configure logging
        log_file = getattr(args, 'log_file', None)

        # Delete any existing handlers on the root logger, so if this is called
        # multiple times it will reset the root logger configuration.
        del logging.getLogger().handlers[:]

        # stdio_redirect_tqdm is required so that stdout logging will cooperate
        # with any commands that use a tqdm progress bar; if they don't use
        # tqdm this will just write through to stdout as normal
        with stdio_redirect_tqdm():
            if coloredlogs and not getattr(args, 'log_nc', False):
                # Annoying inconsistency between coloredlogs.install and
                # logging.basicConfig
                logging_config = dict(cls.logging_config)
                logging_config['fmt'] = logging_config.pop('format', None)
                coloredlogs.install(level=log_level, stream=sys.stdout,
                                    **logging_config)
            else:
                logging.basicConfig(
                        stream=sys.stdout,
                        level=logging.getLevelName(log_level),
                        **cls.logging_config)

        # In addition to the basic configuration, add a filter so that only log
        # messages from DNADNA (unless they are warnings or errors) are logged;
        # some other libraries are spamming the root logger with uninteresting
        # info messages
        for handler in logging.getLogger().handlers:
            handler.addFilter(DNADNAFilter(log_level))

        if log_file:
            cls.configure_log_file(log_file, log_level)

        logging.captureWarnings(True)

    @classmethod
    def configure_log_file(cls, filename, log_level=None):
        fh = logging.FileHandler(filename, delay=True)
        fh.setLevel(log_level)
        fh.setFormatter(logging.Formatter(
            cls.logging_config['format'],
            cls.logging_config['datefmt']
        ))
        fh.addFilter(DNADNAFilter(log_level))
        logging.getLogger().addHandler(fh)

    @classmethod
    def run_subcommand(cls, args):
        command = args.command
        try:
            command_cls = cls.subcommands[command[0]]
        except KeyError:
            subcommands = ' \n'.join(cls.subcommands)
            cls.exit_error(
                f'unknown subcommand "{command[0]}"; known subcommands '
                f'are:\n {subcommands}')

        return command_cls.main(command[1:], namespace=args)

    @classmethod
    def exit_error(cls, msg='', exit_code=1):
        if msg:
            sys.stdout.flush()
            print(msg, file=sys.stderr)

        sys.exit(exit_code)

    @classmethod
    def main(cls, argv=None, namespace=None, raise_exceptions=False):
        args, argv = cls.preparse_args(argv, namespace=namespace)

        # Special handling of program name if the __main__ module is run:
        main_py = cls._main_module_file()
        if not hasattr(args, 'prog_name') and sys.argv[0] == main_py:
            package = __package__.split('.')[0]
            args.prog_name = f'{pth.basename(sys.executable)} -m {package}'

        parser = cls.create_argument_parser(namespace=args)
        args = parser.parse_args(argv, namespace=args)
        try:
            if cls.logging or args.debug:
                cls.configure_logging(args)
            ret = cls.run(args)
            if cls.subcommands:
                if not args.command:
                    parser.print_usage()
                    message = (f'{parser.prog}: error: ' +
                            cls._format_subcommand_help(
                                heading='a sub-command is required'))
                    parser.exit(status=2, message=message)
                ret2 = cls.run_subcommand(args)
                if ret2 is not None:
                    ret = ret2
            return ret
        except Exception as exc:
            if raise_exceptions:
                raise

            msgs = [f'{type(exc).__name__}: {exc}']

            if not args.debug:
                msgs.append(
                    'run again with --debug to view the full traceback, '
                    'or with --pdb to drop into a debugger')

            if cls.logging:
                if args.debug:
                    log_method = log.exception
                else:
                    log_method = log.error

                for msg in msgs:
                    log_method(msg)
            else:
                msgs.insert(0, 'error:')
                for msg in msgs:
                    print(msg, '\n', file=sys.stderr)

                if args.debug:
                    print(file=sys.stderr)
                    traceback.print_exc()

            if args.pdb:
                import pdb
                pdb.post_mortem()

            errno = getattr(exc, 'errno', 1)
            return errno

    @classmethod
    def _format_subcommand_help(cls, heading='sub-commands'):
        subcommand_names = list(cls.subcommands)
        justify = max(len(s) for s in subcommand_names) + 4
        max_justify = 10
        indent = 2
        width = shutil.get_terminal_size().columns
        lines = [heading.strip() + ':']
        for name, command_cls in cls.subcommands.items():
            doc = textwrap.dedent((command_cls.__doc__ or '')).strip()
            doc_lines = textwrap.wrap(doc,
                                      width=(width - justify - indent))
            if not doc_lines:
                doc_lines = ['']

            # Handle first line of the command doc; if the sub-command name is
            # too long, we start its documentation on the next line after it,
            # otherwise on the same line
            line = (' ' * indent) + f'{name:<{justify}}'
            if len(name) > max_justify:
                lines.append(line)
                lines.append('')
                next_line = 0
            else:
                line += f'{doc_lines[0]}'
                lines.append(line)
                next_line = 1

            lines.extend([' ' * (indent + justify) + line
                          for line in doc_lines[next_line:]])
        lines.append('')
        return '\n'.join(lines)

    @staticmethod
    def _main_module_file():
        """Returns the path to the ``dnadna.__main__`` module."""
        return pth.normpath(pth.join(
            pth.dirname(__file__), pth.pardir, '__main__.py'))


class CommandWithPlugins(Command):
    """
    Like `Command`, but with built-in support for a ``--plugins`` argument (one
    or more) which loads specified plugins before processing the rest of the
    command line.
    """

    default_plugins = []
    """Subclasses can provide a list of plugins to load by default."""

    @classmethod
    def preparse_args(cls, argv=None, namespace=None):
        namespace, argv = super().preparse_args(argv, namespace)
        # preparser implements the --plugin argument; after processing plugin
        # arguments the full arguments are re-parsed with all plugins loaded,
        # which my provide additional command-line interface extensions
        preparser = argparse.ArgumentParser(add_help=False)
        cls._add_plugin_argument(preparser, namespace=namespace)

        args, argv = preparser.parse_known_args(argv, namespace=namespace)
        # Add logging support even for commands that don't support logging
        # by default, so that plugin-loading can be logged
        if args.trace_plugins:
            cls.configure_logging(args)

        # uniquify plugins
        args.plugins = unique(args.plugins)
        load_plugins(args.plugins)
        return args, argv

    @classmethod
    @abc.abstractmethod
    def create_argument_parser(cls, namespace=None, **kwargs):
        parser = super().create_argument_parser(namespace=namespace, **kwargs)
        cls._add_plugin_argument(parser, namespace=namespace)
        return parser

    @classmethod
    def _add_plugin_argument(cls, parser, namespace=None):
        """Adds the --plugin argument to the given argument parser."""

        parser.add_argument('--plugin', type=str, action='append',
            metavar='PLUGIN', dest='plugins', default=cls.default_plugins,
            help='load a plugin module; the plugin may be specified either '
                 'as the file path to a Python module, or the name of a '
                 'module importable on the current Python module path (i.e. '
                 'sys.path); plugins are just Python modules which '
                 'may load arbitrary code (new simulators, loss functions, '
                 'etc.) during DNADNA startup); --plugin may be passed '
                 'multiple times to load multiple plugins')
        parser.add_argument('--trace-plugins', action='store_true',
            help='enable tracing of plugin loading; for most commands this '
                 'is enabled by default, but for other commands is disabled '
                 'to reduce noise; this forces it to be enabled')

        # If the existing argument namespace already contains a plugins list
        # (as may be the case when running a subcommand of a command that also
        # supports --plugin) go ahead and *extend* the list with this command's
        # default plugins (otherwise the defaults won't be added)
        if (namespace is not None and
                isinstance(getattr(namespace, 'plugins', None), list)):
            namespace.plugins.extend(cls.default_plugins)


def str_or_int(value):
    """
    Argument type that can be either a string or a non-negative integer.

    If the given string looks like a non-negative integer it is converted to an
    `int`; otherwise it is left as a `str`.

    Examples
    --------
    >>> from dnadna.utils.cli import str_or_int
    >>> str_or_int('a')
    'a'
    >>> str_or_int(0)
    0
    >>> str_or_int('0')
    0
    >>> str_or_int('-1')
    '-1'
    """

    value = str(value)

    try:
        value = int(value)
        if value < 0:
            return str(value)

        return value
    except ValueError:
        return value
