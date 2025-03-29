from ._base import BaseWrapper
from ...._utils.formatutils import format_bytes


class BytesWrapper(BaseWrapper):
    base: bytes

    def origin(self) -> bytes:
        return self.base

    def __init__(self, base: bytes):
        self.base = base

    def __str__(self):
        return self.base.__str__()

    def __repr__(self):
        return self.base.__repr__()

    def __format__(self, format_spec: str):
        return format_bytes(self.base, format_spec)


def _count_zero_prefix(value: bytes) -> int:
    count = 0
    for b in value:
        if b == 0:
            count += 1
        else:
            break
    return count
