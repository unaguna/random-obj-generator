time Mode
=========

In time mode, time values are generated. The format of the command is as follows:

.. code-block:: shell

    randog time [MINIMUM MAXIMUM] [--iso | --fmt FORMAT] [common-options]


Arguments and Options
---------------------

- :code:`MINIMUM` (optional):

    - the minimum value; see also :ref:`here <time-min-max-expression>`. If not specified, the behavior is left to the specification of `randtime <randog.factory.html#randog.factory.randtime>`_.

- :code:`MAXIMUM` (optional):

    - the maximum value; see also :ref:`here <time-min-max-expression>`. If not specified, the behavior is left to the specification of `randtime <randog.factory.html#randog.factory.randtime>`_.

- :code:`--iso` (optional):

    - if specified, it outputs generated object with `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_.

- :code:`--fmt FORMAT` (optional):

    - if specified, it outputs generated object with the specified format; The format is specified in `the form of strftime or strptime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_.

- :code:`common-options`

    - :doc:`common options <doc.as_command.common_option>`


.. _time-min-max-expression:

Expression of MINIMUM and MAXIMUM
---------------------------------

You can specify the arguments :code:`MINIMUM` and :code:`MAXIMUM` with following expressions:

- :code:`now`: it means current time

- `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_, such as :code:`11:22:33.000000`, or, :code:`11:22:33`.

- time combined with :ref:`simple format of timedelta <timedelta-simple-format>`, such as :code:`now+2h`, or, :code:`01:00:00-1h30m`.

- :ref:`simple format of timedelta <timedelta-simple-format>` (time term is omitted), such as :code:`+2h`:, or, :code:`-30m`

  - If the other (MAXIMUM or MINIMUM) is specified with time term, it means the other plus the timedelta.
  - If the other (MAXIMUM or MINIMUM) is fully omitted or time term of the other is omitted, it means :code:`now` plus the timedelta.

.. note::
    A simple expression such as :code:`-30m` can be used, but since it begins with :code:`-`, it is interpreted as an optional argument and will cause an error. To avoid this, it must be specified after :code:`--`, as in the following example.

    .. code-block:: shell

        # valid (example for usage with --repeat)
        randog time --repeat 10 -- -30m +30m

        # invalid (unknown option -30m)
        randog time --repeat 10 -30m +30m


Examples
--------

The simplest example is the following, which outputs a time value.

.. code-block:: shell

    randog time

You can specify a range of values to be generated, as in the following example:

.. code-block:: shell

    # generates a value between 00:00:00 and 12:00:00
    randog time 00:00:00 12:00:00

    # generates a value between 1 hour ago and 1 hour later
    randog time -- -1h +1h

    # generates a value between 12 hours ago and now
    randog time -- -12h

    # generates a value between now and 30 minutes later
    randog time +30m

.. note::

    See :ref:`time-min-max-expression` for expressions such as :code:`+1h`.

Format: ISO-8601, etc.
~~~~~~~~~~~~~~~~~~~~~~

By default, the output is in the standard python format, but you can change the output format to the format specified in `the form of strftime or strptime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_ or `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_ by specifying options as follows:

.. code-block:: shell

    # generates a value with ISO-8601 format
    randog time --iso

    # generates a value with the specified format
    randog time --fmt '%H:%M'

Repeatedly Generate
~~~~~~~~~~~~~~~~~~~

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    randog time -r 10

    # Generate list which contains 10 values
    randog time -L 10 --json --iso

.. note::
    In time mode, date is not generated simultaneously. If both is wanted, use :doc:`datetime mode <doc.as_command.datetime>`.

    Also, if you want to generate an elapsed time rather than a time that points to a certain point in time, use :doc:`timedelta mode <doc.as_command.timedelta>`.
