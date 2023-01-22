import typing as t
from random import Random

from ._base import Factory
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError

T = t.TypeVar("T", bound=t.Sequence)


def randlist(
    *items: Factory,
    length: t.Optional[int] = None,
    type: t.Callable[[t.Iterator[t.Any]], T] = list,
    rnd: t.Optional[Random] = None,
    items_list: t.Optional[t.Sequence[Factory]] = None,
) -> Factory[list]:
    """Return a factory generating random list.

    Parameters
    ----------
    items : Factory
        the factories of each item. If `items_list` is specified, `items` will be ignored.
    length : int, optional
        length of generated list.
        If not specified, the length of generated list will be equals to the number of `items`.
    type : type, default=list
        the type of generated object
    rnd : Random, optional
        random number generator to be used
    items_list : Sequence[Factory], optional
        the factories of each item. Use when positional arguments cannot be specified.

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    if items_list is not None:
        items = items_list

    return ListRandomFactory(items, length=length, type=type, rnd=rnd)


class ListRandomFactory(Factory[list], t.Generic[T]):
    """factory generating random list values"""

    _random: Random
    _length: int
    _factories: t.Sequence[Factory]
    _type: t.Callable[[t.Iterator[t.Any]], T]

    def __init__(
        self,
        items: t.Sequence[Factory],
        *,
        length: t.Optional[int] = None,
        type: t.Callable[[t.Iterator[t.Any]], T] = list,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random list values.

        Parameters
        ----------
        items : t.Sequence[Factory]
            the factories of each item
        length : int, optional
            length of generated list.
            If not specified, the length of generated list will be equals to the number of `items`.
        type : type, default=list
            the type of generated object
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
        self._type = type

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

    def next(self) -> T:
        return self._type(self._next_generator())
