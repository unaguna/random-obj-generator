import datetime as dt

import pytest

import randog.factory


def test__random_time():
    factory = randog.factory.randtime()

    value = factory.next()

    assert isinstance(value, dt.time)


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
