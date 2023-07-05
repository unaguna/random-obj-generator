import datetime as dt
from decimal import Decimal
import re


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

    if value.days > 0:
        result += f"{value.days}D"

    minutes, seconds = divmod(value.seconds, 60)
    hours, minutes = divmod(minutes, 60)

    # add decimal part into seconds
    if not exclude_milliseconds and value.microseconds != 0:
        seconds += Decimal(value.microseconds).scaleb(-6).normalize()

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
    >>> assert timedelta_util.from_str("1d2h3m4s5ms6us") == timedelta(days=1, hours=2, minutes=3, seconds=4, milliseconds=5, microseconds=6)

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
