List factory
============

You can create a factory that generates :code:`list` (or :code:`tuple`). The elements of the list are always randomly generated each time.

In many cases, the factory is created with `randlist <randog.factory.html#randog.factory.randlist>`_ instead of `from_example <randog.factory.html#randog.factory.from_example>`_ because the generation of the list needs to be tailored to the application.

.. doctest::

    >>> import randog.factory

    >>> factory = randog.factory.randlist(
    ...     randog.factory.randint(0, 100),
    ...     randog.factory.randstr(),
    ... )

    >>> generated = factory.next()
    >>> assert isinstance(generated, list)
    >>> assert isinstance(generated[0], int)
    >>> assert isinstance(generated[1], str)

.. note::

    If you want to generate multiple records by a single factory, it may be appropriate to use :code:`iter` rather than :code:`randlist`.

    .. doctest::

        >>> import randog.factory

        >>> factory = randog.factory.randdict(
        ...     id=randog.factory.randint(0, 999_999),
        ...     price=randog.factory.randdecimal(0, 1000, decimal_len=2),
        ... )

        >>> # generate 200 records
        >>> record_list = list(factory.iter(200))

    The same can be done for :doc:`command execution <doc.as_command>` by using :code:`--list` or :code:`--repeat` option.


Each elements
-------------
You can specify a factory for each element. Normally, the i-th factory is used to generate the i-th element, but if you are generating a list longer than the number of factories, repeat the last factory.

.. doctest::

    >>> import randog.factory

    >>> el_factories = [
    ...     randog.factory.randint(0, 100),
    ...     randog.factory.randstr(),
    ...     randog.factory.randbool(),
    ... ]
    >>> factory = randog.factory.randlist(
    ...     *el_factories,
    ...     length=4,
    ... )

    >>> generated = factory.next()
    >>> assert isinstance(generated, list)
    >>> assert len(generated) == 4
    >>> assert isinstance(generated[0], int)    # by el_factories[0]
    >>> assert isinstance(generated[1], str)    # by el_factories[1]
    >>> assert isinstance(generated[2], bool)   # by el_factories[2]
    >>> assert isinstance(generated[3], bool)   # by el_factories[2]

Therefore, if you want to generate a typical list where each element has no specific meaning, specify only one element factory.

.. doctest::

    >>> import randog.factory

    >>> factory = randog.factory.randlist(
    ...     randog.factory.randint(0, 100),
    ...     length=4,
    ... )

    >>> generated = factory.next()
    >>> assert isinstance(generated, list)
    >>> assert len(generated) == 4
    >>> for el in generated:
    ...     assert isinstance(el, int)


Length
------

The length of the list can also be randomized.

.. doctest::

    >>> import randog.factory

    >>> factory = randog.factory.randlist(
    ...     randog.factory.randint(0, 100),
    ...     length=randog.factory.randint(3, 5),
    ... )

    >>> # Repeat generation to make sure length is at random
    >>> lengths = set(map(len, factory.iter(1000)))
    >>> assert lengths == {3, 4, 5}

If no length is specified, the length will be the same as the number of pieces in the factory.

.. doctest::

    >>> import randog.factory

    >>> el_factories = [
    ...     randog.factory.randint(0, 100),
    ...     randog.factory.randstr(),
    ...     randog.factory.randbool(),
    ... ]
    >>> factory = randog.factory.randlist(
    ...     *el_factories,
    ... )

    >>> generated = factory.next()
    >>> assert isinstance(generated, list)
    >>> assert len(generated) == len(el_factories)


Generate tuple
--------------

The attribute :code:`type` can be used to generate a tuple instead of a list.

.. doctest::

    >>> import randog.factory

    >>> factory = randog.factory.randlist(
    ...     randog.factory.randint(0, 100),
    ...     randog.factory.randstr(),
    ...     type=tuple,
    ... )

    >>> generated = factory.next()
    >>> assert isinstance(generated, tuple)

.. note::
    The length attribute is not necessary when generating a typical tuple in which each element has a separate schema, since omitting length will generate tuples with a length equal to the number of factories.

.. warning::
    Other types that accept iterators can be specified as :code:`type`, but if :code:`set` is used, the number of elements is not guaranteed.


Factory by :code:`from_example`
-------------------------------

If you use `from_example <randog.factory.html#randog.factory.from_example>`_, for example, the code would look like this:

.. doctest::

    >>> import randog.factory

    >>> factory = randog.factory.from_example([1, "a"])

    >>> generated = factory.next()
    >>> assert isinstance(generated, list)
    >>> assert isinstance(generated[0], int)
    >>> assert isinstance(generated[1], str)

Each element of the list given as an example is used as an example for each element of the generated list.
