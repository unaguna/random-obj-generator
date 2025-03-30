import base64
import typing as t

from ._base import BasePostProcess


class Base64PostProcess(BasePostProcess):
    _strict_type: bool

    def __init__(self, *, strict_type: bool = True):
        self._strict_type = strict_type

    def get_input_type(self) -> t.Sequence[t.Type]:
        return (bytes,)

    def get_output_type(self) -> t.Sequence[t.Type]:
        return (str,)

    def __call__(self, pre_value: t.Any) -> t.Any:
        next_val = _b64encode_or_asis(pre_value)
        if self._strict_type and pre_value is next_val:
            raise TypeError(
                f"base64 requires a bytes-like object, not '{type(pre_value).__name__}'"
            )

        return next_val


def _b64encode_or_asis(pre_value: t.Any) -> t.Any:
    if isinstance(pre_value, bytes):
        return base64.b64encode(pre_value).decode("utf-8")
    elif isinstance(pre_value, t.Mapping):
        return {key: _b64encode_or_asis(value) for key, value in pre_value.items()}
    elif isinstance(pre_value, t.Sequence) and not isinstance(pre_value, str):
        next_type = tuple
        if isinstance(pre_value, t.MutableSequence):
            next_type = list

        return next_type(_b64encode_or_asis(value) for value in pre_value)
    else:
        return pre_value
