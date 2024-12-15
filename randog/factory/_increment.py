import math
from random import Random
import typing as t

from ._logging import logger
from ._base import Factory
from ._by_iterator import by_iterator
from ..exceptions import FactoryConstructionError


def increment(
    initial_value: t.Optional[int] = None,
    maximum: t.Optional[int] = None,
    step: t.Optional[int] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    """Return a factory which returns sequential numbers.

    Parameters
    ----------
    initial_value : int, optional
        the first value
    maximum : int, optional
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
    if initial_value is None:
        initial_value = 1
    if maximum is None:
        maximum = math.inf
    if step is None:
        step = 1

    if not (initial_value <= maximum):
        raise FactoryConstructionError(
            "arguments of increment(initial_value, maximum) must satisfy "
            "initial_value <= maximum"
        )

    return by_iterator(_increment(initial_value, maximum, step))


def _increment(initial_value: int, maximum: int, step: int) -> t.Iterator[int]:
    next_value = initial_value
    while True:
        yield next_value
        next_value += step

        if next_value > maximum:
            logger.debug("increment() has reached its maximum value and resumes from 1")
            next_value = 1
