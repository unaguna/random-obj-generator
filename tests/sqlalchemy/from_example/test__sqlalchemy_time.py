import datetime

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
    "type_pos", (lambda: sqlalchemy.Time, lambda: sqlalchemy.Time())
)
def test__sqlalchemy_custom__time(nullable, type_pos):
    example = sqlalchemy.Column("col", type_pos(), nullable=nullable)
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {datetime.time, type(None)}
    else:
        assert value_types == {datetime.time}


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize("timezone", (True, False))
def test__sqlalchemy_custom__time__timezone(timezone):
    example = sqlalchemy.Column(
        "col", sqlalchemy.Time(timezone=timezone), nullable=False
    )
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_tzinfo = set(map(lambda _: factory.next().tzinfo, range(200)))

    if timezone:
        assert value_tzinfo == {datetime.timezone.utc}
    else:
        assert value_tzinfo == {None}


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__time2(my_base, nullable):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[datetime.time] = sqlalchemy.orm.mapped_column(
            nullable=nullable
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {datetime.time, type(None)}
    else:
        assert value_types == {datetime.time}


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize("timezone", (True, False))
def test__sqlalchemy_custom__time2__timezone(my_base, timezone):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[datetime.time] = sqlalchemy.orm.mapped_column(
            sqlalchemy.Time(timezone=timezone), nullable=False
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_tzinfo = set(map(lambda _: factory.next().tzinfo, range(200)))

    if timezone:
        assert value_tzinfo == {datetime.timezone.utc}
    else:
        assert value_tzinfo == {None}
