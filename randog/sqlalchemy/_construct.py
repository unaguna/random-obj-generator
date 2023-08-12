import datetime
from decimal import Decimal
import typing as t
from random import Random

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.sql.schema

import randog.factory
from .._utils.nullsafe import dfor
from ..factory import Factory, randdict, from_example
from ..exceptions import FactoryConstructionError

M = t.TypeVar("M")


@t.overload
def factory(
    model: t.Type[M],
    override_columns: t.Mapping[str, t.Union[Factory, t.Any]] = None,
    *,
    as_dict: t.Literal[False] = False,
    rnd: t.Optional[Random] = None,
) -> Factory[M]:
    ...


@t.overload
def factory(
    model: t.Type[M],
    override_columns: t.Mapping[str, t.Union[Factory, t.Any]] = None,
    *,
    as_dict: t.Literal[True],
    rnd: t.Optional[Random] = None,
) -> Factory[dict]:
    ...


def factory(
    model: t.Type[M],
    override_columns: t.Mapping[str, t.Union[Factory, t.Any]] = None,
    *,
    as_dict: bool = False,
    rnd: t.Optional[Random] = None,
) -> t.Union[Factory[M], Factory[dict]]:
    """Return a factory generating Model instances randomly.

    Parameters
    ----------
    model : Type[Model]
        the model class of sqlalchemy
    override_columns : Mapping[str, Union[Factory, Column, Any]], optional
        For each column that is specified in this dictionary,
        create a factory using it instead of the column of the model class.
        If factory is specified as value of this dict, it is used to generate the field;
        if other is specified, the factory obtained by using `from_example`
        with it as an example is used to generate the field.
    as_dict : bool, default=False
        If it is True, values generated by the factory will be dict,
        not model instances.
    rnd : Random, optional
        random number generator to be used
    """
    if override_columns is None:
        override_columns = dict()

    mapper = sqlalchemy.inspect(model, raiseerr=False)
    if not isinstance(mapper, sqlalchemy.orm.Mapper):
        raise FactoryConstructionError("specified object is not model of sqlalchemy")

    factories_of_column = {
        key: _factory_from_column_etc(override_columns.get(key, column), rnd=rnd)
        for key, column in mapper.columns.items()
    }

    dict_factory = randdict(factories_of_column, rnd=rnd)

    if as_dict:
        return dict_factory
    else:
        return dict_factory.post_process(lambda r: model(**r))


def _factory_from_column_etc(
    column: t.Any,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory:
    if isinstance(column, Factory):
        return column
    elif isinstance(column, sqlalchemy.Column):
        return factory_from_column(column, rnd=rnd)
    else:
        return from_example(column, rnd=rnd)


def factory_from_column(
    column: sqlalchemy.sql.schema.Column,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory:
    """Return a factory generating values that matches the column.

    Parameters
    ----------
    column : Column
        the column of sqlalchemy
    rnd : Random, optional
        random number generator to be used
    """

    # type checks of `column`
    column_type, column_python_type = _get_column_types(column)
    enums = getattr(column_type, "enums", None) if column_type is not None else None
    autoincrement = getattr(column, "autoincrement", False)

    # normalize example for the function `from_example`.
    # If this is difficult, create the factory directly.
    if enums is not None and column_python_type == str:
        # use randchoice instead from_example(str) if it is enumeration
        factory_ = randog.factory.randchoice(*enums, rnd=rnd)
    elif autoincrement and column_python_type == int:
        # use increment instead from_example(int) if it is auto incremental
        factory_ = randog.factory.increment(maximum=2**31 - 1, rnd=rnd)
    elif column_python_type in __FACTORY_FOR_SPEC_TYPE:
        factory_ = __FACTORY_FOR_SPEC_TYPE[column_python_type](
            column_type,
            rnd=rnd,
        )
    elif isinstance(column_python_type, type):
        factory_ = randog.factory.from_example(column_python_type, rnd=rnd)
    else:
        raise FactoryConstructionError(
            f"cannot create factory from sqlalchemy.Column type of {column_type}: "
            "not implemented"
        )

    # Create a factory based on the normalized example.
    if not isinstance(factory_, Factory):
        factory_ = randog.factory.from_example(factory_, rnd=rnd)
    # make the factory nullable
    if hasattr(column, "nullable") and column.nullable:
        factory_ = factory_.or_none(rnd=rnd)

    return factory_


def _factory_for_str_column(
    column_type,
    rnd: t.Optional[Random] = None,
):
    length = getattr(column_type, "length", None)
    if length is not None:
        return randog.factory.randstr(length=length, rnd=rnd)
    else:
        return str


def _factory_for_numeric_column(
    column_type,
    rnd: t.Optional[Random] = None,
) -> Factory:
    precision = getattr(column_type, "precision", None)
    scale = getattr(column_type, "scale", None)

    if precision is not None:
        scale_n = dfor(scale, 0)

        maximum = Decimal("1").scaleb(precision - scale_n) - Decimal("1").scaleb(
            -scale_n
        )
        minimum = -maximum
    else:
        minimum = None
        maximum = None

    return randog.factory.randdecimal(minimum, maximum, decimal_len=scale, rnd=rnd)


def _factory_for_datetime_column(
    column_type,
    rnd: t.Optional[Random] = None,
) -> Factory[datetime.datetime]:
    use_timezone = getattr(column_type, "timezone", None)

    if use_timezone:
        return randog.factory.randdatetime(tzinfo=datetime.timezone.utc, rnd=rnd)
    else:
        return randog.factory.randdatetime(tzinfo=None, rnd=rnd)


def _factory_for_time_column(
    column_type,
    rnd: t.Optional[Random] = None,
) -> Factory[datetime.time]:
    use_timezone = getattr(column_type, "timezone", None)

    if use_timezone:
        return randog.factory.randtime(tzinfo=datetime.timezone.utc, rnd=rnd)
    else:
        return randog.factory.randtime(tzinfo=None, rnd=rnd)


__FACTORY_FOR_SPEC_TYPE = {
    str: _factory_for_str_column,
    Decimal: _factory_for_numeric_column,
    datetime.datetime: _factory_for_datetime_column,
    datetime.time: _factory_for_time_column,
}


def _get_column_types(column) -> t.Tuple[t.Any, t.Any]:
    # type checks of `column`
    if hasattr(column, "type"):
        column_type = column.type
    else:
        raise FactoryConstructionError(
            f"cannot create factory from {column}: not implemented"
        )
    if hasattr(column_type, "python_type"):
        column_python_type = column_type.python_type
    else:
        raise FactoryConstructionError(
            f"cannot create factory from {column}: not implemented"
        )

    return column_type, column_python_type
