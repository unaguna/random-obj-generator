int Mode
========

In int mode, integer values are generated. The format of the command is as follows:

.. code-block:: shell

    randog int MINIMUM MAXIMUM [--exp-uniform] [--fmt FORMAT] [common-options]


Arguments and Options
---------------------

- :code:`MINIMUM`:

    - the minimum value.

- :code:`MAXIMUM`:

    - the maximum value.

- :code:`--exp-uniform` (optional):

    - if specified, the distribution of digits (log with base 2) is uniform.

- :code:`--fmt FORMAT` (optional):

    - the output format written in `format specification mini-language <https://docs.python.org/3/library/string.html?highlight=string#format-specification-mini-language>`_

- :code:`common-options`

    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs a value in the specified range.

.. code-block:: shell

    randog int 0 100

.. note::

    If you want to generate decimal values, use :doc:`decimal mode <doc.as_command.decimal>` or :doc:`float mode <doc.as_command.float>`.

Format: 0-padding, etc.
~~~~~~~~~~~~~~~~~~~~~~~

The output format can be specified in `format specification mini-language <https://docs.python.org/3/library/string.html?highlight=string#format-specification-mini-language>`_ as follows:

.. code-block:: shell

    # output 0-padded integer such as '00000042'
    randog int 0 100 --fmt 08

    # output 0-padded integer such as '+42'
    randog int 0 100 --fmt +

Repeatedly Generate
~~~~~~~~~~~~~~~~~~~

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    randog int -r 10

    # Generate list which contains 10 values
    randog int -L 10

Probability Distribution; uniform distribution of digits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the probability distribution of generation is uniform. For example, when generating values from 1 to 10000, the probabilities of generating 1, 50, and 10000 are all identical.

If you are not particular, a uniform distribution is fine, but if you want values to be generated with a variety of digits, this can be problematic. In the above example, there is a 90% probability that a 4-digit number (1000 - 9999) will be generated, and only a 0.1% probability that a 1-digit number will be generated. In other words, the majority of the values generated are 4-digit.

To make the distribution of digits uniform, use :code:`--exp-uniform`. This option gives greater weight to numbers with smaller digits, so that the number of digits is generally uniform. More precisely, the distribution of :code:`floor(log2(x))`, digits in binary notation, is uniform; However, the number of digits of 0 is assumed to be 0, and positive and negative numbers have separate probabilities. For example, when generating integers from -15 to 47, the following events all have the same probability:

- from -15 to -8
- 0
- 1
- from 8 to 15
- from 16 to 31

Note that if only a portion of the number of the digit is in the generation range, the probability of numbers of the digit is reduced; In the example above, only half of 32-63 are included in the range, so the probability is half that of the other digits.

.. note::

    Although it will not make much difference, if you want to determine the probability distribution based on the number of digits in decimal notation, use :doc:`decimal mode <doc.as_command.decimal>`. You can limit the generation to integers by specifying option :code:`--decimal-len=0`.
