import datetime
from decimal import Decimal

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


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize(
    ("column_type", "expected_type", "additional_assertion"),
    (
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
    ),
)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_factory(
    my_base1, column_type, expected_type, additional_assertion, nullable
):
    class MyModel(my_base1):
        __tablename__ = "my_table"

        id = sqlalchemy.Column(
            "id", sqlalchemy.Integer, primary_key=True, autoincrement=True
        )
        field = sqlalchemy.Column("field", column_type(), nullable=nullable)

    factory = randog.sqlalchemy.factory(MyModel)

    if nullable:
        expected_type = (expected_type, type(None))
    for _ in range(200):
        value = factory.next()

        assert isinstance(value, MyModel)
        assert isinstance(value.id, int)
        assert isinstance(value.field, expected_type)
        if additional_assertion is not None:
            assert value.field is None or additional_assertion(value.field)


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize(
    "expected_type",
    (int, str),
)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_factory2(my_base, expected_type, nullable):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[expected_type] = sqlalchemy.orm.mapped_column(
            nullable=nullable
        )

    factory = randog.sqlalchemy.factory(MyModel)

    if nullable:
        expected_type = (expected_type, type(None))
    for _ in range(200):
        value = factory.next()

        assert isinstance(value, MyModel)
        assert isinstance(value.id, int)
        assert isinstance(value.field, expected_type)


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize(
    ("column_type", "expected_type", "additional_assertion"),
    (
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
    ),
)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_factory2__with_column_type(
    my_base, column_type, expected_type, additional_assertion, nullable
):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[expected_type] = sqlalchemy.orm.mapped_column(
            column_type(),
            nullable=nullable,
        )

    factory = randog.sqlalchemy.factory(MyModel)

    if nullable:
        expected_type = (expected_type, type(None))
    for _ in range(200):
        value = factory.next()

        assert isinstance(value, MyModel)
        assert isinstance(value.id, int)
        assert isinstance(value.field, expected_type)
        if additional_assertion is not None:
            assert value.field is None or additional_assertion(value.field)
