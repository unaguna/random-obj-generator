from random import Random
import typing as t

from ._base import Factory
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError


def randfloat(
    a: float,
    b: float,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[float]:
    """Return a factory generating random float values.

    Parameters
    ----------
    a : float
        the minimum
    b : float
        the maximum
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return FloatRandomFactory(a, b, rnd=rnd)


class FloatRandomFactory(Factory[float]):
    """factory generating random float values"""

    _random: Random
    _min: float
    _max: float

    def __init__(
        self,
        minimum: float,
        maximum: float,
        *,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random float values.

        Parameters
        ----------
        minimum : float
            the minimum
        maximum : float
            the maximum
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = dfor(rnd, Random())
        self._min = minimum
        self._max = maximum

        if minimum > maximum:
            raise FactoryConstructionError("the generating conditions are inconsistent")

    def next(self) -> float:
        weight = self._random.random()
        return self._max * weight + self._min * (1 - weight)
