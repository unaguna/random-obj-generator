from random import Random
import typing as t

from ._base import Factory
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError


def randbool(
    prop_true: float = 0.5,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[bool]:
    """Return a factory generating random bool values.

    Parameters
    ----------
    prop_true : float
        the probability of True
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return BoolRandomFactory(prop_true, rnd=rnd)


class BoolRandomFactory(Factory[bool]):
    """factory generating random bool values"""

    _random: Random
    _prop_true: float

    def __init__(
        self,
        prop_true: float,
        *,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random bool values.

        Parameters
        ----------
        prop_true : float
            the probability of True
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = dfor(rnd, Random())
        self._prop_true = prop_true

        if self._prop_true < 0.0 or 1.0 < self._prop_true:
            raise FactoryConstructionError(
                "the probability `prob_true` must range from 0 to 1"
            )

    def next(self) -> int:
        return self._random.random() < self._prop_true
