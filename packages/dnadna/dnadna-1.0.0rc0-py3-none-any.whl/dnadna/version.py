"""
Utility for determining the package version.

Normally this is hard-coded to the dnadna._version module if it exists.  But
if we are running a development version out of the source repo, we want a
dynamic version based on the state of the repo.
"""


import configparser
import os
import os.path as pth
import warnings


def get_version(name='dnadna', fallback='0.0.0'):
    # Check whether we are unambiguously in the dnadna source repo.
    in_dev = True
    root_dir = pth.dirname(pth.dirname(__file__))

    if not pth.isdir(pth.join(root_dir, '.git')):
        # If a .git directory doesn't exist we're definitely not in the repo
        in_dev = False
    else:
        # The setup.cfg must exist as well
        setup_cfg = pth.join(root_dir, 'setup.cfg')
        if not pth.isfile(setup_cfg):
            in_dev = False
        else:
            # Finally confirm that it's the *right* setup.cfg
            parser = configparser.ConfigParser()
            parser.read(setup_cfg)
            in_dev = (parser.has_option('metadata', 'name') and
                      parser.get('metadata', 'name') == name)

    if in_dev:
        try:
            import setuptools_scm
            with warnings.catch_warnings():
                if os.environ.get('CI'):
                    # Prevent shallow clone warning when running in CI; see
                    # https://gitlab.inria.fr/ml_genetics/private/dnadna/-/merge_requests/75
                    warnings.filterwarnings('ignore',
                            message='.*is shallow and may cause errors.*')
                return setuptools_scm.get_version(
                        root='..',
                        relative_to=__file__,
                        local_scheme='node-and-timestamp',
                        write_to=pth.join(pth.dirname(__file__), '_version.py'))
        except Exception as exc:
            warnings.warn(
                f'could not determine {name} package version from repository: '
                f'{exc}; make sure setuptools_scm is installed')

    try:
        from ._version import version
        return version
    except ImportError:
        warnings.warn(f'could not determine {name} package version')
        return fallback
