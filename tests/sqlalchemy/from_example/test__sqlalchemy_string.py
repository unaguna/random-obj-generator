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
    "type_pos",
    (
        lambda: sqlalchemy.String,
        lambda: sqlalchemy.String(),
        lambda: sqlalchemy.Text,
        lambda: sqlalchemy.Text(),
    ),
)
def test__sqlalchemy_custom__string(nullable, type_pos):
    example = sqlalchemy.Column("col", type_pos(), nullable=nullable)
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {str, type(None)}
    else:
        assert value_types == {str}


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize(
    ("length", "type_pos"),
    (
        (
            2,
            lambda: sqlalchemy.String(2),
        ),
        (
            500,
            lambda: sqlalchemy.String(500),
        ),
        (
            2,
            lambda: sqlalchemy.Text(2),
        ),
        (
            500,
            lambda: sqlalchemy.Text(500),
        ),
    ),
)
def test__sqlalchemy_custom__string__with_length(length, type_pos):
    example = sqlalchemy.Column("col", type_pos(), nullable=False)
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    for _ in range(200):
        value = factory.next()

        assert isinstance(value, str)
        assert len(value) <= length


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__string2(my_base, nullable):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
            nullable=nullable
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {str, type(None)}
    else:
        assert value_types == {str}


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize(
    ("length", "type_pos"),
    (
        (
            2,
            lambda: sqlalchemy.String(2),
        ),
        (
            500,
            lambda: sqlalchemy.String(500),
        ),
        (
            2,
            lambda: sqlalchemy.Text(2),
        ),
        (
            500,
            lambda: sqlalchemy.Text(500),
        ),
    ),
)
def test__sqlalchemy_custom__string2__with_length(my_base, length, type_pos):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
            type_pos(), nullable=False
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    for _ in range(200):
        value = factory.next()

        assert isinstance(value, str)
        assert len(value) <= length
