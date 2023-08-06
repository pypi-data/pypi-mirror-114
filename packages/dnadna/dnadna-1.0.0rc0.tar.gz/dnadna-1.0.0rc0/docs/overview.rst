Usage Overview
##############

There are five main stages in training a model with DNADNA, each of which
are run independently, and some of which are optional:

1. :ref:`Simulation <overview-simulation>` (optional) -- generate a
   simulated SNP dataset on which to train models.
2. :ref:`Training initialization <overview-initialization>` -- sets up
   output directories and example configuration files.
3. :ref:`Preprocessing <overview-preprocessing>` -- checks your dataset and
   filters out scenarios that don't meet minimal criteria required for your
   training run (e.g.  minimal number of SNPs).
4. :ref:`Training <overview-training>` -- trains a neural net on your data,
   outputting a PyTorch network with the optimized parameters.
5. :ref:`Prediction <overview-prediction>` -- evaluate your trained network
   on new data in order to make predictions and further evaluate the
   efficacy of your model.

Each of these steps corresponds with a sub-command of the ``dnadna``
command-line interface:

1. ``dnadna simulation``
2. ``dnadna init``
3. ``dnadna preprocess``
4. ``dnadna train``
5. ``dnadna predict``

If you already have an existing dataset in the :ref:`DNADNA data format
<dataset-formats-dnadna>` you can skip straight to running ``dnadna init``.

Many of these commands have an associated configuration file allowing
extensive customization of their options.  For example the training config
file is where you select which network to train your model on, parameters to
that network, and many other details.

Each config file is documented in the corresponding documentation sections,
though for an overview of the configuration file syntax and structure see
the :ref:`configuration` documentation.


.. _overview-simulation:

Simulation
==========

The "simulation" step is purely optional.  Currently it is mostly useful for
adapting new or existing simulation code to output data in the DNADNA
format.  There is no significant simulation code built into DNADNA, but
rather simulators are provided as plugins confirming to a simple interface
specification.

There is a built-in example simulator in then `dnadna.examples.one_event`
module.

Another usage of the simulation interface may be as a *converter*: Since the
simulator interface outputs data in the DNADNA format, a "simulator" may be
written which reads some dataset in from another data format, and outputs it
to the DNADNA format.

More details are provided in the :ref:`simulators` documentation.


.. _overview-initialization:

Initialization
==============

To get started DNADNA needs a few things:

1. An existing dataset in the :ref:`DNADNA format <dataset-formats-dnadna>`
   on which to train the model.

2. A :ref:`dataset config file <dnadna-dataset-simulation-config>` giving
   the software additional details of the dataset.

3. A directory to which files associated with each training run will be
   output (e.g. the trained model, log files, etc.).

4. A preprocessing config file to pass to the next stage,
   :ref:`overview-preprocessing`.

Item 1 is obtained either by using an existing published dataset (possibly
reformatted into the correct format) or by running a DNADNA :ref:`Simulator
<overview-simulation>`.  This also outputs a dataset config file that can be
used.

The ``dnadna init`` command helps with item 2 through 4.  It creates a
directory for outputs of your training runs, and generates an example
preprocessing config file that you can then adapt to the specifics of your
dataset and training objectives.  It will also output an example dataset
config file if you do not already have one.

If you have an existing dataset config you can pass it to ``dnadna init``
like:

.. code-block:: bash

    $ dnadna init --dataset-config=path/to/my_simulation_dataset_config.yml

which would output the file
``my_simulation/my_simulation_preprocessing_config.yml`` which can then be
further edited by hand.

Otherwise you can run:

.. code-block:: bash

    $ dnadna init -m my_model

which outputs ``my_model/my_model_dataset_config.yml`` and
``my_model/my_model_preprocessing_config.yml``.

How the directory/file names are determined
-------------------------------------------

If ``dnadna init`` is passed an existing dataset/simulation config file,
it will automatically use the ``dataset_name`` option in the config file
to name its output files/directories.  For example if the dataset config
contains ``dataset_name: my_simulation`` then the root directory for the
model will be ``./my_simulation/`` in the current working directory.

If you are not using an existing dataset/simulation config file, or would
like to specify a model name other than the default, pass the ``-m`` or
``--model-name`` option to ``dnadna init``.

If you would like to create the output directory somewhere other than the
current working directory, the last argument to ``dnadna init`` is an
optional root directory:

.. code-block:: bash

    $ dnadna init -m my_model /mnt/nfs/username/models

would output config files to ``/mnt/nfs/username/models/my_model/``.


.. _overview-preprocessing:

