import datetime
from decimal import Decimal
import typing as t

import randog.factory
from randog.exceptions import FactoryConstructionError
from .._utils.nullsafe import dfor


def custom(example, **kwargs):
    """custom_func for `randog.factory.from_example` to generate sqlalchemy-derived objects

    This function is an add-on for `randog.factory.from_example`.

    Specify this function as `custom_func` if you want to create a factory that generates sqlalchemy-derived objects in
    `from_example`.

    Examples
    --------
    >>> from sqlalchemy import Column, Integer, String
    >>> from sqlalchemy.orm import declarative_base
    >>> import randog.factory
    >>> import randog.sqlalchemy
    >>>
    >>> Base = declarative_base()
    >>>
    >>> class User(Base):
    ...     __tablename__ = "user"
    ...
    ...     id = Column(Integer, primary_key=True, autoincrement=True)
    ...     name = Column(String)
    >>>
    >>> # specify `randog.sqlalchemy.custom` as `custom_func`
    >>> factory = randog.factory.from_example(User, custom_func=randog.sqlalchemy.custom)
    >>> generated = factory.next()
    """
    if type(example).__module__.startswith("sqlalchemy."):
        # example is Model
        if hasattr(example, "_sa_class_manager"):
            return _custom_func_for_model(example._sa_class_manager, **kwargs)
        # example is Column or like it
        else:
            return _custom_func_for_column(example, **kwargs)
    else:
        return NotImplemented


def _custom_func_for_model(
    class_manager,
    **kwargs,
):
    return dict(class_manager)


def _custom_func_for_column(
    column,  # : sqlalchemy.sql.ColumnElement,
    *,
    context: randog.factory.FromExampleContext,
    **kwargs,
):
    # type checks of `column`
    column_type, column_python_type = _get_column_types(column)
    enums = getattr(column_type, "enums", None) if column_type is not None else None
    autoincrement = getattr(column, "autoincrement", False)

    # normalize example for the function `from_example`.
    # If this is difficult, create the factory directly.
    factory = None
    customized_example = None
    if enums is not None and column_python_type == str:
        # use randchoice instead from_example(str) if it is enumeration
        factory = randog.factory.randchoice(*enums, rnd=context.rnd)
    elif autoincrement and column_python_type == int:
        # use increment instead from_example(int) if it is auto incremental
        factory = randog.factory.increment(maximum=2**31 - 1, rnd=context.rnd)
    elif column_python_type in __CUSTOM_FUNC_FOR_SPEC_TYPE:
        customized_example = __CUSTOM_FUNC_FOR_SPEC_TYPE[column_python_type](
            column_type, context=context, **kwargs
        )
    elif isinstance(column_python_type, type):
        customized_example = column_python_type
    else:
        raise FactoryConstructionError(
            f"cannot create factory from sqlalchemy.Column type of {column_type}: not implemented"
        )

    # Create a factory based on the normalized example.
    # If a factory has already been created directly, it is used.
    if factory is None:
        factory = randog.factory.from_example(customized_example, context=context)
    # make the factory nullable
    if hasattr(column, "nullable") and column.nullable:
        factory = factory.or_none(rnd=context.rnd)

    return factory


def _custom_func_for_str_column(
    column_type,
    **kwargs,
):
    length = getattr(column_type, "length", None)
    if length is not None:
        return randog.factory.randstr(length=length)
    else:
        return str


def _custom_func_for_numeric_column(
    column_type,
    **kwargs,
):
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

    return randog.factory.randdecimal(minimum, maximum, decimal_len=scale)


def _custom_func_for_datetime_column(
    column_type,
    **kwargs,
):
    use_timezone = getattr(column_type, "timezone", None)

    if use_timezone:
        return randog.factory.randdatetime(tzinfo=datetime.timezone.utc)
    else:
        return randog.factory.randdatetime(tzinfo=None)


def _custom_func_for_time_column(
    column_type,
    **kwargs,
):
    use_timezone = getattr(column_type, "timezone", None)

    if use_timezone:
        return randog.factory.randtime(tzinfo=datetime.timezone.utc)
    else:
        return randog.factory.randtime(tzinfo=None)


__CUSTOM_FUNC_FOR_SPEC_TYPE = {
    str: _custom_func_for_str_column,
    Decimal: _custom_func_for_numeric_column,
    datetime.datetime: _custom_func_for_datetime_column,
    datetime.time: _custom_func_for_time_column,
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
