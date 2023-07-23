Str factory
===========

You can create a factory that generates string values with `randstr <randog.factory.html#randog.factory.randstr>`_.

.. note::
    Although a factory of str can be created by passing a string as an example to `from_example <randog.factory.html#randog.factory.from_example>`_, it is not possible to specify the creation condition.


Simple factory
--------------

If all that is needed is for the generated value to be a string, use `randstr <randog.factory.html#randog.factory.randstr>`_ with no arguments as follows:

.. doctest::

    >>> import randog.factory

    >>> # create a factory
    >>> factory = randog.factory.randstr()

    >>> generated = factory.next()
    >>> assert isinstance(generated, str)


Specify the length or/and character set
---------------------------------------

The arguments :code:`length` and :code:`charset` can be used to specify the length of the generated string and the character set to be used.

.. doctest::

    >>> import string
    >>> import randog.factory

    >>> # create a factory
    >>> factory = randog.factory.randstr(length=8, charset=string.ascii_uppercase)

    >>> generated = factory.next()
    >>> assert isinstance(generated, str)
    >>> assert len(generated) == 8
    >>> assert set(generated) <= set(string.ascii_uppercase)

The length of the string can also be randomized by specifying `randint() <randog.factory.html#randog.factory.randint>`_ for :code:`length` as follows:

.. doctest::

    >>> import string
    >>> import randog.factory

    >>> # create a factory
    >>> factory = randog.factory.randstr(length=randog.factory.randint(10, 19))

    >>> generated = factory.next()
    >>> assert isinstance(generated, str)
    >>> assert 10 <= len(generated) <= 19

The argument :code:`charset` is a string consisting of the characters to be used. Usually a constant from `string <https://docs.python.org/3/library/string.html>`_ module, but you can also specify your own string as follows:

.. doctest::

    >>> import string
    >>> import randog.factory

    >>> # create a factory
    >>> factory = randog.factory.randstr(charset="AZ")

    >>> generated = factory.next()
    >>> assert isinstance(generated, str)
    >>> assert set(generated) <= {"A", "Z"}


Specify a regular expression
----------------------------

A regular expression can be used to specify the string to be generated.

.. doctest::

    >>> import re
    >>> import randog.factory

    >>> # create a factory
    >>> factory = randog.factory.randstr(regex=r"\d{3}-\d{4}-\d{4}")

    >>> generated = factory.next()
    >>> assert isinstance(generated, str)
    >>> assert re.fullmatch(r"\d{3}-\d{4}-\d{4}", generated)

.. warning::
    When using the argument :code:`regex`, the arguments :code:`length` and :code:`charset` cannot be used.

.. note::
    To generate strings using regular expressions, use the `rstr <https://pypi.org/project/rstr/>`_ package, which must be installed beforehand, e.g., by :code:`pip install rstr`.

.. warning::
    To generate strings using regular expressions, use the `rstr <https://pypi.org/project/rstr/>`_ package.
    If you use it, please review and follow the license terms of rstr.

