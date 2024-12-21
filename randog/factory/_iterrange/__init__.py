import datetime as dt
import numbers
import typing as t
from random import Random

from ._iterrange_date import iterrange_date
from ._iterrange_datetime import iterrange_datetime
from ._iterrange_number import iterrange_number
from ._iterrange_timedelta import iterrange_timedelta
from .._base import Factory


@t.overload
def iterrange(
    initial_value: t.Optional[int] = None,
    maximum: t.Optional[int] = None,
    step: t.Optional[int] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[int]: ...


@t.overload
def iterrange(
    initial_value: dt.datetime,
    maximum: t.Optional[dt.datetime] = None,
    step: t.Optional[dt.timedelta] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.datetime]: ...


@t.overload
def iterrange(
    initial_value: dt.date,
    maximum: t.Optional[dt.date] = None,
    step: t.Optional[dt.timedelta] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.date]: ...


@t.overload
def iterrange(
    initial_value: dt.timedelta,
    maximum: t.Optional[dt.timedelta] = None,
    step: t.Optional[dt.timedelta] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.timedelta]: ...


def iterrange(
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
        return iterrange_number(initial_value, maximum, step, rnd=rnd)
    elif isinstance(initial_value, dt.datetime):
        return iterrange_datetime(initial_value, maximum, step, rnd=rnd)
    elif isinstance(initial_value, dt.date):
        return iterrange_date(initial_value, maximum, step, rnd=rnd)
    elif isinstance(initial_value, dt.timedelta):
        return iterrange_timedelta(initial_value, maximum, step, rnd=rnd)
    else:
        raise TypeError(
            "cannot create 'iterrange' factory with initial_value "
            f"type of {type(initial_value)}"
        )
