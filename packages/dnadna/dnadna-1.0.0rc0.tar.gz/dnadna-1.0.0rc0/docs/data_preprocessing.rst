Dataset Preprocessing
######################

What does preprocessing do?
===========================

The preprocessing step is required for different purposes:

#. Input file validation

    #. It verifies that each input file exists

    #. It discards simulations that don't have the correct dimension

#. Split the dataset into training/validation/test sets (the latter is
   optional)

#. Apply transformations to parameters (e.g. log transformation) when required by the user

#. Standardize target parameter(s) for regression tasks.

This step is necessary before performing the first training run. Depending
on the size of the dataset, it can take some time, but this is usually done
once per iteration of fine-tuning the hyperparameters in the training step
of one or multiple networks. It is necessary to re-run processing on the
same dataset only if:

    * The task changes (e.g. predicting other parameters or the same parameters but with different transformations)

    * The required input dimensions change (e.g. to match the dimensions expected by some networks).


How do you configure the preprocessing command?
===============================================

To run the preprocessing command, a configuration file needs to be completed.
This file, as the other configuration files, has two purposes: specifying
the parameters the model will be trained to predict, and specifying how the
preprocessing script should filter the dataset.

We will discuss the different sections of the configuration file separately,
but they all go into the same file.

Input file validation
---------------------

Why?
^^^^

The paths of the dataset files are given by the dataset configuration
section (present in the simulation config file or in its own config file).
Along with checking the existence of the files, it will discard scenarios in
which at least one of the replicated simulations does not have the correct
dimensions (indicated by the ``min_snp`` and ``min_indiv`` settings in the
preprocessing config file).

There are multiple reasons a user might specify these thresholds:

#. Respecting the constraints of an architecture:

   * If the network's input has a fixed size across examples, simulations
     must contain at least ``min_snp SNPs`` and ``min_indiv`` individuals
     (and should be truncated to exactly these numbers later using the
     `~dnadna.transforms.Crop` transform).

   * If the network is invariant to the number of SNPs or individuals, it
     might still require a minimal input size so that all operations can be
     correctly applied (such as successive pooling operations that strongly
     reduce the data size)

#. Discarding scenarios which are unrealistically small (as determined
   according to the user's best judgment).

How?
^^^^

In the ``preprocessing`` block of the config file, e.g.:

.. code-block:: yaml

    preprocessing:
        # minimum number of SNPs each sample should have
        min_snp: 500

        # minimum number of individuals in each sample
        min_indiv: 20


Splitting the dataset into training/validation/test sets
--------------------------------------------------------

Why?
^^^^

To avoid overfitting the network to the dataset, the network is trained on a
subset of the data (the training set), and is validated against another part
of the dataset that the network did not use for training (the validation
set).

While developing the network, we adjust the hyperparameters (type of
architecture, batch size, learning rate, etc...) until we have good
performance on the validation set.  This can indirect overfitting of the
validation set. A good practice is to run the trained and fine-tuned
network(s) only once on yet another subset of the data (the test set). This
is done at the very end of all experiments in order to measure consistency
in the results of each experiment.

Because this test set can be stored elsewhere or simulated later, specifying
a test set is optional.  Remember that the final test set should not be used
for hyperparameter optimization.

.. note::

    The current version does not automatically run the network on the test
    set; this feature will be added in a future release.

How?
^^^^

In the ``dataset_splits`` block of the preprocessing config file, the
proportion of the different sets can be specified.  If it sums to less than
1.0 (100%) some simulations are not used, and it must not sum to greater
than 1.0:

.. code-block:: yaml

    # split the dataset in the different subsets. training and validation
    # are mandatory.

    dataset_splits:
        training: 0.6
        validation: 0.2
        test: 0.1


Specify learned parameters and apply transformations
----------------------------------------------------

Why?
^^^^

At this step we must specify the parameters learned by the network, and
which task we apply to them (regression or classification), as well as
whether or not they should be log transformed in the case of regression
parameters.

How?
^^^^

In the ``learned_params`` block, we have one sub-block per parameter. This sub-block has the properties describing the corresponding parameter.

.. code-block:: yaml

    learned_params:
        event_time:
            type: regression
            log_transform: true
        recent_size:
            type: regression
            log_transform: true
        event_size:
            type: regression
            log_transform: true
        selection:
            type: classification
            classes:
                - "no"
                - "yes"


In this example, three demographic parameters (``event_time``,
``recent_size`` and ``event_size``) should be predicted via regression and
one parameter (``selection``) via classification.  In the latter case, the
``classes`` setting may either be an integer giving the number of classes,
or a list of strings giving names to each of the classes.

.. note::

    Currently the class names are not used in any way, and the scenario
    parameters table is expected to have classes labeled by integers.  This
    will be improved in a future release (see `issue #99
    <https://gitlab.inria.fr/ml_genetics/private/dnadna/-/issues/99>`_.


What are the input and output files for the preprocessing step?
===============================================================

The required dataset files are:

- A :ref:`directory <dnadna-dataset-filesystem>` containing the simulation
  data files
- A :ref:`table <dnadna-dataset-scenario-params>` in CSV format with the
  different parameters (in columns) used to simulate the different scenarios
  (in rows)
- A :ref:`dataset configuration file <dnadna-dataset-simulation-config>`  which provides notably the path to the previously mentioned elements

The additional required input is:

- A preprocessing configuration file, which contains the different
  parameters that will tell what kind of preprocessing is wanted (described
  in the previous section as well as the :ref:`schema specifying the file
  format <schema-preprocessing>`.

The first three elements are obtained easily when using the :doc:`simulation
<simulator>` sub-command of ``dnadna``, otherwise, one should create them.

An example preprocessing config file is generated when running the ``dnadna
init`` command.  See :ref:`overview-initialization`.

The output files produced by this step are:

- A table ``<model_name>_preprocessed_params.csv`` that contains the target
  parameters, possibly normalized and/or transformed. It also contains for a
  given scenario, to which set (train/validation/test) it belongs

- The training configuration file, to modify before doing the next step:
  ``dnadna train``.

The training configuration file will indicate the mean and standard
deviation computed over the training set for each standardized target
parameter. Those will be used to unstandardize the predicted values during
the prediction step.

It will also contain the date and time of when the preprocessing was done,
as well as the version of ``dnadna`` used.

Command line
============

Once the preprocessing configuration file has been filled and the required input files are created, the command to start the preprocessing is simply:

.. code-block:: bash

    dnadna preprocess <model_name>_preprocessing_config.yml


More details can be found in the :ref:`introduction:Quickstart Tutorial`.


Next step
=========

After successful pre-processing you can :doc:`train <training>` your
network.
