timedelta Mode
==============

In timedelta mode, timedelta values are generated. The format of the command is as follows:

.. code-block:: shell

    python -m randog timedelta [MINIMUM MAXIMUM] [--unit UNIT] [--iso | --fmt FORMAT] [common-options]


Arguments and Options
---------------------

- :code:`MINIMUM` (optional):
    - the minimum value with the simple format; see also :ref:`here <simple-format>`. If not specified, the behavior is left to the specification of `randtimedelta <randog.factory.html#randog.factory.randtimedelta>`_.

- :code:`MAXIMUM` (optional):
    - the maximum value with the simple format; see also :ref:`here <simple-format>`. If not specified, the behavior is left to the specification of `randtimedelta <randog.factory.html#randog.factory.randtimedelta>`_.

- :code:`--unit UNIT` (optional):
    - the minimum unit of generated values with the simple format; see also :ref:`here <simple-format>`. If not specified, the behavior is left to the specification of `randtimedelta <randog.factory.html#randog.factory.randtimedelta>`_.

- :code:`--iso` (optional):
    - if specified, it outputs generated object with `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_.

- :code:`--fmt FORMAT` (optional):
    - if specified, it outputs generated object with the specified format; The format is specified in :ref:`the format codes <format-codes>`.

- :code:`common-options`
    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs a timedelta value.

.. code-block:: shell

    python -m randog timedelta

You can specify a range of values to be generated, as in the following example:

.. code-block:: shell

    # generates a value between 1 day and 7 day
    python -m randog timedelta 1d 7d

If the minimum unit is not specified, it will be adjusted to the appropriate length. In many cases, it may be necessary to specify this manually as follows

.. code-block:: shell

    # generates a value between 0 day and 1 day with minimum unit 1 second
    python -m randog timedelta 0d 1d --unit 1s

By default, the output is in :ref:`the simple format <simple-format>`, but you can change the output format to the format specified in :ref:`the format codes <format-codes>` or `ISO-8601 format <https://en.wikipedia.org/wiki/ISO_8601>`_ by specifying options as follows:

.. code-block:: shell

    # generates a value with ISO-8601 format
    python -m randog timedelta 0d 1d --unit 1s --iso

    # generates a value with the specified format　(x days xx:xx:xx)
    python -m randog timedelta 0d 7d --unit 1s --fmt '%D days %H:%M:%S'
    # generates a value with the specified format　(x:xx:xx)
    python -m randog timedelta 0d 7d --unit 1s --fmt '%tH:%M:%S'

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    python -m randog timedelta -r 10

    # Generate list which contains 10 values
    python -m randog timedelta -L 10 --json --iso


.. _simple-format:

Simple Format
-------------

In this mode, duration is represented in a proprietary format, such as :code:`1h30m` or :code:`1d2h3m4s5ms6us`.

This format expresses duration by concatenating one or more of the following elements:

.. list-table::
   :header-rows: 1

   * - Directive
     - Meaning

   * - :code:`Xd`
     - X is number of days. For example, :code:`2d` means "2 days"

   * - :code:`Xh`
     - X is number of hours. For example, :code:`2h` means "2 hours"

   * - :code:`Xm`
     - X is number of minutes. For example, :code:`2m` means "2 minutes"

   * - :code:`Xs`
     - X is number of seconds. For example, :code:`2s` means "2 seconds"

   * - :code:`Xms`
     - X is number of milliseconds. For example, :code:`2ms` means "2 milliseconds"

   * - :code:`Xus`
     - X is number of microseconds. For example, :code:`2us` means "2 microseconds"


.. note::

    It is not possible to specify by months or years.
    This is because python's timedelta does not manage units larger than days and cannot distinguish between a month and 30 days, for example.


.. _format-codes:

Format codes
------------

Python timedelta has no format codes defined, but in this mode, you can use proprietary format codes:

.. list-table::
   :header-rows: 1

   * - Directive
     - Meaning
     - Example

   * - :code:`%D`
     - equals to :code:`timedelta.days`
     - 0, 1, 2, ...

   * - :code:`%H`
     - hours part (zero-padded to 2 digits)
     - 00, 01, ..., 23

   * - :code:`%tH`
     - total duration in hours (rounded down)
     - 0, 1, 2, ...

   * - :code:`%M`
     - minutes part (zero-padded to 2 digits)
     - 00, 01, ..., 59

   * - :code:`%tM`
     - total duration in minutes (rounded down)
     - 0, 1, 2, ...

   * - :code:`%S`
     - seconds part (zero-padded to 2 digits)
     - 00, 01, ..., 59

   * - :code:`%tS`
     - total duration in seconds (rounded down)
     - 0, 1, 2, ...

   * - :code:`%f`
     - decimal part in seconds (zero-padded to 6 digits)
     - 000000, 000001, ..., 999999

Typically, the following formats are used:

- :code:`%D %H:%M:%S`
    - "140 hours" is represented as "5 20:00:00"
- :code:`%tH:%M:%S`
    - "140 hours" is represented as "140:00:00"


.. note::

    It is not possible to specify by months or years.
    This is because python's timedelta does not manage units larger than days and cannot distinguish between a month and 30 days, for example.
