import typing as t

T = t.TypeVar("T")


def dfor(value: t.Optional[T], default: T) -> T:
    if value is None:
        return default
    else:
        return value
