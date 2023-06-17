Factory from sqlalchemy
=======================

You can create a factory that generates instances of SQLAlchemy Model. The elements of the Model instance are always randomly generated each time.

Like any other factory, a model factory can be built in two ways: `randog.sqlalchemy.factory <randog.sqlalchemy.html#randog.sqlalchemy.factory>`_, `from_example <randog.factory.html#randog.factory.from_example>`_.

.. warning::
    This is an experimental feature. It may be removed or significantly changed in the future.

.. warning::
    This is an experimental feature. Various :ref:`limitations <limitations>` apply.

.. note::
    The following examples use the model of sqlalchemy 1.4, but also supports the 2.0 using :code:`mapped_column`.


Factory by :code:`randog.sqlalchemy.factory`
--------------------------------------------

If you use `randog.sqlalchemy.factory <randog.sqlalchemy.html#randog.sqlalchemy.factory>`_, for example, the code would look like this:

.. doctest::

    >>> from sqlalchemy import Column, Integer, String
    >>> from sqlalchemy.orm import declarative_base
    >>> import randog.factory
    >>> import randog.sqlalchemy

    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "user"
    ...
    ...     id = Column(Integer, primary_key=True, autoincrement=True)
    ...     type = Column(String(4), nullable=False)
    ...     name = Column(String)
    ...     age = Column(Integer)

    >>> # create a factory
    >>> factory = randog.sqlalchemy.factory(
    ...     User,
    ...     {"age": randog.factory.randint(20, 60)},
    ... )

    >>> generated = factory.next()

    >>> assert isinstance(generated, User)

    >>> # [id] incremental integer
    >>> assert generated.id == 1

    >>> # [type] string of length at least 4
    >>> assert isinstance(generated.type, str)
    >>> assert len(generated.type) == 4

    >>> # [name] string (nullable)
    >>> assert isinstance(generated.name, str) or generated.name is None

    >>> # [age] int (overridden)
    >>> assert isinstance(generated.age, int) and 20 <= generated.age <= 60

As in this example, by passing a model class of SQLAlchemy to :code:`randog.sqlalchemy.factory`, you can create a model instance factory that randomly generates each field. By passing fields' factories as second argument, this factories are used instead of factories created from Column objects of the model; like :code:`age` in the example above.

.. note::

    See also :doc:`here <doc.construct_factories>` for how to build each factory of fields.

Factory by :code:`from_example`
-------------------------------
If you use `from_example <randog.factory.html#randog.factory.from_example>`_, for example, the code would look like this:

.. doctest::

    >>> from sqlalchemy import Column, Integer, String
    >>> from sqlalchemy.orm import declarative_base
    >>> import randog.factory
    >>> import randog.sqlalchemy

    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "user"
    ...
    ...     id = Column(Integer, primary_key=True, autoincrement=True)
    ...     type = Column(String(4), nullable=False)
    ...     name = Column(String)

    >>> # specify `randog.sqlalchemy.custom` as `custom_func`
    >>> factory = randog.factory.from_example(User, custom_func=randog.sqlalchemy.custom)
    >>> generated = factory.next()

    >>> assert isinstance(generated, User)

    >>> # [id] incremental integer
    >>> assert generated.id == 1

    >>> # [type] string of length at least 4
    >>> assert isinstance(generated.type, str)
    >>> assert len(generated.type) == 4

    >>> # [name] string (nullable)
    >>> assert isinstance(generated.name, str) or generated.name is None

.. note::
    In this example, the model class is given to :code:`from_example`,
    but it works the same way if a model instance is given.

Supported column type
---------------------

The following types of columns are supported

- Integer, BigInteger
- Numeric
- Float
- String, Text
- Boolean
- Date
- DateTime, TIMESTAMP
- Time
- Interval

.. _limitations:

Limitations
-----------

randog does not support all of sqlalchemy and RDB features. In particular, please note the following:

- A factory CANNOT be generated if the model contains a relationship.

- Foreign key constraints are ignored.

- Even with unique constraints (includes primary key constraint), they are ignored, so fields may be duplicated when values are generated repeatedly. The probability of duplication is known to be greater than intuition (`birthday problem <https://en.wikipedia.org/wiki/Birthday_problem>`_).

