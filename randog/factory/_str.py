import string
import typing as t
from random import Random

from ._base import Factory
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError


def randstr(
    *,
    length: t.Union[int, Factory[int]] = 8,
    charset: t.Optional[str] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[str]:
    """Return a factory generating random str values.

    Parameters
    ----------
    length : int|Factory[int], default=8
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
    _length: t.Union[int, Factory[int]]
    _charset: str

    def __init__(
        self,
        *,
        length: t.Union[int, Factory[int]] = 8,
        charset: t.Optional[str] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random str values.

        Parameters
        ----------
        length : int|Factory[int], default=8
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
        self._length = length
        self._charset = dfor(charset, string.ascii_letters + string.digits)

        if isinstance(self._length, Factory) and len(self._charset) == 0:
            raise FactoryConstructionError(
                "the charset for randstr() must not be empty if length is at random"
            )
        if (
            not isinstance(self._length, Factory)
            and self._length > 0
            and len(self._charset) == 0
        ):
            raise FactoryConstructionError(
                "the charset for randstr() must not be empty if length is positive"
            )

    def next(self) -> str:
        length = self._next_length()
        return "".join(self._random.choices(self._charset, k=length))

    def _next_length(self) -> int:
        if isinstance(self._length, Factory):
            return self._length.next()
        else:
            return self._length
