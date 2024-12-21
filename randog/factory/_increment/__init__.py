import datetime as dt
import numbers
import typing as t
from random import Random

from ._increment_date import increment_date
from ._increment_datetime import increment_datetime
from ._increment_number import increment_number
from ._increment_timedelta import increment_timedelta
from .._base import Factory


@t.overload
def increment(
    initial_value: t.Optional[int] = None,
    maximum: t.Optional[int] = None,
    step: t.Optional[int] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[int]: ...


@t.overload
def increment(
    initial_value: dt.datetime,
    maximum: t.Optional[dt.datetime] = None,
    step: t.Optional[dt.timedelta] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.datetime]: ...


@t.overload
def increment(
    initial_value: dt.date,
    maximum: t.Optional[dt.date] = None,
    step: t.Optional[dt.timedelta] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.date]: ...


@t.overload
def increment(
    initial_value: dt.timedelta,
    maximum: t.Optional[dt.timedelta] = None,
    step: t.Optional[dt.timedelta] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.timedelta]: ...


def increment(
    initial_value: t.Optional[t.Any] = None,
    maximum: t.Optional[t.Any] = None,
    step: t.Optional[t.Any] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    """Return a factory which returns sequential numbers.

    Parameters
    ----------
    initial_value : optional
        the first value
    maximum : optional
        the maximum value. If the generated value reaches the maximum value,
        1 is generated next.
        If the maximum value is not specified, it is not reset to 1.
    step : optional
        difference between generated values
    rnd : Random, optional
        It is not normally used, but it can be accepted as an argument
        to match other Factory construction functions.

    Raises
    ------
    FactoryConstructionError
        if it is not satisfied `initial_value <= maximum`
    """
    if initial_value is None or isinstance(initial_value, numbers.Real):
        return increment_number(initial_value, maximum, step, rnd=rnd)
    elif isinstance(initial_value, dt.datetime):
        return increment_datetime(initial_value, maximum, step, rnd=rnd)
    elif isinstance(initial_value, dt.date):
        return increment_date(initial_value, maximum, step, rnd=rnd)
    elif isinstance(initial_value, dt.timedelta):
        return increment_timedelta(initial_value, maximum, step, rnd=rnd)
    else:
        raise TypeError(
            "cannot create 'increment' factory with initial_value "
            f"type of {type(initial_value)}"
        )
