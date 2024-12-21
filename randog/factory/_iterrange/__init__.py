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
    cyclic: bool = False,
    rnd: t.Optional[Random] = None,
) -> Factory[int]: ...


@t.overload
def iterrange(
    initial_value: dt.datetime,
    maximum: t.Optional[dt.datetime] = None,
    step: t.Optional[dt.timedelta] = None,
    *,
    cyclic: bool = False,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.datetime]: ...


@t.overload
def iterrange(
    initial_value: dt.date,
    maximum: t.Optional[dt.date] = None,
    step: t.Optional[dt.timedelta] = None,
    *,
    cyclic: bool = False,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.date]: ...


@t.overload
def iterrange(
    initial_value: dt.timedelta,
    maximum: t.Optional[dt.timedelta] = None,
    step: t.Optional[dt.timedelta] = None,
    *,
    cyclic: bool = False,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.timedelta]: ...


def iterrange(
    initial_value: t.Optional[t.Any] = None,
    maximum: t.Optional[t.Any] = None,
    step: t.Optional[t.Any] = None,
    *,
    cyclic: bool = False,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    """Return a factory which returns sequential numbers.

    This is a factory that generates values that are shifted by the value specified in
    step from `initial_value`.

    If you specify maximum, it will emit StopIterator when a value that exceeds it is
    about to be generated. However, if cyclic is True, it will not emit StopIterator,
    but will restart generating from initial_value.

    Parameters
    ----------
    initial_value
        the first value
    maximum : optional
        the maximum value
    step : optional
        difference between generated values
    cyclic : bool
        If it is True, the next value of `maximum` will be `initial_value`.
    rnd : Random, optional
        It is not normally used, but it can be accepted as an argument
        to match other Factory construction functions.

    Raises
    ------
    FactoryConstructionError
        if it is not satisfied `initial_value <= maximum`
    """
    if initial_value is None or isinstance(initial_value, numbers.Real):
        return iterrange_number(initial_value, maximum, step, cyclic=cyclic, rnd=rnd)
    elif isinstance(initial_value, dt.datetime):
        return iterrange_datetime(initial_value, maximum, step, cyclic=cyclic, rnd=rnd)
    elif isinstance(initial_value, dt.date):
        return iterrange_date(initial_value, maximum, step, cyclic=cyclic, rnd=rnd)
    elif isinstance(initial_value, dt.timedelta):
        return iterrange_timedelta(initial_value, maximum, step, cyclic=cyclic, rnd=rnd)
    else:
        raise TypeError(
            "cannot create 'iterrange' factory with initial_value "
            f"type of {type(initial_value)}"
        )
