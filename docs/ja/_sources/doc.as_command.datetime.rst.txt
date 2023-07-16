datetime Mode
=============

In datetime mode, datetime values are generated. The format of the command is as follows:

.. code-block:: shell

    python -m randog datetime [MINIMUM MAXIMUM] [--iso | --fmt FORMAT] [common-options]


Arguments and Options
---------------------

- :code:`MINIMUM` (optional):
    - the minimum value with the ISO-8601 format. If not specified, the behavior is left to the specification of `randdatetime <randog.factory.html#randog.factory.randdatetime>`_.

- :code:`MAXIMUM` (optional):
    - the maximum value with the ISO-8601 format. If not specified, the behavior is left to the specification of `randdatetime <randog.factory.html#randog.factory.randdatetime>`_.

- :code:`--iso` (optional):
    - if specified, it outputs generated object with ISO-8601 format.

- :code:`--fmt FORMAT` (optional):
    - if specified, it outputs generated object with the specified format; The format is specified in `the form of strftime or strptime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_.

- :code:`common-options`
    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs a datetime value.

.. code-block:: shell

    python -m randog datetime

You can specify a range of values to be generated, as in the following example:

.. code-block:: shell

    # generates a value between 2021-01-01T00:00:00 and 2021-01-01T12:00:00
    python -m randog datetime 2021-01-01 2021-01-01T12:00:00

By default, the output is in the standard python format, but you can change the output format to the format specified in `the form of strftime or strptime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_ or ISO-8601 by specifying options as follows:

.. code-block:: shell

    # generates a value with ISO-8601 format
    python -m randog datetime --iso

    # generates a value with the specified format
    python -m randog datetime --fmt '%Y/%m/%d %H:%M'

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    python -m randog datetime -r 10

    # Generate list which contains 10 values
    python -m randog datetime -L 10 --json --fmt '%Y/%m/%d %H:%M'

.. note::
    In datetime mode, date and time are generated simultaneously. If only one is wanted, use :doc:`date mode <doc.as_command.date>` or :doc:`time mode <doc.as_command.time>`.

    Also, if you want to generate an elapsed time rather than a time that points to a certain point in time, use :doc:`timedelta mode <doc.as_command.timedelta>`.
