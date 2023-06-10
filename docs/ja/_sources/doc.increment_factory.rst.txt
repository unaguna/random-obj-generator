Incremental integer factory
===========================

You can create a factory that generates incremental integers.

.. doctest::

    >>> import randog.factory
    >>> from randog.factory import DictItem

    >>> # create a factory
    >>> factory = randog.factory.increment()

    >>> generated = factory.next()
    >>> assert generated == 1
    >>> generated = factory.next()
    >>> assert generated == 2
    >>> generated = factory.next()
    >>> assert generated == 3


If you wish to specify an initial value and a maximum value, such as when generating data to be added to an existing database, you can do so as follows:

.. doctest::

    >>> import randog.factory
    >>> from randog.factory import DictItem

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
