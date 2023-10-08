import math
import random
from decimal import Decimal
from fractions import Fraction

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__random_decimal():
    factory = randog.factory.randdecimal()

    value = factory.next()

    assert isinstance(value, Decimal)


@pytest.mark.parametrize(
    "expected_value",
    (
        Decimal("0.25"),
        Decimal("0.125"),
    ),
)
def test__random_decimal__by_decimal(expected_value):
    factory = randog.factory.randdecimal(expected_value, expected_value)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "expected_value"),
    (
        (-1.0, Decimal(-1)),
        (0.0, Decimal(0)),
        (1.0, Decimal(1)),
    ),
)
def test__random_decimal__by_float(condition, expected_value):
    factory = randog.factory.randdecimal(condition, condition)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "expected_value"),
    (
        (1, Decimal(1)),
        (2, Decimal(2)),
    ),
)
def test__random_decimal__by_int(condition, expected_value):
    factory = randog.factory.randdecimal(condition, condition)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "expected_value"),
    (
        (Fraction("1/4"), Decimal(0.25)),
        (Fraction("1/8"), Decimal(0.125)),
    ),
)
def test__random_decimal__by_fraction(condition, expected_value):
    factory = randog.factory.randdecimal(condition, condition)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


@pytest.mark.parametrize(
    ("minimum", "maximum", "decimal_len", "expected_value"),
    (
        (1.0, 1.0, 0, Decimal("1")),
        (1.0, 1.0, 1, Decimal("1.0")),
        (1.0, 1.0, 2, Decimal("1.00")),
        (0.25, 0.25, 2, Decimal("0.25")),
        (15.0, 15.0, 0, Decimal("15")),
        (15.0, 15.0, 1, Decimal("15.0")),
        (15.0, 15.0, 2, Decimal("15.00")),
        (Decimal("1"), Decimal("1"), None, Decimal("1")),
        (Decimal("1.0"), Decimal("1.0"), None, Decimal("1.0")),
        (Decimal("1.0"), Decimal("1.00"), None, Decimal("1.00")),
        (Decimal("1.00"), Decimal("1.0"), None, Decimal("1.00")),
        (Decimal("1.00"), 1.0, None, Decimal("1.00")),
        (1.0, Decimal("1.00"), None, Decimal("1.00")),
        (Decimal("1E+2"), Decimal("1E+2"), None, Decimal("1E+2")),
        # TODO: min も max も non-Decimal で decimal_len の指定がない場合の仕様を検討
    ),
)
def test__random_decimal__decimal_len(minimum, maximum, decimal_len, expected_value):
    factory = randog.factory.randdecimal(minimum, maximum, decimal_len=decimal_len)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value
    assert value.as_tuple() == expected_value.as_tuple()  # check decimal length


@pytest.mark.parametrize(
    "decimal_len",
    [0, 1, 2],
)
@pytest.mark.parametrize(
    ("condition", "is_expected"),
    (
        ({"p_inf": 1}, lambda v: v == Decimal("Infinity")),
        ({"n_inf": 1}, lambda v: v == Decimal("-Infinity")),
        ({"nan": 1}, lambda v: isinstance(v, Decimal) and v.is_nan()),
    ),
)
def test__random_decimal__decimal_len__inf_nan(condition, decimal_len, is_expected):
    # The main purpose is to check that no exceptions raise

    factory = randog.factory.randdecimal(decimal_len=decimal_len, **condition)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert is_expected(value)


@pytest.mark.parametrize(
    ("p_inf", "n_inf", "expected_value"),
    (
        (1.0, 0.0, Decimal("inf")),
        (0.0, 1.0, Decimal("-inf")),
    ),
)
def test__random_decimal__inf(p_inf, n_inf, expected_value):
    factory = randog.factory.randdecimal(p_inf=p_inf, n_inf=n_inf)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


def test__random_decimal__nan():
    factory = randog.factory.randdecimal(nan=1.0)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert math.isnan(value)


@pytest.mark.parametrize(
    ("p_inf", "n_inf"),
    (
        (0.0, 0.0),
        (-0.0, 0.0),
        (0.0, -0.0),
        (-0.0, -0.0),
    ),
)
def test__random_decimal__inf_zero(p_inf, n_inf):
    factory = randog.factory.randdecimal(p_inf=p_inf, n_inf=n_inf)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert math.isfinite(value)


def test__random_decimal__or_none():
    factory = randog.factory.randdecimal(1, 1).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {Decimal("1"), None}
    value = next(filter(lambda x: x is not None, values))
    assert isinstance(value, Decimal)


def test__random_decimal__or_none_0():
    factory = randog.factory.randdecimal(1, 1).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {Decimal("1")}
    value = next(filter(lambda x: x is not None, values))
    assert isinstance(value, Decimal)


@pytest.mark.parametrize(
    ("minimum", "maximum", "kwargs"),
    [
        (2, 1, {}),
        (Decimal("0.01"), Decimal("0.02"), {"decimal_len": 1}),
    ],
)
def test__random_decimal__error_when_edges_inverse(minimum, maximum, kwargs):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randdecimal(minimum, maximum, **kwargs)
    e = e_ctx.value

    assert e.message == "empty range for randdecimal"


def test__random_decimal__error_when_probability_gt_1():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randdecimal(p_inf=0.625, n_inf=0.5)
    e = e_ctx.value

    assert (
        e.message
        == "the sum of probabilities `p_inf`, `n_inf`, and `nan` must range from 0 to 1"
    )


@pytest.mark.parametrize(
    ("p_inf", "n_inf", "nan"),
    (
        (-0.1, 0.1, 0.1),
        (0.1, -0.1, 0.1),
        (-0.1, -0.1, 0.1),
        (0.1, 0.1, -0.1),
        (-0.1, 0.1, -0.1),
        (0.1, -0.1, -0.1),
        (-0.1, -0.1, -0.1),
    ),
)
def test__random_decimal__error_when_negative_probability(p_inf, n_inf, nan):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randdecimal(p_inf=p_inf, n_inf=n_inf, nan=nan)
    e = e_ctx.value

    assert (
        e.message
        == "the probabilities `p_inf`, `n_inf`, and `nan` must range from 0 to 1"
    )


@pytest.mark.parametrize(
    ("rnd1", "rnd2", "expect_same_output"),
    [
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(12)}, True),
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(13)}, False),
        (lambda: {"rnd": random.Random(12)}, lambda: {}, False),
        (lambda: {}, lambda: {}, False),
    ],
)
@pytest.mark.parametrize(
    ("args", "kwargs"),
    [
        ([-1.25, 1.5], {}),
        ([-1.25, 1.5], {"decimal_len": 5}),
        ([-1.25, 1.5], {"p_inf": 0.5}),
        ([-1.25, 1.5], {"n_inf": 0.5}),
        ([-1.25, 1.5], {"nan": 0.5}),
        ([-1.25, 1.5], {"p_inf": 0.3, "n_inf": 0.3}),
        ([-1.25, 1.5], {"p_inf": 0.2, "n_inf": 0.2, "nan": 0.2}),
    ],
)
def test__random_decimal__seed(rnd1, rnd2, expect_same_output, args, kwargs):
    repeat = 20
    factory1 = randog.factory.randdecimal(*args, **rnd1(), **kwargs)
    factory2 = randog.factory.randdecimal(*args, **rnd2(), **kwargs)

    # NaN != NaN となってしまうため、repr 文字列で比較する
    generated1 = [repr(v) for v in factory1.iter(repeat)]
    generated2 = [repr(v) for v in factory2.iter(repeat)]

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
