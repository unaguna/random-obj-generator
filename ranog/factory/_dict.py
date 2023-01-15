from dataclasses import dataclass
from random import Random
import typing as t

from ._base import Factory
from .._utils.nullsafe import dfor


_item_tuple = t.Tuple[Factory, float]


@dataclass
class DictItem:
    factory: Factory
    prop_exists: float

    @t.overload
    def __init__(self, factory: Factory):
        ...

    @t.overload
    def __init__(self, factory: Factory, prop_exists: float):
        ...

    @t.overload
    def __init__(self, item: _item_tuple):
        ...

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Factory):
            self.prop_exists = 1.0
            self.factory = args[0]
        elif len(args) == 1 and isinstance(args[0], tuple):
            self.prop_exists = args[0][1]
            self.factory = args[0][0]
        elif len(args) == 2:
            self.prop_exists = args[0]
            self.factory = args[1]
        else:
            raise ValueError()


def randdict(
    items: t.Mapping[t.Hashable, t.Union[Factory, _item_tuple, DictItem]],
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[int]:
    """Return a factory generating random dict.

    Parameters
    ----------
    items : Mapping
        the factories of each key
    rnd : Random, optional
        random number generator to be used
    """
    items_normalized = {
        k: v if isinstance(v, DictItem) else DictItem(v) for k, v in items.items()
    }

    return DictRandomFactory(items_normalized, rnd=rnd)


class DictRandomFactory(Factory[dict]):
    """factory generating random dict"""

    _random: Random
    _items: t.Mapping[t.Hashable, DictItem]

    def __init__(
        self,
        items: t.Mapping[t.Hashable, DictItem],
        *,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random dict.

        Parameters
        ----------
        items : Mapping
            the factories of each key
        rnd : Random, optional
            random number generator to be used
        """
        self._random = dfor(rnd, Random())
        self._items = items

    def next(self) -> dict:
        result = {}

        for key, cond in self._items.items():
            if self._random.random() < cond.prop_exists:
                result[key] = cond.factory.next()

        return result
