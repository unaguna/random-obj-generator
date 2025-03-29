import abc
import typing as t


class BasePostProcess(abc.ABC):
    @abc.abstractmethod
    def get_input_type(self) -> t.Sequence[t.Type]: ...

    @abc.abstractmethod
    def get_output_type(self) -> t.Sequence[t.Type]: ...
