import base64
import typing as t

from ._base import BasePostProcess


class Base64PostProcess(BasePostProcess):
    def get_input_type(self) -> t.Sequence[t.Type]:
        return (bytes,)

    def get_output_type(self) -> t.Sequence[t.Type]:
        return (str,)

    def __call__(self, pre_value: t.Any) -> t.Any:
        if isinstance(pre_value, t.Mapping):
            return {
                key: (
                    self(value)
                    if isinstance(value, (t.Sequence, t.Mapping, bytes))
                    and not isinstance(value, str)
                    else value
                )
                for key, value in pre_value.items()
            }
        elif isinstance(pre_value, t.Sequence) and not isinstance(
            pre_value, (str, bytes)
        ):
            next_type = tuple
            if isinstance(pre_value, t.MutableSequence):
                next_type = list

            return next_type(
                [
                    (
                        self(value)
                        if isinstance(value, (t.Sequence, t.Mapping, bytes))
                        and not isinstance(value, str)
                        else value
                    )
                    for value in pre_value
                ]
            )

        return base64.b64encode(pre_value).decode("utf-8")
