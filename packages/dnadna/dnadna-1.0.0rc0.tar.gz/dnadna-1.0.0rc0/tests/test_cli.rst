Additional tests of the command-line interface; these are implemented as
doctests in order to take advantage of the partial text matching
capabilities of the doctest format.

Test ``dnadna --help`` output of sub-commands::

    >>> from dnadna.utils.testing import run_main
    >>> run_main(['dnadna', '--help'])
    usage: dnadna [-h] [COMMAND]
    <BLANKLINE>
    dnadna version ... top-level command.
    <BLANKLINE>
    See dnadna <sub-command> --help for help on individual sub-commands.
    <BLANKLINE>
    optional arguments:
      -h, --help       show this help message and exit
      --plugin PLUGIN  load a plugin module; the plugin may be specified ...
      -V, --version    show the dnadna version and exit
    <BLANKLINE>
    sub-commands:
      init          Initialize a new model training configuration and directory
                    structure.
      preprocess    Prepare a training run from an existing model training
                    configuration.
      train         Train a model on a simulation using a specified pre-processed
                    training config.
      predict       Make parameter predictions on existing SNP data using an already
                    trained model.
      sumstats      Compute summary statistics on a simulation data set.
      simulation    Run a registered simulation.

Test ``dnadna --version``::

    >>> from dnadna import __version__
    >>> from dnadna.utils.testing import run_main
    >>> v = run_main(['dnadna', '--version'], capture=True)
    >>> v.strip() == __version__
    True

Some commands don't do anything unless a sub-command is provided; in these
cases the usage message should be printed::

    >>> from dnadna.utils.testing import run_main
    >>> run_main(['dnadna'], exitcode=2)
    usage:  dnadna [-h] [COMMAND]
    dnadna: error: a sub-command is required:
    ...
    >>> run_main(['dnadna', 'simulation'], exitcode=2)
    usage:  dnadna simulation [-h] [COMMAND]
    dnadna simulation: error: a sub-command is required:
    ...

Tests the usage output when running via ``python -m dnadna``::

    >>> from dnadna.cli import DnadnaCommand
    >>> from dnadna.utils.testing import run_main
    >>> main_py = DnadnaCommand._main_module_file()
    >>> run_main([main_py], exitcode=2, sys_executable='python')
    usage: python -m dnadna [-h] [COMMAND]
    ...
    >>> run_main([main_py, '--help'], sys_executable='python')
    usage: python -m dnadna [-h] [COMMAND]
    ...
    >>> run_main([main_py, 'init', '--help'], sys_executable='python')
    usage: python -m dnadna init [-h]
    ...


Regression test for #15--ensure that ``dnadna init`` without any arguments
still results in a reasonable output for a "generic" model::

    >>> from dnadna.utils.testing import run_main
    >>> tmpdir = getfixture('tmpdir')
    >>> with tmpdir.as_cwd():
    ...     run_main(['dnadna', 'init'])
    Writing sample dataset config to generic/generic_dataset_config.yml ...
    Writing sample preprocessing config to generic/generic_preprocessing_config.yml ...
    >>> assert tmpdir.join('generic').ensure(dir=True)
    >>> config_file = tmpdir.join('generic', 'generic_preprocessing_config.yml')
    >>> assert config_file.ensure()
    >>> from dnadna.utils.config import Config, load_dict
    >>> default_config = Config.from_default('preprocessing').copy(True)
    >>> config = load_dict(str(config_file))
    >>> _ = config.pop('dataset', None)  # the one difference from the template
    >>> _ = default_config.pop('dataset', None)
    >>> assert config == default_config


Regression test for #4--this ensures that for most commands and
sub-commands, merely running the command's ``--help`` does not result in
importing PyTorch, which in particular is the slowest and most heavy-weight
import that can slow down execution of the CLI.  With the exception of
sub-commands that load the ``dnadna.examples.one_event`` plugin by default,
since that does result in loading PyTorch, even for ``--help``::

    >>> from dnadna.utils.testing import run_main
    >>> import sys
    >>> monkeypatch = getfixture('monkeypatch')
    >>> monkeypatch.delitem(sys.modules, 'torch')
    >>> def run_help_recursive(cmd_cls, cmd_args):
    ...     if not getattr(cmd_cls, 'default_plugins', None):
    ...         print(cmd_cls.__name__)
    ...         run_main(cmd_args + ['--help'], capture=True, cmd=cmd_cls)
    ...         assert 'torch' not in sys.modules
    ...         for name, subcmd_cls in cmd_cls.subcommands.items():
    ...             run_help_recursive(subcmd_cls, cmd_args + [name])
    ...

This should just print the names of the classes whose ``--help`` was run::

    >>> run_help_recursive(DnadnaCommand, ['dnadna'])
    DnadnaCommand
    PreprocessCommand
    TrainCommand
    PredictCommand
    SumStatsCommand
    >>> monkeypatch.undo()

Regression test: Test running ``dnadna simulation init``,
ensuring that the correct default config is output::

    >>> from dnadna.utils.testing import run_main
    >>> tmpdir = getfixture('tmpdir')
    >>> with tmpdir.as_cwd():
    ...     run_main(['dnadna', 'simulation', 'init', 'my_model', 'one_event'])
    Writing sample simulation config to my_model/my_model_simulation_config.yml ...
    >>> filename = tmpdir.join('my_model', 'my_model_simulation_config.yml')
    >>> with open(str(filename)) as fobj:
    ...     print(fobj.read())
    # JSON Schema...
    ...
    simulator_name: one_event
    ...
    plugins:
    - dnadna.examples.one_event
    ...

 Test functionality of the ``--debug`` flag.  To do this, deliberately
 monkey-patch some of the commands so that they raise an unhandled
 exception::


    >>> from dnadna.utils.testing import run_main
    >>> import sys
    >>> monkeypatch = getfixture('monkeypatch')
    >>> from dnadna.cli.simulation import SimulationCommand, SimulationInitCommand
    >>> def raise_exception(*args, **kwargs):
    ...     raise RuntimeError('test exception')
    ...
    >>> monkeypatch.setattr(SimulationCommand, 'run', raise_exception)
    >>> run_main(['dnadna', 'simulation'])
    error:
    <BLANKLINE>
    RuntimeError: test exception
    <BLANKLINE>
    run again with --debug to view the full traceback, or with --pdb to drop
    into a debugger
    >>> run_main(['dnadna', 'simulation', '--debug'])
    error:
    <BLANKLINE>
    RuntimeError: test exception
    <BLANKLINE>
    <BLANKLINE>
    Traceback (most recent call last):
    ...
    RuntimeError: test exception
    >>> monkeypatch.undo()

Then try it on a sub-command (which requires slightly different handling in
the code)::

    >>> monkeypatch.setattr(SimulationInitCommand, 'run', raise_exception)
    >>> run_main(['dnadna', 'simulation', 'init'])
    error:
    <BLANKLINE>
    RuntimeError: test exception
    <BLANKLINE>
    run again with --debug to view the full traceback, or with --pdb to drop
    into a debugger
    >>> run_main(['dnadna', 'simulation', 'init', '--debug'])
    error:
    <BLANKLINE>
    RuntimeError: test exception
    <BLANKLINE>
    <BLANKLINE>
    Traceback (most recent call last):
    ...
    RuntimeError: test exception
    >>> monkeypatch.undo()
