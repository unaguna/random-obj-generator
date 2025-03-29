import abc
import typing as t


class BaseWrapper(abc.ABC):
    @abc.abstractmethod
    def origin(self): ...


class StripWrapper:
    _next_process: t.Callable[[t.Any], t.Any]

    def __init__(self, next_process: t.Callable[[t.Any], t.Any]):
        self._next_process = next_process

    def __call__(self, pre_value: t.Any) -> t.Any:
        inter_val = strip_wrapper(pre_value)
        return self._next_process(inter_val)


def strip_wrapper(value: t.Any):
    if isinstance(value, BaseWrapper):
        return value.origin()
    else:
        return value
