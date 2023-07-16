time Mode
=========

In time mode, time values are generated. The format of the command is as follows:

.. code-block:: shell

    python -m randog time [MINIMUM MAXIMUM] [--iso | --fmt FORMAT] [common-options]


Arguments and Options
---------------------

- :code:`MINIMUM` (optional):
    - the minimum value with the `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_. If not specified, the behavior is left to the specification of `randtime <randog.factory.html#randog.factory.randtime>`_.

- :code:`MAXIMUM` (optional):
    - the maximum value with the `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_. If not specified, the behavior is left to the specification of `randtime <randog.factory.html#randog.factory.randtime>`_.

- :code:`--iso` (optional):
    - if specified, it outputs generated object with `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_.

- :code:`--fmt FORMAT` (optional):
    - if specified, it outputs generated object with the specified format; The format is specified in `the form of strftime or strptime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_.

- :code:`common-options`
    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs a time value.

.. code-block:: shell

    python -m randog time

You can specify a range of values to be generated, as in the following example:

.. code-block:: shell

    # generates a value between 00:00:00 and 12:00:00
    python -m randog time 00:00:00 12:00:00

By default, the output is in the standard python format, but you can change the output format to the format specified in `the form of strftime or strptime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_ or `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_ by specifying options as follows:

.. code-block:: shell

    # generates a value with ISO-8601 format
    python -m randog time --iso

    # generates a value with the specified format
    python -m randog time --fmt '%H:%M'

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    python -m randog time -r 10

    # Generate list which contains 10 values
    python -m randog time -L 10 --json --iso

.. note::
    In time mode, date is not generated simultaneously. If both is wanted, use :doc:`datetime mode <doc.as_command.datetime>`.

    Also, if you want to generate an elapsed time rather than a time that points to a certain point in time, use :doc:`timedelta mode <doc.as_command.timedelta>`.
