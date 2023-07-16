date Mode
=========

In date mode, date values are generated. The format of the command is as follows:

.. code-block:: shell

    python -m randog date [MINIMUM MAXIMUM] [--iso | --fmt FORMAT] [common-options]


Arguments and Options
---------------------

- :code:`MINIMUM` (optional):
    - the minimum value with the ISO-8601 format. If not specified, the behavior is left to the specification of `randdate <randog.factory.html#randog.factory.randdate>`_.

- :code:`MAXIMUM` (optional):
    - the maximum value with the ISO-8601 format. If not specified, the behavior is left to the specification of `randdate <randog.factory.html#randog.factory.randdate>`_.

- :code:`--iso` (optional):
    - if specified, it outputs generated object with ISO-8601 format.

- :code:`--fmt FORMAT` (optional):
    - if specified, it outputs generated object with the specified format; The format is specified in `the form of strftime or strptime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_.

- :code:`common-options`
    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs a date value.

.. code-block:: shell

    python -m randog date

You can specify a range of values to be generated, as in the following example:

.. code-block:: shell

    # generates a value between 2021-01-01 and 2021-01-31
    python -m randog date 2021-01-01 2021-01-31

By default, the output is in the standard python format, but you can change the output format to the format specified in `the form of strftime or strptime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_ or ISO-8601 by specifying options as follows:

.. code-block:: shell

    # generates a value with ISO-8601 format
    python -m randog date --iso

    # generates a value with the specified format
    python -m randog date --fmt '%Y/%m/%d'

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    python -m randog date -r 10

    # Generate list which contains 10 values
    python -m randog date -L 10 --json --iso

.. note::
    In date mode, time in a date is not generated simultaneously. If both is wanted, use :doc:`datetime mode <doc.as_command.datetime>`.