Preprocessing
=============

The preprocessing step performs the following:

* validating input files and filtering out scenarios that do not match minimal requirements (defined by users)
* splitting the dataset into training/validation/test sets (the latter is optional)
* applying transformations to target parameter(s) if required by users (e.g. log transformation)
* standardizing target parameter(s) for regression tasks (the mean and standard deviation used in standardization are computed based on the training set only).

Preprocessing is necessary before performing the first training run and should
be re-run if and only if one of the following is true:

* the dataset changed,

* the task changed (e.g. predicting other parameters or the same parameters but with different transformations),

* the required input dimensions changed (e.g. to match the dimensions expected by some networks).

At this stage we expect the user to open ``my_model_preprocessing_config.yml``
and edit the properties to match the task/network needs in terms of minimal
number of SNPs and individuals required for a dataset to be valid, names of the
evolutionary parameters to be targeted, split proportions, etc. More details
are provided in the :doc:`dedicated preprocessing page <data_preprocessing>`.

Once the preprocessing configuration file has been filled and the required input
files are created, run preprocessing with:

.. code-block:: bash

  $ dnadna preprocess my_model_preprocessing_config.yml


which outputs ``my_model/my_model_training_config.yml``,
``my_model/my_model_preprocessed_params.csv`` and
``my_model/my_model_preprocessing.log``.

The latter is simply a log file. ``my_model_preprocessed_params.csv`` is a
parameter table similar to ``my_model_params.csv`` but with log-transformed (if
required) and standardized target parameters, and with an additional column
indicating the assignment of each scenario to training, validation or test sets.
Note that all replicates of a scenario are assigned to the same class.
``my_model/my_model_training_config.yml`` will be described in the next section.

More details on the dedicated :doc:`preprocessing page
<data_preprocessing>`.

.. _overview-training:

Training
========

We can now proceed to training. It consists of optimizing the parameters of a
statistical model (here the weights of a network) based on a training dataset
and optimization hyperparameters, and evaluating the performance on a validation
set.

First edit ``my_model/my_model_training_config.yml`` to define, in
particular, which network should be trained, its hyperparameters and loss
function, the optimization hyperparameters, transformation for data
augmentation, etc. More details on the dedicated :doc:`training page
<training>`.

Then run:

.. code-block:: bash

    $ dnadna train my_model_name_training_config.yml

which creates a subdirectory ``run_{run_id}/`` containing the optimized network
``my_model_run_{run_id}_best_net.pth`` as well as checkpoints during training, a
log file and loss values stored in a tensorboard directory.

``dnadna train`` takes additional arguments such as:

* ``--plugin PLUGIN`` to pass plugin files that define custom networks,
  optimizers or transformation that we would like to use for training
  despite them not being in the original dnadna code. See :doc:`dedicated
  plugin page<extending>`.

* ``-r RUN_ID`` or ``--run-id RUN_ID`` to specify a run identifier different from the one created by default (the default starts at run_000 and then monotonically increases to run_001 etc.). RUN_ID can also be specified in the config file.

* ``--overwrite`` to overwrite the previous run (otherwise, create a new run directory).


More details on the dedicated :doc:`training page <training>`.

.. _overview-prediction:

Prediction
==========

Once trained, a network can be applied to a dataset in :doc:`DNADNA dataset format <datasets>` to classify/predict its evolutionary parameters. The following command is used:

.. code-block:: bash

    $ dnadna predict run_{run_id}/my_model_run_{run_id}_best_net.pth realdata/dataset.npz



This will use the best net, but you can use any net name, such as ``run_{run_id}/my_model_run_{run_id}_last_epoch_net.pth``.

This outputs the predictions in CSV format which is printed to standard out
by default while the process runs.  You can pipe this to a file using
standard shell redirection operators like ``dnadna predict {args} >
predictions.csv``, or you can specify a file to output to using the
``--output`` option.


You can also apply ``dnadna predict`` to multiple npz files as follows:

.. code-block:: bash

  $ dnadna predict run_{run_id}/my_model_run_{run_id}_best_net.pth {extra_dir_name}/scenario*/*.npz

where ``{extra_dir_name}`` is a directory (that you created) containing
independent simulations which will serve as test for all networks or as
illustration of predictive performance under specific conditions.


Importantly if you want to ensure that target examples comply to the
preprocessing constraints (such as the minimal number of SNPs and individuals)
use ``--preprocess``. In that case, a warning will be displayed for each rejected scenario, with the reason of rejection (such as the minimal number of SNPs).


More details on the dedicated :doc:`prediction page <prediction>`.
