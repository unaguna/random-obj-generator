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
     - detail

   * - :code:`NoneType`
     - | (There is no dedicated function,
       | but `const <randog.factory.html#randog.factory.const>`_ can be used instead.)
     - :code:`None`
     -

   * - :code:`bool`
     - `randbool <randog.factory.html#randog.factory.randbool>`_
     - :code:`True` or :code:`False`
     -

   * - :code:`int`
     - `randint <randog.factory.html#randog.factory.randint>`_
     - a integer value
     -

   * - :code:`float`
     - `randfloat <randog.factory.html#randog.factory.randfloat>`_
     - a float value
     -

   * - :code:`str`
     - `randstr <randog.factory.html#randog.factory.randstr>`_
     - a string value
     - :doc:`detail <doc.str_factory>`

   * - :code:`list`
     - `randlist <randog.factory.html#randog.factory.randlist>`_
     - a list
     - :doc:`detail <doc.list_factory>`

   * - :code:`tuple`
     - `randlist <randog.factory.html#randog.factory.randlist>`_ (argument :code:`type=tuple`)
     - a tuple
     - :doc:`detail <doc.list_factory>`

   * - :code:`dict`
     - `randdict <randog.factory.html#randog.factory.randdict>`_
     - a dict
     - :doc:`detail <doc.dict_factory>`

   * - `decimal.Decimal <https://docs.python.org/3/library/decimal.html#decimal.Decimal>`_
     - `randdecimal <randog.factory.html#randog.factory.randdecimal>`_
     - a Decimal value
     -

   * - `datetime.datetime <https://docs.python.org/3/library/datetime.html#datetime.datetime>`_
     - `randdatetime <randog.factory.html#randog.factory.randdatetime>`_
     - a datetime value
     -

   * - `datetime.date <https://docs.python.org/3/library/datetime.html#datetime.date>`_
     - `randdate <randog.factory.html#randog.factory.randdate>`_
     - a date value
     -

   * - `datetime.time <https://docs.python.org/3/library/datetime.html#datetime.time>`_
     - `randtime <randog.factory.html#randog.factory.randtime>`_
     - a time value
     -

   * - `datetime.timedelta <https://docs.python.org/3/library/datetime.html#datetime.timedelta>`_
     - `randtimedelta <randog.factory.html#randog.factory.randtimedelta>`_
     - a timedelta value
     -


   * - An `enumeration <https://docs.python.org/3/library/enum.html>`_
     - `randenum <randog.factory.html#randog.factory.randenum>`_
     - a value of the enumeration
     - :doc:`detail <doc.enum_factory>`


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

.. note::
    Normally, when an or_null factory generates a value, it first randomly determines whether to return None or generate a value and return it, and then generates a value only if it is returned.
    However, if the argument is specified as in :code:`or_none(..., lazy_choice=True)`, then when the union factory generates the value, it first generates the value using the factory and then randomly decides whether to adopt it or None.

    This difference affects, for example, the use of non-random factories.


.. _construct_union:

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


.. note::
    Normally, when a union factory generates a value, it first randomly determines which factory to use, and only that factory generates the value.
    However, if the argument is specified as in :code:`union(..., lazy_choice=True)`, then when the union factory generates the value, it first generates the values using all the factories and then randomly decides which of them to use.

    This difference affects, for example, the use of non-random factories.



Randomly choice
---------------

If you want a factory to randomly return one of specific values, you can use `randchoice <randog.factory.html#randog.factory.randchoice>`_.

.. doctest::

   >>> import randog.factory

   >>> factory = randog.factory.randchoice("allow", "deny")

   >>> for _ in range(10):
   ...     generated = factory.next()
   ...     assert generated in ["allow", "deny"]


.. note::

    If you want to randomly generate values of a particular enumeration type, you can also use `randenum <randog.factory.html#randog.factory.randenum>`_. See also: :doc:`doc.enum_factory`


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


If the value to be generated is a dict and you want to process the items, you can easily code it by using :code:`post_process_items` instead of :code:`post_process`, as in the following example.

.. doctest::

    >>> import randog

    >>> # use post_process_items to format the random decimal value '["count"]'
    >>> factory = (
    ...     randog.factory.randdict(
    ...         name=randog.factory.randstr(),
    ...         count=randog.factory.randdecimal(0, 50000, decimal_len=2),
    ...     ).post_process_items(count=lambda x: f"${x:,}")
    ... )

    >>> # examples: {'name': 'sir1w94s', 'count': '$12,345.67'}, etc.
    >>> generated = factory.next()
    >>> assert isinstance(generated["count"], str)
    >>> assert generated["count"][0] == "$"

.. note::
    If a non-dict value is generated, conversion by :code:`post_process_items` is skipped, so it can be used in combination with :ref:`or_none <nullable>` and :ref:`union <construct_union>`.


.. _custom_factory:

Custom Factory
--------------

Values of type not provided by randog can also be generated in the context of randog by using functions, iterators (include `generator iterators <https://docs.python.org/3/glossary.html#term-generator-iterator>`_), or custom factories. Normally, you would think that you could just use that function or iterator directly, but this method is needed to generate elements when generating dict or list in randog.

.. doctest::

   >>> import itertools
   >>> import random
   >>> import uuid
   >>> import randog.factory

   >>> # define custom factory
   >>> class MailAddressFactory(randog.factory.Factory[str]):
   ...     def _next(self):
   ...         return random.randint(1, 10) * "a" + "@example.com"

   >>> factory = randog.factory.from_example({
   ...     # use iterator (https://docs.python.org/3/library/itertools.html#itertools.count)
   ...     "id": itertools.count(1),
   ...     # use function
   ...     "uuid": uuid.uuid4,
   ...     # use function
   ...     "name": lambda: random.randint(1, 10) * "a",
   ...     # use custom factory
   ...     "mail": MailAddressFactory(),
   ... })
   >>> generated = factory.next()

   >>> assert isinstance(generated, dict)
   >>> assert generated["id"] == 1
   >>> assert isinstance(generated["uuid"], uuid.UUID)
   >>> assert isinstance(generated["name"], str)
   >>> assert set(generated["name"]) == {"a"}
   >>> assert isinstance(generated["mail"], str)
   >>> assert generated["mail"].endswith("@example.com")

.. note::
    You can also create a factory using the factory constructor: `by_callable <randog.factory.html#randog.factory.by_callable>`_, `by_iterator <randog.factory.html#randog.factory.by_iterator>`_

.. warning::
    A finite iterator can be used as an example, but once the iterator terminates, the factory cannot generate any more values.


Details on how to build individual factories
--------------------------------------------

.. toctree::
   :maxdepth: 1

   doc.dict_factory
   doc.list_factory
   doc.str_factory
   doc.enum_factory


.. _special_factory:

Special Factory
---------------

Although any factory can be created with the :ref:`custom factory <custom_factory>`, some of the most commonly used factories are provided by randog.

.. toctree::
   :maxdepth: 1

   doc.increment_factory
   doc.iterrange_factory
   doc.sqlalchemy
