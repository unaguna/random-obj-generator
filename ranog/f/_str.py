import typing as t
from random import Random

from ._base import Factory
from .._utils.nullsafe import dfor


def randstr(
    *,
    length: int = 8,
    charset: t.Optional[str] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[str]:
    """Return a factory generating random str values.

    Parameters
    ----------
    length : int, default=8
        length of generated string
    charset : str, optional
        characters to be used
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return StrRandomFactory(length=length, charset=charset, rnd=rnd)


class StrRandomFactory(Factory[str]):
    """factory generating random int values"""

    _random: Random

    def __init__(
        self,
        *,
        length: int = 8,
        charset: t.Optional[str] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random str values.

        Parameters
        ----------
        length : int, default=8
            length of generated string
        charset : str, optional
            characters to be used
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = dfor(rnd, Random())

    def next(self) -> int:
        pass
