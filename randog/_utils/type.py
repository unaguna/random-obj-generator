import datetime as dt
from .. import timedelta_util


def positive_int(value):
    value_int = int(value)
    if value_int <= 0:
        raise ValueError("must be positive")
    return value_int


def non_negative_int(value):
    value_int = int(value)
    if value_int < 0:
        raise ValueError("must be non-negative")
    return value_int


def probability(value):
    value_float = float(value)
    if 0 <= value_float <= 1:
        return value_float
    else:
        raise ValueError("must be in the range [0, 1]")


def datetime(value):
    return dt.datetime.fromisoformat(value)


def time(value):
    return dt.time.fromisoformat(value)


def date(value):
    return dt.date.fromisoformat(value)


def timedelta(value):
    return timedelta_util.from_str(value)


def positive_timedelta(value):
    result = timedelta_util.from_str(value)
    if result <= dt.timedelta(0):
        raise ValueError("must be positive")
    return timedelta_util.from_str(value)
