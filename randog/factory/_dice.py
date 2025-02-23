import re
import typing as t
from random import Random

from ._base import Factory, decide_rnd
from ._int import randint

_RE_DICE_NOTATION = re.compile("([0-9]*)[dD]([0-9]+)")


def dice(
    code: str,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[int]:
    """Return a factory generating random int values by total of the dice faces.

    Parameters
    ----------
    code : str
        dice notation
    rnd : Random, optional
        random number generator to be used
    """
    return DiceRandomFactory(code, rnd=rnd)


class DiceRandomFactory(Factory[int]):
    """factory generating random int values by total of the dice faces."""

    _random: Random
    _base_factory: Factory[int]
    _dice_num: int

    def __init__(
        self,
        code: str,
        *,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random int values by total of the dice faces.

        Parameters
        ----------
        code : str
            dice notation
        rnd : Random, optional
            random number generator to be used
        """
        self._random = decide_rnd(rnd)

        code_match = re.fullmatch(_RE_DICE_NOTATION, code)
        if code_match is None:
            raise ValueError(f"invalid dice notation: {code}")

        self._dice_num = int(code_match.group(1) or "1")
        dice_max = int(code_match.group(2))

        self._base_factory = randint(1, dice_max, rnd=self._random)

    def _next(self) -> int:
        return sum(self._base_factory.iter(self._dice_num))
