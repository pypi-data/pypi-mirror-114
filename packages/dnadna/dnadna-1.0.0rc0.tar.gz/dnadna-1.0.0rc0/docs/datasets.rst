.. _datasets:

Simulation Datasets
###################

Simulation data used by DNADNA consists of two components, an SNP matrix and
a positions array; one of each for each simulation.

- The SNP matrix is a 2-D array, typically arranged such that the number of
  rows is the number of individuals sampled in the simulation, and the
  number of columns is the number of SNPs.  The matrix contains boolean
  data, with a 1 when a variation is present, and a 0 otherwise.

- The positions array has length equal to the number of columns in the
  associated SNP matrix. That is, it is the positions within a genome where
  the SNPs occur.  The positions array may come in one of a number of
  different normalizations, such as absolute positions within a genome, or
  relative positions (distance to the previous SNP).  They may also be whole
  numbers, or re-normalized to a floating point value in the range [0.0,
  1.0). The format of position in your simulated data can be specified
  thanks to the properties ``distance:True/False`` and
  ``normalized:True/False`` in the :ref:`dataset config file
  <dnadna-dataset-simulation-config>`.

.. note::

    Individual simulations are represented internally by the
    `~dnadna.snp_sample.SNPSample` class, and the SNP matrix and position
    array are returned as PyTorch `Tensors <torch.Tensor>` by the
    `~dnadna.snp_sample.SNPSample.snp` and
    `~dnadna.snp_sample.SNPSample.pos` attributes respectively.

.. _dataset-formats-dnadna:


The DNADNA Dataset Format
-------------------------

DNADNA trains its models on large collections of simulation data, which is
assumed to be organized on disk in the "DNADNA Format".  Although most of
the internal :ref:`API <api>` is agnostic to how simulation data is located
and loaded, the high-level user interface currently assumes this format by
default.  Support for using arbitrary data sources via plugins will be
available in a future version.

The DNADNA Format assumes that each SNP matrix and associated positions
array are stored together in a single NPZ_ file, either compressed or
uncompressed, under the ``'SNP'`` and ``'POS'`` keys respectively.  The SNP
matrix is a 2-D array of 8-bit unsigned integer type, and the positions
array may consist of integers or single- or double-precision floats.

Each simulation has associated with it one or more *scenario parameters*
(see :ref:`the scenario parameters table <dnadna-dataset-scenario-params>`
below) which are known parameters, specific to the simulation.  This
scenario parameters table will be used while training your neural net to
provide target values for parameters in your training and validation sets.

Each simulation dataset includes one or more *scenarios* which represent
different a specific combination of scenario parameters which were used for
simulations in that scenario.  And each scenario may consist of one or more
*replicates*, which are multiple copies of simulations with the same
parameters, but differently randomized.

To summarize, each simulation dataset consists of:

- One or more scenarios containing one or more simulation replicates, with
  one NPZ file per-replicate, per-scenario
- A table of scenario parameters with one row for each scenario
- A :ref:`simulation config file <dnadna-dataset-simulation-config>`
  containing additional metadata about the simulation dataset, and
  configuration on how to read it.

.. _NPZ: https://numpy.org/devdocs/reference/generated/numpy.savez.html#numpy.savez


.. _dnadna-dataset-filesystem:

Filesystem layout
^^^^^^^^^^^^^^^^^

Although the DNADNA Format allows some :ref:`customization
<dnadna-dataset-simulation-config>` as to how simulation files are organized
on disk, by default it assumes a layout that looks like::

    _ simulations/  # root directory of all simulation datasets; arbitrary name
        \_ model-A/
            \_ model-A_params.csv  # the scenario parameters table
            |_ model-A_simulation_config.yml  # the simulation config file
            |_ scenario_000/
                \_ model-A_000_00.npz  # scenario 0 replicate 0
                ...
                |_ model-A_000_NN.npz
            |_ scenario_001/
                \_ model-A_001_00.npz  # scenario 1 replicate 0
                ...
                |_ model-A_001_NN.npz
            ...
            |_ scenario_NNN/
                \_ model-A_NNN_00.npz
                ...
                |_ model-A_NNN_NN.npz

.. note::

    Scenarios and replicates are always assumed to be numbered starting from
    zero, up to the number of scenarios/replicates minus one, for standard
    C/Python-style indexing.

    Simulation and replicate numbers in filenames are typically zero-padded
    with the largest number of zeros to make the filesize consistent across
    the dataset, but this is optional.


.. _dnadna-dataset-scenario-params:

The scenario params table
^^^^^^^^^^^^^^^^^^^^^^^^^

The scenario parameters table, or just "scenario params" for short lists the
simulation parameters of each scenario in the dataset.  It is currently
assumed to be a CSV_ file containing at a minimum three columns (including a
header container containing the column names):

- ``scenario_idx`` - this is the scenario number to which these parameters
  apply (integer)
- ``<parameter>`` - at least *one* parameter, the name of which may be
  anything except ``scenario_idx`` or ``n_replicates``, and is particular to
  the dataset (float or integer)
