import math
import random
from collections import Counter
from decimal import Decimal
from fractions import Fraction

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float(weight):
    factory = randog.factory.randfloat(**weight)

    value = factory.next()

    assert isinstance(value, float)


@pytest.mark.parametrize("expected_value", (-1.0, 0.0, 1.0))
@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float__by_float(expected_value, weight):
    factory = randog.factory.randfloat(expected_value, expected_value, **weight)

    value = factory.next()

    assert isinstance(value, float)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "expected_value"),
    (
        (1, 1.0),
        (2, 2.0),
    ),
)
@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float__by_int(condition, expected_value, weight):
    factory = randog.factory.randfloat(condition, condition, **weight)

    value = factory.next()

    assert isinstance(value, float)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "expected_value"),
    (
        (Decimal("0.25"), 0.25),
        (Decimal("0.125"), 0.125),
    ),
)
@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float__by_decimal(condition, expected_value, weight):
    factory = randog.factory.randfloat(condition, condition, **weight)

    value = factory.next()

    assert isinstance(value, float)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "expected_value"),
    (
        (Fraction("1/4"), 0.25),
        (Fraction("1/8"), 0.125),
    ),
)
@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float__by_fraction(condition, expected_value, weight):
    factory = randog.factory.randfloat(condition, condition, **weight)

    value = factory.next()

    assert isinstance(value, float)
    assert value == expected_value


@pytest.mark.parametrize(
    ("p_inf", "n_inf", "expected_value"),
    (
        (1.0, 0.0, float("inf")),
        (0.0, 1.0, float("-inf")),
    ),
)
@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float__inf(p_inf, n_inf, expected_value, weight):
    factory = randog.factory.randfloat(p_inf=p_inf, n_inf=n_inf, **weight)

    value = factory.next()

    assert isinstance(value, float)
    assert value == expected_value


@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float__nan(weight):
    factory = randog.factory.randfloat(nan=1.0, **weight)

    value = factory.next()

    assert isinstance(value, float)
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
@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float__inf_zero(p_inf, n_inf, weight):
    factory = randog.factory.randfloat(p_inf=p_inf, n_inf=n_inf, **weight)

    value = factory.next()

    assert isinstance(value, float)
    assert math.isfinite(value)


@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float__or_none(weight):
    factory = randog.factory.randfloat(1, 1, **weight).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1.0, None}


@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float__or_none_0(weight):
    factory = randog.factory.randfloat(1, 1, **weight).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1.0}


@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float_error_when_edges_inverse(weight):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randfloat(2, 1, **weight)
    e = e_ctx.value

    assert e.message == "empty range for randfloat"


@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float_error_when_probability_gt_1(weight):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randfloat(p_inf=0.625, n_inf=0.5, **weight)
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
@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float__error_when_negative_probability(p_inf, n_inf, nan, weight):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randfloat(p_inf=p_inf, n_inf=n_inf, nan=nan, **weight)
    e = e_ctx.value

    assert (
        e.message
        == "the probabilities `p_inf`, `n_inf`, and `nan` must range from 0 to 1"
    )


def _sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def _log2(x):
    if x != 0:
        return math.log2(abs(x))
    else:
        return None


@pytest.mark.parametrize(
    ("minimum", "maximum"),
    [
        (1.0, 8.0),
        (-8.0, -1.0),
    ],
)
def test__random_float__log_flat__distribution(minimum, maximum):
    # TODO: log_count.keys() の値域のアサーション
    # TODO: 端点の取り扱い（負の min や正の max を値域に含むかどうか）
    factory = randog.factory.randfloat(minimum, maximum, weight="log_flat")

    log_count = Counter((_sign(x), math.floor(_log2(x))) for x in factory.iter(200000))

    count_min = min(log_count.values())
    count_max = max(log_count.values())

    assert (count_max - count_min) / (count_max + count_min) < 0.01


@pytest.mark.parametrize(
    ("rnd1", "rnd2", "expect_same_output"),
    [
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(12)}, True),
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(13)}, False),
        (lambda: {"rnd": random.Random(12)}, lambda: {}, False),
        (lambda: {}, lambda: {}, False),
    ],
)
@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
@pytest.mark.parametrize(
    ("args", "kwargs"),
    [
        ([-1.25, 1.5], {}),
        ([-1.25, 1.5], {"p_inf": 0.5}),
        ([-1.25, 1.5], {"n_inf": 0.5}),
        ([-1.25, 1.5], {"nan": 0.5}),
        ([-1.25, 1.5], {"p_inf": 0.3, "n_inf": 0.3}),
        ([-1.25, 1.5], {"p_inf": 0.2, "n_inf": 0.2, "nan": 0.2}),
    ],
)
def test__random_float__seed(rnd1, rnd2, expect_same_output, weight, args, kwargs):
    repeat = 20
    factory1 = randog.factory.randfloat(*args, **weight, **rnd1(), **kwargs)
    factory2 = randog.factory.randfloat(*args, **weight, **rnd2(), **kwargs)

    # NaN != NaN となってしまうため、repr 文字列で比較する
    generated1 = [repr(v) for v in factory1.iter(repeat)]
    generated2 = [repr(v) for v in factory2.iter(repeat)]

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
