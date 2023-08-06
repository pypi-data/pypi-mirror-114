"""Tests spanning the `dnadna` package."""


import doctest
import io
import os.path as pth
import subprocess as sp
from argparse import Namespace

import mistletoe
import pandas as pd
import pytest
from pytest_doctestplus.output_checker import OutputChecker, FLOAT_CMP

from dnadna.cli import DnadnaCommand
from dnadna.examples import one_event
from dnadna.examples.one_event import OneEventSimulator
from dnadna.utils.config import Config
from dnadna.utils.misc import indent


# NOTE: FLOAT_IGNORE implies FLOAT_CMP, but modifies it to always return
# True for the comparison
FLOAT_IGNORE = doctest.register_optionflag('FLOAT_IGNORE') | FLOAT_CMP


class IgnoreFloatsOutputChecker(OutputChecker):
    """
    Extends the pytest-doctestplus ``OutputChecker`` with a new flag to
    completely ignore differences in floating point values.

    For the purposes of ``TestQuickStartTutorial`` the numerical outputs
    of the tests are not meaningful, but it is still more interesting for
    the test's expected output to contain real numbers instead of ``...``,
    so we will use this to ignore differences in floating point values.
    """

    ignore_floats = False

    def check_output(self, want, got, flags):
        self.ignore_floats = bool(flags & FLOAT_IGNORE)
        return super().check_output(want, got, flags)

    def equal_floats(self, a, b):
        # In the base class, this method performs comparison between two floats
        # using absolute and relative tolerances.  If we ran check_output with
        # the FLOAT_IGNORE flag enabled, this just returns True
        if self.ignore_floats:
            return True

        return super().equal_floats(a, b)


