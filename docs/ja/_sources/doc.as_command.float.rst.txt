float Mode
==========

In float mode, floating-point numeric values are generated. The format of the command is as follows:

.. code-block:: shell

    randog float [MINIMUM MAXIMUM] [--p-inf PROB_P_INF] [--n-inf PROB_N_INF] [--nan PROB_NAN] [--exp-uniform] [--fmt FORMAT] [common-options]


Arguments and Options
---------------------

- :code:`MINIMUM` (optional):

    - the minimum value. If not specified, the behavior is left to the specification of `randfloat <randog.factory.html#randog.factory.randfloat>`_.

- :code:`MAXIMUM` (optional):

    - the maximum value. If not specified, the behavior is left to the specification of `randfloat <randog.factory.html#randog.factory.randfloat>`_.

- :code:`--p-inf PROB_P_INF` (optional, default=0.0):

    - the probability of positive infinity.

- :code:`--n-inf PROB_N_INF` (optional, default=0.0):

    - the probability of negative infinity.

- :code:`--nan PROB_NAN` (optional, default=0.0):

    - the probability of NaN.

- :code:`--exp-uniform` (optional):

    - if specified, the distribution of digits (log with base 2) is uniform.

- :code:`--fmt FORMAT` (optional):

    - the output format written in `format specification mini-language <https://docs.python.org/3/library/string.html?highlight=string#format-specification-mini-language>`_

- :code:`common-options`

    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs a value between 0 and 1.

.. code-block:: shell

    randog float

You can specify a range of values to be generated, as in the following example:

.. code-block:: shell

    # generates a value between 0.01 and 10^100
    randog float 0.01 1e+100

.. note::

    You can also use :doc:`decimal mode <doc.as_command.decimal>`.

    If you want to generate an integer with no decimal part, use :doc:`int mode <doc.as_command.int>`.

Infinity and NaN
~~~~~~~~~~~~~~~~

Infinity and NaN can be included as candidates for generation by specifying optional arguments.

.. code-block:: shell

    # Generates positive infinity with 10% probability
    randog float 0 1e+100 --p-inf 0.1

    # Generates NaN with 15% probability
    randog float --nan 0.15

Use python standard for representing infinity and NaN such as :code:`inf`, :code:`-inf`, and, :code:`nan`.
The output can also be in JSON format, such as :code:`Infinity`, :code:`-Infinity`, and, :code:`NaN`, by :code:`--json` option if there is a problem, such as when reading the output in programs written in other languages.

.. code-block:: shell

    # Generates Infinity, -Infinity, or, NaN
    randog float --p-inf 0.4 --n-inf 0.4 --nan 0.2 --json

Format: Significant Digits, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The output format can be specified in `format specification mini-language <https://docs.python.org/3/library/string.html?highlight=string#format-specification-mini-language>`_ as follows:

.. code-block:: shell

    # output numeric such as '4.20e+98', which has (2+1) significant digits
    randog float 0.01 1e+100 --fmt .2e

.. note::

    Although the length of the decimal part can be specified as in :code:`--fmt .2f`, :doc:`decimal mode <doc.as_command.decimal>` is suitable for generating numbers with a fixed length of decimal part.

Repeatedly Generate
~~~~~~~~~~~~~~~~~~~

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    randog float -r 10

    # Generate list which contains 10 values
    randog float -L 10

Probability Distribution; uniform distribution of digits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the probability distribution of generation is uniform. For example, when generating values from 0.1 to 1000.0, the probabilities of generating 0.1, 5.0, and 500.0 are all identical.

If you are not particular, a uniform distribution is fine, but if you want values to be generated with a variety of digits, this can be problematic. In the above example, there is a 90% probability that a 3-digit number (100.0 - 1000.0) will be generated, and only a 0.1% probability that a number less than 1 will be generated. In other words, the majority of the values generated are 3-digit.

To make the distribution of digits uniform, use :code:`--exp-uniform`. This option gives greater weight to numbers with smaller digits, so that the number of digits is generally uniform. More precisely, the distribution of :code:`floor(log2(x))`, digits in binary notation, is uniform; However, the number of digits of 0 is assumed to be 0, and positive and negative numbers have separate probabilities. For example, when generating numbers from -8 to 24, the following events all have the same probability:

- from -8.0 to -4.0
- from -0.25 to -0.125
- 0.0
- 1.0
- from 0.125 to 0.25
- from 8.0 to 16.0

Note that if only a portion of the number of the digit is in the generation range, the probability of numbers of the digit is reduced; In the example above, only half of 16-32 are included in the range, so the probability is half that of the other digits.

.. note::

    Since floating-point numbers can be represented to the smallest power of -1022 of 2, including 0 in the generation range tends to result in only small absolute values. For example, if the range is 0 to 100, the number of digits ranges from -1022 to 7, so 90% of the generated values will be smaller than 2 to the power of -100.

    If this is not desired, use :doc:`decimal mode <doc.as_command.decimal>`. The probability distribution will be based on decimal notation, but you can limit the smallest unit with option :code:`--decimal-len`.
