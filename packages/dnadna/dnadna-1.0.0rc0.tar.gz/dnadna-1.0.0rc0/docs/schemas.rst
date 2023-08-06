.. _schemas:

Configuration Schemas
=====================

.. contents::
   :local:


Dataset config schema
---------------------

The dataset config is the base format for simulation configs (see below).  A
dataset config just specifies some generic details about the files in any
dataset (whether or not it was produced by a simulation), and how to load
them.  The simulation config extends this by adding further details about
the simulation which produced the dataset.

.. schema:: ../dnadna/schemas/dataset.yml
   :annotated-example: dnadna.defaults.DEFAULT_DATASET_CONFIG


Simulation config schema
------------------------

The simulation config format is the same as the one for :ref:`dataset
<schema-dataset>` but with an additional ``simulator_name`` property, as
well as `.Simulator`-specific properties.

.. schema:: ../dnadna/schemas/simulation.yml
   :annotated-example: dnadna.examples.one_event.DEFAULT_ONE_EVENT_CONFIG


Preprocessing config schema
---------------------------

.. schema:: ../dnadna/schemas/preprocessing.yml
   :annotated-example: dnadna.defaults.DEFAULT_PREPROCESSING_CONFIG


Learned params schema
---------------------

.. schema:: ../dnadna/schemas/param-set.yml


Training config schema
----------------------

.. schema:: ../dnadna/schemas/training.yml
   :annotated-example: dnadna.defaults.DEFAULT_TRAINING_CONFIG


Summary statistics config schema
--------------------------------

.. schema:: ../dnadna/schemas/summary-statistics.yml
