from random import Random
import typing as t

from ._base import Factory
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError


def randchoice(
    *values: t.Any,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    """Return a factory choosing one of values.

    Parameters
    ----------
    values : Any
        the values
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        No values are specified.
    """
    return ChoiceRandomFactory(values, rnd=rnd)


class ChoiceRandomFactory(Factory[t.Any]):
    """factory choosing one of values."""

    _random: Random
    _values: t.Sequence[t.Any]

    def __init__(
        self,
        values: t.Sequence,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory choosing one of values.

        Parameters
        ----------
        values : Any
            the values
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            No values are specified.
        """
        self._random = dfor(rnd, Random())
        self._values = values

        if len(values) <= 0:
            raise FactoryConstructionError(
                "the generating conditions are inconsistent: specify at least one value"
            )

    def next(self) -> t.Any:
        return self._random.choice(self._values)
