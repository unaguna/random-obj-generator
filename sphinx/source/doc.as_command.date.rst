date Mode
=========

In date mode, date values are generated. The format of the command is as follows:

.. code-block:: shell

    python -m randog date [MINIMUM MAXIMUM] [--iso | --fmt FORMAT] [common-options]


Arguments and Options
---------------------

- :code:`MINIMUM` (optional):

    - the minimum value; see also :ref:`here <date-min-max-expression>`. If not specified, the behavior is left to the specification of `randdate <randog.factory.html#randog.factory.randdate>`_.

- :code:`MAXIMUM` (optional):

    - the maximum value; see also :ref:`here <date-min-max-expression>`. If not specified, the behavior is left to the specification of `randdate <randog.factory.html#randog.factory.randdate>`_.

- :code:`--iso` (optional):

    - if specified, it outputs generated object with `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_.

- :code:`--fmt FORMAT` (optional):

    - if specified, it outputs generated object with the specified format; The format is specified in `the form of strftime or strptime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_.

- :code:`common-options`

    - :doc:`common options <doc.as_command.common_option>`


.. _date-min-max-expression:

Expression of MINIMUM and MAXIMUM
---------------------------------

You can specify the arguments :code:`MINIMUM` and :code:`MAXIMUM` with following expressions:

- :code:`today`: it means current date

- `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_, such as :code:`2022-01-01`.

- date combined with :ref:`simple format of timedelta <timedelta-simple-format>`, such as :code:`today+2d`, or, :code:`2022-01-01-1d`.

- :ref:`simple format of timedelta <timedelta-simple-format>` (date term is omitted), such as :code:`+2d`:, or, :code:`-7d`

  - If the other (MAXIMUM or MINIMUM) is specified with date term, it means the other plus the timedelta.
  - If the other (MAXIMUM or MINIMUM) is fully omitted or date term of the other is omitted, it means :code:`today` plus the timedelta.

.. note::
    A simple expression such as :code:`-7d` can be used, but since it begins with :code:`-`, it is interpreted as an optional argument and will cause an error. To avoid this, it must be specified after :code:`--`, as in the following example.

    .. code-block:: shell

        # valid (example for usage with --repeat)
        python -m randog date --repeat 10 -- -7d +7d

        # invalid (unknown option -30m)
        python -m randog date --repeat 10 -7d +7d


Examples
--------

The simplest example is the following, which outputs a date value.

.. code-block:: shell

    python -m randog date

You can specify a range of values to be generated, as in the following example:

.. code-block:: shell

    # generates a value between 2021-01-01 and 2021-01-31
    python -m randog date 2021-01-01 2021-01-31

    # generates a value between yesterday and tomorrow
    python -m randog date -- -1d +1d

    # generates a value between 7 days ago and today
    python -m randog date -- -7d

    # generates a value between today and 1 day later
    python -m randog date +1d

.. note::

    See :ref:`date-min-max-expression` for expressions such as :code:`+1d`.

Format: ISO-8601, etc.
~~~~~~~~~~~~~~~~~~~~~~

By default, the output is in the standard python format, but you can change the output format to the format specified in `the form of strftime or strptime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_ or `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_ by specifying options as follows:

.. code-block:: shell

    # generates a value with ISO-8601 format
    python -m randog date --iso

    # generates a value with the specified format
    python -m randog date --fmt '%Y/%m/%d'

Repeatedly Generate
~~~~~~~~~~~~~~~~~~~

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    python -m randog date -r 10

    # Generate list which contains 10 values
    python -m randog date -L 10 --json --iso

.. note::
    In date mode, time in a date is not generated simultaneously. If both is wanted, use :doc:`datetime mode <doc.as_command.datetime>`.
