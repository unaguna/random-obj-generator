import datetime
import typing as t

import randog.factory
from randog.exceptions import FactoryConstructionError


def custom(example, **kwargs):
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

    if column_python_type in __CUSTOM_FUNC_FOR_SPEC_TYPE:
        customized_example = __CUSTOM_FUNC_FOR_SPEC_TYPE[column_python_type](
            column_type, context=context, **kwargs
        )
    elif isinstance(column_python_type, type):
        customized_example = column_python_type
    else:
        raise FactoryConstructionError(
            f"cannot create factory from sqlalchemy.Column type of {column_type}: not implemented"
        )

    factory = randog.factory.from_example(customized_example, context=context)
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


def _custom_func_for_datetime_column(
    column_type,
    **kwargs,
):
    use_timezone = getattr(column_type, "timezone", None)

    if use_timezone:
        local_timezone = datetime.datetime.now().astimezone().tzinfo
        return randog.factory.randdatetime(tzinfo=local_timezone)
    else:
        return randog.factory.randdatetime(tzinfo=None)


__CUSTOM_FUNC_FOR_SPEC_TYPE = {
    str: _custom_func_for_str_column,
    datetime.datetime: _custom_func_for_datetime_column,
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
