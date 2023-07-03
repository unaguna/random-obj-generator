import datetime as dt
import re


def from_str(value: str) -> dt.timedelta:
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
