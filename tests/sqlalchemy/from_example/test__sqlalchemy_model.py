import pytest
import randog.factory

# run tests even if it failed to import
try:
    import sqlalchemy
    from randog.sqlalchemy import custom as sqlalchemy_custom
except ModuleNotFoundError:
    pass


@pytest.fixture()
def my_base1():
    try:
        from sqlalchemy.orm import declarative_base
    except ImportError:
        from sqlalchemy.ext.declarative import declarative_base

    return declarative_base()


@pytest.fixture()
def my_base():
    import sqlalchemy.orm

    class Base(sqlalchemy.orm.DeclarativeBase):
        pass

    return Base


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize(
    "get_example", (lambda model_cls: model_cls, lambda model_cls: model_cls())
)
def test__sqlalchemy_custom__model(my_base1, get_example):
    class MyModel(my_base1):
        __tablename__ = "my_table"

        id = sqlalchemy.Column(
            "id", sqlalchemy.Integer, primary_key=True, autoincrement=True
        )
        name = sqlalchemy.Column("name", sqlalchemy.String(200), nullable=False)
        age = sqlalchemy.Column("age", sqlalchemy.Integer, nullable=False)
        email = sqlalchemy.Column("e_mail", sqlalchemy.String(100), nullable=True)

    example = get_example(MyModel)
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    for _ in range(200):
        value = factory.next()

        assert isinstance(value, MyModel)
        assert isinstance(value.id, int)
        assert isinstance(value.name, str)
        assert isinstance(value.age, int)
        assert isinstance(value.email, (str, type(None)))


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize(
    "get_example", (lambda model_cls: model_cls, lambda model_cls: model_cls())
)
def test__sqlalchemy_custom__model2(my_base, get_example):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(nullable=False)
        age: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(nullable=False)
        email: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
            "e_mail", nullable=True
        )

    example = get_example(MyModel)
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    for _ in range(200):
        value = factory.next()

        assert isinstance(value, MyModel)
        assert isinstance(value.id, int)
        assert isinstance(value.name, str)
        assert isinstance(value.age, int)
        assert isinstance(value.email, (str, type(None)))
