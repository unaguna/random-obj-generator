from random import Random
import typing as t

from ..._utils.comp import ANYWAY_MAXIMUM, ANYWAY_MINIMUM
from .._base import Factory
from .._by_iterator import by_iterator
from ...exceptions import FactoryConstructionError
from ._inner import _iterrange


def iterrange_number(
    initial_value: t.Optional[t.Any] = None,
    maximum: t.Optional[t.Any] = None,
    step: t.Optional[t.Any] = None,
    *,
    cyclic: bool = False,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    if step is not None and step < 0:
        minimum = maximum
        maximum = None
    else:
        minimum = None
    if initial_value is None:
        initial_value = 1
    if minimum is None:
        minimum = ANYWAY_MINIMUM
    if maximum is None:
        maximum = ANYWAY_MAXIMUM
    if step is None:
        step = 1
    resume_value = initial_value

    if step >= 0:
        if not (initial_value <= maximum):
            raise FactoryConstructionError(
                "arguments of iterrange(initial_value, maximum) must satisfy "
                "initial_value <= maximum"
            )
    else:
        if not (initial_value >= minimum):
            raise FactoryConstructionError(
                "arguments of iterrange(initial_value, maximum) must satisfy "
                "maximum <= initial_value if step < 0"
            )

    return by_iterator(
        _iterrange(initial_value, minimum, maximum, step, resume_value, cyclic=cyclic)
    )
