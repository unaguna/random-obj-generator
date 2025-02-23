import random

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


@pytest.mark.parametrize(
    ("code", "expected_value"),
    [
        ("1d1", 1),
        ("d1", 1),
        ("3d1", 3),
        ("1D1", 1),
        ("D1", 1),
        ("3D1", 3),
    ],
)
def test__random_dice(code, expected_value):
    factory = randog.factory.dice(code)

    values = set(factory.iter(10))

    assert values == {expected_value}


@pytest.mark.parametrize(
    ("code", "maximum"),
    [
        ("1d10", 10),
        ("d6", 6),
        ("3d100", 300),
        ("1D10", 10),
        ("D6", 6),
        ("3D100", 300),
    ],
)
def test__random_dice_code(code, maximum):
    factory = randog.factory.dice(code)

    values = set(factory.iter(100))

    assert 1 <= min(values)
    assert max(values) <= maximum


@pytest.mark.parametrize(
    ("code", "expected_value"),
    [
        ("1d1", 1),
        ("d1", 1),
        ("3d1", 3),
    ],
)
def test__random_dice__or_none(code, expected_value):
    factory = randog.factory.dice(code).or_none(0.5)

    values = set(factory.iter(200))

    assert values == {expected_value, None}


@pytest.mark.parametrize(
    ("code", "expected_value"),
    [
        ("1d1", 1),
        ("d1", 1),
        ("3d1", 3),
    ],
)
def test__random_dice__or_none_0(code, expected_value):
    factory = randog.factory.dice(code).or_none(0)

    values = set(factory.iter(200))

    assert values == {expected_value}


@pytest.mark.parametrize(
    ("code",),
    [
        ("100",),
        ("10d",),
    ],
)
def test__random_dice_error_with_invalid_code(code):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.dice(code)
    e = e_ctx.value

    assert e.args[0] == f"invalid dice notation: {code}"


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
    "code",
    [
        "3d100",
    ],
)
def test__random_dice__seed(rnd1, rnd2, expect_same_output, code):
    repeat = 20
    factory1 = randog.factory.dice(code, **rnd1())
    factory2 = randog.factory.dice(code, **rnd2())

    generated1 = list(factory1.iter(repeat))
    generated2 = list(factory2.iter(repeat))

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
