import math
import random
from collections import Counter, defaultdict
from decimal import Decimal
from fractions import Fraction

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError
from randog.rangeutils import interval


@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal(distribution):
    factory = randog.factory.randdecimal(**distribution)

    value = factory.next()

    assert isinstance(value, Decimal)


@pytest.mark.parametrize(
    "expected_value",
    (
        Decimal("0.25"),
        Decimal("0.125"),
    ),
)
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__by_decimal(expected_value, distribution):
    factory = randog.factory.randdecimal(expected_value, expected_value, **distribution)

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
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__by_float(condition, expected_value, distribution):
    factory = randog.factory.randdecimal(condition, condition, **distribution)

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
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__by_int(condition, expected_value, distribution):
    factory = randog.factory.randdecimal(condition, condition, **distribution)

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
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__by_fraction(condition, expected_value, distribution):
    factory = randog.factory.randdecimal(condition, condition, **distribution)

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
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__decimal_len(
    minimum, maximum, decimal_len, expected_value, distribution
):
    factory = randog.factory.randdecimal(
        minimum, maximum, decimal_len=decimal_len, **distribution
    )

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
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__decimal_len__inf_nan(
    condition, decimal_len, is_expected, distribution
):
    # The main purpose is to check that no exceptions raise

    factory = randog.factory.randdecimal(
        decimal_len=decimal_len, **condition, **distribution
    )

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
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__inf(p_inf, n_inf, expected_value, distribution):
    factory = randog.factory.randdecimal(p_inf=p_inf, n_inf=n_inf, **distribution)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__nan(distribution):
    factory = randog.factory.randdecimal(nan=1.0, **distribution)

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
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__inf_zero(p_inf, n_inf, distribution):
    factory = randog.factory.randdecimal(p_inf=p_inf, n_inf=n_inf, **distribution)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert math.isfinite(value)


@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__or_none(distribution):
    factory = randog.factory.randdecimal(1, 1, **distribution).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {Decimal("1"), None}
    value = next(filter(lambda x: x is not None, values))
    assert isinstance(value, Decimal)


@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__or_none_0(distribution):
    factory = randog.factory.randdecimal(1, 1, **distribution).or_none(0)

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
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__error_when_edges_inverse(
    minimum, maximum, kwargs, distribution
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randdecimal(minimum, maximum, **kwargs, **distribution)
    e = e_ctx.value

    assert e.message == "empty range for randdecimal"


@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__error_when_probability_gt_1(distribution):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randdecimal(p_inf=0.625, n_inf=0.5, **distribution)
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
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__error_when_negative_probability(
    p_inf, n_inf, nan, distribution
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randdecimal(p_inf=p_inf, n_inf=n_inf, nan=nan, **distribution)
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


def _log10_int(x):
    if x != 0:
        return math.floor(math.log10(abs(x)))
    else:
        return None


def _sign_and_log10(x):
    return _sign(x), _log10_int(x)


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
            Decimal("1.0"),
            Decimal("999.9"),
            False,
            {0, 1, 2},
            set(),
            defaultdict(lambda: interval(1 / 3).radius(0.02)),
            lambda x: 1.0 <= x < 1000.0,
        ),
        (
            Decimal("0.01"),
            Decimal("999.99"),
            False,
            {-2, -1, 0, 1, 2},
            set(),
            defaultdict(lambda: interval(1 / 5).radius(0.02)),
            lambda x: Decimal("0.01") <= x < 1000.0,
        ),
        (
            Decimal("-999.9"),
            Decimal("-1.0"),
            False,
            set(),
            {0, 1, 2},
            defaultdict(lambda: interval(1 / 3).radius(0.02)),
            lambda x: -1000.0 < x <= -1.0,
        ),
        (
            Decimal("-99.9"),
            Decimal("999.9"),
            True,
            {-1, 0, 1, 2},
            {-1, 0, 1},
            defaultdict(lambda: interval(1 / 8).radius(0.02)),
            lambda x: -100.0 < x < 1000.0,
        ),
        (
            1,
            54,  # ; it is not 10^x
            False,
            {0, 1},
            set(),
            {
                (1, 0): interval(2 / 3).radius(0.02),
                (1, 1): interval(1 / 3).radius(0.02),
            },
            lambda x: 1.0 <= x < 55.0,
        ),
        (
            Decimal(-324),  # ; it is not 10^x
            Decimal(-1),
            False,
            set(),
            {0, 1, 2},
            defaultdict(
                lambda: interval(4 / 9).radius(0.01),
                {
                    (-1, 2): interval(1 / 9).radius(0.01),
                },
            ),
            lambda x: -325.0 < x <= -1.0,
        ),
    ],
)
def test__random_float__exp_uniform__distribution(
    minimum,
    maximum,
    expect0,
    expected_log_range_pos,
    expected_log_range_neg,
    distribution,
    value_is_valid,
):
    iter_count = 200000
    factory = randog.factory.randdecimal(minimum, maximum, distribution="exp_uniform")

    def assert_value(value: Decimal) -> Decimal:
        assert value_is_valid(value)
        return value

    print([(x, _sign_and_log10(x)) for x in factory.iter(20)])
    log_count = Counter(
        _sign_and_log10(assert_value(x)) for x in factory.iter(iter_count)
    )
    print(log_count)
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
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_decimal__seed(
    rnd1, rnd2, expect_same_output, args, kwargs, distribution
):
    repeat = 20
    factory1 = randog.factory.randdecimal(*args, **rnd1(), **kwargs, **distribution)
    factory2 = randog.factory.randdecimal(*args, **rnd2(), **kwargs, **distribution)

    # NaN != NaN となってしまうため、repr 文字列で比較する
    generated1 = [repr(v) for v in factory1.iter(repeat)]
    generated2 = [repr(v) for v in factory2.iter(repeat)]

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
