decimal Mode
============

In decimal mode, decimal values are generated. The format of the command is as follows:

.. code-block:: shell

    python -m randog decimal [MINIMUM MAXIMUM] [--decimal-len DECIMAL_LENGTH] [--p-inf PROB_P_INF] [--n-inf PROB_N_INF] [--nan PROB_NAN] [common-options]


Arguments and Options
---------------------

- :code:`MINIMUM` (optional):
    - the minimum value. If not specified, the behavior is left to the specification of `randdecimal <randog.factory.html#randog.factory.randdecimal>`_.

- :code:`MAXIMUM` (optional):
    - the maximum value. If not specified, the behavior is left to the specification of `randdecimal <randog.factory.html#randog.factory.randdecimal>`_..

- :code:`--decimal-len DECIMAL_LENGTH` (optional):
    - the length of decimal part of generated values. If not specified, the behavior is left to the specification of `randdecimal <randog.factory.html#randog.factory.randdecimal>`_.

- :code:`--p-inf PROB_P_INF` (optional, default=0.0):
    - the probability of positive infinity.

- :code:`--n-inf PROB_N_INF` (optional, default=0.0):
    - the probability of negative infinity.

- :code:`--nan PROB_NAN` (optional, default=0.0):
    - the probability of NaN.

- :code:`common-options`
    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs a value between 0 and 1.

.. code-block:: shell

    python -m randog decimal

You can specify a range of values to be generated, as in the following example:

.. code-block:: shell

    # generates a value between 0.01 and 10^100
    python -m randog decimal 0.01 1e+100

When using decimal numbers, you will often want to limit the number of decimal places. In that case, use :code:`--decimal-len` as in the following example:

.. code-block:: shell

    # generates a value such as 245.91
    python -m randog decimal 0 1000 --decimal-len 2

Infinity and NaN can be included as candidates for generation by specifying optional arguments.

.. code-block:: shell

    # Generates positive infinity with 10% probability
    python -m randog decimal 0 1e+100 --p-inf 0.1

    # Generates NaN with 15% probability
    python -m randog decimal --nan 0.15

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    python -m randog decimal --decimal-len 2 -r 10

    # Generate list which contains 10 values
    python -m randog decimal --decimal-len 2 -L 10 --json

