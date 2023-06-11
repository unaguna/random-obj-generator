import enum

import pytest
import randog.factory
from randog.sqlalchemy import custom as sqlalchemy_custom


class MyEnum(enum.Enum):
    one = 1
    two = 2
    three = 3


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
def test__sqlalchemy_custom__enum(nullable):
    example = sqlalchemy.Column("col", sqlalchemy.Enum(MyEnum), nullable=nullable)
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {MyEnum, type(None)}
    else:
        assert value_types == {MyEnum}


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__enum2(my_base, nullable):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[MyEnum] = sqlalchemy.orm.mapped_column(
            nullable=nullable
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {MyEnum, type(None)}
    else:
        assert value_types == {MyEnum}


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__enum__by_str(nullable):
    example = sqlalchemy.Column(
        "col", sqlalchemy.Enum("E1", "E2", "E3"), nullable=nullable
    )
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    values = set(map(lambda _: factory.next(), range(500)))

    if nullable:
        assert values == {"E1", "E2", "E3", None}
    else:
        assert values == {"E1", "E2", "E3"}


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__enum2__by_str(my_base, nullable):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
            sqlalchemy.Enum("E1", "E2", "E3"), nullable=nullable
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    values = set(map(lambda _: factory.next(), range(500)))

    if nullable:
        assert values == {"E1", "E2", "E3", None}
    else:
        assert values == {"E1", "E2", "E3"}
