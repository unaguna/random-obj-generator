import datetime as dt
import logging

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


@pytest.mark.parametrize(
    ("initial_value", "expected"),
    (
        (
            dt.timedelta(0),
            (
                dt.timedelta(seconds=0),
                dt.timedelta(seconds=1),
                dt.timedelta(seconds=2),
            ),
        ),
        (
            dt.timedelta(hours=1),
            (
                dt.timedelta(hours=1, seconds=0),
                dt.timedelta(hours=1, seconds=1),
                dt.timedelta(hours=1, seconds=2),
            ),
        ),
    ),
)
def test__increment__timedelta(initial_value, expected):
    factory = randog.factory.increment(initial_value)

    values = (*factory.iter(3),)

    assert values == expected
    assert set(map(type, values)) == {dt.timedelta}


def test__increment__timedelta__or_none():
    initial_value = dt.timedelta(hours=1)
    factory = randog.factory.increment(initial_value).or_none()

    values = [factory.next() for _ in range(200)]

    assert {type(v) for v in values} == {dt.timedelta, type(None)}


def test__increment__timedelta__or_none_0():
    initial_value = dt.timedelta(hours=1)
    factory = randog.factory.increment(initial_value).or_none(0)

    values = [factory.next() for _ in range(200)]

    assert {type(v) for v in values} == {dt.timedelta}


@pytest.mark.parametrize(
    ("maximum", "expected", "resume"),
    (
        (
            dt.timedelta(minutes=1),
            (
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=60),
                dt.timedelta(seconds=59),
            ),
            True,
        ),
        (
            dt.timedelta(minutes=1, seconds=1),
            (
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=60),
                dt.timedelta(seconds=61),
            ),
            False,
        ),
    ),
)
def test__increment__timedelta__maximum(maximum, expected, resume, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.timedelta(seconds=59)
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
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=60),
                dt.timedelta(seconds=61),
            ),
        ),
        (
            dt.timedelta(seconds=10),
            (
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=69),
                dt.timedelta(seconds=79),
            ),
        ),
        (
            dt.timedelta(milliseconds=10),
            (
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=59, milliseconds=10),
                dt.timedelta(seconds=59, milliseconds=20),
            ),
        ),
    ),
)
def test__increment__timedelta__step(step, expected, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.timedelta(seconds=59)
    factory = randog.factory.increment(initial_value, step=step)

    values = (*factory.iter(3),)

    assert values == expected

    # assert logging
    assert len(caplog.records) == 0


@pytest.mark.parametrize(
    ("initial_value", "maximum"),
    (
        (
            dt.timedelta(days=1, microseconds=1),
            dt.timedelta(days=1),
        ),
        (
            dt.timedelta(microseconds=1),
            dt.timedelta(0),
        ),
    ),
)
def test__increment__timedelta__error_when_maximum_is_lower_than_initial_value(
    initial_value, maximum
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.increment(initial_value, maximum)
    e = e_ctx.value

    assert (
        e.message == "arguments of increment(initial_value, maximum) must satisfy "
        "initial_value <= maximum"
    )