class TestQuickStartTutorial:
    """
    This test actually parses the ``README.md`` file, locates the tutorial
    section, and runs the commands in the tutorial exactly as presented to
    the user, to ensure that those commands at least run as expected and
    produce the expected output.

    This ensures that this important user documentation, which most users
    will see first, is working at least seemingly as expected.
    """

    README_FILE = pth.join(pth.dirname(pth.dirname(__file__)), 'README.md')
    SECTION_TITLE = 'Quickstart Tutorial'

    examples = []

    @classmethod
    def setup_class(cls):
        """
        Use mistletoe to parse the ``README.md``, find the tutorial section,
        and parse all fenced code blocks out of it into the ``examples`` list.

        There are currently two example types:

            * ``('bash', <command>, <stdout>)`` -- this is an example shell
              command to run, extracted by a fenced code block with the
              language set to "bash". Any lines following the line with the
              ``$`` prompt (not counting line continuations with \\) are
              assumed to be standard out.

            * ``('yaml', <contents>, <filename>)`` -- this is an example
              config file to write; the filename should be in a comment in
              the first line of the example file contents (the filename should
              be the only thing in the comment).  If the file of that name
              already exists, it will instead be *updated* with the contents
              from the example, allowing partial updates of files.

        """

        with open(cls.README_FILE) as fobj:
            doctree = mistletoe.Document(fobj)

        title = level = None
        # Find the beginning of the tutorial section
        for idx, node in enumerate(doctree.children):
            if not isinstance(node, mistletoe.block_token.Heading):
                continue

            # Heading nodes should have one RawText child containing
            # the title
            title = node.children[0].content
            level = node.level
            if title.strip() == cls.SECTION_TITLE:
                break

        assert title == cls.SECTION_TITLE, \
                f'section {cls.SECTION_TITLE} not found in {cls.README_FILE}'

        # Find and parse all fenced code blocks until the next section at the
        # same heading level
        for node in doctree.children[idx + 1:]:
            if (isinstance(node, mistletoe.block_token.Heading) and
                    node.level == level):
                # end of the section
                break

            if isinstance(node, mistletoe.block_token.CodeFence):
                content = node.children[0].content
                if node.language in ('bash', 'console', 'sh'):
                    cls.examples.append(cls.parse_bash_example(content))
                elif node.language == 'yaml':
                    cls.examples.append(cls.parse_yaml_example(content))
                # else: Ignore unrecognized example languages for now

    @staticmethod
    def parse_bash_example(text):
        lines = [line.rstrip() for line in text.splitlines()]
        command = []
        continuing = True
        for idx, line in enumerate(lines):
            assert command or line[0] in ('#', '$'), (
                f'invalid bash example:\n\n{text}\n\nthe example must '
                f'begin with a comment, or a $ prompt')

            if line[0] == '#':
                continue
            elif line[0] == '$':
                line = line[1:].lstrip()

            if line[-1] == '\\':
                line = line[:-1].rstrip()
            else:
                continuing = False

            command.append(line)

            if not continuing:
                break

        command = ' '.join(command)

        # The rest of the block is stdout
        stdout = lines[idx + 1:]
        # If there are blank links in the stdout output, replace them with the
        # <BLANKLINE> placeholder expected by doctest.OutputChecker
        stdout = [line if line.strip() else '<BLANKLINE>' for line in stdout]
        stdout = '\n'.join(stdout)

        return ('bash', command, stdout)

    @staticmethod
    def run_bash_example(command, want):
        print('running example: $ ' + command)
        cp = sp.run(command, stdout=sp.PIPE, stderr=sp.STDOUT, shell=True)
        oc = IgnoreFloatsOutputChecker()
        flags = doctest.ELLIPSIS | doctest.REPORT_UDIFF | FLOAT_IGNORE
        got = cp.stdout.decode('utf-8').rstrip()
        if got:
            print('\noutput:\n', got, '\n')
        else:
            print()
        # stupid output_difference wants an example object as its first
        # argument even though it only uses the example.want attribute
        # We also add a newline because the output from output_difference
        # omits it, which is a bug IMO
        example = Namespace(want=want + '\n')
        assert oc.check_output(want, got, flags), \
                '\n' + oc.output_difference(example, got, flags)

    @staticmethod
    def parse_yaml_example(text):
        lines = text.splitlines()
        sample = '\n'.join(lines[:5] + ['...'])
        assert lines[0][0] == '#', (
            f'yaml examples must begin with a comment containing the '
            f'filename, got:\n\n{sample}')

        filename = lines[0][1:].strip()
        return ('yaml', text, filename)

    @staticmethod
    def run_yaml_example(contents, filename):
        if pth.exists(filename):
            print(f'updating "{filename}" with:\n{indent(contents)}\n')
            orig = Config.from_file(filename)
        else:
            print(f'writing "{filename}" with:\n{indent(contents)}\n')
            orig = {}

        contents = io.StringIO(contents)
        contents.filename = filename
        new = Config.from_file(contents)

        merged = Config(new, orig)
        merged.to_file(filename, sort_keys=False)

    @classmethod
    def run_examples(cls):
        print()
        for example in cls.examples:
            type_ = example[0]
            if type_ in ('bash', 'console', 'sh'):
                cls.run_bash_example(*example[1:])
            elif type_ == 'yaml':
                cls.run_yaml_example(*example[1:])

    def test(self, tmpdir):
        with tmpdir.as_cwd():
            self.run_examples()


