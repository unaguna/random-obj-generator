import typing as t
from decimal import Decimal
from random import Random

from ._base import Factory
from ._float import randfloat
from .._utils.nullsafe import dfor


def randdecimal(
    a: t.Optional[t.SupportsFloat] = None,
    b: t.Optional[t.SupportsFloat] = None,
    *,
    p_inf: t.SupportsFloat = 0.0,
    n_inf: t.SupportsFloat = 0.0,
    nan: t.SupportsFloat = 0.0,
    rnd: t.Optional[Random] = None,
) -> Factory[Decimal]:
    """Return a factory generating random Decimal values.

    Parameters
    ----------
    a : float, optional
        the minimum
    b : float, optional
        the maximum
    p_inf : float, default=0
        the probability of positive infinity
    n_inf : float, default=0
        the probability of negative infinity
    nan : float, default=0
        the probability of NaN
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return DecimalRandomFactory(a, b, p_inf=p_inf, n_inf=n_inf, nan=nan, rnd=rnd)


class DecimalRandomFactory(Factory[Decimal]):
    """factory generating random Decimal values"""

    _random: Random
    _factory: Factory[float]

    def __init__(
        self,
        minimum: t.Optional[t.SupportsFloat] = None,
        maximum: t.Optional[t.SupportsFloat] = None,
        *,
        p_inf: t.SupportsFloat = 0.0,
        n_inf: t.SupportsFloat = 0.0,
        nan: t.SupportsFloat = 0.0,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random Decimal values.

        Parameters
        ----------
        minimum : float, optional
            the minimum
        maximum : float, optional
            the maximum
        p_inf : float, default=0
            the probability of positive infinity
        n_inf : float, default=0
            the probability of negative infinity
        nan : float, default=0
            the probability of NaN
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = dfor(rnd, Random())
        self._factory = randfloat(
            minimum, maximum, p_inf=p_inf, n_inf=n_inf, nan=nan, rnd=self._random
        )

    def next(self) -> Decimal:
        pre_value = self._factory.next()

        return Decimal(pre_value)
