import typing as t
from random import Random

from ._base import Factory, decide_rnd
from ..exceptions import FactoryConstructionError
from ..rangeutils import interval, IntInterval


def randint(
    minimum: int,
    maximum: int,
    *,
    distribution: t.Literal["uniform", "exp_uniform"] = "uniform",
    rnd: t.Optional[Random] = None,
) -> Factory[int]:
    """Return a factory generating random int values.

    Parameters
    ----------
    minimum : int
        the minimum
    maximum : int
        the maximum
    distribution : "uniform"|"exp_uniform", default="flat"
        probability distribution. If 'flat', the distribution is uniform.
        If 'exp_uniform', the distribution of digits (log with a base of 2) is uniform.
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    if distribution is None or distribution == "uniform":
        return IntRandomFactory(minimum, maximum, rnd=rnd)
    elif distribution == "exp_uniform":
        return IntExpRandomFactory(minimum, maximum, rnd=rnd)
    else:
        raise ValueError(f"illegal distribution: {distribution}")


class IntRandomFactory(Factory[int]):
    """factory generating random int values"""

    _random: Random
    _min: int
    _max: int

    def __init__(
        self,
        minimum: int,
        maximum: int,
        *,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random int values.

        Parameters
        ----------
        minimum : int
            the minimum
        maximum : int
            the maximum
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = decide_rnd(rnd)
        self._min = minimum
        self._max = maximum

        if minimum > maximum:
            raise FactoryConstructionError("empty range for randint")

    def _next(self) -> int:
        return self._random.randint(self._min, self._max)


class IntExpRandomFactory(Factory[int]):
    """factory generating random int values"""

    _random: Random
    _min: int
    _max: int
    _range_of_min_bit_len: IntInterval
    _range_of_max_bit_len: IntInterval
    _prop_min_bit_len: float
    _prop_max_bit_len: float

    _range_of_non_edge_signed_bit_len: IntInterval
    """positive a means 2^(a-1), negative -a means -2^(a-1), 0 means 0"""

    def __init__(
        self,
        minimum: int,
        maximum: int,
        *,
        rnd: t.Optional[Random] = None,
    ):
        self._random = decide_rnd(rnd)
        self._min = minimum
        self._max = maximum

        if minimum > maximum:
            raise FactoryConstructionError("empty range for randint")

        min_bit_len = self._min.bit_length()
        signed_min_bit_len = min_bit_len * _sign(self._min)
        max_bit_len = self._max.bit_length()
        signed_max_bit_len = max_bit_len * _sign(self._max)

        if min_bit_len == max_bit_len:
            self._range_of_min_bit_len = interval(self._min, self._max)
            self._range_of_max_bit_len = interval(self._min, self._max)
            self._range_of_non_edge_signed_bit_len = interval(empty=True)

            self._prop_min_bit_len = 1.0
            self._prop_max_bit_len = 1.0
        else:
            if self._min > 0:
                _max_of_min_bit_len = (1 << min_bit_len) - 1
            elif self._min < 0:
                _max_of_min_bit_len = -(1 << (min_bit_len - 1))
            else:
                _max_of_min_bit_len = 0
            if self._max > 0:
                _min_of_max_bit_len = 1 << (max_bit_len - 1)
            elif self._max < 0:
                _min_of_max_bit_len = -((1 << max_bit_len) - 1)
            else:
                _min_of_max_bit_len = 0

            self._range_of_non_edge_signed_bit_len = interval(
                signed_min_bit_len + 1, signed_max_bit_len - 1
            )
            self._range_of_min_bit_len = interval(self._min, _max_of_min_bit_len)
            self._range_of_max_bit_len = interval(_min_of_max_bit_len, self._max)

            non_edge_bit_len_count = signed_max_bit_len - signed_min_bit_len - 1
            prop_base = (
                self._range_of_min_bit_len.count_int() / _count_by_bit_len(min_bit_len)
                + self._range_of_max_bit_len.count_int()
                / _count_by_bit_len(max_bit_len)
                + non_edge_bit_len_count
            )
            self._prop_min_bit_len = (
                self._range_of_min_bit_len.count_int()
                / _count_by_bit_len(min_bit_len)
                / prop_base
            )
            self._prop_max_bit_len = (
                self._range_of_max_bit_len.count_int()
                / _count_by_bit_len(max_bit_len)
                / prop_base
            )

    def _next(self) -> int:
        pre_weight = self._random.random()
        pre_weight -= self._prop_min_bit_len
        if pre_weight < 0:
            return self._random.randint(*self._range_of_min_bit_len.minmax())
        pre_weight -= self._prop_max_bit_len
        if pre_weight < 0:
            return self._random.randint(*self._range_of_max_bit_len.minmax())

        signed_bit_len = self._random.randint(
            *self._range_of_non_edge_signed_bit_len.minmax()
        )
        bit_len = abs(signed_bit_len)
        sign = _sign(signed_bit_len)

        if bit_len != 0:
            return sign * self._random.randint(1 << (bit_len - 1), (1 << bit_len) - 1)
        else:
            return 0


def _count_by_bit_len(bit_len: int) -> int:
    """count the number of non-negative integer n such as n.bit_len = bit_len"""

    if bit_len > 0:
        return 1 << (bit_len - 1)
    elif bit_len == 0:
        return 1
    else:
        raise ValueError(bit_len)


def _sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
