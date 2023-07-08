import datetime as dt
from decimal import Decimal
import re
import typing as t


class TimedeltaTuple(t.NamedTuple):
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    milliseconds: int = 0
    microseconds: int = 0

    @classmethod
    def of(cls, value: dt.timedelta) -> "TimedeltaTuple":
        minutes, seconds = divmod(value.seconds, 60)
        hours, minutes = divmod(minutes, 60)

        milliseconds, microseconds = divmod(value.microseconds, 1000)

        return TimedeltaTuple(
            days=value.days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=milliseconds,
            microseconds=microseconds,
        )


def to_iso(
    value: dt.timedelta,
    *,
    exclude_milliseconds: bool = False,
    point_char: str = ".",
) -> str:
    """Convert timedelta into ISO-8601 format

    Because the timedelta object manages the date part in terms of days,
    the date parts in the output string are also expressed in terms of days only.
    For example, 365 days are represented as "P365D" instead of "P1Y".

    Parameters
    ----------
    value : timedelta
        the timedelta object
    exclude_milliseconds : bool
        If it is True, the microsecond part is excluded.
    point_char : str
        the point character. For example, if "," is specified, 500 milliseconds would be "PT0,5S".

    Returns
    -------
    str
        the ISO-8601 format of the received timedelta
    """
    if value < dt.timedelta():
        result = "-P"
        value = -1 * value
    else:
        result = "P"

    days, hours, minutes, seconds, _, _ = TimedeltaTuple.of(value)

    # add decimal part into seconds
    if not exclude_milliseconds and value.microseconds != 0:
        seconds += Decimal(value.microseconds).scaleb(-6).normalize()

    if value.days > 0:
        result += f"{days}D"

    result_time_part = ""
    if hours != 0:
        result_time_part += f"{hours}H"
    if minutes != 0:
        result_time_part += f"{minutes}M"
    if seconds != 0:
        result_time_part += f"{seconds}S".replace(".", point_char)

    if len(result_time_part) > 0:
        result += "T" + result_time_part

    # "P" is invalid even if the value equals 0
    if len(result) <= 1:
        return "PT0S"

    return result


def from_str(value: str) -> dt.timedelta:
    """Converts a string of the format to timedelta.

    Examples
    --------
    >>> from datetime import timedelta
    >>> import randog.timedelta_util as timedelta_util
    >>>
    >>> assert timedelta_util.from_str("1h30m") == timedelta(hours=1, minutes=30)
    >>> assert timedelta_util.from_str("1d2h3m4s5ms6us") == timedelta(
    ...             days=1, hours=2, minutes=3, seconds=4, milliseconds=5, microseconds=6)

    Parameters
    ----------
    value : str
        the string of the format

    Returns
    -------
    timedelta
        the timedelta object for the received value
    """
    if not re.match(r"^([-+]?\d+[a-zA-Z]+)+$", value):
        raise TimedeltaExpressionError(f"illegal timedelta expression: {value}")

    result = dt.timedelta(0)

    try:
        for combined_term in re.finditer(r"(?:^|[-+])(?:\d+[a-zA-Z]+)+", value):
            result += _term_from_str(combined_term.group(0))
    except TimedeltaExpressionError as e:
        raise TimedeltaExpressionError(f"illegal timedelta expression: {value}") from e

    return result


__TO_FMT_MAP: t.Mapping[str, t.Callable[[dt.timedelta], str]] = {
    "%D": lambda td: str(td.days),
    "%H": lambda td: f"{td.seconds // 3600:02}",
    "%tH": lambda td: f"{td.total_seconds() // 3600:.0f}",
    "%M": lambda td: f"{(td.seconds % 3600) // 60:02}",
    "%tM": lambda td: f"{td.total_seconds() // 60:.0f}",
    "%S": lambda td: f"{td.seconds % 60:02}",
    "%tS": lambda td: f"{int(td.total_seconds())}",
    "%f": lambda td: f"{td.microseconds:06}",
}


def to_fmt(value: dt.timedelta, fmt: str) -> str:
    """Convert timedelta into the specified format

    The following is a list of all the format codes:

    * :code:`%D`: replaced by :code:`timedelta.days`
    * :code:`%H`: hours part (zero-padded to 2 digits)
    * :code:`%tH`: total duration in hours (rounded down)
    * :code:`%M`: minutes part (zero-padded to 2 digits)
    * :code:`%tH`: total duration in minutes (rounded down)
    * :code:`%S`: seconds part (zero-padded to 2 digits)
    * :code:`%tS`: total duration in seconds (rounded down)
    * :code:`%f`: decimal part in seconds (zero-padded to 6 digits)

    Parameters
    ----------
    value : timedelta
        the timedelta object
    fmt : str
        the format string

    Returns
    -------
    str
        the specified format of the specified timedelta
    """
    result = ""
    replace_map = {}

    i = 0
    while i < len(fmt):
        if fmt[i] == "%":
            if fmt[i + 1] == "t":
                fmt_exp = fmt[i : i + 3]
            else:
                fmt_exp = fmt[i : i + 2]

            if fmt_exp not in replace_map:
                try:
                    replace_map[fmt_exp] = __TO_FMT_MAP[fmt_exp](value)
                except KeyError:
                    raise ValueError("Invalid format string")
            result += replace_map[fmt_exp]

            i += len(fmt_exp)
        else:
            result += fmt[i]
            i += 1

    return result


def _term_from_str(term_str: str) -> dt.timedelta:
    if not re.match(r"^[-+]?(?:\d+[a-zA-Z]+)+$", term_str):
        raise ValueError(f"illegal timedelta term expression: {term_str}")

    sign = -1 if term_str.startswith("-") else 1
    result = dt.timedelta(0)

    try:
        for single_unit_term in re.finditer(r"(\d+)([a-zA-Z]+)", term_str):
            numeric_str, unit = single_unit_term.group(1, 2)
            numeric = int(numeric_str)
            result += _UNIT_TERM_CONSTRUCTOR[unit](numeric)
    except (TypeError, KeyError):
        raise TimedeltaExpressionError(f"illegal timedelta term expression: {term_str}")

    return sign * result


_UNIT_TERM_CONSTRUCTOR = {
    "d": lambda num: dt.timedelta(days=num),
    "h": lambda num: dt.timedelta(hours=num),
    "m": lambda num: dt.timedelta(minutes=num),
    "s": lambda num: dt.timedelta(seconds=num),
    "ms": lambda num: dt.timedelta(milliseconds=num),
    "us": lambda num: dt.timedelta(microseconds=num),
}


class TimedeltaExpressionError(ValueError):
    pass
