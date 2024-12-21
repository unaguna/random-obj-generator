import datetime as dt
import numbers
from random import Random
import typing as t

from ..._utils.comp import ANYWAY_MAXIMUM
from .._base import Factory
from .._by_iterator import by_iterator
from ...exceptions import FactoryConstructionError
from ._inner import _iterrange


def iterrange_date(
    initial_value: dt.date = None,
    maximum: t.Optional[dt.date] = None,
    step: t.Union[dt.timedelta, int, None] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    if maximum is None:
        maximum = ANYWAY_MAXIMUM
    if step is None:
        step = dt.timedelta(days=1)
    elif isinstance(step, numbers.Integral):
        step = dt.timedelta(days=step)
    resume_value = initial_value

    if not (initial_value <= maximum):
        raise FactoryConstructionError(
            "arguments of iterrange(initial_value, maximum) must satisfy "
            "initial_value <= maximum"
        )
    if step.microseconds + step.seconds > 0:
        raise FactoryConstructionError(
            "step must be a day/days if initial_value is date"
        )

    return by_iterator(_iterrange(initial_value, maximum, step, resume_value))
