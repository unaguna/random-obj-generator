import datetime as dt
import random

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__random_date():
    factory = randog.factory.randdate()

    value = factory.next()

    assert isinstance(value, dt.date)


@pytest.mark.parametrize(
    "expected_value",
    (
        dt.date(2021, 1, 2),
        dt.date(2024, 2, 29),
    ),
)
def test__random_date__by_date(expected_value):
    factory = randog.factory.randdate(expected_value, expected_value)

    value = factory.next()

    assert isinstance(value, dt.date)
    assert value == expected_value


@pytest.mark.parametrize(
    "condition",
    (
        dt.datetime(2021, 1, 2, 11, 22, 33, 444_555),
        dt.datetime(2021, 1, 2, 11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
    ),
)
def test__random_date__by_datetime(condition):
    expected_value = condition.date()
    factory = randog.factory.randdate(condition, condition)

    value = factory.next()

    assert isinstance(value, dt.date)
    assert value == expected_value


def test__random_date__or_none():
    expected_value = dt.date(2021, 1, 2)
    factory = randog.factory.randdate(expected_value, expected_value).or_none(0.5)

    values = set(factory.iter(200))

    assert values == {expected_value, None}


def test__random_date__or_none_0():
    expected_value = dt.date(2021, 1, 2)
    factory = randog.factory.randdate(expected_value, expected_value).or_none(0)

    values = set(factory.iter(200))

    assert values == {expected_value}


def test__random_date__error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randdate(
            dt.date(2021, 1, 3),
            dt.date(2021, 1, 2),
        )
    e = e_ctx.value

    assert e.message == "empty range for randdate"


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
        [dt.date(2022, 4, 1), dt.date(2023, 4, 1)],
    ],
)
def test__random_date__seed(rnd1, rnd2, expect_same_output, args):
    repeat = 20
    factory1 = randog.factory.randdate(*args, **rnd1())
    factory2 = randog.factory.randdate(*args, **rnd2())

    generated1 = list(factory1.iter(repeat))
    generated2 = list(factory2.iter(repeat))

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
