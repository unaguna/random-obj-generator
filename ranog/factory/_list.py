import typing as t
from random import Random

from ._base import Factory
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError


def randlist(
    *items: Factory,
    length: t.Optional[int] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[list]:
    """Return a factory generating random list.

    Parameters
    ----------
    items : Factory
        the factories of each item
    length : int, optional
        length of generated list.
        If not specified, the length of generated list will be equals to the number of `items`.
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return ListRandomFactory(*items, length=length, rnd=rnd)


class ListRandomFactory(Factory[list]):
    """factory generating random list values"""

    _random: Random
    _length: int
    _factories: t.Sequence[Factory]

    def __init__(
        self,
        *items: Factory,
        length: t.Optional[int] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random list values.

        Parameters
        ----------
        items : Factory
            the factories of each item
        length : int, optional
            length of generated list.
            If not specified, the length of generated list will be equals to the number of `items`.
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = dfor(rnd, Random())
        self._length = dfor(length, len(items))
        self._factories = items

        if self._length > 0 and len(self._factories) == 0:
            raise FactoryConstructionError("the generating conditions are inconsistent")

    def _factory_generator(self, length) -> t.Iterator[Factory]:
        generated = 0
        last_factory = None
        for factory in self._factories:
            if generated >= length:
                return
            yield factory
            last_factory = factory
            generated += 1
        while generated < length:
            yield last_factory
            generated += 1

    def _next_generator(self) -> t.Iterator[t.Any]:
        length = self._length
        for factory in self._factory_generator(length):
            yield factory.next()

    def next(self) -> list:
        return list(self._next_generator())
