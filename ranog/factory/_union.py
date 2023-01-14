from random import Random
import typing as t

from ._base import Factory
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError


def union(
    *factories: Factory,
    rnd: t.Optional[Random] = None,
) -> Factory[int]:
    """Return a factory generating value by one of specified factories.

    Parameters
    ----------
    factories : Factory
        the factories
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        No factories are specified.
    """
    return UnionRandomFactory(*factories, rnd=rnd)


class UnionRandomFactory(Factory[int]):
    """factory generating value by one of specified factories."""

    _random: Random
    _factories: t.Sequence[Factory]

    def __init__(
        self,
        *factories: Factory,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating value by one of specified factories.

        Parameters
        ----------
        factories : Factory
            the factories
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            No factories are specified.
        """
        self._random = dfor(rnd, Random())
        self._factories = factories

        if len(factories) <= 0:
            raise FactoryConstructionError(
                "the generating conditions are inconsistent: specify at least one factory"
            )

    def next(self) -> int:
        return self._random.choice(self._factories).next()
