import datetime as dt
import random

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__random_datetime():
    factory = randog.factory.randdatetime()

    value = factory.next()

    assert isinstance(value, dt.datetime)
    assert value.tzinfo is None


@pytest.mark.parametrize(
    "expected_value",
    (
        dt.datetime(2021, 1, 2, 11, 22, 33, 444_555),
        dt.datetime(2021, 1, 2, 11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
    ),
)
def test__random_datetime__by_datetime(expected_value):
    factory = randog.factory.randdatetime(expected_value, expected_value)

    value = factory.next()

    assert isinstance(value, dt.datetime)
    assert value == expected_value
    assert value.tzinfo == expected_value.tzinfo


@pytest.mark.parametrize(
    ("condition", "expected_min", "expected_max"),
    (
        (dt.date(2021, 1, 2), dt.datetime(2021, 1, 2), dt.datetime(2021, 1, 3)),
        (dt.date(2021, 1, 5), dt.datetime(2021, 1, 5), dt.datetime(2021, 1, 6)),
    ),
)
def test__random_datetime__by_date(condition, expected_min, expected_max):
    factory = randog.factory.randdatetime(condition, condition)

    for _ in range(200):
        value = factory.next()

        assert isinstance(value, dt.datetime)
        assert expected_min <= value < expected_max


def test__random_datetime__by_different_tz_datetime():
    minimum = dt.datetime(2021, 1, 2, 11, 22, 33, 444_555, tzinfo=dt.timezone.utc)
    maximum = dt.datetime(
        2021, 1, 2, 12, 22, 33, 444_555, tzinfo=dt.timezone(dt.timedelta(hours=1))
    )
    assert minimum == maximum

    factory = randog.factory.randdatetime(minimum, maximum)

    value = factory.next()

    assert isinstance(value, dt.datetime)
    assert value == minimum
    assert value.tzinfo == minimum.tzinfo


@pytest.mark.parametrize(
    ("condition", "tzinfo", "expected_value"),
    (
        # naive to UTC
        (
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555),
            dt.timezone.utc,
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
        ),
        # naive to UTC
        (
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555, tzinfo=None),
            dt.timezone.utc,
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
        ),
        # naive to +01:00
        (
            dt.datetime(2021, 1, 2, 11, 22),
            dt.timezone(dt.timedelta(hours=1)),
            dt.datetime(2021, 1, 2, 11, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
        ),
        # UTC to UTC
        (
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
            dt.timezone.utc,
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
        ),
        # UTC to +01:00
        (
            dt.datetime(2021, 1, 2, 11, 22, tzinfo=dt.timezone.utc),
            dt.timezone(dt.timedelta(hours=1)),
            dt.datetime(2021, 1, 2, 12, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
        ),
        # +01:00 to UTC
        (
            dt.datetime(2021, 1, 2, 12, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
            dt.timezone.utc,
            dt.datetime(2021, 1, 2, 11, 22, tzinfo=dt.timezone.utc),
        ),
        # +01:00 to +01:00
        (
            dt.datetime(2021, 1, 2, 12, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
            dt.timezone(dt.timedelta(hours=1)),
            dt.datetime(2021, 1, 2, 12, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
        ),
        # +01:00 to +02:00
        (
            dt.datetime(2021, 1, 2, 12, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
            dt.timezone(dt.timedelta(hours=2)),
            dt.datetime(2021, 1, 2, 13, 22, tzinfo=dt.timezone(dt.timedelta(hours=2))),
        ),
        # UTC to naive
        (
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
            None,
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555),
        ),
        # +01:00 to naive
        (
            dt.datetime(2021, 1, 2, 11, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
            None,
            dt.datetime(2021, 1, 2, 11, 22),
        ),
        # naive to naive
        (
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555),
            None,
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555),
        ),
    ),
)
def test__random_datetime__by_datetime_and_tzinfo(condition, tzinfo, expected_value):
    factory = randog.factory.randdatetime(condition, condition, tzinfo=tzinfo)

    value = factory.next()

    assert isinstance(value, dt.datetime)
    assert value == expected_value
    assert value.tzinfo == expected_value.tzinfo


def test__random_datetime__or_none():
    expected_value = dt.datetime(2021, 1, 2, 11, 22, 33, 444_555)
    factory = randog.factory.randdatetime(expected_value, expected_value).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {expected_value, None}


def test__random_datetime__or_none_0():
    expected_value = dt.datetime(2021, 1, 2, 11, 22, 33, 444_555)
    factory = randog.factory.randdatetime(expected_value, expected_value).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {expected_value}


def test__random_datetime__error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randdatetime(
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_555),
            dt.datetime(2021, 1, 2, 11, 22, 33, 444_554),
        )
    e = e_ctx.value

    assert e.message == "empty range for randdatetime"


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
        randog.factory.randdatetime(minimum, maximum)
    e = e_ctx.value

    assert (
        e.message
        == "cannot define range for randdatetime with a naive datetime and an aware "
        "datetime"
    )


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
        ([dt.datetime(2022, 4, 1), dt.datetime(2023, 4, 1)], {}),
        ([dt.datetime(2022, 4, 1), dt.datetime(2023, 4, 1)], {"tzinfo": None}),
        (
            [dt.datetime(2022, 4, 1), dt.datetime(2023, 4, 1)],
            {"tzinfo": dt.timezone.utc},
        ),
    ],
)
def test__random_datetime__seed(rnd1, rnd2, expect_same_output, args, kwargs):
    repeat = 20
    factory1 = randog.factory.randdatetime(*args, **rnd1(), **kwargs)
    factory2 = randog.factory.randdatetime(*args, **rnd2(), **kwargs)

    generated1 = list(factory1.iter(repeat))
    generated2 = list(factory2.iter(repeat))

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
