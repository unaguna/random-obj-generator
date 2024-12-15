import datetime as dt
import logging

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


@pytest.mark.parametrize(
    ("initial_value", "expected"),
    (
        (
            dt.date(2000, 1, 30),
            (
                dt.date(2000, 1, 30),
                dt.date(2000, 1, 31),
                dt.date(2000, 2, 1),
            ),
        ),
        (
            dt.date(2000, 2, 28),
            (
                dt.date(2000, 2, 28),
                dt.date(2000, 2, 29),
                dt.date(2000, 3, 1),
            ),
        ),
    ),
)
def test__increment__date(initial_value, expected):
    factory = randog.factory.increment(initial_value)

    values = (*factory.iter(3),)

    assert values == expected
    assert set(map(type, values)) == {dt.date}


def test__increment__date__or_none():
    initial_value = dt.date(2000, 1, 2)
    factory = randog.factory.increment(initial_value).or_none()

    values = [factory.next() for _ in range(200)]

    assert {type(v) for v in values} == {dt.date, type(None)}


def test__increment__date__or_none_0():
    initial_value = dt.date(2000, 1, 2)
    factory = randog.factory.increment(initial_value).or_none(0)

    values = [factory.next() for _ in range(200)]

    assert {type(v) for v in values} == {dt.date}


@pytest.mark.parametrize(
    ("maximum", "expected", "resume"),
    (
        (
            dt.date(2000, 1, 31),
            (
                dt.date(2000, 1, 30),
                dt.date(2000, 1, 31),
                dt.date(2000, 1, 30),
            ),
            True,
        ),
        (
            dt.date(2000, 2, 1),
            (
                dt.date(2000, 1, 30),
                dt.date(2000, 1, 31),
                dt.date(2000, 2, 1),
            ),
            False,
        ),
    ),
)
def test__increment__date__maximum(maximum, expected, resume, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.date(2000, 1, 30)
    factory = randog.factory.increment(initial_value, maximum=maximum)

    values = (*factory.iter(3),)

    assert values == expected

    # assert logging
    if resume:
        assert len(caplog.record_tuples) == 1
        assert caplog.record_tuples[0] == (
            "randog.factory",
            logging.DEBUG,
            "increment() has reached its maximum value and resumes "
            f"from {initial_value}",
        )
    else:
        assert len(caplog.records) == 0


@pytest.mark.parametrize(
    ("step", "expected"),
    (
        (
            None,
            (
                dt.date(2000, 1, 30),
                dt.date(2000, 1, 31),
                dt.date(2000, 2, 1),
            ),
        ),
        (
            dt.timedelta(days=7),
            (
                dt.date(2000, 1, 30),
                dt.date(2000, 2, 6),
                dt.date(2000, 2, 13),
            ),
        ),
    ),
)
def test__increment__date__step(step, expected, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.date(2000, 1, 30)
    factory = randog.factory.increment(initial_value, step=step)

    values = (*factory.iter(3),)

    assert values == expected

    # assert logging
    assert len(caplog.records) == 0


@pytest.mark.parametrize(
    ("step",),
    (
        (dt.timedelta(hours=23),),
        (dt.timedelta(hours=1),),
        (dt.timedelta(minutes=1),),
        (dt.timedelta(seconds=1),),
        (dt.timedelta(milliseconds=1),),
        (dt.timedelta(microseconds=1),),
    ),
)
def test__increment__date__error_with_tiny_step(step, caplog):
    initial_value = dt.date(2000, 1, 30)

    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.increment(initial_value, step=step)
    e = e_ctx.value

    assert e.message == "step must be a day/days if initial_value is date"


@pytest.mark.parametrize(
    ("initial_value", "maximum"),
    (
        (
            dt.datetime(2000, 1, 30),
            dt.datetime(2000, 1, 29),
        ),
        (
            dt.datetime(2000, 2, 1),
            dt.datetime(2000, 1, 31),
        ),
    ),
)
def test__increment__date__error_when_maximum_is_lower_than_initial_value(
    initial_value, maximum
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.increment(initial_value, maximum)
    e = e_ctx.value

    assert (
        e.message == "arguments of increment(initial_value, maximum) must satisfy "
        "initial_value <= maximum"
    )