- Check constraints are ignored.

.. note::
    If the constraints are known in advance, it may be possible to satisfy the constraint by specifying the factory of the field. See also: :ref:`override_columns`



.. _override_columns:

Specify factories for individual fields
---------------------------------------

The factory that generates each field is automatically created from the column definitions in the model class, but some or all of it can be specified manually. For example:

.. doctest::

    >>> from sqlalchemy import Column, Integer, String
    >>> from sqlalchemy.orm import declarative_base
    >>> import randog.factory
    >>> import randog.sqlalchemy

    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "user"
    ...
    ...     id = Column(Integer, primary_key=True)
    ...     type = Column(String(10), nullable=False)
    ...     name = Column(String)
    ...     group_id = Column(Integer)

    >>> factory = randog.sqlalchemy.factory(
    ...     User,
    ...     {
    ...         # Example of manually responding to check constraints
    ...         "type": randog.factory.randchoice("regular", "manager"),
    ...         # Example of manually responding to foreign key constraints
    ...         "group_id": randog.factory.randint(1, 3)
    ...     },
    ... )

    >>> generated = factory.next()

    >>> assert isinstance(generated, User)
    >>> assert isinstance(generated.id, int)
    >>> assert isinstance(generated.name, str) or generated.name is None
    >>> assert generated.type in ("regular", "manager")
    >>> assert generated.group_id in (1, 2, 3)

In the above example, factories that generate :code:`type` and :code:`group_id` are specified in order to generate records that satisfy foreign key constraints and check constraints specified in the actual database. :code:`id` and :code:`name`, whose factories are not specified, are generated by the factories created from the column definitions as default.


Generate a dict instance
------------------------

.. warning::
    Reiteration: This is an experimental feature. It may be removed or significantly changed in the future. Various :ref:`limitations <limitations>` apply.

As in the previous examples, a model instance is generated by default, but you can generate a dict object for each case of using :code:`randog.sqlalchemy.factory` and :code:`from_example`, respectively.

.. note::
    If you simply want to generate dict objects independent of model classes, use :doc:`randdict <doc.dict_factory>`.

When using :code:`randog.sqlalchemy.factory`, a factory that generates a dict object can be created by specifying :code:`as_dict=True` as an argument. For example:

.. doctest::

    >>> from sqlalchemy import Column, Integer, String
    >>> from sqlalchemy.orm import declarative_base
    >>> import randog.factory
    >>> import randog.sqlalchemy

    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "user"
    ...
    ...     id = Column(Integer, primary_key=True, autoincrement=True)
    ...     type = Column(String(4), nullable=False)
    ...     name = Column(String)

    >>> # create a factory
    >>> factory = randog.sqlalchemy.factory(
    ...     User,
    ...     as_dict=True,
    ... )

    >>> generated = factory.next()
    >>> assert isinstance(generated, dict)
    >>> assert generated.keys() == {"id", "type", "name"}
    >>> assert generated["id"] == 1
    >>> assert isinstance(generated["type"], str)
    >>> assert isinstance(generated["name"], str) or generated["name"] is None

When using :code:`from_example`, a factory that generates a dict object can be created by using `post_process <doc.construct_factories.html#processing-output>`_. For example:

.. doctest::

    >>> from sqlalchemy import Column, Integer, inspect, String
    >>> from sqlalchemy.orm import declarative_base
    >>> import randog.factory
    >>> import randog.sqlalchemy

    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "user"
    ...
    ...     id = Column(Integer, primary_key=True, autoincrement=True)
    ...     type = Column(String(4), nullable=False)
    ...     name = Column(String)

    >>> # In post_process, convert a generated User instance into a dict object.
    >>> factory = randog.factory.from_example(User, custom_func=randog.sqlalchemy.custom) \
    ...     .post_process(lambda r: {k: col.value for k, col in inspect(r).attrs.items()})

    >>> generated = factory.next()
    >>> assert isinstance(generated, dict)
    >>> assert generated.keys() == {"id", "type", "name"}
    >>> assert generated["id"] == 1
    >>> assert isinstance(generated["type"], str)
    >>> assert isinstance(generated["name"], str) or generated["name"] is None
