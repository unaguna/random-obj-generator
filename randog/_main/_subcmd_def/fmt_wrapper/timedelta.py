import datetime as dt

from . import BaseWrapper
from .... import timedelta_util


class TimedeltaWrapper(BaseWrapper):
    _base: dt.timedelta

    def origin(self) -> dt.timedelta:
        return self._base

    def __init__(self, base: dt.timedelta):
        self._base = base

    def __str__(self):
        return timedelta_util.to_str(self._base)

    def __repr__(self):
        return repr(self._base)

    def __format__(self, format_spec):
        return timedelta_util.to_fmt(self._base, format_spec)

    def isoformat(self):
        return timedelta_util.to_iso(self._base)
