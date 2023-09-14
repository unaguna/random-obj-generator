import random

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


@pytest.mark.parametrize("expected_value", (-1, 0, 1))
def test__random_int(expected_value):
    factory = randog.factory.randint(expected_value, expected_value)

    value = factory.next()

    assert isinstance(value, int)
    assert value == expected_value


def test__random_int__or_none():
    factory = randog.factory.randint(1, 1).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1, None}


def test__random_int__or_none_0():
    factory = randog.factory.randint(1, 1).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1}


def test__random_int_error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randint(2, 1)
    e = e_ctx.value

    assert e.message == "empty range for randint"


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
def test__random_int__seed(rnd1, rnd2, expect_same_output, args):
    repeat = 20
    factory1 = randog.factory.randint(*args, **rnd1())
    factory2 = randog.factory.randint(*args, **rnd2())

    generated1 = list(factory1.iter(repeat))
    generated2 = list(factory2.iter(repeat))

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
