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
    "args",
    [
        [1, 200],
    ],
)
def test__random_int__seed(args):
    seed = 12
    rnd1 = random.Random(seed)
    rnd2 = random.Random(seed)
    factory1 = randog.factory.randint(*args, rnd=rnd1)
    factory2 = randog.factory.randint(*args, rnd=rnd2)

    generated1 = list(factory1.iter(20))
    generated2 = list(factory2.iter(20))

    assert generated1 == generated2
