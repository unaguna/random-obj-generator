float Mode
==========

In float mode, floating-point numeric values are generated. The format of the command is as follows:

.. code-block:: shell

    python -m randog float [MINIMUM MAXIMUM] [--p-inf PROB_P_INF] [--n-inf PROB_N_INF] [--nan PROB_NAN] [--fmt FORMAT] [common-options]


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

- :code:`--fmt FORMAT` (optional):

    - the output format written in `format specification mini-language <https://docs.python.org/3/library/string.html?highlight=string#format-specification-mini-language>`_

- :code:`common-options`

    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs a value between 0 and 1.

.. code-block:: shell

    python -m randog float

You can specify a range of values to be generated, as in the following example:

.. code-block:: shell

    # generates a value between 0.01 and 10^100
    python -m randog float 0.01 1e+100

.. note::

    You can also use :doc:`decimal mode <doc.as_command.decimal>`.

    If you want to generate an integer with no decimal part, use :doc:`int mode <doc.as_command.int>`.

Infinity and NaN
~~~~~~~~~~~~~~~~

Infinity and NaN can be included as candidates for generation by specifying optional arguments.

.. code-block:: shell

    # Generates positive infinity with 10% probability
    python -m randog float 0 1e+100 --p-inf 0.1

    # Generates NaN with 15% probability
    python -m randog float --nan 0.15

Use python standard for representing infinity and NaN such as :code:`inf`, :code:`-inf`, and, :code:`nan`.
The output can also be in JSON format, such as :code:`Infinity`, :code:`-Infinity`, and, :code:`NaN`, by :code:`--json` option if there is a problem, such as when reading the output in programs written in other languages.

.. code-block:: shell

    # Generates Infinity, -Infinity, or, NaN
    python -m randog float --p-inf 0.4 --n-inf 0.4 --nan 0.2 --json

Format: Significant Digits, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The output format can be specified in `format specification mini-language <https://docs.python.org/3/library/string.html?highlight=string#format-specification-mini-language>`_ as follows:

.. code-block:: shell

    # output numeric such as '4.20e+98', which has (2+1) significant digits
    python -m randog float 0.01 1e+100 --fmt .2e

.. note::

    Although the length of the decimal part can be specified as in :code:`--fmt .2f`, :doc:`decimal mode <doc.as_command.decimal>` is suitable for generating numbers with a fixed length of decimal part.

Repeatedly Generate
~~~~~~~~~~~~~~~~~~~

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    python -m randog float -r 10

    # Generate list which contains 10 values
    python -m randog float -L 10
