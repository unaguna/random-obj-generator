import math
import random
from collections import Counter, defaultdict
from itertools import groupby, chain

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError
from randog.rangeutils import interval


@pytest.mark.parametrize("expected_value", (-1, 0, 1))
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_int(expected_value, distribution):
    factory = randog.factory.randint(expected_value, expected_value, **distribution)

    value = factory.next()

    assert isinstance(value, int)
    assert value == expected_value


@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_int__or_none(distribution):
    factory = randog.factory.randint(1, 1, **distribution).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1, None}


@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_int__or_none_0(distribution):
    factory = randog.factory.randint(1, 1, **distribution).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1}


@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_int_error_when_edges_inverse(distribution):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randint(2, 1, **distribution)
    e = e_ctx.value

    assert e.message == "empty range for randint"


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
        "expected_values",
        "distribution",
    ),
    [
        (
            1,
            7,
            set(range(1, 8)),
            defaultdict(lambda: interval(1 / 3).radius(0.02)),
        ),
        (
            -7,
            -1,
            set(range(-7, 0)),
            defaultdict(lambda: interval(1 / 3).radius(0.02)),
        ),
        (
            -3,
            7,
            set(range(-3, 8)),
            defaultdict(lambda: interval(1 / 6).radius(0.02)),
        ),
        (
            1,
            5,  # ; it is not 2^x
            {1, 2, 3, 4, 5},
            defaultdict(
                lambda: interval(2 / 5).radius(0.02),
                {
                    (1, 2): interval(1 / 5).radius(0.02),
                },
            ),
        ),
        (
            -5,  # ; it is not 2^x
            -1,
            {-5, -4, -3, -2, -1},
            defaultdict(
                lambda: interval(2 / 5).radius(0.01),
                {
                    (-1, 2): interval(1 / 5).radius(0.02),
                },
            ),
        ),
    ],
)
def test__random_int__exp_uniform__distribution(
    minimum,
    maximum,
    expected_values,
    distribution,
):
    iter_count = 5000
    factory = randog.factory.randint(minimum, maximum, distribution="exp_uniform")

    value_count = {
        # Reduce redundant count by chain of `expected_values`.
        k: v - 1
        for k, v in Counter(
            # For ascending order by generated value, recode `expected_values` first.
            chain(sorted(expected_values), factory.iter(iter_count))
        ).items()
    }
    log_count = {
        k: sum((v for _, v in v_c))
        for k, v_c in groupby(value_count.items(), lambda v_c: _sign_and_log2(v_c[0]))
    }

    assert value_count.keys() == expected_values
    for key, count in log_count.items():
        assert count / iter_count in distribution[key]


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
    "args",
    [
        [1, 200],
    ],
)
@pytest.mark.parametrize(
    "distribution", [{}, {"distribution": "uniform"}, {"distribution": "exp_uniform"}]
)
def test__random_int__seed(rnd1, rnd2, expect_same_output, args, distribution):
    repeat = 20
    factory1 = randog.factory.randint(*args, **rnd1(), **distribution)
    factory2 = randog.factory.randint(*args, **rnd2(), **distribution)

    generated1 = list(factory1.iter(repeat))
    generated2 = list(factory2.iter(repeat))

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
