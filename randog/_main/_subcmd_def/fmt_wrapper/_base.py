import abc
import typing as t


class BaseWrapper(abc.ABC):
    @abc.abstractmethod
    def origin(self): ...


def strip_wrapper(value: t.Any):
    if isinstance(value, BaseWrapper):
        return value.origin()
    else:
        return value
