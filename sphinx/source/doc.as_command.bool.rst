bool Mode
=========

In bool mode, boolean values are generated. The format of the command is as follows:

.. code-block:: shell

    randog bool [PROP_TRUE] [--fmt FORMAT] [common-options]


Arguments and Options
---------------------

- :code:`PROP_TRUE` (optional, default=0.5):

    - the probability of True.

- :code:`--fmt FORMAT` (optional):

    - the output format written in `format specification mini-language <https://docs.python.org/3/library/string.html?highlight=string#format-specification-mini-language>`_

- :code:`common-options`

    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs True or False with a 50% probability of each.

.. code-block:: shell

    randog bool

You can specify the probability of True.

.. code-block:: shell

    # output True with 80% probability and False with 20% probability
    randog bool 0.8

Format: Lowercase or Numeric
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It may be necessary to output in lower case, for example, if the output is to be processed by a program in another language. In that case, the desired format can be obtained by outputting in json format as follows:

.. code-block:: shell

    # Output True or False
    randog bool

    # Output true or false
    randog bool --json

If you want to make it numeric, you can use :code:`--fmt`.

.. code-block:: shell

    # Output 1 or 0
    randog bool --fmt 1

.. note::
    This takes advantage of the property that `values of type bool are treated as integer values in some contexts <https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values>`_.

Repeatedly Generate
~~~~~~~~~~~~~~~~~~~

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    randog bool -r 10

    # Generate list which contains 10 values
    randog bool -L 10
