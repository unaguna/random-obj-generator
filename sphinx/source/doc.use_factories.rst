Use Factories
=============

Once a factory is created, its `next <randog.factory.html#randog.factory.Factory.next>`_ method can be used to generate random values. Generate a value for each use.

.. doctest::

    >>> import randog.factory

    >>> # create a factory
    >>> factory = randog.factory.randstr(length=128)

    >>> generated1 = factory.next()
    >>> assert isinstance(generated1, str)

    >>> generated2 = factory.next()
    >>> # Note: There is a low probability that they may be identical.
    >>> assert generated1 != generated2

Usually used in this way, the following sugar-coated syntax can also be used.


As iterator
-----------

Although a factory itself is not an iterator, `iter <randog.factory.html#randog.factory.Factory.iter>`_ method can be used to create an iterator.

.. doctest::

    >>> import randog.factory

    >>> factory = randog.factory.randstr(length=10)

    >>> cnt = 0
    >>> for generated in factory.iter(10):
    ...     cnt += 1
    ...     assert isinstance(generated, str)
    >>> assert cnt == 10

    >>> generated_values = list(factory.iter(5))
    >>> assert isinstance(generated_values, list)
    >>> assert len(generated_values) == 5

.. note::
    The return value of :code:`iter` is not just an Iterable, but also an Iterator. Iterators are disposable and must be regenerated each time they are used.

`infinity_iter <randog.factory.html#randog.factory.Factory.infinity_iter>`_ also returns an iterator, but this iterator will be not terminated.

.. doctest::

    >>> import randog.factory

    >>> factory = randog.factory.randstr(length=10)

    >>> keys = ["foo", "bar"]
    >>> for k, v in zip(keys, factory.infinity_iter()):
    ...     assert k in keys
    ...     assert isinstance(v, str)

    >>> # WARN: Running the code below will continue to generate values indefinitely
    >>> # list(factory.infinity_iter())

.. warning::
    :code:`infinity_iter` causes an infinite loop. Handle it with care.

.. note::
    The return value of :code:`infinity_iter` is not just an Iterable, but also an Iterator. Iterators are disposable and must be regenerated each time they are used.