@pytest.mark.parametrize('network', [
    ('MLP', {}),
    ('CustomCNN', {}),
    ('SPIDNA', {'n_features': 3, 'n_blocks': 2})
])
def test_end_to_end(tmp_path, cached_simulation, monkeypatch, network):
    """
    Tests all the command line scripts from data simulation through learning,
    with some default/sample configuration.

    Does not significantly test the results, but just that the example code can
    run without crashing and produces something resembling an expected output
    (i.e. a trained neural net).

    This test is parametrized to test multiple networks--each network it's
    tested with is given as a tuple ``(network_name, net_params)``--the name of
    the network, and an optional dict of additional parameters (as given by
    ``net_params`` in the config).

    .. note::

        Some of this overlaps with
        ``tests.test_simulation.test_simulation_main``, but with fewer
        assertions; that test should ensure that the ``simulation.main()``
        function is working as expected.
    """

    simulation_config = cached_simulation[0]
    preprocessing_config = one_event.DEFAULT_ONE_EVENT_PREPROCESSING_CONFIG
    simulation_name = simulation_config['dataset_name']
    model_name = preprocessing_config['model_name']

    net_name, net_params = network

    # Generate the example simulation config
    argv = ['simulation', 'init', simulation_name, 'one_event', str(tmp_path)]
    assert DnadnaCommand.main(['--debug'] + argv) is None

    dataset_dir = tmp_path / simulation_name

    # Check that the simulation parameters JSON file was created
    simulation_config_filename = \
            OneEventSimulator.config_filename_format.format(
                    dataset_name=simulation_name)
    simulation_config_path = dataset_dir / simulation_config_filename

    # Now run the simulation with the generated config file.
    argv = ['simulation', 'run', str(simulation_config_path)]
    assert DnadnaCommand.main(['--debug'] + argv) is None

    # Run `dnadna init` to produce the preprocessing config file
    argv = ['init', '--simulation-config', str(simulation_config_path),
            str(tmp_path)]
    assert DnadnaCommand.main(['--debug'] + argv) is None

    preprocessing_config_path = (dataset_dir /
                                 'one_event_preprocessing_config.yml')
    assert preprocessing_config_path.is_file()

    # Update some of the values in the preprocessing config
    preprocessing_config = Config.from_file(preprocessing_config_path)

    # Make these parameters an order of magnitude smaller, making the data size
    # for the test more manageable
    preprocessing_config['dataset_splits'] = {
        'training': 2.0 / 3,
        'validation': 1.0 / 3
    }
    preprocessing_config['preprocessing'].update({
        'min_snp': 100
    })
    preprocessing_config.to_file()

    argv = ['preprocess', str(preprocessing_config_path)]
    assert DnadnaCommand.main(['--debug'] + argv) is None

    training_config_path = dataset_dir / 'one_event_training_config.yml'
    assert training_config_path.is_file()

    training_config = Config.from_file(training_config_path)
    training_config.update({
        'dataset_transforms': [{'crop': {'max_snp': 100}}],
        'n_epochs': 1,
        'network': {
            'name': net_name,
            'params': net_params
        }
    })
    training_config.to_file()

    # TODO: The training process is also time-consuming and not really the
    # main purpose of this test; perhaps we could cache the training results
    # as well...
    argv = ['train', str(training_config_path)]
    assert DnadnaCommand.main(['--debug'] + argv) is None

    run_name = training_config['run_name_format'].format(
            datset_name=simulation_name, run_id='000')
    # data_preprocessing will save the run-specific training params file to
    # the following filename
    run_dir = dataset_dir / run_name
    run_config_path = run_dir / f'{model_name}_run_000_final_config.yml'
    assert run_config_path.is_file()

    # The output should be a last_epoch_net (currently there is not an option
    # to save the net with the *best* loss, not just the last (which will
    # usually be the best, but not necessarily?)
    net_path = run_dir / f'{model_name}_{run_name}_last_epoch_net.pth'
    assert net_path.is_file()

    # Run `dnadna predict` on the dataset and check some of the predictions
    # In TestQuickStartTutorial we test `dnadna predict` using a model file
    # and some .npz files as the inputs.  In order to improve test converage,
    # in this case we use a training config file and the simulation config as
    # inputs, and also test the --preprocess flag.
    output_filename = tmp_path / 'predictions.csv'
    argv = ['predict', '--preprocess', '--output', str(output_filename),
            str(run_config_path), str(simulation_config_path)]
    assert DnadnaCommand.main(['--debug'] + argv) is None

    # Try loading the predictions, first check that all the expected columns
    # are present
    predictions = pd.read_csv(output_filename)
    columns = ['path', 'scenario_idx', 'replicate_idx', 'event_time',
               'recent_size', 'event_size']
    assert (predictions.columns == columns).all()

    # Confirm that the scenarios in the predictions output are a superset
    # of the scenarios in the pre-processed scenario params.  It can be a
    # superset because the predict command does not throw out entire scenarios
    # that don't pass the pre-processing check; it only throws out individual
    # replicates
    # We don't check the predicted values themselves since for the purpose of
    # this test (very small dataset) they are not necessarily very meaningful
    params_path = run_dir / f'{model_name}_{run_name}_preprocessed_params.csv'
    params = pd.read_csv(params_path)
    assert set(predictions['scenario_idx']).issuperset(params['scenario_idx'])
