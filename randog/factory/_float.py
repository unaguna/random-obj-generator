import typing as t
from random import Random

from ._base import Factory, decide_rnd
from ._int import randint
from .._utils import floatutils
from ..exceptions import FactoryConstructionError


def randfloat(
    minimum: t.Optional[t.SupportsFloat] = None,
    maximum: t.Optional[t.SupportsFloat] = None,
    *,
    p_inf: t.SupportsFloat = 0.0,
    n_inf: t.SupportsFloat = 0.0,
    nan: t.SupportsFloat = 0.0,
    weight: t.Literal["flat", "log_flat"] = "flat",
    rnd: t.Optional[Random] = None,
) -> Factory[float]:
    """Return a factory generating random float values.

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
    weight : "flat"|"log_flat", default="flat"
        probability distribution. If 'flat', the distribution is uniform.
        If 'log_flat', the distribution of digits (log with a base of 2) is uniform.
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    if weight == "flat":
        return FloatRandomFactory(
            minimum,
            maximum,
            p_inf=p_inf,
            n_inf=n_inf,
            nan=nan,
            rnd=rnd,
        )
    elif weight == "log_flat":
        return FloatExpRandomFactory(
            minimum,
            maximum,
            p_inf=p_inf,
            n_inf=n_inf,
            nan=nan,
            rnd=rnd,
        )
    else:
        raise ValueError(f"illegal weight: {weight}")


class FloatRandomFactory(Factory[float]):
    """factory generating random float values"""

    _random: Random
    _min: float
    _max: float
    _p_inf: float
    _n_inf: float
    _nan: float

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
        """Return a factory generating random float values.

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
        self._random = decide_rnd(rnd)
        self._min, self._max = self._normalize(minimum, maximum)
        self._p_inf = float(p_inf)
        self._n_inf = float(n_inf)
        self._nan = float(nan)

        if self._min > self._max:
            raise FactoryConstructionError("empty range for randfloat")
        if self._p_inf < 0.0 or self._n_inf < 0.0 or self._nan < 0.0:
            raise FactoryConstructionError(
                "the probabilities `p_inf`, `n_inf`, and `nan` must range from 0 to 1"
            )
        if self._p_inf + self._n_inf + self._nan > 1.0:
            raise FactoryConstructionError(
                "the sum of probabilities `p_inf`, `n_inf`, and `nan` "
                "must range from 0 to 1"
            )

    def _next(self) -> float:
        pre_weight = self._random.random()
        pre_weight -= self._p_inf
        if pre_weight < 0:
            return float("inf")
        pre_weight -= self._n_inf
        if pre_weight < 0:
            return float("-inf")
        pre_weight -= self._nan
        if pre_weight < 0:
            return float("NaN")

        weight = self._random.random()
        return self._max * weight + self._min * (1 - weight)

    @classmethod
    def _normalize(
        cls,
        minimum: t.Optional[t.SupportsFloat],
        maximum: t.Optional[t.SupportsFloat],
    ) -> t.Tuple[float, float]:
        default_range = 1.0

        if minimum is None and maximum is None:
            return 0.0, 1.0
        elif minimum is None:
            maximum = float(maximum)
            return maximum - default_range, maximum
        elif maximum is None:
            minimum = float(minimum)
            return minimum, minimum + default_range
        else:
            return float(minimum), float(maximum)


