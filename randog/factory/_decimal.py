import math
import sys
import typing as t
from decimal import Decimal
from random import Random

from ._base import Factory, decide_rnd
from ._int import randint
from ..exceptions import FactoryConstructionError


def randdecimal(
    minimum: t.Optional[t.SupportsFloat] = None,
    maximum: t.Optional[t.SupportsFloat] = None,
    *,
    decimal_len: t.Optional[int] = None,
    p_inf: t.SupportsFloat = 0.0,
    n_inf: t.SupportsFloat = 0.0,
    nan: t.SupportsFloat = 0.0,
    rnd: t.Optional[Random] = None,
) -> Factory[Decimal]:
    """Return a factory generating random Decimal values.

    Parameters
    ----------
    minimum : float, optional
        the minimum
    maximum : float, optional
        the maximum
    decimal_len : int, optional
        the length of decimal part
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
    return DecimalRandomFactory(
        minimum,
        maximum,
        decimal_len=decimal_len,
        p_inf=p_inf,
        n_inf=n_inf,
        nan=nan,
        rnd=rnd,
    )


class DecimalRandomFactory(Factory[Decimal]):
    """factory generating random Decimal values"""

    _random: Random
    _p_inf: float
    _n_inf: float
    _nan: float
    _factory: Factory[int]
    _decimal_len: t.Optional[int]

    def __init__(
        self,
        minimum: t.Optional[t.SupportsFloat] = None,
        maximum: t.Optional[t.SupportsFloat] = None,
        *,
        decimal_len: t.Optional[int] = None,
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
        decimal_len : int, optional
            the length of decimal part
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
        self._random = decide_rnd(rnd)
        self._p_inf = float(p_inf)
        self._n_inf = float(n_inf)
        self._nan = float(nan)
        self._decimal_len = _calc_decimal_len(minimum, maximum, decimal_len)

        if (minimum is not None and math.isnan(minimum)) or (
            maximum is not None and math.isnan(maximum)
        ):
            raise FactoryConstructionError("minimum and maximum are must not be nan")
        if minimum == float("inf") or maximum == float("-inf"):
            raise FactoryConstructionError("empty range for randdecimal")
        if self._p_inf < 0.0 or self._n_inf < 0.0 or self._nan < 0.0:
            raise FactoryConstructionError(
                "the probabilities `p_inf`, `n_inf`, and `nan` must range from 0 to 1"
            )
        if self._p_inf + self._n_inf + self._nan > 1.0:
            raise FactoryConstructionError(
                "the sum of probabilities `p_inf`, `n_inf`, and `nan` "
                "must range from 0 to 1"
            )

        min_int, max_int = self._normalize_as_int(minimum, maximum, self._decimal_len)

        if min_int > max_int:
            raise FactoryConstructionError("empty range for randdecimal")

        self._factory = randint(min_int, max_int, rnd=self._random)

    def _next(self) -> Decimal:
        pre_weight = self._random.random()
        pre_weight -= self._p_inf
        if pre_weight < 0:
            return Decimal("inf")
        pre_weight -= self._n_inf
        if pre_weight < 0:
            return Decimal("-inf")
        pre_weight -= self._nan
        if pre_weight < 0:
            return Decimal("NaN")

        return self._next_finite()

    def _next_finite(self) -> Decimal:
        int_value = self._factory.next()
        return Decimal(int_value).scaleb(-self._decimal_len)

    @classmethod
    def _normalize_as_int(
        cls,
        minimum: t.Optional[t.SupportsFloat],
        maximum: t.Optional[t.SupportsFloat],
        decimal_len: int,
    ) -> t.Tuple[int, int]:
        default_range = 100

        if minimum == float("-inf"):
            minimum = -sys.float_info.max
        if maximum == float("inf"):
            maximum = sys.float_info.max

        minimum = _cast_to_decimal(minimum)
        maximum = _cast_to_decimal(maximum)

        if minimum is None and maximum is None:
            return 0, 10 ** max(0, decimal_len)
        elif minimum is None:
            max_int = math.floor(maximum.scaleb(decimal_len))
            return max_int - default_range, max_int
        elif maximum is None:
            min_int = math.ceil(minimum.scaleb(decimal_len))
            return min_int, min_int + default_range
        else:
            min_int = math.ceil(minimum.scaleb(decimal_len))
            max_int = math.floor(maximum.scaleb(decimal_len))
            return min_int, max_int


def _cast_to_decimal(value: t.Optional[t.SupportsFloat]) -> t.Optional[Decimal]:
    if value is None:
        return None
    elif isinstance(value, Decimal):
        return value
    else:
        try:
            return Decimal(t.cast(t.Any, value))
        except TypeError:
            return Decimal(float(value))


def _calc_decimal_len(
    minimum: t.Optional[t.SupportsFloat],
    maximum: t.Optional[t.SupportsFloat],
    decimal_len: t.Optional[int],
) -> t.Optional[int]:
    if decimal_len is not None:
        return decimal_len

    edge_exponents = []
    if isinstance(minimum, Decimal):
        edge_exponents.append(minimum.as_tuple().exponent)
    if isinstance(maximum, Decimal):
        edge_exponents.append(maximum.as_tuple().exponent)

    if len(edge_exponents) > 0:
        return -min(edge_exponents)

    if minimum is not None and maximum is not None and maximum > minimum:
        return -math.floor(math.log10(maximum - minimum))
    else:
        # TODO: 仕様を検討
        return 5
