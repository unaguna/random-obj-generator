import typing as t
from random import Random

import rstr

from .._base import Factory, _global_rnd
from ..._utils.nullsafe import dfor


class StrRegexRandomFactory(Factory[str]):
    """factory generating random str values"""

    _xeger: rstr.Xeger
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
        self._xeger = rstr.Xeger(*_get_xeger_args(rnd))

    def _next(self) -> str:
        return self._xeger.xeger(self._regex)


def _get_xeger_args(rnd: t.Optional[Random]) -> t.Sequence[t.Any]:
    rnd = dfor(rnd, _global_rnd())

    if rnd is not None:
        return [rnd]
    else:
        return []
