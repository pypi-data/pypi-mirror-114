.. _prediction:

Prediction
##########


Once trained a network can be applied (through a simple forward pass) to other
datasets, such as:

* a test set, after hyperparameter optimization has been done for all networks. It enables to compare fairly multiple networks and check whether they overfitted the validation set,

* specific examples, to evaluate predictive performance on specific scenarios or the robustness under specific conditions (such as new data under selection while selection was absent from the training set),

* real datasets to reconstruct the past evolutionary history of real populations.


The required arguments for ``dnadna predict`` are:

* MODEL: most commonly a path to a .pth file, such as
  ``run_{runid}/my_model_run_{runid}_best_net.pth``, that contains the
  trained network we wish to use and additional information (such as data
  transformation that should be applied beforehand and info to unstandardize
  and/or "untransform" the predicted parameters).  Alternatively the final
  config file of a run ``run_{runid}/my_model_run_{runid}_final_config.yml``
  can be passed (in which case the best network of the given run is used by
  default).

* INPUT: path to one or more npz files, or to a :ref:`dataset config file <dnadna-dataset-simulation-config>` (describing a whole dataset).


A typical usage will thus be:

.. code-block:: bash

    $ dnadna predict run_{run_id}/my_model_run_{run_id}_best_net.pth realdata/sample.npz

to classify/predict evolutionary parameters for a single data sample
``realdata/sample.npz`` in :doc:`DNADNA dataset format <datasets>`.

This will use the best net, but you can use any net name, such as ``run_{run_id}/my_model_run_{run_id}_last_epoch_net.pth``.

This outputs the predictions in CSV format which is printed to standard out
by default while the process runs.  You can pipe this to a file using
standard shell redirection operators like ``dnadna predict {args} >
predictions.csv``, or you can specify a file to output to using the
``--output`` option.


You can also apply dnadna predict to multiple npz files as follows:

.. code-block:: bash

  $ dnadna predict run_{run_id}/my_model_run_{run_id}_best_net.pth {extra_dir_name}/scenario*/*.npz

where ``{extra_dir_name}`` is a directory (that you created) containing
independent simulations which will serve as test for all networks or as
illustration of predictive performance under specific conditions.


The previous command is equivalent to:

.. code-block:: bash

    $ dnadna predict run_{run_id}/my_model_run_{run_id}_final_config.yml {extra_dir_name}/scenario*/*.npz

where the training config file is passed rather than the ``.pth`` of the best
network, but you could alternatively add the option ``--checkpoint last_epoch``
to use the network at final stage of training rather than the best one.


Importantly if you want to ensure that target examples comply to the
preprocessing constraints (such as the minimal number of SNPs and individuals)
use ``--preprocess``. In that case, a warning will be displayed for each rejected scenario, with the reason of rejection (such as the minimal number of SNPs).

In the current version the same data transformations are applied to the
training/validation/test sets and to extra simulations or real data on which
the prediction is made. These are the same data transformations that are
defined in the training config file for the training run that produced the
model.

Finally you can fine-tune resource usage with the options ``--gpus --GPUS`` and
``--loader-num-workers LOADER_NUM_WORKERS`` to indicate the specific GPUs and
the number of CPUs to use. You can display a progress bar with the option
``--progress-bar``.
