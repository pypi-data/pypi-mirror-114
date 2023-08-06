.. _extending:

Extending DNADNA with Plugins
#############################

DNADNA has a simple but powerful plugin capability which allows providing
new networks, transforms, and other extensions.

Many of the main DNADNA commands support loading a plugin when running the
command, particularly:

* ``dnadna init``
* ``dnadna train``
* ``dnadna simulation``

To check if a command accepts plugins, run the command's ``--help`` and see
if the ``--plugin`` option is listed.

To pass plugins to a command, provide the ``--plugin <plugin-name>``
argument to the command.  ``--plugin`` can be specified more than once in
order to load multiple plugins.

The ``plugin-name`` can be one of two things:

* The path to a Python file (e.g. a ``.py`` file).
* The name of an importable Python module; this allows writing your own
  Python packages that provide DNADNA plugins.  In this case pass
  ``--plugin module_name`` where ``module_name`` is the same name by which
  you would import the module in Python with ``import module_name``.

In either case, a DNADNA plugin is just a Python module that is imported
when DNADNA starts up.  It may run any arbitrary Python code.  But in
particular, DNADNA provides specific plugin interfaces that should be used
to extend DNADNA.

The plugin interfaces take the form of *classes* that should be *subclassed*
in order to provide the plugin.  Current pluggable classes include:

* `dnadna.nets.Network` for providing a new network,
* `dnadna.transforms.Transform` for providing new a new dataset transform
* `dnadna.simulator.Simulator` for providing a new simulator,

with others to be added.

To register a plugin, your plugin module must simply subclass one of those
classes.  Each pluggable class then defines additional methods that must
be implemented by your subclass in order for the plugin to work; the
specific methods depend on the plugin interface.


Adding a network
================

To add a new network to DNADNA, your plugin module should subclass
`dnadna.nets.Network` which is a subclass of `torch.nn.Module`.  At a
minimum it must provide a ``forward`` method which computes the forward
function called when evaluating the network.

First you can create a Python file named ``mynetwork.py`` and in that file
write:

.. code-block:: python

    from dnadna.nets import Network

    class MyNetwork(Network):
        def forward(self, input):
            # compute the forward function on the network and return
            # the output

When writing a training config file for your training, you can now specify

.. code-block:: yaml

    network_name: "MyNetwork"

to specify that you want to train with this network.  Then when running
``dnadna train`` you can load your plugin like:

.. code-block:: shell

    $ dnadna train --plugin mynetwork.py path/to/training_config.yml

Additionally/alternatively if you put a ``plugins:`` key at the top-level
of your training config like:

.. code-block:: yaml

    plugins:
        - /path/to/mynetwork.py

The plugin will automatically be loaded (without having to specify
``--plugin``) when running:

.. code-block:: shell

    $ dnadna train path/to/training_config.yml


Network configuration
---------------------

If your network accepts additional configuration parameters, those
parameters can be passed to the class's ``__init__`` like:

.. code-block::

    class MyNetwork(Network):
        def __init__(self, param1=0, param2=1):
            # Make sure to call the parent class's __init__
            super().__init__()
            self.param1 = param1
            self.param2 = param2

        def forward(self, input):
            # compute the forward function on the network and return
            # the output

In your training config file, you can specify the parameters to pass to your
network (if different from their default values or if there are no default
values) in the ``net_params:`` key, just as with DNADNA's built-in nets:

.. code-block:: yaml

    net_params:
        param1: 100
        param2: 200

When starting training these parameters are passed to your network's
``__init__``.

By default, your custom ``net_params`` are not validated when loading the
config file, so you are at your own risk with respect to providing
appropriate ``net_params`` values.


(Advanced) Network configuration schema
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Optionally*, when defining your `~dnadna.nets.Network` subclass, you may
provide a ``schema`` attribute given in `JSON Schema
<https://json-schema.org/understanding-json-schema/>`_ format to provide
additional verification of your net's configuration.  For example:

.. code-block::

    class MyNetwork(Network):
        schema = {
            'properties': {
                'param1': {
                    'description': 'param1 must be a non-negative integer',
                    'type': 'integer',
                    'minimum': 0,
                    'default': 0
                },
                'param2': {
                    'description': 'param2 must be a positive integer',
                    'type': 'integer',
                    'minimum': 1,
                    'default': 1
                }
            }
        }

        def __init__(self, param1=0, param2=1):
            # Make sure to call the parent class's __init__
            super().__init__()
            self.param1 = param1
            self.param2 = param2

        def forward(self, input):
            # compute the forward function on the network and return
            # the output

JSON Schema has a bit of a learning curve, so if you may omit this step if
you don't have time to become comfortable with it, but it can be a powerful
tool to help ensure correctness of your training configuration.
