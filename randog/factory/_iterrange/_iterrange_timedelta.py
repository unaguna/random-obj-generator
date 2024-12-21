import datetime as dt
from random import Random
import typing as t

from ..._utils.comp import ANYWAY_MAXIMUM
from .._base import Factory
from .._by_iterator import by_iterator
from ...exceptions import FactoryConstructionError
from ._inner import _iterrange


def iterrange_timedelta(
    initial_value: dt.timedelta,
    maximum: t.Optional[dt.timedelta] = None,
    step: t.Optional[dt.timedelta] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.timedelta]:
    if maximum is None:
        maximum = ANYWAY_MAXIMUM
    if step is None:
        step = dt.timedelta(seconds=1)
    resume_value = initial_value

    if not (initial_value <= maximum):
        raise FactoryConstructionError(
            "arguments of iterrange(initial_value, maximum) must satisfy "
            "initial_value <= maximum"
        )

    return by_iterator(_iterrange(initial_value, maximum, step, resume_value))
