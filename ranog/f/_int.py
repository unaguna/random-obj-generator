from random import Random
import typing as t

from ._base import Factory
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError


def randint(
    a: int,
    b: int,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[int]:
    """整数乱数ファクトリー

    Parameters
    ----------
    a : int
        最小値
    b : int
        最大値
    rnd : int, optional
        使用する乱数生成器

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return IntRandomFactory(a, b, rnd=rnd)


class IntRandomFactory(Factory[int]):
    """整数乱数ファクトリー"""

    _random: Random
    _min: int
    _max: int

    def __init__(
        self,
        minimum: int,
        maximum: int,
        *,
        rnd: t.Optional[Random] = None,
    ):
        """整数乱数ファクトリー

        Parameters
        ----------
        minimum : int
            最小値
        maximum : int
            最大値
        rnd : int, optional
            使用する乱数生成器

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

    def next(self) -> int:
        return self._random.randint(self._min, self._max)
