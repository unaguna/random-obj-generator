Dict factory
============

You can create a factory that generates :code:`dict`. The elements of the dict are always randomly generated each time.

Like any other factory, a dict factory can be built in two ways: `randdict <randog.factory.html#randog.factory.randdict>`_, `from_example <randog.factory.html#randog.factory.from_example>`_.


Factory by :code:`randdict`
---------------------------

If you use `randdict <randog.factory.html#randog.factory.randdict>`_, for example, the code would look like this:

.. doctest::

    >>> import randog.factory
    >>> from randog.factory import DictItem

    >>> # create a factory
    >>> factory = randog.factory.randdict(
    ...     name=randog.factory.randstr(length=16),
    ...     sex=randog.factory.randchoice("F", "M"),
    ...     age=DictItem(  # by DictItem, key existence is also at random.
    ...         randog.factory.randint(0, 100),
    ...         0.9,
    ...     ),
    ... )

    >>> generated = factory.next()
    >>> assert isinstance(generated, dict)
    >>> assert isinstance(generated["name"], str)
    >>> assert generated["sex"] in ["F", "M"]
    >>> assert "age" not in generated or isinstance(generated["age"], int)

As in this example, by passing value factories as keyword arguments to :code:`randdict`, you can create a dict factory that randomly generates each element. By passing a `DictItem <randog.factory.html#randog.factory.DictItem>`_ as an argument instead of a factory, it is also possible to randomize whether the key is generated in the generated dictionary; like :code:`age` in the example above.

.. note::

    See also :doc:`here <doc.construct_factories>` for how to build each factory.


Factory by :code:`from_example`
-------------------------------

If you use `from_example <randog.factory.html#randog.factory.from_example>`_, for example, the code would look like this:

.. doctest::

    >>> import randog.factory
    >>> from randog import DictItemExample

    >>> # create a factory
    >>> factory = randog.factory.from_example({
    ...     "name": "Smith",
    ...     "sex": randog.factory.randchoice("F", "M"),
    ...     "age": DictItemExample(22, 0.9)
    ... })

    >>> generated = factory.next()
    >>> assert isinstance(generated, dict)
    >>> assert isinstance(generated["name"], str)
    >>> assert generated["sex"] in ["F", "M"]
    >>> assert "age" not in generated or isinstance(generated["age"], int)

Not limited to dictionaries, :code:`from_example` is a function that, given an object that is an example output, returns a factory that generates an object similar to that example. If a dict is given to :code:`from_example`, each of its values can be either an example value or a factory that generates values. Or, if you pass an example wrapped in `DictItemExample <randog.html#randog.DictItemExample>`_, you can also randomize whether or not a key is generated; like :code:`age` in the example above.
