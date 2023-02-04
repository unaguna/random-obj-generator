import datetime
import datetime as dt

import pytest

import ranog.factory
from ranog.exceptions import FactoryConstructionError


def test__random_datetime():
    factory = ranog.factory.randdatetime()

    value = factory.next()

    assert isinstance(value, dt.datetime)


@pytest.mark.parametrize(
    "expected_value",
    (
        dt.datetime(2021, 1, 2, 11, 22, 33, 444_555),
        dt.datetime(2021, 1, 2, 11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
    ),
)
def test__random_datetime__by_datetime(expected_value):
    factory = ranog.factory.randdatetime(expected_value, expected_value)

    value = factory.next()

    assert isinstance(value, dt.datetime)
    assert value == expected_value


def test__random_datetime__by_different_tz_datetime():
    minimum = dt.datetime(2021, 1, 2, 11, 22, 33, 444_555, tzinfo=dt.timezone.utc)
    maximum = dt.datetime(
        2021, 1, 2, 12, 22, 33, 444_555, tzinfo=dt.timezone(datetime.timedelta(hours=1))
    )
    assert minimum == maximum

    factory = ranog.factory.randdatetime(minimum, maximum)

    value = factory.next()

    assert isinstance(value, dt.datetime)
    assert value == minimum


def test__random_datetime__or_none():
    expected_value = dt.datetime(2021, 1, 2, 11, 22, 33, 444_555)
    factory = ranog.factory.randdatetime(expected_value, expected_value).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {expected_value, None}


def test__random_datetime__or_none_0():
    expected_value = dt.datetime(2021, 1, 2, 11, 22, 33, 444_555)
    factory = ranog.factory.randdatetime(expected_value, expected_value).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {expected_value}


def test__random_datetime__error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.randdatetime(
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555),
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_554),
        )
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"


@pytest.mark.parametrize(
    ("minimum", "maximum"),
    (
        (
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555),
            dt.datetime(2022, 1, 2, 11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
        ),
        (
            dt.datetime(2022, 1, 2, 11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555),
        ),
    ),
)
def test__random_datetime__error_when_naive_and_aware(minimum, maximum):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.randdatetime(minimum, maximum)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"
