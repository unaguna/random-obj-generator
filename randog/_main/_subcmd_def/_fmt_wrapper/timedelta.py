import datetime as dt

from .... import timedelta_util


class TimedeltaWrapper(dt.timedelta):
    _base: dt.timedelta

    def __new__(cls, base: dt.timedelta):
        ins = super(TimedeltaWrapper, cls).__new__(
            cls,
            days=base.days,
            seconds=base.seconds,
            microseconds=base.microseconds,
        )
        ins._base = base
        return ins

    def __str__(self):
        return timedelta_util.to_str(self)

    def __repr__(self):
        return repr(self._base)

    def __format__(self, format_spec):
        return timedelta_util.to_fmt(self, format_spec)

    def isoformat(self):
        return timedelta_util.to_iso(self)
