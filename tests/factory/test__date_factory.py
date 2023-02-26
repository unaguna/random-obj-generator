import datetime as dt

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

    assert e.message == "the generating conditions are inconsistent"
