Model Training
##############

What does training do?
======================

Training is the main step of a machine learning pipeline. The weights of the
network are optimized based on a training set, while the performance is
regularly evaluated on a validation set in order to monitor overfitting (i.e.
the loss of generalization by a network).

Training is usually run many times to investigate different sets of hyperparameters.  In
the previous preprocessing step, a training configuration file is created. This
file contains classical hyperparameters that users can modify, and others may be
added.


The workflow is the following:

#. Obtain the sample training config file
   (``<model_name>_training_config.yml``) after initialization and
   preprocessing.

#. Modify ``<model_name>_training_config.yml`` to adapt the hyperparameters
   to your training data, network and optimization needs.

#. Run the command ``dnadna train <model_name>_training_config.yml``

    * It creates a directory ``run_000`` containing all the output files (see below)

#. Modify the values in the same ``<model_name>_training_config.yml`` to
   investigate another hyperparameterization.

#. Run the same command ``dnadna train <model_name>_training_config.yml``

     * It creates another directory ``run_001``.

The idea is that the ``<model_name>_training_config.yml`` enables
hyperparameter tuning for a new run, while
``run_{run_id}/<model_name>_final_training_config.yml`` contains every
configuration setting required to reproduce the ``run_{run_id}`` experiment.

.. note::

    It is possible to specify the run identifier manually, and identifiers
    are not restricted to numbers, for instance::

        $ dnadna train my_model_training_config --run lr0.001-BS64

    This allows tracking the learning rate (lr) and batch size (BS) within the
    run name (note that this information is also saved in the final config
    file).

    The format can also be specified in the training config file through the
    the ``run_name_format`` setting, though it is currently limited in
    flexibility.


How do you configure the training command?
==========================================

The training configuration file inherits from the preprocessing
configuration file, and is pre-filled with default hyperparameters. We will
discuss here the important elements separately, although they all appear in
the same training configuration file.

Loss functions for learned parameters (targets)
-----------------------------------------------

Why?
^^^^

We need to define a loss function for each of the target parameters. The
loss function can be different for each parameter, and can have a different
weight in the final loss, which is a weighted sum of all losses.

If not specified explicitly, the loss function defaults to `MSE
<torch.nn.MSELoss>` for regression tasks, and to `Cross Entropy
<torch.nn.CrossEntropyLoss>` for classification tasks.


How?
^^^^

Following the example of the preprocessing step, the network will predict
four parameters, three via regression and one via classification.
This information is inherited from the preprocessing config file, and completed
with default values for:

* ``loss_func``: loss function, can be any of the loss function defined in
  PyTorch (specifically all the ``Loss`` functions in `torch.nn`).

* ``loss_weight``: relative weight for the parameter loss in the final loss.

* ``tied_to_position``: a boolean indicating whether the parameter to
  predict is tied to a position along the chromosome.  If True, the loss
  will account for any change affecting SNP localization.  For instance, if
  one wants to predict the position of a recombination site, and use a
  transformation for data augmentation that modifies positions, the loss
  will be computed based on the corrected target positions.

* ``n_classes``: The number of classes, inferred from ``classes``, this
  should not be modified manually.

Corresponding section in an example training config file:

.. code-block:: yaml

    learned_params:
    -   event_time:
            type: regression
            log_transform: true
            loss_func: MSE
            loss_weight: 1
            tied_to_position: false
    -   recent_size:
            type: regression
            log_transform: true
            loss_func: MSE
            loss_weight: 1
            tied_to_position: false
    -   event_size:
            type: regression
            log_transform: true
            loss_func: MSE
            loss_weight: 1
            tied_to_position: false
    -   selection:
            type: classification
            classes: ['no', 'yes']
            loss_func: Cross Entropy
            loss_weight: 1


Hyperparameters controlling training
------------------------------------

Hyperparameters usually have a huge effect on training speed and quality.
They are specified through each of the following:

    * ``network`` section defining the network name and parameters
    * ``optimizer`` section defining the optimizer name and parameters
    * ``batch_size``: number of examples in a batch
    * ``n_epochs``: number of epochs
    * ``evaluation_interval``: interval (number of batches processed) between two validation steps.

.. code-block:: yaml

    # number of epochs over which to repeat the training process
    n_epochs: 5

    # sample batch size to train on
    batch_size: 10

    # interval in the training loop in which to perform model validation
    evaluation_interval: 10

    # name and parameters of the neural net model to train
    network:
        name: SPIDNA

        # net parameters for SPIDNA
        params:
            n_blocks: 7
            n_features: 50

    # name and parameters of the optimizer to use; all built-in optimizers from the
    # torch.optim package are available for use here, and you can also provide a
    # custom optimizer via a plugin
    optimizer:
        name: Adam
        params:
            learning_rate: 0.001
            weight_decay: 0
            betas: [0.9, 0.999]
            eps: 1.0e-08
            amsgrad: false


Computing resources, I/O information, misc
------------------------------------------

