import typing as t
from random import Random

from ._base import Factory, decide_rnd
from .._utils.nullsafe import dfor


def randbytes(
    *,
    length: t.Union[int, Factory[int], None] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[bytes]:
    """Return a factory generating random bytes values.

    Parameters
    ----------
    length : int|Factory[int], default=8
        length of generated string
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return BytesRandomFactory(length=length, rnd=rnd)


class BytesRandomFactory(Factory[bytes]):
    """factory generating random bytes values"""

    _random: Random
    _length: t.Union[int, Factory[int]]

    def __init__(
        self,
        *,
        length: t.Union[int, Factory[int], None] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random bytes values.

        Parameters
        ----------
        length : int|Factory[int], default=8
            length of generated bytes
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = decide_rnd(rnd)
        self._length = dfor(length, 8)

    def _next(self) -> bytes:
        length = self._next_length()
        if length == 0:
            return b""
        return self._random.getrandbits(8 * length).to_bytes(length, "big")

    def _next_length(self) -> int:
        if isinstance(self._length, Factory):
            return self._length.next()
        else:
            return self._length
