import datetime as dt
import logging

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


@pytest.mark.parametrize(
    ("initial_value", "expected"),
    (
        (
            dt.datetime(2000, 1, 2, 3, 4, 58),
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 59),
                dt.datetime(2000, 1, 2, 3, 5, 0),
            ),
        ),
        (
            dt.datetime(2000, 1, 2, 3, 59, 58),
            (
                dt.datetime(2000, 1, 2, 3, 59, 58),
                dt.datetime(2000, 1, 2, 3, 59, 59),
                dt.datetime(2000, 1, 2, 4, 0, 0),
            ),
        ),
    ),
)
def test__iterrange__datetime(initial_value, expected):
    factory = randog.factory.iterrange(initial_value)

    values = (*factory.iter(3),)

    assert values == expected
    assert set(map(type, values)) == {dt.datetime}


def test__iterrange__datetime__or_none():
    initial_value = dt.datetime(2000, 1, 2, 3, 4, 58)
    factory = randog.factory.iterrange(initial_value).or_none()

    values = [factory.next() for _ in range(200)]

    assert {type(v) for v in values} == {dt.datetime, type(None)}


def test__iterrange__datetime__or_none_0():
    initial_value = dt.datetime(2000, 1, 2, 3, 4, 58)
    factory = randog.factory.iterrange(initial_value).or_none(0)

    values = [factory.next() for _ in range(200)]

    assert {type(v) for v in values} == {dt.datetime}


@pytest.mark.parametrize(
    ("maximum", "expected"),
    (
        (
            dt.datetime(2000, 1, 2, 3, 4, 59, 999),
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 59),
            ),
        ),
        (
            dt.datetime(2000, 1, 2, 4, 0, 0, 999),
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 59),
                dt.datetime(2000, 1, 2, 3, 5, 0),
            ),
        ),
    ),
)
def test__iterrange__datetime__maximum(maximum, expected, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.datetime(2000, 1, 2, 3, 4, 58)
    factory = randog.factory.iterrange(initial_value, maximum=maximum)

    values = (*factory.iter(3),)

    assert values == expected

    # assert logging
    assert len(caplog.records) == 0


@pytest.mark.parametrize(
    ("maximum", "expected", "resume"),
    (
        (
            dt.datetime(2000, 1, 2, 3, 4, 59, 999),
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 59),
                dt.datetime(2000, 1, 2, 3, 4, 58),
            ),
            True,
        ),
        (
            dt.datetime(2000, 1, 2, 4, 0, 0, 999),
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 59),
                dt.datetime(2000, 1, 2, 3, 5, 0),
            ),
            False,
        ),
    ),
)
def test__iterrange__datetime__maximum__cyclic(maximum, expected, resume, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.datetime(2000, 1, 2, 3, 4, 58)
    factory = randog.factory.iterrange(initial_value, maximum=maximum, cyclic=True)

    values = (*factory.iter(3),)

    assert values == expected

    # assert logging
    if resume:
        assert len(caplog.record_tuples) == 1
        assert caplog.record_tuples[0] == (
            "randog.factory",
            logging.DEBUG,
            "iterrange() has reached its maximum value and resumes "
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
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 59),
                dt.datetime(2000, 1, 2, 3, 5, 0),
            ),
        ),
        (
            dt.timedelta(seconds=10),
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 5, 8),
                dt.datetime(2000, 1, 2, 3, 5, 18),
            ),
        ),
    ),
)
def test__iterrange__datetime__step(step, expected, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.datetime(2000, 1, 2, 3, 4, 58)
    factory = randog.factory.iterrange(initial_value, step=step)

    values = (*factory.iter(3),)

    assert values == expected

    # assert logging
    assert len(caplog.records) == 0


@pytest.mark.parametrize(
    ("initial_value", "maximum"),
    (
        (
            dt.datetime(2000, 1, 2, 3, 4, 58),
            dt.datetime(2000, 1, 2, 3, 4, 57),
        ),
        (
            dt.datetime(2000, 1, 2, 3, 4, 58),
            dt.datetime(2000, 1, 2, 3, 4, 56),
        ),
    ),
)
def test__iterrange__datetime__error_when_maximum_is_lower_than_initial_value(
    initial_value, maximum
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(initial_value, maximum)
    e = e_ctx.value

    assert (
        e.message == "arguments of iterrange(initial_value, maximum) must satisfy "
        "initial_value <= maximum"
    )
