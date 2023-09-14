import random

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


@pytest.mark.parametrize(
    ("prop_true", "expected_values"),
    (
        (0, {False}),
        (1, {True}),
        (0.5, {True, False}),
    ),
)
def test__random_bool(prop_true, expected_values):
    factory = randog.factory.randbool(prop_true)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == expected_values


@pytest.mark.parametrize("prop_true", (-0.1, 1.1))
def test__random_int_error_when_illegal_probability(prop_true):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randbool(prop_true)
    e = e_ctx.value

    assert e.message == "the probability `prob_true` must range from 0 to 1"


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
    ("args", "substantial_constant"),
    [
        ([0], True),
        ([0.5], False),
        ([1], True),
    ],
)
def test__random_bool__seed(rnd1, rnd2, expect_same_output, args, substantial_constant):
    repeat = 200
    factory1 = randog.factory.randbool(*args, **rnd1())
    factory2 = randog.factory.randbool(*args, **rnd2())

    generated1 = list(factory1.iter(repeat))
    generated2 = list(factory2.iter(repeat))

    if substantial_constant or expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
