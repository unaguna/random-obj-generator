import datetime

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
    "type_pos", (lambda: sqlalchemy.DateTime, lambda: sqlalchemy.DateTime())
)
def test__sqlalchemy_custom__datetime(nullable, type_pos):
    example = sqlalchemy.Column("col", type_pos(), nullable=nullable)
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {datetime.datetime, type(None)}
    else:
        assert value_types == {datetime.datetime}


@pytest.mark.require_sqlalchemy(1, 2)
@pytest.mark.parametrize("timezone", (True, False))
def test__sqlalchemy_custom__datetime__timezone(timezone):
    local_timezone = datetime.datetime.now().astimezone().tzinfo
    example = sqlalchemy.Column(
        "col", sqlalchemy.DateTime(timezone=timezone), nullable=False
    )
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_tzinfo = set(map(lambda _: factory.next().tzinfo, range(200)))

    if timezone:
        assert value_tzinfo == {local_timezone}
    else:
        assert value_tzinfo == {None}


@pytest.mark.require_sqlalchemy(2)
@pytest.mark.parametrize("nullable", (True, False))
def test__sqlalchemy_custom__datetime2(my_base, nullable):
    import sqlalchemy.orm

    class MyModel(my_base):
        __tablename__ = "my_table"

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        field: sqlalchemy.orm.Mapped[datetime.datetime] = sqlalchemy.orm.mapped_column(
            nullable=nullable
        )

    example = MyModel.field
    factory = randog.factory.from_example(example, custom_func=sqlalchemy_custom)

    value_types = set(map(lambda _: type(factory.next()), range(200)))

    if nullable:
        assert value_types == {datetime.datetime, type(None)}
    else:
        assert value_types == {datetime.datetime}