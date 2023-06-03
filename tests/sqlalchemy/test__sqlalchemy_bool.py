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
def test__sqlalchemy_custom__boolean(nullable):
    example = sqlalchemy.Column("col", sqlalchemy.Boolean, nullable=nullable)
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {bool, type(None)}
    else:
        assert value_types == {bool}


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__boolean2(my_base, nullable):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[bool] = sqlalchemy.orm.mapped_column(
            nullable=nullable
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {bool, type(None)}
    else:
        assert value_types == {bool}
