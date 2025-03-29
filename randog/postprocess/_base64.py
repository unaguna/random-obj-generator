import base64
import typing as t

from ._base import BasePostProcess


class Base64PostProcess(BasePostProcess):
    def get_input_type(self) -> t.Sequence[t.Type]:
        return (bytes,)

    def get_output_type(self) -> t.Sequence[t.Type]:
        return (str,)

    def __call__(self, pre_value: bytes) -> str:
        return base64.b64encode(pre_value).decode("utf-8")