- ``n_replicates`` - for each scenario, the number of replicates in that
  scenario; this may or may not be the same for all scenarios (integer)

Any number of additional columns are allowed, each of which are assumed to
be a different simulation parameter.  Example:

.. code-block:: csv

    scenario_idx,mutation_rate,recombination_rate,event_time,recent_size,event_size,segment_length,n_samples,n_replicates
    0,1e-08,1e-08,0.3865300203456797,-0.497464473948751,-0.5251379654844626,2000000,50,100
    1,1e-08,1e-08,0.19344551118300793,0.16419897912977574,0.22637196776073554,2000000,50,100
    ...

.. _CSV: https://en.wikipedia.org/wiki/Comma-separated_values

.. _dnadna-dataset-simulation-config:

The dataset config file
^^^^^^^^^^^^^^^^^^^^^^^

The dataset configuration, just "dataset config" for short contains some
required additional metadata about the dataset, as well as optional
parameters for customizing how the dataset is formatted, or additional
metadata specific to the :ref:`simulator <simulators>` that output the
simulation.  It can also be referred to as the "simulation config" in the
latter case.

The dataset config is also always validated against a :ref:`schema
<schema-dataset>` which both documents the format, and ensures the
correctness of config files.

Here is an example, mostly minimal simulation config file:

.. literalinclude:: ../dnadna/defaults/dataset.yml
    :language: yaml
    :linenos:

The ``data_root`` property gives the root directory for all files in the
dataset.  This is typically just the relative directory ``.``, which means
the same directory as the simulation config file itself, which is the
default :ref:`layout <dnadna-dataset-filesystem>` for the DNADNA format.

You can also see that the ``data_source.filename_format`` gives a template
for ``.npz`` filenames which matches with the default :ref:`filesystem
layout <dnadna-dataset-filesystem>` of the DNADNA Format.  This property may
be omitted from the config file if the default format is used, but this
demonstrates that the filename format allows some customization.


Alternative dataset formats
---------------------------

As previously mentioned, although the :ref:`DNADNA Format
<dataset-formats-dnadna>` is used by default, alternative dataset formats
are supported at the API level, and may be supported at the high-level via
config files in the future.

In the meantime, if you have :ref:`msprime <msprime:sec_intro>` or ``SLiM``
scripts for your simulations, you can easily save the tree sequence object
into DNADNA format npz files by adding the following lines into your
scripts:

.. code-block:: python

  # If tree_sequence was simulated for multiple replicate of a given scenario
  # scenario corresponds to a number indexing one set of parameter values
  # cf scenario params table
  for replicate, ts in enumerate(tree_sequence):
      snps = ts.genotype_matrix().T.astype(np.uint8)
      pos = np.round(ts.tables.sites.position).astype(np.int)
      # Default layout (can be changed)
      filename = f"scenario_{scenario}/{dataset_name}_{scenario}_{replicate}.npz"
      np.savez_compressed(os.path.join(outdir, filename), SNP=snps, POS=pos)

Note that the default :ref:`layout <dnadna-dataset-filesystem>` for the
DNADNA format can be changed to suit your wishes, e.g. you could change to::

  filename = f"{dataset_name}/scen_{scenario}_arbitrary_text/rep_{replicate}/{scenario}_{replicate}.npz"


In which case you will update ``filename_format`` in the
:ref:`dataset config file <dnadna-dataset-simulation-config>`:

.. code-block:: YAML

  data_source:
    # string template for per-replicate simulation files in Python
    # string template format; the following template variables may be
    # used: 'name', the same as the name property used in this config
    # file; 'scenario', the scenario number, and 'replicate', the
    # replicate number of the scenario (if there are multiple
    # replicates); path separators may also be used in the template to
    # form a directory structure
    filename_format: {dataset_name}/scen_{scenario}_arbitrary_text/rep_{replicate}/{scenario}_{replicate}.npz


before running:

.. code-block:: bash

  $ dnadna init --dataset-config={dataset_name}/{dataset_name}_dataset_config.yml

where ``{dataset_name}/{dataset_name}_dataset_config.yml`` is the name you
picked for the config file.


You can check our `notebook
<https://gitlab.com/mlgenetics/dnadna/-/tree/master/examples/example_simulate_msprime_save_dnadna_npz.ipynb>`_
for an illustration of a simple constant demographic scenario in ``msprime``
saved as DNADNA format.

If you want to run several simulations or share your simulation code with
other DNADNA users, it may be useful to adapt your existing simulation code
to a :ref:`Simulator plugin <simulator-tutorial>` for DNADNA.

.. note::

    ``msprime`` outputs positions in bp, i.e. not normalized between 0 and 1, and
    chromosomes are not circular (contrary to some bacterial simulators), thus
    in the :ref:`dataset config file <dnadna-dataset-simulation-config>` you
    will indicate:

    .. code-block:: YAML

      position_format:
          distance: false
          normalized: false
          circular: false


.. todo::

    Add some basic documentation on how "SNP Sources" such as
    `~dnadna.datasets.NpzSNPSource` and `~dnadna.datasets.DictSNPSource` are
    implemented, and how advanced users could implement their own.
