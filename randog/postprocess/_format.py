import typing as t

from ._base import BasePostProcess


class FormatPostProcess(BasePostProcess):
    _fmt_spec: str

    def get_input_type(self) -> t.Sequence[t.Type]:
        return (t.Any,)

    def get_output_type(self) -> t.Sequence[t.Type]:
        return (str,)

    def __init__(self, fmt_spec: str):
        self._fmt_spec = fmt_spec

    def __call__(self, pre_value: t.Any) -> t.Optional[str]:
        if pre_value is None:
            return None

        return format(pre_value, self._fmt_spec)


class IsoFormatPostProcess(BasePostProcess):
    def get_input_type(self) -> t.Sequence[t.Type]:
        return (t.Any,)

    def get_output_type(self) -> t.Sequence[t.Type]:
        return (str,)

    def __call__(self, pre_value: t.Any) -> t.Optional[str]:
        if pre_value is None:
            return None

        return pre_value.isoformat()
