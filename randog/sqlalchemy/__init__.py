import typing as t

import randog.factory
from randog.exceptions import FactoryConstructionError

__EXAMPLE_FOR_PYTHON_TYPE: t.Mapping[t.Type, t.Any] = {
    int: 0,
    bool: bool,
}


def custom(example, **kwargs):
    if type(example).__module__.startswith("sqlalchemy."):
        return _custom_func_for_column(example, **kwargs)
    else:
        return NotImplemented


def _custom_func_for_column(
    column,  # : sqlalchemy.sql.ColumnElement,
    *,
    context: randog.factory.FromExampleContext,
    **kwargs,
):
    # type checks of `column`
    column_type, column_python_type = _get_column_types(column)

    if column_python_type in __EXAMPLE_FOR_PYTHON_TYPE:
        customized_example = __EXAMPLE_FOR_PYTHON_TYPE[column_python_type]
    else:
        raise FactoryConstructionError(
            f"cannot create factory from sqlalchemy.Column type of {column_type}: not implemented"
        )

    factory = randog.factory.from_example(customized_example, context=context)
    if hasattr(column, "nullable") and column.nullable:
        factory = factory.or_none(rnd=context.rnd)

    return factory


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
