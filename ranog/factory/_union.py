from random import Random
import typing as t

from ._base import Factory
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError


def union(
    *factories: Factory,
    weights: t.Optional[t.Sequence[float]] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    """Return a factory generating value by one of specified factories.

    Parameters
    ----------
    factories : Factory
        the factories
    weights : Sequence[float], optional
        the probabilities that each value is chose.
        The length must equal to the number of factories.
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        No factories are specified.
    """
    return UnionRandomFactory(*factories, weights=weights, rnd=rnd)


class UnionRandomFactory(Factory[t.Any]):
    """factory generating value by one of specified factories."""

    _random: Random
    _weights: t.Optional[t.Sequence[float]]
    _factories: t.Sequence[Factory]

    def __init__(
        self,
        *factories: Factory,
        weights: t.Optional[t.Sequence[float]] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating value by one of specified factories.

        Parameters
        ----------
        factories : Factory
            the factories
        weights : Sequence[float], optional
            the probabilities that each value is chose.
            The length must equal to the number of factories.
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            No factories are specified.
        """
        self._random = dfor(rnd, Random())
        self._weights = weights
        self._factories = factories

        if len(factories) <= 0:
            raise FactoryConstructionError(
                "the generating conditions are inconsistent: specify at least one factory"
            )
        if self._weights is not None and len(self._weights) != len(self._factories):
            raise FactoryConstructionError(
                "the generating conditions are inconsistent: the number of weights does not match the values"
            )

    def next(self) -> t.Any:
        return self._random.choices(self._factories, self._weights)[0].next()
