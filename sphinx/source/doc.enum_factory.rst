Enum factory
============

You can create a factory that generates a value of the enumeration type.

Like any other factory, an enum factory can be built in two ways: `randenum <randog.factory.html#randog.factory.randenum>`_, `from_example <randog.factory.html#randog.factory.from_example>`_.


Factory by :code:`randenum`
---------------------------

If you use `randenum <randog.factory.html#randog.factory.randenum>`_, for example, the code would look like this:

.. doctest::

    >>> import enum
    >>> import randog.factory
    >>> from randog.factory import DictItem

    >>> class MyEnum(enum.Enum):
    ...     one = 1
    ...     two = 2

    >>> # create a factory
    >>> factory = randog.factory.randenum(MyEnum)

    >>> generated = factory.next()
    >>> assert generated in MyEnum


.. note::

    The same can be done with `randchoice <randog.factory.html#randog.factory.randchoice>`_: :code:`randog.factory.randchoice(*MyEnum)`


By default, each value is generated with the same probability, but the probability can be biased by specifying the argument :code:`weights`.

.. doctest::

    >>> import enum
    >>> import randog.factory
    >>> from randog.factory import DictItem

    >>> class MyEnum(enum.Enum):
    ...     one = 1
    ...     two = 2

    >>> # a function which returns the probabilities of each value
    >>> def weights(value):
    ...     if value == MyEnum.one:
    ...         return 0.8
    ...     elif value == MyEnum.two:
    ...         return 0.2

    >>> # create a factory
    >>> factory = randog.factory.randenum(MyEnum, weights=weights)

    >>> generated = factory.next()
    >>> assert generated in MyEnum


Factory by :code:`from_example`
-------------------------------

If you use `from_example <randog.factory.html#randog.factory.from_example>`_, for example, the code would look like this:

.. doctest::

    >>> import enum
    >>> import randog.factory
    >>> from randog import DictItemExample

    >>> class MyEnum(enum.Enum):
    ...     one = 1
    ...     two = 2

    >>> # create a factory
    >>> factory = randog.factory.from_example(MyEnum.one)

    >>> generated = factory.next()
    >>> assert generated in MyEnum
