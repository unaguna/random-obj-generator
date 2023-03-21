from random import Random
import typing as t

from ._base import Factory
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError


def randchoice(
    *values: t.Any,
    weights: t.Optional[t.Sequence[float]] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    """Return a factory choosing one of values.

    Parameters
    ----------
    values : Any
        the values
    weights : Sequence[float], optional
        the probabilities that each value is chosen.
        The length must equal to the number of values.
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        No values are specified.
    """
    return ChoiceRandomFactory(values, weights=weights, rnd=rnd)


class ChoiceRandomFactory(Factory[t.Any]):
    """factory choosing one of values."""

    _random: Random
    _weights: t.Optional[t.Sequence[float]]
    _values: t.Sequence[t.Any]

    def __init__(
        self,
        values: t.Sequence,
        weights: t.Optional[t.Sequence[float]] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory choosing one of values.

        Parameters
        ----------
        values : Any
            the values
        weights : Sequence[float], optional
            the probabilities that each value is chosen.
            The length must equal to the number of values.
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            No values are specified.
        """
        self._random = dfor(rnd, Random())
        self._weights = weights
        self._values = values

        if len(values) <= 0:
            raise FactoryConstructionError("empty candidate for randchoice")
        if self._weights is not None and len(self._weights) != len(self._values):
            raise FactoryConstructionError(
                "the number of weights must match the candidates"
            )

    def next(self) -> t.Any:
        return self._random.choices(self._values, self._weights)[0]
