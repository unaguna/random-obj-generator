Construct Factories (generator of random values)
================================================

In randog, factory is an object that generates values at random. The rules for generation are specified when the factory is created.

If you do not care about conditions other than type, you can create a factory by simply supplying an example value to `from_example <randog.factory.html#randog.factory.from_example>`_. If you want to specify the conditions in detail, create a factory using the factory constructor corresponding to the type.

.. doctest::

   >>> import randog.factory

   >>> # create a factory simply
   >>> factory_a = randog.factory.from_example("")
   >>> generated_a = factory_a.next()
   >>> assert isinstance(generated_a, str)

   >>> # create a factory with conditions in detail
   >>> factory_b = randog.factory.randstr(length=16)
   >>> generated_b = factory_b.next()
   >>> assert isinstance(generated_b, str)
   >>> assert len(generated_b) == 16


Elemental types
---------------

You can create a factory that generates values of the following types:

.. list-table::
   :header-rows: 1

   * - value type
     - factory constructor
     - argument for `from_example <randog.factory.html#randog.factory.from_example>`_

   * - :code:`NoneType`
     - | (There is no dedicated function,
       | but `const <randog.factory.html#randog.factory.const>`_ can be used instead.)
     - :code:`None`

   * - :code:`bool`
     - `randbool <randog.factory.html#randog.factory.randbool>`_
     - :code:`True` or :code:`False`

   * - :code:`int`
     - `randint <randog.factory.html#randog.factory.randint>`_
     - a integer value

   * - :code:`float`
     - `randfloat <randog.factory.html#randog.factory.randfloat>`_
     - a float value

   * - :code:`str`
     - `randstr <randog.factory.html#randog.factory.randstr>`_
     - a string value

   * - :code:`list`
     - `randlist <randog.factory.html#randog.factory.randlist>`_
     - a list

   * - :code:`tuple`
     - `randlist <randog.factory.html#randog.factory.randlist>`_ (argument :code:`type=tuple`)
     - a tuple

   * - :code:`dict`
     - `randdict <randog.factory.html#randog.factory.randdict>`_
     - a dict

   * - `decimal.Decimal <https://docs.python.org/3/library/decimal.html#decimal.Decimal>`_
     - `randdecimal <randog.factory.html#randog.factory.randdecimal>`_
     - a Decimal value

   * - `datetime.datetime <https://docs.python.org/3/library/datetime.html#datetime.datetime>`_
     - `randdatetime <randog.factory.html#randog.factory.randdatetime>`_
     - a datetime value



.. _nullable:

Nullable
--------

If you want None to be a candidate for generation, use `or_none <randog.factory.html#randog.factory.Factory.or_none>`_.

.. doctest::

   >>> import randog.factory

   >>> factory = randog.factory.from_example("")
   >>> factory_nullable = factory.or_none(0.1)

   >>> # a string
   >>> generated_a = factory.next()
   >>> # a string or None
   >>> generated_b = factory_nullable.next()

.. note::

   If you want to get a factory that always returns None, use :ref:`const <constance>` instead.


Union type
----------

Several methods can be used to determine randomly generated values from multiple types.

.. note::

   If you want to make it nullable, i.e., union type with None, use :ref:`or_none <nullable>` instead.

If you use `from_example <randog.factory.html#randog.factory.from_example>`_, you can use :code:`Example` as the argument. The following example uses :code:`-1`, :code:`""`, and :code:`True` as examples, so generated values will be integer, string, or boolean values.

.. doctest::

   >>> from randog import Example
   >>> import randog.factory

   >>> factory = randog.factory.from_example(Example(-1, "", True))

   >>> for _ in range(10):
   ...     generated = factory.next()
   ...     assert isinstance(generated, (int, str, bool))

If you create candidate factories, you can use `union <randog.factory.html#randog.factory.union>`_. The following example creates a factory, which chooses either randint or randbool each time randomly and returns the result of the chosen factory.

.. doctest::

   >>> import randog.factory

   >>> factory = randog.factory.union(
   ...     randog.factory.randint(0, 10),  # integer
   ...     randog.factory.randbool(),  # True or False
   ... )

   >>> for _ in range(10):
   ...     generated = factory.next()
   ...     assert isinstance(generated, (int, bool))


Randomly choice
---------------

If you want a factory to randomly return one of specific values, you can use `randchoice <randog.factory.html#randog.factory.randchoice>`_.

.. doctest::

   >>> import randog.factory

   >>> factory = randog.factory.randchoice("allow", "deny")

   >>> for _ in range(10):
   ...     generated = factory.next()
   ...     assert generated in ["allow", "deny"]


.. _constance:

Constance
---------

If you want a factory that always returns the same value, you can use `const <randog.factory.html#randog.factory.const>`_.

.. doctest::

   >>> import randog.factory

   >>> # same as `factory = randog.factory.randchoice("python")`
   >>> factory = randog.factory.const("python")

   >>> for _ in range(10):
   ...     generated = factory.next()
   ...     assert generated == "python"


Processing output
-----------------

The processing of factory output can be predefined. This can be used to change the type of output.

.. doctest::

   >>> import randog

   >>> # use post_process to format the random decimal value
   >>> factory = (
   ...     randog.factory.randdecimal(0, 50000, decimal_len=2)
   ...                   .post_process(lambda x: f"${x:,}")
   ... )

   >>> # examples: '$12,345.67', '$3,153.21', '$12.90', etc.
   >>> generated = factory.next()
   >>> assert isinstance(generated, str)
   >>> assert generated[0] == "$"
