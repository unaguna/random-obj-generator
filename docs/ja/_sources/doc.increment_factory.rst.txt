Incremental Factory
===================

You can create a factory that generates incremental integers, datetimes or dates.


Incremental Integer Factory
---------------------------

The most typical example is the use of generating integers, as in the following example:

.. doctest::

    >>> import randog.factory

    >>> # create a factory to generate integers
    >>> factory = randog.factory.increment()

    >>> factory.next()
    1
    >>> factory.next()
    2
    >>> factory.next()
    3

If you wish to specify an initial value and a maximum value, such as when generating data to be added to an existing database, you can do so as follows:

.. doctest::

    >>> import randog.factory

    >>> # create a factory (initial_value = 101, maximum value is 2^31-1)
    >>> factory = randog.factory.increment(101, 2**31-1)

    >>> generated = factory.next()
    >>> assert generated == 101
    >>> generated = factory.next()
    >>> assert generated == 102
    >>> generated = factory.next()
    >>> assert generated == 103

If a maximum value is specified, the next generated value for that value will be 1.
In the example above, the next value after 2^31-1 would be 1,
so the generated value is guaranteed to be a positive integer that fits into the signed 32-bit integer type.

.. note::

    Only one of the initial and maximum values may be specified.

Incremental Datetime/Date Factory
---------------------------------

If you specify a datetime or date value as the initial value, you can create a factory that will generate values of those types in sequence. You can specify the amount of increase for each generation by specifying the step as in the following example.

.. doctest::

    >>> import datetime as dt
    >>> import randog.factory

    >>> # create a factory to generate datetimes
    >>> factory = randog.factory.increment(
    ...     dt.datetime(2020, 10, 11, 12, 0, 0),
    ...     step=dt.timedelta(hours=1),
    ... )

    >>> print(factory.next())
    2020-10-11 12:00:00
    >>> print(factory.next())
    2020-10-11 13:00:00
    >>> print(factory.next())
    2020-10-11 14:00:00
