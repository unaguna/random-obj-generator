import typing as t

T = t.TypeVar("T")
R = t.TypeVar("R")


def dfor(value: t.Optional[T], default: T) -> T:
    if value is None:
        return default
    else:
        return value


def dforc(m: t.Callable[[T], R], value: t.Optional[T]) -> t.Optional[R]:
    if value is None:
        return None
    else:
        return m(value)
