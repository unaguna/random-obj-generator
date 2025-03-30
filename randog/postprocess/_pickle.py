import pickle
import typing as t

from ._base import BasePostProcess


class PicklePostProcess(BasePostProcess):
    def get_input_type(self) -> t.Sequence[t.Type]:
        return (t.Any,)

    def get_output_type(self) -> t.Sequence[t.Type]:
        return (bytes,)

    def __call__(self, pre_value: t.Any) -> t.Any:
        return pickle.dumps(pre_value)
