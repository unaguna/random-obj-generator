datetime Mode
=============

In datetime mode, datetime values are generated. The format of the command is as follows:

.. code-block:: shell

    python -m randog datetime [MINIMUM MAXIMUM] [--iso | --fmt FORMAT] [common-options]


Arguments and Options
---------------------

- :code:`MINIMUM` (optional):
    - the minimum value; see also :ref:`here <datetime-min-max-expression>`. If not specified, the behavior is left to the specification of `randdatetime <randog.factory.html#randog.factory.randdatetime>`_.

- :code:`MAXIMUM` (optional):
    - the maximum value; see also :ref:`here <datetime-min-max-expression>`. If not specified, the behavior is left to the specification of `randdatetime <randog.factory.html#randog.factory.randdatetime>`_.

- :code:`--iso` (optional):
    - if specified, it outputs generated object with `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_.

- :code:`--fmt FORMAT` (optional):
    - if specified, it outputs generated object with the specified format; The format is specified in `the form of strftime or strptime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_.

- :code:`common-options`
    - :doc:`common options <doc.as_command.common_option>`


.. _datetime-min-max-expression:

Expression of MINIMUM and MAXIMUM
---------------------------------

You can specify the arguments :code:`MINIMUM` and :code:`MAXIMUM` with following expressions:

- :code:`now`: it means current datetime

- `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_, such as :code:`2022-01-01T00:00:00.000000`, :code:`2022-01-01T00:00:00`, or, :code:`2022-01-01`.

- datetime combined with :ref:`simple format of timedelta <timedelta-simple-format>`, such as :code:`now+2h`, or, :code:`2022-01-01-1h30m`.

- :ref:`simple format of timedelta <timedelta-simple-format>` (datetime term is omitted), such as :code:`+2h`:, or, :code:`-30m`

  - If the other (MAXIMUM or MINIMUM) is specified with datetime term, it means the other plus the timedelta.
  - If the other (MAXIMUM or MINIMUM) is fully omitted or datetime term of the other is omitted, it means :code:`now` plus the timedelta.

.. note::
    A simple expression such as :code:`-30m` can be used, but since it begins with :code:`-`, it is interpreted as an optional argument and will cause an error. To avoid this, it must be specified after :code:`--`, as in the following example.

    .. code-block:: shell

        # valid (example for usage with --repeat)
        python -m randog datetime --repeat 10 -- -30m +30m

        # invalid (unknown option -30m)
        python -m randog datetime --repeat 10 -30m +30m


Examples
--------

The simplest example is the following, which outputs a datetime value.

.. code-block:: shell

    python -m randog datetime

You can specify a range of values to be generated, as in the following example:

.. code-block:: shell

    # generates a value between 2021-01-01T00:00:00 and 2021-01-01T12:00:00
    python -m randog datetime 2021-01-01 2021-01-01T12:00:00

    # generates a value between yesterday and tomorrow
    python -m randog datetime -- -1d +1d

    # generates a value between 7 days ago and now
    python -m randog datetime -- -7d

    # generates a value between now and 1 hour later
    python -m randog datetime +1h

.. note::

    See :ref:`datetime-min-max-expression` for expressions such as :code:`+1d`.

By default, the output is in the standard python format, but you can change the output format to the format specified in `the form of strftime or strptime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_ or `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_ by specifying options as follows:

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
