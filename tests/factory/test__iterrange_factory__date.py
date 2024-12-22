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
def test__iterrange__date(initial_value, expected):
    factory = randog.factory.iterrange(initial_value)

    values = (*factory.iter(3),)

    assert values == expected
    assert set(map(type, values)) == {dt.date}


def test__iterrange__date__or_none():
    initial_value = dt.date(2000, 1, 2)
    factory = randog.factory.iterrange(initial_value).or_none()

    values = [factory.next() for _ in range(200)]

    assert {type(v) for v in values} == {dt.date, type(None)}


def test__iterrange__date__or_none_0():
    initial_value = dt.date(2000, 1, 2)
    factory = randog.factory.iterrange(initial_value).or_none(0)

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
def test__iterrange__date__maximum(maximum, expected, resume, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.date(2000, 1, 30)
    factory = randog.factory.iterrange(initial_value, maximum=maximum)

    values = (*factory.iter(3),)

    assert values == expected

    # assert logging
    if resume:
        assert len(caplog.record_tuples) == 1
        assert caplog.record_tuples[0] == (
            "randog.factory",
            logging.DEBUG,
            "iterrange() has reached its maximum value. "
            "This factory no longer generates values.",
        )
    else:
        assert len(caplog.records) == 0


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
def test__iterrange__date__maximum__cyclic(maximum, expected, resume, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.date(2000, 1, 30)
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
        (
            dt.timedelta(days=-1),
            (
                dt.date(2000, 1, 30),
                dt.date(2000, 1, 29),
                dt.date(2000, 1, 28),
            ),
        ),
    ),
)
def test__iterrange__date__step(step, expected, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.date(2000, 1, 30)
    factory = randog.factory.iterrange(initial_value, step=step)

    values = (*factory.iter(3),)

    assert values == expected

    # assert logging
    assert len(caplog.records) == 0


@pytest.mark.parametrize(
    ("step", "maximum", "cyclic", "expected"),
    (
        (
            dt.timedelta(days=-1),
            dt.date(2000, 1, 26),
            False,
            (
                dt.date(2000, 1, 30),
                dt.date(2000, 1, 29),
                dt.date(2000, 1, 28),
                dt.date(2000, 1, 27),
            ),
        ),
        (
            dt.timedelta(days=-2),
            dt.date(2000, 1, 26),
            False,
            (
                dt.date(2000, 1, 30),
                dt.date(2000, 1, 28),
                dt.date(2000, 1, 26),
            ),
        ),
        (
            dt.timedelta(days=-1),
            dt.date(2000, 1, 26),
            True,
            (
                dt.date(2000, 1, 30),
                dt.date(2000, 1, 29),
                dt.date(2000, 1, 28),
                dt.date(2000, 1, 27),
            ),
        ),
        (
            dt.timedelta(days=-2),
            dt.date(2000, 1, 26),
            True,
            (
                dt.date(2000, 1, 30),
                dt.date(2000, 1, 28),
                dt.date(2000, 1, 26),
                dt.date(2000, 1, 30),
            ),
        ),
    ),
)
def test__iterrange__date__negative_step__maximum(
    step, maximum, cyclic, expected, caplog
):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.date(2000, 1, 30)
    factory = randog.factory.iterrange(initial_value, maximum, step=step, cyclic=cyclic)

    values = (*factory.iter(4),)

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
@pytest.mark.parametrize("step_sign", (1, -1))
def test__iterrange__date__error_with_tiny_step(step, step_sign, caplog):
    initial_value = dt.date(2000, 1, 30)

    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(initial_value, step=(step * step_sign))
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
def test__iterrange__date__error_when_maximum_is_lower_than_initial_value(
    initial_value, maximum
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(initial_value, maximum)
    e = e_ctx.value

    assert (
        e.message == "arguments of iterrange(initial_value, maximum) must satisfy "
        "initial_value <= maximum"
    )


@pytest.mark.parametrize(
    ("initial_value", "maximum", "step"),
    (
        (
            dt.datetime(2000, 1, 29),
            dt.datetime(2000, 1, 30),
            dt.timedelta(days=-1),
        ),
        (
            dt.datetime(2000, 1, 29),
            dt.datetime(2000, 1, 30),
            dt.timedelta(days=-10),
        ),
    ),
)
def test__iterrange__date__error_when_maximum_is_great_than_initial_value_with_neg_step(
    initial_value, maximum, step
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(initial_value, maximum, step=step)
    e = e_ctx.value

    assert (
        e.message == "arguments of iterrange(initial_value, maximum) must satisfy "
        "maximum <= initial_value if step < 0"
    )