class FloatExpRandomFactory(Factory[float]):
    _random: Random
    _exp_factory: Factory[int]
    _min: float
    _max: float
    _min_exp: int
    _max_exp: int
    _fraction_minmax_of_min_exp: t.Tuple[int, int]
    _fraction_minmax_of_max_exp: t.Tuple[int, int]
    _p_inf: float
    _n_inf: float
    _nan: float

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
        self._random = decide_rnd(rnd)
        self._min, self._max = self._normalize(minimum, maximum)
        self._p_inf = float(p_inf)
        self._n_inf = float(n_inf)
        self._nan = float(nan)

        if self._min > self._max:
            raise FactoryConstructionError("empty range for randfloat")
        if self._p_inf < 0.0 or self._n_inf < 0.0 or self._nan < 0.0:
            raise FactoryConstructionError(
                "the probabilities `p_inf`, `n_inf`, and `nan` must range from 0 to 1"
            )
        if self._p_inf + self._n_inf + self._nan > 1.0:
            raise FactoryConstructionError(
                "the sum of probabilities `p_inf`, `n_inf`, and `nan` "
                "must range from 0 to 1"
            )

        self._min_exp, self._min_fraction = self._calc_exp_and_fraction(
            self._min, for_min=True
        )
        self._max_exp, self._max_fraction = self._calc_exp_and_fraction(
            self._max, for_max=True
        )
        self._exp_factory = randint(self._min_exp, self._max_exp, rnd=self._random)

        if self._min_exp == self._max_exp:
            if self._min_exp < 0:
                self._fraction_minmax_of_min_exp = (
                    self._max_fraction,
                    self._min_fraction,
                )
                self._fraction_minmax_of_max_exp = (
                    self._max_fraction,
                    self._min_fraction,
                )
            else:
                self._fraction_minmax_of_min_exp = (
                    self._min_fraction,
                    self._max_fraction,
                )
                self._fraction_minmax_of_max_exp = (
                    self._min_fraction,
                    self._max_fraction,
                )
        else:
            if self._min_exp < 0:
                self._fraction_minmax_of_min_exp = 0, self._min_fraction
            else:
                self._fraction_minmax_of_min_exp = self._min_fraction, 2**52 - 1
            if self._max_exp < 0:
                self._fraction_minmax_of_max_exp = self._max_fraction, 2**52 - 1
            else:
                self._fraction_minmax_of_max_exp = 0, self._max_fraction

    def _next(self) -> float:
        pre_weight = self._random.random()
        pre_weight -= self._p_inf
        if pre_weight < 0:
            return float("inf")
        pre_weight -= self._n_inf
        if pre_weight < 0:
            return float("-inf")
        pre_weight -= self._nan
        if pre_weight < 0:
            return float("NaN")

        exp = self._exp_factory.next()
        fraction = self._next_fraction(exp)

        return self._calc_float_from_exp_and_fraction(exp, fraction)

    def _next_fraction(self, next_exp: int) -> int:
        if next_exp == 0:
            return 0
        elif next_exp == self._min_exp:
            return self._random.randint(*self._fraction_minmax_of_min_exp)
        elif next_exp == self._max_exp:
            return self._random.randint(*self._fraction_minmax_of_max_exp)
        else:
            return self._random.randrange(0, 2**52)

    @classmethod
    def _normalize(
        cls,
        minimum: t.Optional[t.SupportsFloat],
        maximum: t.Optional[t.SupportsFloat],
    ) -> t.Tuple[float, float]:
        default_range = 1.0

        if minimum is None and maximum is None:
            return 0.0, 1.0
        elif minimum is None:
            maximum = float(maximum)
            return maximum - default_range, maximum
        elif maximum is None:
            minimum = float(minimum)
            return minimum, minimum + default_range
        else:
            return float(minimum), float(maximum)

    @classmethod
    def _calc_exp_and_fraction(
        cls, edge: float, for_min: bool = False, for_max: bool = False
    ) -> t.Tuple[int, int]:
        sign, exp, fraction = floatutils.to_tuple(edge)

        # don't contain negative min and positive max into random value range
        if for_min and sign == 1 or for_max and sign == 0:
            sign, exp, fraction = floatutils.next_to_0(sign, exp, fraction)

        if sign == 1:
            exp *= -1
        return exp, fraction

    @classmethod
    def _calc_float_from_exp_and_fraction(cls, exp: int, fraction: int) -> float:
        sign = t.cast(t.Literal[0, 1], 1 if exp < 0 else 0)
        unsigned_exp = abs(exp)

        return floatutils.parse(sign, unsigned_exp, fraction)
