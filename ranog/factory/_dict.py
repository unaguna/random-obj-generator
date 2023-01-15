from dataclasses import dataclass
from random import Random
import typing as t

from ._base import Factory
from .._utils.nullsafe import dfor


_item_tuple = t.Tuple[Factory, float]


def randdict(
    items: t.Mapping[t.Hashable, t.Union[Factory, _item_tuple]],
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

    def normalize_item(item: t.Union[Factory, _item_tuple]) -> _Item:
        if isinstance(item, Factory):
            return _Item(1.0, item)
        else:
            return _Item(item[1], item[0])

    items_normalized = {k: normalize_item(v) for k, v in items.items()}

    return DictRandomFactory(items_normalized, rnd=rnd)


@dataclass
class _Item:
    prop_exists: float
    factory: Factory


class DictRandomFactory(Factory[dict]):
    """factory generating random dict"""

    _random: Random
    _items: t.Mapping[t.Hashable, _Item]

    def __init__(
        self,
        items: t.Mapping[t.Hashable, _Item],
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
