import datetime as dt

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__random_timedelta():
    factory = randog.factory.randtimedelta()

    value = factory.next()

    assert isinstance(value, dt.timedelta)


@pytest.mark.parametrize(
    "expected_value",
    (
        dt.timedelta(0),
        dt.timedelta(days=2),
        dt.timedelta(seconds=5),
        dt.timedelta(microseconds=5),
        dt.timedelta(days=1, seconds=10, microseconds=500),
    ),
)
def test__random_timedelta__value(expected_value):
    factory = randog.factory.randtimedelta(expected_value, expected_value)

    value = factory.next()

    assert isinstance(value, dt.timedelta)
    assert value == expected_value


@pytest.mark.parametrize(
    ("minimum", "maximum", "expected_unit"),
    (
        (
            dt.timedelta(days=10),
            dt.timedelta(days=15),
            dt.timedelta(days=1),
        ),
        (
            dt.timedelta(days=1),
            dt.timedelta(days=1, hours=12),
            dt.timedelta(hours=1),
        ),
        (
            dt.timedelta(days=1, minutes=30),
            dt.timedelta(days=2),
            dt.timedelta(minutes=1),
        ),
        (
            dt.timedelta(days=1),
            dt.timedelta(days=1, seconds=6),
            dt.timedelta(seconds=1),
        ),
        (
            dt.timedelta(days=1),
            dt.timedelta(days=1, milliseconds=6),
            dt.timedelta(milliseconds=1),
        ),
        (
            dt.timedelta(days=1),
            dt.timedelta(days=1, microseconds=6),
            dt.timedelta(microseconds=1),
        ),
        (
            dt.timedelta(days=1, minutes=5),
            dt.timedelta(days=2, seconds=6),
            dt.timedelta(seconds=1),
        ),
    ),
)
def test__random_timedelta__default_unit(minimum, maximum, expected_unit):
    factory = randog.factory.randtimedelta(minimum, maximum)

    for value in factory.iter(200):
        assert (value / expected_unit).is_integer()


@pytest.mark.parametrize(
    ("min_or_max", "expected_unit"),
    (
        (
            dt.timedelta(days=10),
            dt.timedelta(days=1),
        ),
        (
            dt.timedelta(days=1, hours=12),
            dt.timedelta(hours=1),
        ),
        (
            dt.timedelta(days=1, minutes=30),
            dt.timedelta(minutes=1),
        ),
        (
            dt.timedelta(days=1, seconds=6),
            dt.timedelta(seconds=1),
        ),
        (
            dt.timedelta(days=1, milliseconds=6),
            dt.timedelta(milliseconds=1),
        ),
        (
            dt.timedelta(days=1, microseconds=6),
            dt.timedelta(microseconds=1),
        ),
    ),
)
def test__random_timedelta__default_unit__omit_min_or_max(min_or_max, expected_unit):
    factory_a = randog.factory.randtimedelta(min_or_max, None)
    factory_b = randog.factory.randtimedelta(None, min_or_max)

    for value_a, value_b in zip(factory_a.iter(200), factory_b.iter(200)):
        assert min_or_max <= value_a
        assert (value_a / expected_unit).is_integer()
        assert min_or_max >= value_b
        assert (value_b / expected_unit).is_integer()


@pytest.mark.parametrize(
    ("minimum", "maximum", "unit"),
    (
        (
            None,
            dt.timedelta(days=10),
            dt.timedelta(days=1),
        ),
        (
            dt.timedelta(days=1, hours=12),
            None,
            dt.timedelta(hours=1),
        ),
        (
            None,
            None,
            dt.timedelta(days=1),
        ),
    ),
)
def test__random_timedelta__default_min_max__with_unit(minimum, maximum, unit):
    factory = randog.factory.randtimedelta(minimum, maximum, unit=unit)

    for value in factory.iter(200):
        assert (value / unit).is_integer()
        if minimum is not None:
            assert minimum <= value
        if maximum is not None:
            assert maximum >= value


@pytest.mark.parametrize(
    ("minimum", "maximum", "unit", "expected_value"),
    (
        (
            dt.timedelta(days=1),
            dt.timedelta(days=1, hours=12),
            dt.timedelta(days=1),
            dt.timedelta(days=1),
        ),
        (
            dt.timedelta(days=1),
            dt.timedelta(days=1, seconds=6),
            dt.timedelta(seconds=7),
            dt.timedelta(days=1, seconds=1),
        ),
        (
            dt.timedelta(days=1),
            dt.timedelta(days=1, microseconds=6),
            dt.timedelta(microseconds=7),
            dt.timedelta(days=1, microseconds=1),
        ),
        (
            dt.timedelta(seconds=1),
            dt.timedelta(seconds=1, microseconds=5),
            dt.timedelta(microseconds=6),
            dt.timedelta(seconds=1, microseconds=2),
        ),
    ),
)
def test__random_timedelta__unit(minimum, maximum, unit, expected_value):
    factory = randog.factory.randtimedelta(minimum, maximum, unit=unit)

    value = factory.next()

    assert isinstance(value, dt.timedelta)
    assert value == expected_value
    assert (value / unit).is_integer()


def test__random_timedelta__error_when_unit_is_zero():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randtimedelta(unit=dt.timedelta(0))
    e = e_ctx.value

    assert e.message == "the unit for randtimedelta must not be zero"


def test__random_timedelta__or_none():
    expected_value = dt.timedelta(seconds=5)
    factory = randog.factory.randtimedelta(expected_value, expected_value).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {expected_value, None}


def test__random_timedelta__or_none_0():
    expected_value = dt.timedelta(seconds=5)
    factory = randog.factory.randtimedelta(expected_value, expected_value).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {expected_value}


def test__random_timedelta__error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randtimedelta(
            dt.timedelta(seconds=5, microseconds=1),
            dt.timedelta(seconds=5),
        )
    e = e_ctx.value

    assert e.message == "empty range for randtimedelta"


@pytest.mark.parametrize(
    ("minimum", "maximum", "unit"),
    (
        (
            dt.timedelta(days=1, hours=1),
            dt.timedelta(days=1, hours=12),
            dt.timedelta(days=1),
        ),
        (
            dt.timedelta(seconds=5),
            dt.timedelta(seconds=7),
            dt.timedelta(seconds=4),
        ),
    ),
)
def test__random_timedelta__error_when_too_tight_edges_for_unit(minimum, maximum, unit):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randtimedelta(minimum, maximum, unit=unit)
    e = e_ctx.value

    assert e.message == "empty range for randtimedelta"
