from random import Random
import typing as t

from ..._utils.comp import ANYWAY_MAXIMUM
from .._base import Factory
from .._by_iterator import by_iterator
from ...exceptions import FactoryConstructionError
from ._inner import _iterrange


def iterrange_number(
    initial_value: t.Optional[t.Any] = None,
    maximum: t.Optional[t.Any] = None,
    step: t.Optional[t.Any] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    if initial_value is None:
        initial_value = 1
    if maximum is None:
        maximum = ANYWAY_MAXIMUM
    if step is None:
        step = 1
    resume_value = 1

    if not (initial_value <= maximum):
        raise FactoryConstructionError(
            "arguments of iterrange(initial_value, maximum) must satisfy "
            "initial_value <= maximum"
        )

    return by_iterator(_iterrange(initial_value, maximum, step, resume_value))
