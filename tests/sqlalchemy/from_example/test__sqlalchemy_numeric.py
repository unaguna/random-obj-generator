from decimal import Decimal

import pytest

import randog.factory

# run tests even if it failed to import
try:
    import sqlalchemy
    from randog.sqlalchemy import custom as sqlalchemy_custom
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
    "type_pos", (lambda: sqlalchemy.Numeric, lambda: sqlalchemy.Numeric())
)
def test__sqlalchemy_custom__numeric(nullable, type_pos):
    example = sqlalchemy.Column("col", type_pos(), nullable=nullable)
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {Decimal, type(None)}
    else:
        assert value_types == {Decimal}


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize(("precision", "scale"), ((5, 2), (10, 3)))
def test__sqlalchemy_custom__numeric__digits(precision, scale):
    example = sqlalchemy.Column(
        "col", sqlalchemy.Numeric(precision, scale), nullable=False
    )
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    values = list(factory.iter(200))
    value_precisions = set(map(lambda v: len(v.as_tuple()[1]), values))
    value_scales = set(map(lambda v: -v.as_tuple()[2], values))

    assert value_precisions <= set(range(precision + 1))
    assert value_scales <= set(range(scale + 1))


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__numeric__as_float(nullable):
    example = sqlalchemy.Column(
        "col", sqlalchemy.Numeric(asdecimal=False), nullable=nullable
    )
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {float, type(None)}
    else:
        assert value_types == {float}


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__numeric2(my_base, nullable):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[Decimal] = sqlalchemy.orm.mapped_column(
            nullable=nullable
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {Decimal, type(None)}
    else:
        assert value_types == {Decimal}


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize(("precision", "scale"), ((5, 2), (10, 3)))
def test__sqlalchemy_custom__numeric2__digits(my_base, precision, scale):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[Decimal] = sqlalchemy.orm.mapped_column(
            sqlalchemy.Numeric(precision, scale), nullable=False
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    values = list(factory.iter(200))
    value_precisions = set(map(lambda v: len(v.as_tuple()[1]), values))
    value_scales = set(map(lambda v: -v.as_tuple()[2], values))

    assert value_precisions <= set(range(precision + 1))
    assert value_scales <= set(range(scale + 1))


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__numeric2__as_float(my_base, nullable):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[float] = sqlalchemy.orm.mapped_column(
            sqlalchemy.Numeric(asdecimal=False), nullable=nullable
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {float, type(None)}
    else:
        assert value_types == {float}
