decimal Mode
============

In decimal mode, decimal values are generated. The format of the command is as follows:

.. code-block:: shell

    randog decimal [MINIMUM MAXIMUM] [--decimal-len DECIMAL_LENGTH] [--p-inf PROB_P_INF] [--n-inf PROB_N_INF] [--nan PROB_NAN] [--exp-uniform] [--fmt FORMAT] [common-options]


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

- :code:`--exp-uniform` (optional):

    - if specified, the distribution of digits (log with base 10) is uniform.

- :code:`--fmt FORMAT` (optional):

    - the output format written in `format specification mini-language <https://docs.python.org/3/library/string.html?highlight=string#format-specification-mini-language>`_

- :code:`common-options`

    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs a value between 0 and 1.

.. code-block:: shell

    randog decimal

You can specify a range of values to be generated, as in the following example:

.. code-block:: shell

    # generates a value between 0.01 and 10^100
    randog decimal 0.01 1e+100

When using decimal numbers, you will often want to limit the number of decimal places. In that case, use :code:`--decimal-len` as in the following example:

.. code-block:: shell

    # generates a value such as 245.91
    randog decimal 0 1000 --decimal-len 2

Infinity and NaN
~~~~~~~~~~~~~~~~

Infinity and NaN can be included as candidates for generation by specifying optional arguments.

.. code-block:: shell

    # Generates positive infinity with 10% probability
    randog decimal 0 1e+100 --p-inf 0.1

    # Generates NaN with 15% probability
    randog decimal --nan 0.15

Format: Thousands Separator, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The output format can be specified in `format specification mini-language <https://docs.python.org/3/library/string.html?highlight=string#format-specification-mini-language>`_ as follows:

.. code-block:: shell

    # output separated numeric such as '12,345.67'
    randog decimal 0.01 99999.99 --decimal-len 2 --fmt ','


Repeatedly Generate
~~~~~~~~~~~~~~~~~~~

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    randog decimal --decimal-len 2 -r 10

    # Generate list which contains 10 values
    randog decimal --decimal-len 2 -L 10 --json

Probability Distribution; uniform distribution of digits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the probability distribution of generation is uniform. For example, when generating values from 0.1 to 1000.0, the probabilities of generating 0.1, 5.0, and 500.0 are all identical.

If you are not particular, a uniform distribution is fine, but if you want values to be generated with a variety of digits, this can be problematic. In the above example, there is a 90% probability that a 3-digit number (100.0 - 1000.0) will be generated, and only a 0.1% probability that a number less than 1 will be generated. In other words, the majority of the values generated are 3-digit.

To make the distribution of digits uniform, use :code:`--exp-uniform`. This option gives greater weight to numbers with smaller digits, so that the number of digits is generally uniform. More precisely, the distribution of :code:`floor(log10(x))`, digits in binary notation, is uniform; However, the number of digits of 0 is assumed to be 0, and positive and negative numbers have separate probabilities. For example, when generating numbers from -1000.00 to 55000.00, the following events all have the same probability:

- from -1000.00 to -100.00
- from -0.10 to -0.01
- 0.00
- 1.00
- from 0.01 to 0.10
- from 1000.00 to 10000.00

Note that if only a portion of the number of the digit is in the generation range, the probability of numbers of the digit is reduced; In the example above, only half of 10000.00-100000.00 are included in the range, so the probability is half that of the other digits.
