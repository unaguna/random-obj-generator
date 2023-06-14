import datetime
from decimal import Decimal
import typing as t

import pytest

import randog.factory

# run tests even if it failed to import
try:
    import sqlalchemy
    import randog.sqlalchemy
except ModuleNotFoundError:
    pass


@pytest.fixture()
def my_base1():
    from sqlalchemy.ext.declarative import declarative_base

    return declarative_base()


@pytest.fixture()
def my_base():
    import sqlalchemy.orm

    class Base(sqlalchemy.orm.DeclarativeBase):
        pass

    return Base


def _is_integer(x) -> bool:
    return int(x) == x


# "column_type", "expected_type", "additional_assertion"
__TEST_PARAMS: t.Sequence[
    t.Tuple[t.Callable[[], t.Any], t.Type, t.Optional[t.Callable[[t.Any], bool]]]
] = (
    (lambda: sqlalchemy.Integer, int, None),
    (lambda: sqlalchemy.BigInteger, int, None),
    (lambda: sqlalchemy.Numeric, Decimal, None),
    (lambda: sqlalchemy.Numeric(asdecimal=False), float, None),
    (lambda: sqlalchemy.Numeric(asdecimal=True), Decimal, None),
    (
        lambda: sqlalchemy.Numeric(4, 1),
        Decimal,
        lambda x: _is_integer(x / Decimal("0.1")) and -1000 < x < 1000,
    ),
    (lambda: sqlalchemy.Float, float, None),
    (lambda: sqlalchemy.Float(asdecimal=False), float, None),
    (lambda: sqlalchemy.Float(asdecimal=True), Decimal, None),
    (lambda: sqlalchemy.String, str, None),
    (lambda: sqlalchemy.String(3), str, lambda x: len(x) <= 3),
    (lambda: sqlalchemy.Text, str, None),
    (lambda: sqlalchemy.Boolean, bool, None),
    (lambda: sqlalchemy.Date, datetime.date, None),
    (lambda: sqlalchemy.DateTime, datetime.datetime, None),
    (
        lambda: sqlalchemy.DateTime(timezone=False),
        datetime.datetime,
        lambda x: x.tzinfo is None,
    ),
    (
        lambda: sqlalchemy.DateTime(timezone=True),
        datetime.datetime,
        lambda x: x.tzinfo == datetime.timezone.utc,
    ),
    (lambda: sqlalchemy.TIMESTAMP, datetime.datetime, None),
    (lambda: sqlalchemy.Time, datetime.time, None),
    (
        lambda: sqlalchemy.Time(timezone=False),
        datetime.time,
        lambda x: x.tzinfo is None,
    ),
    (
        lambda: sqlalchemy.Time(timezone=True),
        datetime.time,
        lambda x: x.tzinfo == datetime.timezone.utc,
    ),
    (lambda: sqlalchemy.Interval, datetime.timedelta, None),
)


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize(
    ("column_type", "expected_type", "additional_assertion"),
    __TEST_PARAMS,
)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_factory(
    my_base1, column_type, expected_type, additional_assertion, nullable
):
    if nullable:
        expected_field_types = {expected_type, type(None)}
    else:
        expected_field_types = {expected_type}

    class MyModel(my_base1):
        __tablename__ = "my_table"

        id = sqlalchemy.Column(
            "id", sqlalchemy.Integer, primary_key=True, autoincrement=True
        )
        field = sqlalchemy.Column("field", column_type(), nullable=nullable)

    factory = randog.sqlalchemy.factory(MyModel)
    values = list(factory.iter(200))
    field_types = set((type(value.field) for value in values))

    assert field_types == expected_field_types
    for value in values:
        assert isinstance(value, MyModel)
        assert isinstance(value.id, int)
        if additional_assertion is not None:
            assert value.field is None or additional_assertion(value.field)


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize(
    "expected_type",
    (
        int,
        Decimal,
        float,
        str,
        bool,
        datetime.date,
        datetime.datetime,
        datetime.time,
        datetime.timedelta,
    ),
)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_factory2(my_base, expected_type, nullable):
    import sqlalchemy.orm

    if nullable:
        expected_field_types = {expected_type, type(None)}
    else:
        expected_field_types = {expected_type}

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[expected_type] = sqlalchemy.orm.mapped_column(
            nullable=nullable
        )

    factory = randog.sqlalchemy.factory(MyModel)
    values = list(factory.iter(200))
    field_types = set((type(value.field) for value in values))

    assert field_types == expected_field_types
    for value in values:
        assert isinstance(value, MyModel)
        assert isinstance(value.id, int)


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize(
    ("column_type", "expected_type", "additional_assertion"),
    __TEST_PARAMS,
)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_factory2__with_column_type(
    my_base, column_type, expected_type, additional_assertion, nullable
):
    import sqlalchemy.orm

    if nullable:
        expected_field_types = {expected_type, type(None)}
    else:
        expected_field_types = {expected_type}

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[expected_type] = sqlalchemy.orm.mapped_column(
            column_type(),
            nullable=nullable,
        )

    factory = randog.sqlalchemy.factory(MyModel)
    values = list(factory.iter(200))
    field_types = set((type(value.field) for value in values))

    assert field_types == expected_field_types
    for value in values:
        assert isinstance(value, MyModel)
        assert isinstance(value.id, int)
        if additional_assertion is not None:
            assert value.field is None or additional_assertion(value.field)


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize(
    ("column_type", "expected_type", "additional_assertion"),
    __TEST_PARAMS,
)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_factory__as_dict(
    my_base1, column_type, expected_type, additional_assertion, nullable
):
    if nullable:
        expected_field_types = {expected_type, type(None)}
    else:
        expected_field_types = {expected_type}

    class MyModel(my_base1):
        __tablename__ = "my_table"

        id = sqlalchemy.Column(
            "id", sqlalchemy.Integer, primary_key=True, autoincrement=True
        )
        field = sqlalchemy.Column("field", column_type(), nullable=nullable)

    factory = randog.sqlalchemy.factory(MyModel, as_dict=True)
    values = list(factory.iter(200))
    field_types = set((type(value["field"]) for value in values))

    assert field_types == expected_field_types
    for value in values:
        assert isinstance(value, dict)
        assert isinstance(value["id"], int)
        if additional_assertion is not None:
            assert value["field"] is None or additional_assertion(value["field"])


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize(
    ("column_type", "expected_type", "additional_assertion"),
    __TEST_PARAMS,
)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_factory2__as_dict(
    my_base, column_type, expected_type, additional_assertion, nullable
):
    import sqlalchemy.orm

    if nullable:
        expected_field_types = {expected_type, type(None)}
    else:
        expected_field_types = {expected_type}

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[expected_type] = sqlalchemy.orm.mapped_column(
            column_type(),
            nullable=nullable,
        )

    factory = randog.sqlalchemy.factory(MyModel, as_dict=True)
    values = list(factory.iter(200))
    field_types = set((type(value["field"]) for value in values))

    assert field_types == expected_field_types
    for value in values:
        assert isinstance(value, dict)
        assert isinstance(value["id"], int)
        if additional_assertion is not None:
            assert value["field"] is None or additional_assertion(value["field"])
