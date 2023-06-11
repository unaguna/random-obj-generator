Factory from sqlalchemy
=======================

You can create a factory from Column or Model of sqlalchemy. This feature is enabled by specifying `randog.sqlalchemy.custom <randog.sqlalchemy.html#custom>`_ as custom_func when using `from_example <randog.factory.html#randog.factory.from_example>`_.

.. warning::
    This is an experimental feature. It may be removed or significantly changed in the future.

.. warning::
    This is an experimental feature. Various :ref:`limitations <limitations>` apply.

.. note::
    The following examples use the model of sqlalchemy 1.4, but also supports the 2.0 using :code:`mapped_column`.

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

    >>> assert isinstance(generated, dict)

    >>> # [id] incremental integer
    >>> assert generated["id"] == 1

    >>> # [type] string of length at least 4
    >>> assert isinstance(generated["type"], str)
    >>> assert len(generated["type"]) == 4

    >>> # [name] string (nullable)
    >>> assert isinstance(generated["name"], str) or generated["name"] is None

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


Generate a model instance
-------------------------

As shown in the example above, a dictionary type value is generated.
randog do not provide a feature to generate an instance of the model, but this can be accomplished by using `post_process <doc.construct_factories.html#processing-output>`_.

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

    >>> # In post_process, convert a generated dict value into User instance.
    >>> factory = randog.factory.from_example(User, custom_func=randog.sqlalchemy.custom) \
    ...     .post_process(lambda d: User(**d))
    >>> generated = factory.next()

    >>> assert isinstance(generated, User)
    >>> assert isinstance(generated.id, int)
    >>> assert isinstance(generated.type, str)
    >>> assert isinstance(generated.name, str) or generated.name is None
