bool Mode
=========

In bool mode, boolean values are generated. The format of the command is as follows:

.. code-block:: shell

    python -m randog bool [PROP_TRUE] [common-options]


Arguments and Options
---------------------

- :code:`PROP_TRUE` (optional, default=0.5):
    - the probability of True.

- :code:`common-options`
    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs True or False with a 50% probability of each.

.. code-block:: shell

    python -m randog bool

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    python -m randog bool -r 10

    # Generate list which contains 10 values
    python -m randog bool -L 10

It may be necessary to output in lower case, for example, if the output is to be processed by a program in another language. In that case, the desired format can be obtained by outputting in json format as follows:

.. code-block:: shell

    # Repeat 10 times
    python -m randog bool -r 10 --json

    # Generate list which contains 10 values
    python -m randog bool -L 10 --json
