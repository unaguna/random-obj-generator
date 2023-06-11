import pytest
import randog.factory
from randog.sqlalchemy import custom as sqlalchemy_custom

# run tests even if it failed to import
try:
    import sqlalchemy
except ModuleNotFoundError:
    pass


@pytest.fixture()
def my_base():
    import sqlalchemy.orm

    class Base(sqlalchemy.orm.DeclarativeBase):
        pass

    return Base


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize("nullable", (True, False))
@pytest.mark.parametrize(
    "type_pos", (lambda: sqlalchemy.Integer, lambda: sqlalchemy.Integer())
)
def test__sqlalchemy_custom__integer(nullable, type_pos):
    example = sqlalchemy.Column("col", type_pos(), nullable=nullable)
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {int, type(None)}
    else:
        assert value_types == {int}


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__integer2(my_base, nullable):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
            nullable=nullable
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {int, type(None)}
    else:
        assert value_types == {int}


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__biginteger(nullable):
    example = sqlalchemy.Column("col", sqlalchemy.BigInteger, nullable=nullable)
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {int, type(None)}
    else:
        assert value_types == {int}


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__biginteger2(my_base, nullable):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
            sqlalchemy.types.BIGINT, nullable=nullable
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {int, type(None)}
    else:
        assert value_types == {int}


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize("primary_key", (True, False))
@pytest.mark.parametrize(
    "type_pos",
    (
        lambda: sqlalchemy.Integer,
        lambda: sqlalchemy.Integer(),
        lambda: sqlalchemy.BigInteger,
        lambda: sqlalchemy.BigInteger(),
    ),
)
def test__sqlalchemy_custom__integer__auto_increment(primary_key, type_pos):
    example = sqlalchemy.Column(
        "col", type_pos(), primary_key=primary_key, autoincrement=True
    )
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    values = tuple(factory.iter(5))

    if primary_key:
        assert values == (1, 2, 3, 4, 5)
    else:
        assert set(values) <= {None, 1, 2, 3, 4, 5}


@pytest.mark.require_sqlalchemy(2)
def test__sqlalchemy_custom__integer2__auto_increment(my_base):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
            primary_key=True, autoincrement=True
        )

    example = MyModel.id
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    values = tuple(factory.iter(5))

    assert values == (1, 2, 3, 4, 5)