Technical parameters that should not impact training quality:

    * ``use_cuda``: whether to use GPU or not
    * ``cuda_device``: optional, which GPU(s) to use
    * ``loader_num_workers``: number of CPUs used to load the dataset into
      memory; using more workers can have a moderate impact on performance
      up to a point, but is ultimately limited by disk I/O (assuming the
      data is being loaded from a physical disk and not an in-RAM
      filesystem)
    * ``seed``: seed for initialization of the random number generator(s).
      Using the same seed is required to reproduce a training run exactly.

      .. note::

          When training using GPU support, even setting the random number
          generator seed cannot always reproduce training runs exactly, due
          to nondeterministic aspects of some algorithms.  See PyTorch's
          documentation on `Reproducibility
          <https://pytorch.org/docs/stable/notes/randomness.html>`_ for more
          details.

Parameters that define filenames:

    * ``model_filename_format``: format string for the output models,
      including checkpoints, the version with the best losses, and the final
      version
    * ``run_name_format``: format string for the name given to this run

.. code-block:: yaml

    # format string for the filename of the final output model; it can use the
    # template variables model_name, run_name, and/or run_id, while the
    # required variable "checkpoint" will be replaced with names like "best",
    # "last" and other intermediate checkpoints
    model_filename_format: '{model_name}_{run_name}_{checkpoint}_net.pth'

    # format string for the name given to this run for a sequence of runs of the
    # same model; the outputs of each run are placed in subdirectories of
    # <run_path>/<model_name> with the name of this run; the format string can use
    # the template variables model_name and run_id
    run_name_format: run_{run_id}

On-the-fly data transformation
------------------------------

``dataset_transforms`` is a section of the config file that defines data
transformations applied on the dataset during training. It is useful for
both satisfying specific network requirements (for example if the input size
is fixed) and performing data augmentation.

For instance the `crop <dnadna.transforms.Crop>` transform specifies that
all SNP matrices should be cropped to maximum number of SNPs and/or maximum
number of individuals while the `subsample <dnadna.transforms.Subsample>`
transform randomly subsamples a SNP matrix each time it is loaded. The API
documentation describes currently available `~dnadna.transforms`. Custom
transforms can be implemented by users with the :doc:`plugin interface <extending>`.

The transforms are applied in the order given in the config file. In the example
configuration below, the data loader first randomly subsamples 30 (haploid)
individuals for all SNP matrices and keep only columns that remained polymorphic
after subsampling (``keep_polymorphic_only: true``); then it crops all matrices
to a maximum of 400 SNPs (note that there might still be matrices with less than
400 SNPs, unless ``min_snp`` was set to 400 during preprocessing).

.. code-block:: yaml

    # list of transforms to apply to the dataset; all optional transforms are
    # disabled by default unless specified here; transforms which don't take any
    # parameters can be listed just by their name, whereas transforms which do take
    # parameters are given as {'name': <name>, 'param1':, 'param2':, ...}, where the
    # params map param names (specific to the transform) to their values
    dataset_transforms:
        - subsample:
              size: 30
              keep_polymorphic_only: true
        - crop:
              max_snp: 400
              max_indiv: null
              keep_polymorphic_only: true


Example training config file
-----------------------------

.. code-block:: yaml

    # the main training configuration, typically generated from an existing
    # preprocessing config file

    # format string for the filename of the final output model; it can use the
    # template variables model_name, run_name, and/or run_id
    model_filename_format: '{model_name}_{run_name}_{checkpoint}_net.pth'

    # format string for the name given to this run for a sequence of runs of the
    # same model; the outputs of each run are placed in subdirectories of
    # <run_path>/<model_name> with the name of this run; the format string can use
    # the template variables model_name and run_id
    run_name_format: run_{run_id}

    # name and parameters of the neural net model to train
    network:
      name: SPIDNA

      # net parameters for SPIDNA
      params:
          n_blocks: 7
          n_features: 50

    # name and parameters of the optimizer to use; all built-in optimizers from the
    # torch.optim package are available for use here, and you can also provide a
    # custom optimizer via a plugin
    optimizer:
        name: Adam
        params:
            learning_rate: 0.001
            weight_decay: 0
            betas: [0.9, 0.999]
            eps: 1.0e-08
            amsgrad: false

    # the dataset/simulation configuration
    dataset:
        # path to the CSV file containing the per-scenario parameters used in this
        # simulation, either as an absolute path, or as a path relative to this
        # config file
        scenario_params_path: my_model_preprocessed_params.csv

    # list of transforms to apply to the dataset; all optional transforms are
    # disabled by default unless specified here; transforms which don't take any
    # parameters can be listed just by their name, whereas transforms which do take
    # parameters are given as {'name': <name>, 'param1':, 'param2':, ...}, where the
    # params map param names (specific to the transform) to their values
    dataset_transforms:
    - subsample:
          size: 30
          keep_polymorphic_only: true
    - crop:
          max_snp: 400
          max_indiv: null
          keep_polymorphic_only: true

    # number of epochs over which to repeat the training process
    n_epochs: 5

    # sample batch size to train on
    batch_size: 20

    # interval in the training loop in which to perform model validation
    evaluation_interval: 10

    # seed for initializing the PRNG prior to a training run for reproducible
    # results; if unspecified the PRNG chooses its default seeding method
    # seed: 2

    # number of subprocesses to use for data loading
    loader_num_workers: 4

    # use CUDA-capable GPU where available
    use_cuda: true

    # specifies the CUDA device index to use
    cuda_device: null

    # description of the parameters the network will be trained on
    learned_params:
    -   event_time:
            type: regression
            log_transform: true
            loss_func: MSE
            loss_weight: 1
            tied_to_position: false
    -   recent_size:
            type: regression
            log_transform: true
            loss_func: MSE
            loss_weight: 1
            tied_to_position: false
    -   event_size:
            type: regression
            log_transform: true
            loss_func: MSE
            loss_weight: 1
            tied_to_position: false

    # mean of each regression parameter over the training set
    train_mean:
        event_time: 7.350954994899923
        recent_size: 9.670931802268845
        event_size: 9.616080720072633

    # standard deviation of each regression parameter over the training set
    train_std:
        event_time: 0.8107528444714214
        recent_size: 0.6895220957560944
        event_size: 0.6492308854609464
    dnadna_version: 0.1.dev908+g71ec0f7
    preprocessing_datetime: '2021-07-16T08:32:14.490685+00:00'
    inherit: my_model_preprocessing_config.yml


