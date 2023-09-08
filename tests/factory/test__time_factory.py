import datetime as dt
import random

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__random_time():
    factory = randog.factory.randtime()

    value = factory.next()

    assert isinstance(value, dt.time)
    assert value.tzinfo is None


@pytest.mark.parametrize(
    ("minimum", "maximum"),
    [
        (dt.time(0, 0, 0), dt.time(23, 59, 59)),
        (dt.time(12, 0, 0), dt.time(13, 0, 0)),
        (dt.time(0, 0, 0), dt.time(0, 0, 0)),
        (dt.time(12, 0, 0), dt.time(12, 0, 0)),
    ],
)
def test__random_time__min_le_max(minimum, maximum):
    factory = randog.factory.randtime(minimum, maximum)

    value = factory.next()

    assert isinstance(value, dt.time)
    assert minimum <= value <= maximum


@pytest.mark.parametrize(
    ("minimum", "maximum"),
    [
        (dt.time(23, 59, 59), dt.time(0, 0, 0)),
        (dt.time(13, 0, 0), dt.time(12, 0, 0)),
    ],
)
def test__random_time__min_gt_max(minimum, maximum):
    factory = randog.factory.randtime(minimum, maximum)

    value = factory.next()

    assert isinstance(value, dt.time)
    assert value <= maximum or minimum <= value


@pytest.mark.parametrize(
    ("minimum", "expected_maximum"),
    [
        (dt.time(23, 59, 59), dt.time(0, 59, 59)),
        (dt.time(13, 0, 0), dt.time(14, 0, 0)),
    ],
)
def test__random_time__only_min(minimum, expected_maximum):
    factory = randog.factory.randtime(minimum=minimum)

    values = list(factory.iter(200))

    assert set(map(type, values)) == {dt.time}
    if minimum <= expected_maximum:
        assert all(map(lambda v: minimum <= v <= expected_maximum, values))
    else:
        assert all(map(lambda v: v <= minimum or expected_maximum <= v, values))


@pytest.mark.parametrize(
    ("expected_minimum", "maximum"),
    [
        (dt.time(23, 59, 59), dt.time(0, 59, 59)),
        (dt.time(13, 0, 0), dt.time(14, 0, 0)),
    ],
)
def test__random_time__only_max(expected_minimum, maximum):
    factory = randog.factory.randtime(maximum=maximum)

    values = list(factory.iter(200))

    assert set(map(type, values)) == {dt.time}
    if expected_minimum <= maximum:
        assert all(map(lambda v: expected_minimum <= v <= maximum, values))
    else:
        assert all(map(lambda v: v <= expected_minimum or maximum <= v, values))


def test__random_time__by_different_tz_time():
    minimum = dt.time(11, 22, 33, 444_555, tzinfo=dt.timezone.utc)
    maximum = dt.time(12, 22, 33, 444_555, tzinfo=dt.timezone(dt.timedelta(hours=1)))
    assert minimum == maximum

    factory = randog.factory.randtime(minimum, maximum)

    value = factory.next()

    assert isinstance(value, dt.time)
    assert value == minimum
    assert value.tzinfo == minimum.tzinfo


@pytest.mark.parametrize(
    ("condition", "tzinfo", "expected_value"),
    (
        # naive to UTC
        (
            dt.time(11, 22, 33, 444_555),
            dt.timezone.utc,
            dt.time(11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
        ),
        # naive to UTC
        (
            dt.time(11, 22, 33, 444_555, tzinfo=None),
            dt.timezone.utc,
            dt.time(11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
        ),
        # naive to +01:00
        (
            dt.time(11, 22),
            dt.timezone(dt.timedelta(hours=1)),
            dt.time(11, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
        ),
        # UTC to UTC
        (
            dt.time(11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
            dt.timezone.utc,
            dt.time(11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
        ),
        # UTC to +01:00
        (
            dt.time(11, 22, tzinfo=dt.timezone.utc),
            dt.timezone(dt.timedelta(hours=1)),
            dt.time(12, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
        ),
        # +01:00 to UTC
        (
            dt.time(12, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
            dt.timezone.utc,
            dt.time(11, 22, tzinfo=dt.timezone.utc),
        ),
        # +01:00 to +01:00
        (
            dt.time(12, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
            dt.timezone(dt.timedelta(hours=1)),
            dt.time(12, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
        ),
        # +01:00 to +02:00
        (
            dt.time(12, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
            dt.timezone(dt.timedelta(hours=2)),
            dt.time(13, 22, tzinfo=dt.timezone(dt.timedelta(hours=2))),
        ),
        # UTC to naive
        (
            dt.time(11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
            None,
            dt.time(11, 22, 33, 444_555),
        ),
        # +01:00 to naive
        (
            dt.time(11, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))),
            None,
            dt.time(11, 22),
        ),
        # naive to naive
        (
            dt.time(11, 22, 33, 444_555),
            None,
            dt.time(11, 22, 33, 444_555),
        ),
    ),
)
def test__random_time__by_time_and_tzinfo(condition, tzinfo, expected_value):
    factory = randog.factory.randtime(condition, condition, tzinfo=tzinfo)

    value = factory.next()

    assert isinstance(value, dt.time)
    assert value == expected_value
    assert value.tzinfo == expected_value.tzinfo


@pytest.mark.parametrize(
    "tzinfo",
    (
        None,
        dt.timezone.utc,
    ),
)
def test__random_time__by_tzinfo(tzinfo):
    factory = randog.factory.randtime(tzinfo=tzinfo)

    value = factory.next()

    assert isinstance(value, dt.time)
    assert value.tzinfo == tzinfo


def test__random_time__or_none():
    factory = randog.factory.randtime().or_none(0.5)

    value_types = set(map(lambda x: type(factory.next()), range(200)))

    assert value_types == {type(None), dt.time}


def test__random_time__or_none_0():
    factory = randog.factory.randtime().or_none(0)

    value_types = set(map(lambda x: type(factory.next()), range(200)))

    assert value_types == {dt.time}


@pytest.mark.parametrize(
    ("minimum", "maximum"),
    (
        (
            dt.time(11, 22, 33, 444_555),
            dt.time(11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
        ),
        (
            dt.time(11, 22, 33, 444_555, tzinfo=dt.timezone.utc),
            dt.time(11, 22, 33, 444_555),
        ),
    ),
)
def test__random_time__error_when_naive_and_aware(minimum, maximum):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randtime(minimum, maximum)
    e = e_ctx.value

    assert (
        e.message
        == "cannot define range for randtime with a naive time and an aware time"
    )


@pytest.mark.parametrize(
    ("args", "kwargs"),
    [
        ([dt.time(12, 34, 56), dt.time(14, 34, 56)], {}),
        ([dt.time(12, 34, 56), dt.time(14, 34, 56)], {"tzinfo": None}),
        (
            [dt.time(12, 34, 56), dt.time(14, 34, 56)],
            {"tzinfo": dt.timezone.utc},
        ),
    ],
)
def test__random_time__seed(args, kwargs):
    seed = 12
    rnd1 = random.Random(seed)
    rnd2 = random.Random(seed)
    factory1 = randog.factory.randtime(*args, rnd=rnd1, **kwargs)
    factory2 = randog.factory.randtime(*args, rnd=rnd2, **kwargs)

    generated1 = list(factory1.iter(20))
    generated2 = list(factory2.iter(20))

    assert generated1 == generated2
