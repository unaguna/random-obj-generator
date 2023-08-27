import codecs
import datetime as dt
import re
import typing as t

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


_DATETIME_REGEX = re.compile(
    r"^(\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?)?|now)?(.*)$"
)


def datetime(value) -> t.Union[dt.datetime, dt.timedelta]:
    """datetime include expression type of datetime+timedelta or timedelta

    This function accepts according inputs:

    - ISO-8601 (YYYY-mm-ddTHH:MM:SS, YYYY-mm-ddTHH:MM:SS.ffffff, ...)
    - YYYY-mm-dd HH:MM:SS, YYYY-mm-dd HH:MM:SS.ffffff, ...
    - now
    - timedelta simple expr (1h, +30m, -1h20m, ...)
    - datetime+timedelta (now+1h, YYYY-mm-ddTHH:MM:SS+30m, ...)

    Parameters
    ----------
    value
        string value

    Returns
    -------
    datetime | timedelta
        parsed value
    """
    found = _DATETIME_REGEX.match(value)

    if not found or value == "":
        raise ValueError(f"failed to parse datetime: {value}")

    base_str = found.group(1)
    shift_str = found.group(2)

    if base_str is None:
        base = None
    elif base_str == "now":
        base = dt.datetime.now()
    else:
        base = dt.datetime.fromisoformat(base_str)

    if shift_str != "":
        shift = timedelta_util.from_str(shift_str)
    else:
        shift = dt.timedelta(0)

    if base is None:
        return shift
    else:
        return base + shift


_TIME_REGEX = re.compile(r"^(\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?|now)?(.*)$")


def time(value):
    """time include expression type of time+timedelta or timedelta

    This function accepts according inputs:

    - ISO-8601 (HH:MM:SS, HH:MM:SS.ffffff, HH:MM, ...)
    - now
    - timedelta simple expr (1h, +30m, -1h20m, ...)
    - time+timedelta (now+1h, HH:MM:SS+30m, ...)

    Parameters
    ----------
    value
        string value

    Returns
    -------
    time | timedelta
        parsed value
    """
    found = _TIME_REGEX.match(value)

    if not found or value == "":
        raise ValueError(f"failed to parse time: {value}")

    base_str = found.group(1)
    shift_str = found.group(2)

    if base_str is None:
        base = None
    elif base_str == "now":
        base = dt.datetime.now()
    else:
        base = dt.datetime.combine(dt.date.today(), dt.time.fromisoformat(base_str))

    if shift_str != "":
        shift = timedelta_util.from_str(shift_str)
    else:
        shift = dt.timedelta(0)

    if base is None:
        return shift
    else:
        return (base + shift).time()


def date(value):
    return dt.date.fromisoformat(value)


def timedelta(value):
    return timedelta_util.from_str(value)


def positive_timedelta(value):
    result = timedelta_util.from_str(value)
    if result <= dt.timedelta(0):
        raise ValueError("must be positive")
    return timedelta_util.from_str(value)


def encoding(value):
    try:
        codecs.lookup(value)
    except LookupError as e:
        raise ValueError(*e.args)
    return value