What are the output files for the training step?
================================================

- ``<model_name>_run_{run_id}_training.log``: contains log of the training run
- ``<model_name>_run_{run_id}_best_net.pth``: network having the best validation score over the whole run
- ``<model_name>_run_{run_id}_last_checkpoint_net.pth``: checkpoint allowing
  restoration of the last recorded state of the network being trained
  (currently saved every validation interval)
- ``<model_name>_run_{run_id}_last_epoch_net.pth``: network saved at the end of the training run
- ``tensorboard/``: directory containing logged loss values over time,
  to be visualized with `tensorboard
  <https://www.tensorflow.org/tensorboard/>`_

``.pth`` objects contain the usual network definition and its optimized
weights, but also information from the training config, so that they can
easily be used for :doc:`prediction <prediction>` or for restarting training
from current state and with the exact same parameters (the latter option
will be added in a future release).

Visualize losses
----------------

For each run losses are logged into a subdirectory named `tensorboard/`. Type
``tensorboard --logdir path-to-dir`` on the command line, such as:

.. code-block:: bash

        $ tensorboard --logdir <model_name>/

to visualize all runs under `<model_name>/` or:

.. code-block:: bash

    $ tensorboard --logdir <model_name>/run_{run_id}

for a specific run, and follow the instructions printed on the terminal (i.e.
open the printed link ``http://localhost:XXXX/`` with your web browser).  When
working with docker and/or on a remote server you might need to use the
``--bind_all`` option.

Alternatively, in a jupyter notebook with an environment that has tensorboard
`installed <https://www.tensorflow.org/install>`_ :

.. code-block:: python

    %load_ext tensorboard
    %tensorboard --logdir <model_name>/

This opens a TensorBoard `dashboard <https://www.tensorflow.org/tensorboard/get_started>`_.

The TensorBoard dashboard displays training and validation losses for all runs
in the directory and has interactive options that you can use (for example set
smoothing to 0 to forbid interpolation of the losses, show specific runs, zoom,
get exact value by passing the mouse pointer, etc.).


Losses are also contained in plain text in the log file ``<model_name>_run_{run_id}_training.log``.


Command line
============

Once the hyperparameters and other parameters are set, we can start training the
network by simply running::

    dnadna train <model_name>_training_config.yml



If you want to relaunch a previous run with the exact same hyperparameters, you
can directly pass its final config as an argument::

    dnadna train <model_name>/run_{run_id}/<model_name>_run_{run_id}_final_config.yml

This will create a new run directory, i.e it will not overwrite ``run_{run_id}/``.


If one of your previous run had good/poor performance and you would like to
investigate small changes in hyperparameters, we suggest to **copy** its final
config to ``<model_name>/`` and then edit the desired properties::

        cp <model_name>/run_{run_id}/<model_name>_run_{run_id}_final_config.yml <model_name>/<model_name>_training_config.yml
        # Now edit <model_name>/<model_name>_training_config.yml with your favorite text editor
        #    for instance change the learning rate, etc.
        dnadna train <model_name>/<model_name>_training_config.yml

This will create a new run directory, i.e it will not overwrite
``run_{run_id}/``. Note that you are allowed to pick another name than
``<model_name>_training_config.yml``.


.. note::
  Warning: if the training config is identical between two runs and has the seed
  property set, you will get the exact same result. For adding randomness and
  e.g. testing the stability of a network you have to remove (or comment) the
  seed property. In this case PRNG chooses its default seeding method.


More details can be found in the :ref:`index:Quickstart Tutorial`.


Next step
=========

After a successful training run you can:

- Train other networks or the same network with different hyperparameters
- Use the trained network to :doc:`predict <prediction>` evolutionary
  parameters for simulated or real datasets.
