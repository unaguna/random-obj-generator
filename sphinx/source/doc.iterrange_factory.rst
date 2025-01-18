Iteration of range
==================

You can create a factory that generates the values of the specified range.

.. doctest::

    >>> import randog.factory

    >>> # create a factory to generate 5, 6, 7
    >>> factory = randog.factory.iterrange(5, 7)

    >>> factory.next()
    5
    >>> factory.next()
    6
    >>> factory.next()
    7

If you do not specify a maximum value, it will generate values indefinitely.

.. doctest::

    >>> import randog.factory

    >>> # create a factory to generate 5, 6, 7, ...
    >>> factory = randog.factory.iterrange(5)

Step
----

You can specify an incremental value.

.. doctest::

    >>> import randog.factory

    >>> # create a factory to generate 5, 5+3, 5+3+3
    >>> factory = randog.factory.iterrange(5, 12, step=3)

    >>> factory.next()
    5
    >>> factory.next()
    8
    >>> factory.next()
    11

You can also specify a negative increment so that the generated value decreases.

.. doctest::

    >>> import randog.factory

    >>> # create a factory to generate 5, 5-1, 5-1-1
    >>> factory = randog.factory.iterrange(5, 3, step=-1)

    >>> factory.next()
    5
    >>> factory.next()
    4
    >>> factory.next()
    3

Cyclic
------

If you want the factory to return values cyclically without limit, you can do so as follows:

.. doctest::

    >>> import randog.factory

    >>> # create a factory to generate 5, 6, 7, 5, 6, 7, ...
    >>> factory = randog.factory.iterrange(5, 7, cyclic=True)

    >>> [factory.next() for i in range(10)]
    [5, 6, 7, 5, 6, 7, 5, 6, 7, 5]

You can also set the value returned when the cycle is complete to be different from the initial value.

.. doctest::

    >>> import randog.factory

    >>> # create a factory to generate 5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 7, ...
    >>> factory = randog.factory.iterrange(5, 7, cyclic=True, resume_from=4)

    >>> [factory.next() for i in range(10)]
    [5, 6, 7, 4, 5, 6, 7, 4, 5, 6]

Types of values
---------------

In addition to int values, datetime, date, and timedelta values can also be generated in the same way.

.. doctest::

    >>> import datetime as dt
    >>> import randog.factory

    >>> # create a factory to generate datetime values
    >>> factory = randog.factory.iterrange(dt.datetime(2020, 1, 1), dt.datetime(2020, 1, 2), step=dt.timedelta(hours=1))

    >>> factory.next()
    datetime.datetime(2020, 1, 1, 0, 0)
    >>> factory.next()
    datetime.datetime(2020, 1, 1, 1, 0)
    >>> factory.next()
    datetime.datetime(2020, 1, 1, 2, 0)
