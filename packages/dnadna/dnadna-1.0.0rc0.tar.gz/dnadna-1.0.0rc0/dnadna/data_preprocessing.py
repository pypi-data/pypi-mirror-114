# -*- coding: utf-8 -*-
"""
Implements pre-processing of simulation data in preparation for a training run,
including training config initialization.
"""

import logging
import multiprocessing
import os.path as pth
import sys

import numpy as np
import tqdm

from . import __version__
from .datasets import MissingSNPSample, DNADataset
from .params import LearnedParams
from .simulator import Simulator
from .utils.config import (ConfigError, Config, ConfigMixIn,
        save_dict_annotated)
from .utils.jsonschema import timestamp
from .utils.misc import indent
from .utils.plugins import load_plugins


PREPROCESSED_SCENARIO_PARAMS_FILENAME_FORMAT = \
        '{model_name}_preprocessed_params.csv'

TRAINING_CONFIG_FILENAME_FORMAT = \
        '{model_name}_training_config.yml'

log = logging.getLogger(__name__)


class ScenarioValidationError(Exception):
    """
    Exception raised if the simulation cannot be used with the given training
    parameters.
    """


class DataPreprocessor(ConfigMixIn):
    config_schema = 'preprocessing'

    def __init__(self, config, dataset=None, learned_params=None,
                 validate=True):
        super().__init__(config=config, validate=validate)

        if dataset is None:
            dataset = DNADataset(config['dataset'], validate=False)

        self._dataset = dataset

        if learned_params is None:
            learned_params = LearnedParams(
                    config['learned_params'],
                    self._dataset.scenario_params,
                    validate=False)

        self._learned_params = learned_params

    @property
    def dataset(self):
        return self._dataset

    @property
    def learned_params(self):
        return self._learned_params

    @property
    def min_snp(self):
        return self.preprocessing['min_snp']

    @property
    def min_indiv(self):
        return self.preprocessing['min_indiv']

    @property
    def seed(self):
        return self.preprocessing.get('seed')

    @property
    def n_workers(self):
        return self.preprocessing['n_workers']

    @staticmethod
    def check_snp_sample(scenario_idx, replicate_idx, snp, min_snp=None,
                         min_indiv=None):
        """
        Check that a single `~dnadna.snp_sample.SNPSample` conforms to the
        pre-processing requirements.
        """

        # TODO: Since only the shape of the samples is used in the code (total
        # number of SNPs and number of indviduals) this code previously used an
        # optimization (utils.get_shape_npz) to return this data without
        # loading the full sample into memory.  This could still be done, but
        # that optimization can be moved into the NpzSNPSample class itself

        # NOTE: The wip_hyperopt branch adds another check here in the
        # form of:
        #    if maf != 0:
        #        snp, pos = utils.remove_maf_folded(data['SNP'], None, maf)
        #        if snp.shape[1] < SNP_min:
        #            pass_check = False
        #            logging.warning(
        #                f'{npz_path} not kept because it had {snp.shape[1]} SNPs '
        #                f'(< {SNP_min} SNPs)')
        #
        #            break
        # It then *only* does the below check if `maf == 0`, but as
        # noted the below check is equivalent (?) to checking
        # shapes['SNP'][1] < SNP_min.  Maybe after calling
        # remove_maf_folded that may no longer be the case but we could
        # make this code clearer if so...
        if min_snp is not None and snp.n_snp < min_snp:
            if snp.path is None:
                # Just refer to its replicate number, otherwise
                # refer to its path
                snp_name = f'replicate {replicate_idx}'
            else:
                snp_name = f"'{snp.path}'"

            log.warning(
                f"scenario {scenario_idx} not kept because {snp_name} had "
                f"{snp.n_snp} SNPs (< {min_snp} SNPs)")

            return False
            # TODO ADD CHECK for relative positions
            # TODO with warning + asking for confirmation if
            # conversion+overwrite (before multiprocessing)
        if min_indiv is not None and snp.n_indiv < min_indiv:
            if snp.path is None:
                snp_name = f'replicate {replicate_idx}'
            else:
                snp_name = f"'{snp.path}'"

            log.warning(
                f"scenario {scenario_idx} not kept because {snp_name} had "
                f"{snp.n_indiv} individuals (< {min_indiv} individuals)")

            return False

        return True

    def validate_config(self, config):
        """
        Additional validation of the config preprocessing config file.
        """

        super().validate_config(config)
        dataset_splits = config['dataset_splits']
        total = sum(dataset_splits.values())
        if total < 1.0:
            config_name = config.filename if config.filename else 'the given config'
            log.warning(
                f'dataset_splits must sum to 1.0; the splits in {config_name} '
                f'sum to {total}; remaining scenarios will be unused')
            if 'unused' in dataset_splits:
                dataset_splits['unused'] += (1.0 - total)
            else:
                dataset_splits['unused'] = 1.0 - total
        elif total > 1.0:
            raise ConfigError(config,
                f'dataset_splits must sum to 1.0; the given splits sum to '
                f'{total}; please modify the dataset_splits to sum to '
                f'1.0')

    def check_scenario(self, scenario_idx, scenario):
        """
        Perform validation of an individual scenario's simulations against
        training configuration such as the minimal number of SNPs, among other
        details.
        """

        pass_check = True
        n_replicates = int(scenario['n_replicates'])
        total_replicates = 0

        # TODO: This is another case where having a more generic Dataset class
        # would be useful beyond just direct use with the pytorch APIs.  In
        # this case, the task of iterating over all replicates in a given
        # scenario (and for that matter over all scenarios in the dataset) and
        # returning the SNP data from them is a task that can be handled by the
        # Dataset class itself.  Too much of the code here is otherwise
        # boilerplate which an be seen replicated e.g. in the
        # dnadna.datasets module.
        for replicate_idx in range(n_replicates):
            try:
                snp = self.dataset.source[scenario_idx, replicate_idx]
                total_replicates += 1  # only increment if not missing
                pass_check = self.check_snp_sample(scenario_idx, replicate_idx,
                        snp, min_snp=self.min_snp, min_indiv=self.min_indiv)
                if not pass_check:
                    break
            except MissingSNPSample as exc:
                if not self.dataset['ignore_missing']:
                    pass_check = False
                    log.warning(f"{exc}; entire scenario will be skipped")
                    break
            except Exception as exc:
                pass_check = False
                log.warning(f"Unexpected exception checking scenario: {exc}; "
                             "entire scenario will be skipped")
                break

        return pass_check, scenario_idx, total_replicates

    def _check_scenario_wrapped(self, scenario):
        """
        Helper for checking scenarios with multiprocessing.Pool, needed since
        Pool.map does not support multiple argument functions.
        """
        return self.check_scenario(*scenario)

    def check_scenarios(self):
        """
        Perform validation checks against all scenarios in the dataset,
        optionally using multiple processes.

        Returns a generator yielding ``(keep, scenario_idx, n_replicates)``
        tuples, where ``keep`` is True/False depending on whether or not the
        scenario passed validation and will be used for training,
        ``scenario_idx`` is the index of the scenario checked, and
        ``n_replicates`` the number of valid simulation replicates found
        within that scenario.
        """

        log.info('Removing scenarios with:')
        log.info(' - Missing replicates')

        if self.min_snp is not None:
            log.info(f' - Fewer than {self.min_snp} SNPs')

        if self.min_indiv is not None:
            log.info(f' - Fewer than {self.min_indiv} individuals')

        log.info('...')

        cores = min(multiprocessing.cpu_count(), self.n_workers)

        if not cores:
            use_pool = False
            cores += 1
        else:
            use_pool = True

        log.info(f"Using {cores} CPU for checking scenarios")

        param_iter = self.learned_params.scenario_params.iterrows()
        # TODO: This should get a progress bar as well--a little more complicated
        # due to use of multiprocessing but not much (e.g. it could switch to
        # map_async)
        if use_pool:
            def iter_results():
                with multiprocessing.Pool(cores) as pool:
                    for result in pool.imap_unordered(
                            self._check_scenario_wrapped,
                            param_iter):
                        yield result
                    pool.close()
                    pool.join()
        else:
            def iter_results():
                return iter(map(self._check_scenario_wrapped, param_iter))

        for result in iter_results():
            yield result

    def preprocess_scenario_params(self, run_id=None, progress_bar=False):
        """
        Returns a copy of the simulation's original scenario params table
        suitable for the given training parameters.

        Also returns a copy of the original training configuration with some
        post-processed training parameters inserted.

        All scenarios in the simulation data are checked against the training
        parameters and unsuitable data is removed from the training set.  This
        part can be the most time-consuming depending on the size of the
        data set, so an optional progress bar can be displayed during this
        operation.

        Regression parameter values are also normalized around their mean and
        standard deviation, and specified parameters are log-transformed.
        """

        scenario_params = self.learned_params.scenario_params
        cols = self.learned_params.param_names + ['n_replicates']
        training_params = scenario_params[cols]
        # NOTE: Previously there was some code here, ostensibly for taking a random
        # sampling of scenarios, except it always took all scenarios.  That code
        # has been eliminated now, as it was effectively superfluous.  I wonder
        # what the intent behind it was though.
        n_scenarios = len(training_params)

        to_keep = np.empty(n_scenarios,
                           dtype=[('keep', bool), ('scenario_idx', np.uint64),
                                  ('n_replicates', np.uint64)])

        bar = tqdm.tqdm(self.check_scenarios(), total=n_scenarios,
                        unit='scenario',
                        disable=(not (progress_bar and sys.stderr.isatty())))

        for idx, result in enumerate(bar):
            to_keep[idx] = result

        # NOTE: Here, to_keep is now a <num_scenarios>x2 ndarray where the
        # columns are the return tuple from check_scenario
        # (<scenario_idx>, <valid?>, <n_simulations>).
        # We then sort by scenario index (I guess it's assumed it's possible that
        # the input scenario params are not sorted?  Also, it should be noted,
        # there are more efficient ways to do the sorting here (even ndarray.sort).

        # sort to_keep by the scenario indices
        to_keep = np.sort(to_keep, order='scenario_idx')
        n_scenarios_kept = int(to_keep['keep'].sum())
        # total number of scenario replicates kept
        n_simulations_kept = int(to_keep[to_keep['keep']]['n_replicates'].sum())

        log.info(
            f'{n_scenarios_kept} scenarios out of {n_scenarios} have '
            f'been kept, representing {n_simulations_kept} simulations')

        log.info('Splitting scenarios between training and validation set')

        training_params = \
                training_params.loc[to_keep[to_keep['keep']]['scenario_idx']]

        # Ensure that regression parameters are converted to float data types
        # and that classification parameters are converted to int data types
        # TODO: For classification paramters perhaps they should be normalized
        # to a sequence of class indices starting from 0, and ensure that the
        # data is in fact integral to begin with
        param_type_dtypes = {'regression': 'float', 'classification': 'int'}

        # Map parameter names to the appropriate dtypes to convert them to
        convert_dtypes = {
                param_name: param_type_dtypes[param['type']]
                for param_name, param in self.learned_params.params.items()
        }

        training_params = training_params.astype(convert_dtypes)

        # Log transform regression parameters accordingly
        for param_name, param in self.learned_params.regression_params.items():
            if param.get('log_transform', False):
                training_params[param_name] = \
                        training_params[param_name].apply(np.log)

        # Create masks for training/validation/test sets and randomly shuffle--
        # we randomize this for every pre-processing run so that it will give
        # unique results for different seeds

        # Seed the RNG if a seed was specified
        if self.seed is not None:
            np.random.seed(self.seed)

        # I think there is a better way to do this (using random_split from
        # pytorch maybe?)
        split_names = ['unused', 'training', 'validation', 'test']
        splits = np.zeros(n_scenarios_kept, dtype=int)
        prev_idx = 0
        for split_num, split in enumerate(split_names):
            prob = self.dataset_splits.get(split, 0)
            if prob:
                idx = prev_idx + int(np.ceil(n_scenarios_kept * prob))
                splits[prev_idx:idx] = split_num
                prev_idx = idx

        np.random.shuffle(splits)
        training_params['splits'] = np.array(split_names)[splits]
        # Outright omit 'unused'
        unused = split_names.index('unused')
        mask = splits == unused
        if mask.any():
            log.warning(
                f'{sum(mask)} random scenarios will be unused due to the '
                f'dataset_splits setting, and will be omitted from the '
                f'preprocessed scenario params table')
            training_params = training_params.iloc[~mask]

        # This step is relegated to a sub-routine just to keep this one from
        # getting too large; perhaps this could be broken up in a more useful
        # way but I don't know yet.
        return self._process_scenario_param_values(training_params)

    def _process_scenario_param_values(self, processed_scenario_params):
        """
        Perform additional processing of scenario params, return an updated
        training config with additional parameter metadata added (mean and
        standard deviation).
        """

        log.info("Standardizing continuous parameters")
        stats = {}
        if self.learned_params.regression_params:
            regression_params = list(self.learned_params.regression_params)
            splits = processed_scenario_params['splits']
            training_set = splits == 'training'
            training_params = processed_scenario_params.loc[training_set]
            training_params = training_params[regression_params]

            training_params_mean = training_params.mean()
            training_params_std = training_params.std().replace(0, 1)

            processed_scenario_params[regression_params] = \
                    ((processed_scenario_params[regression_params] -
                      training_params_mean) / training_params_std).fillna(-1)

            # These values are logged in the processed config for future
            # reference, though currently I don't believe they're used
            # elsewhere in the code.
            stats['train_mean'] = training_params_mean.to_dict()
            stats['train_std'] = training_params_std.to_dict()

        training_config = self._get_default_training_config(stats)

        return processed_scenario_params, training_config

    def _get_default_training_config(self, stats={}):
        """
        Get the default training config.

        This is a bit complicated, because the training config is built up from
        multiple sources:

        * The default training config file, which gives a few basic default
          settings (``dnadna/defaults/training.yml`` in the source)
        * If using a simulation config, additional overrides to the defaults
          that are specifically recommended by that simulator
        * The preprocessing config itself, which should be inherited
        * But we include a full copy of learned_params for ease of editing,
          since users might want to change loss functions, etc.
        * We also have to override the ``dataset.scenario_params_path`` to
          point to the new preprocessed scenario params file.
        * Parameter normalization statistics and other metadata.

        So this method builds the training config file from all these sources,
        in multiple "layers" chained together by the
        `~dnadna.config.DeepChainMap` implementation underlying
        `~dnadna.config.Config` in order to keep all these different sources
        arranged in a reasonable ordering (see issue #80).
        """

        # Start with an empty dict, so that when the resulting Config gets
        # updated with defaults, the default values go into the empty dict here
        # instead of modifying self.config
        configs = [{}]

        # Override the dataset.scenario_params_path setting to point to the
        # pre-processed scenario params
        # This has to be done by using a chained mapping rather than simple
        # assignment, or else we will override the dataset property inherited
        # from the preprocessing config
        scenario_params_filename = \
                PREPROCESSED_SCENARIO_PARAMS_FILENAME_FORMAT.format(
                        model_name=self.model_name)

        dataset_config = {'scenario_params_path': scenario_params_filename}
        configs.append({'dataset': dataset_config})

        configs.append(self.config)

        simulator_name = self._dataset.config.get('simulator_name')

        if simulator_name:
            # Load any plugins mentioned in the simulation config
            load_plugins(self._dataset.config.get('plugins', []))
            # See if simulator_name is a known simulator, and get its
            # default preprocessing config
            try:
                simulator_cls = Simulator.get_plugin(simulator_name)
                configs.append(simulator_cls.training_config_default)
            except ValueError:
                pass

        # Add any additional parameters from the default training config
        default = Config.from_default('training', resolve_inherits=False,
                                      validate=False)
        if 'inherit' in default:
            del default['inherit']

        configs.append(default)

        # Rewrite the learned_params value in the ordered mapping format
        # (list of single-element dicts) to ensure that a pre-determined
        # order for the params is kept (see
        # https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/46)
        learned_params = \
                [{k: v} for k, v in self.learned_params.params.items()]
        configs.append({'learned_params': learned_params})

        if stats:
            configs.append(stats)

        # Additional metadata at the end of the config
        configs.append({
            'dnadna_version': __version__,
            'preprocessing_datetime': timestamp()
        })

        config_filename = TRAINING_CONFIG_FILENAME_FORMAT.format(
                model_name=self.model_name)

        training_config_path = pth.normpath(
                pth.join(self.model_root, config_filename))

        return Config(*configs, filename=training_config_path,
                      schema='training',
                      validate={'resolve_filenames': False})

    def run_preprocessing(self, progress_bar=False):
        processed_scenario_params, training_config = \
                self.preprocess_scenario_params(progress_bar=progress_bar)

        scenario_params_filename = \
                training_config['dataset']['scenario_params_path']

        scenario_params_path = pth.normpath(
                pth.join(self.model_root, scenario_params_filename))

        log.info(f"Writing preprocessed scenario parameters to: "
                 f"{scenario_params_path}")

        processed_scenario_params.to_csv(scenario_params_path,
                                         index_label="scenario_idx")

        log.info(f"Writing sample training config to: "
                 f"{training_config.filename}")
        # "uninherit" the current preprocessing config so it is written as an
        # 'inherit' property in the training config, rather than included
        # verbatim
        training_config = training_config.unresolve_inherits(
            config_dir=pth.dirname(self.config.filename),
            only=[self.config])
        save_dict_annotated(training_config.dict(), training_config.filename,
                            schema='training', indent=4, sort_keys=False)
        log.info("Edit the training config file as needed, then start "
                 "the training run with the command:")
        log.info('')
        log.info(indent(f'dnadna train {training_config.filename}'))
