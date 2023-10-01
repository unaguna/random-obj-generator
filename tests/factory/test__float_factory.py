import math
import random
import typing as t
from collections import Counter, defaultdict
from decimal import Decimal
from fractions import Fraction

import pytest

import randog.factory
from randog.rangeutils import interval
from randog.exceptions import FactoryConstructionError


@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float(weight):
    factory = randog.factory.randfloat(**weight)

    value = factory.next()

    assert isinstance(value, float)


@pytest.mark.parametrize(
    ("minimum", "maximum", "weight", "assertion"),
    [
        # negative zero
        (-0.0, -0.0, "flat", lambda x: x == 0),
        (-0.0, 0.0, "flat", lambda x: x == 0),
        (0.0, 0.0, "flat", lambda x: x == 0),
        (-0.0, -0.0, "log_flat", lambda x: x == 0),
        (-0.0, 0.0, "log_flat", lambda x: x == 0),
        (0.0, 0.0, "log_flat", lambda x: x == 0),
        # infinity
        (1.0, float("inf"), "flat", lambda x: x > 0 and math.isfinite(x)),
        (float("-inf"), -1.0, "flat", lambda x: x < 0 and math.isfinite(x)),
        (float("-inf"), float("inf"), "flat", lambda x: math.isfinite(x)),
        (1.0, float("inf"), "log_flat", lambda x: x > 0 and math.isfinite(x)),
        (float("-inf"), -1.0, "log_flat", lambda x: x < 0 and math.isfinite(x)),
        (float("-inf"), float("inf"), "log_flat", lambda x: math.isfinite(x)),
    ],
)
def test__random_float__range(minimum, maximum, weight: t.Any, assertion):
    factory = randog.factory.randfloat(minimum, maximum, weight=weight)

    assert {str(v) for v in factory.iter(100) if not assertion(v)} == set()


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


@pytest.mark.parametrize(
    ("minimum", "maximum"),
    [
        (2, 1),
        (float("inf"), 0),
        (float("inf"), float("inf")),
        (0, float("-inf")),
        (float("-inf"), float("-inf")),
    ],
)
@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float_error_when_edges_inverse(minimum, maximum, weight):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randfloat(minimum, maximum, **weight)
    e = e_ctx.value

    assert e.message == "empty range for randfloat"


@pytest.mark.parametrize(
    ("minimum", "maximum"),
    [
        (float("nan"), 0),
        (0, float("nan")),
        (float("nan"), float("nan")),
    ],
)
@pytest.mark.parametrize("weight", [{}, {"weight": "flat"}, {"weight": "log_flat"}])
def test__random_float_error_when_edges_nan(minimum, maximum, weight):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randfloat(minimum, maximum, **weight)
    e = e_ctx.value

    assert e.message == "minimum and maximum are must not be nan"


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


def _log2_int(x):
    if x != 0:
        return math.floor(math.log2(abs(x)))
    else:
        return None


def _sign_and_log2(x):
    return _sign(x), _log2_int(x)


@pytest.mark.parametrize(
    (
        "minimum",
        "maximum",
        "expect0",
        "expected_log_range_pos",
        "expected_log_range_neg",
        "distribution",
        "value_is_valid",
    ),
    [
        (
            1.0,
            8.0,
            False,
            {0, 1, 2},
            set(),
            defaultdict(lambda: interval(1 / 3).radius(0.02)),
            lambda x: 1.0 <= x < 8.0,
        ),
        (
            0.25,
            8.0,
            False,
            {-2, -1, 0, 1, 2},
            set(),
            defaultdict(lambda: interval(1 / 5).radius(0.02)),
            lambda x: 0.25 <= x < 8.0,
        ),
        (
            -8.0,
            -1.0,
            False,
            set(),
            {0, 1, 2},
            defaultdict(lambda: interval(1 / 3).radius(0.02)),
            lambda x: -8.0 < x <= -1.0,
        ),
        (
            -4.0,
            8.0,
            True,
            set(range(-1022, 3)),
            set(range(-1022, 2)),
            defaultdict(lambda: interval(1 / 2049).radius(0.1)),
            lambda x: -4.0 < x < 8.0,
        ),
        (
            1,
            3,  # ; it is not 2^x
            False,
            {0, 1},
            set(),
            {
                (1, 0): interval(2 / 3).radius(0.02),
                (1, 1): interval(1 / 3).radius(0.02),
            },
            lambda x: 1.0 <= x < 3.0,
        ),
        (
            -5,  # ; it is not 2^x
            -1,
            False,
            set(),
            {0, 1, 2},
            defaultdict(
                lambda: interval(4 / 9).radius(0.01),
                {
                    (-1, 2): interval(1 / 9).radius(0.01),
                },
            ),
            lambda x: -5.0 < x <= -1.0,
        ),
    ],
)
def test__random_float__log_flat__distribution(
    minimum,
    maximum,
    expect0,
    expected_log_range_pos,
    expected_log_range_neg,
    distribution,
    value_is_valid,
):
    iter_count = 200000
    factory = randog.factory.randfloat(minimum, maximum, weight="log_flat")

    def assert_value(value: float) -> float:
        assert value_is_valid(value)
        return value

    log_count = Counter(
        _sign_and_log2(assert_value(x)) for x in factory.iter(iter_count)
    )

    for key, count in log_count.items():
        assert count / iter_count in distribution[key]
    assert {k for sign, k in log_count.keys() if sign > 0} == expected_log_range_pos
    assert {k for sign, k in log_count.keys() if sign < 0} == expected_log_range_neg
    if expect0:
        assert 0 in {sign for sign, k in log_count.keys()}
    else:
        assert 0 not in {sign for sign, k in log_count.keys()}


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
