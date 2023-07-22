import typing as t
from random import Random

import rstr

from .._base import Factory


class StrRegexRandomFactory(Factory[str]):
    """factory generating random str values"""

    _regex: str

    def __init__(
        self,
        *,
        regex: t.Union[str, t.Pattern],
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random str values.

        Parameters
        ----------
        regex : str
            regular expression for generated string
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._regex = regex

    def next(self) -> str:
        return rstr.xeger(self._regex)
