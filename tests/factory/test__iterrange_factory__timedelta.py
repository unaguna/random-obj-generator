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
def test__iterrange__timedelta(initial_value, expected):
    factory = randog.factory.iterrange(initial_value)

    values = (*factory.iter(3),)

    assert values == expected
    assert set(map(type, values)) == {dt.timedelta}


def test__iterrange__timedelta__or_none():
    initial_value = dt.timedelta(hours=1)
    factory = randog.factory.iterrange(initial_value).or_none()

    values = [factory.next() for _ in range(200)]

    assert {type(v) for v in values} == {dt.timedelta, type(None)}


def test__iterrange__timedelta__or_none_0():
    initial_value = dt.timedelta(hours=1)
    factory = randog.factory.iterrange(initial_value).or_none(0)

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
def test__iterrange__timedelta__maximum(maximum, expected, resume, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.timedelta(seconds=59)
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
    ("maximum", "resume_from", "expected", "resume"),
    (
        (
            dt.timedelta(minutes=1),
            None,
            (
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=60),
                dt.timedelta(seconds=59),
            ),
            True,
        ),
        (
            dt.timedelta(minutes=1, seconds=1),
            None,
            (
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=60),
                dt.timedelta(seconds=61),
            ),
            False,
        ),
        # resume_from < initial_value
        (
            dt.timedelta(seconds=60),
            dt.timedelta(seconds=1),
            (
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=60),
                dt.timedelta(seconds=1),
            ),
            True,
        ),
        # initial_value < resume_from
        (
            dt.timedelta(seconds=60),
            dt.timedelta(seconds=59, milliseconds=500),
            (
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=60),
                dt.timedelta(seconds=59, milliseconds=500),
            ),
            True,
        ),
    ),
)
def test__iterrange__timedelta__maximum__cyclic(
    maximum, resume_from, expected, resume, caplog
):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.timedelta(seconds=59)
    factory = randog.factory.iterrange(
        initial_value, maximum=maximum, cyclic=True, resume_from=resume_from
    )

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
        (
            dt.timedelta(milliseconds=-10),
            (
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=58, milliseconds=990),
                dt.timedelta(seconds=58, milliseconds=980),
            ),
        ),
    ),
)
def test__iterrange__timedelta__step(step, expected, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.timedelta(seconds=59)
    factory = randog.factory.iterrange(initial_value, step=step)

    values = (*factory.iter(3),)

    assert values == expected

    # assert logging
    assert len(caplog.records) == 0


@pytest.mark.parametrize(
    ("step", "maximum", "expected", "cycle_len"),
    (
        (
            dt.timedelta(seconds=-1),
            dt.timedelta(seconds=56),
            (
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=58),
                dt.timedelta(seconds=57),
                dt.timedelta(seconds=56),
            ),
            4,
        ),
        (
            dt.timedelta(seconds=-2),
            dt.timedelta(seconds=55),
            (
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=57),
                dt.timedelta(seconds=55),
                dt.timedelta(seconds=59),
            ),
            3,
        ),
        (
            dt.timedelta(seconds=-60),
            dt.timedelta(seconds=-120),
            (
                dt.timedelta(seconds=59),
                dt.timedelta(seconds=-1),
                dt.timedelta(seconds=-61),
                dt.timedelta(seconds=59),
            ),
            3,
        ),
    ),
)
@pytest.mark.parametrize("cyclic", (False, True))
def test__iterrange__timedelta__negative_step__maximum(
    step, maximum, cycle_len, cyclic, expected, caplog
):
    if not cyclic:
        expected = expected[0:cycle_len]

    caplog.set_level(logging.DEBUG)
    initial_value = dt.timedelta(seconds=59)
    factory = randog.factory.iterrange(initial_value, maximum, step=step, cyclic=cyclic)

    values = (*factory.iter(4),)

    assert values == expected


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
def test__iterrange__timedelta__error_when_maximum_is_lower_than_initial_value(
    initial_value, maximum
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(initial_value, maximum)
    e = e_ctx.value

    assert e.message == "arguments of iterrange() must satisfy initial_value <= maximum"


@pytest.mark.parametrize(
    ("initial_value", "resume_from", "maximum"),
    (
        (
            dt.timedelta(days=0.5),
            dt.timedelta(days=1, microseconds=1),
            dt.timedelta(days=1),
        ),
    ),
)
def test__iterrange__timedelta__error_when_maximum_is_lower_than_resume_value(
    initial_value, resume_from, maximum
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(
            initial_value, maximum, cyclic=True, resume_from=resume_from
        )
    e = e_ctx.value

    assert e.message == (
        "arguments of iterrange() must satisfy resume_from <= maximum "
        "if resume_from is specified"
    )


@pytest.mark.parametrize(
    ("initial_value", "maximum", "step"),
    (
        (
            dt.timedelta(days=1),
            dt.timedelta(days=1, microseconds=1),
            dt.timedelta(seconds=-1),
        ),
        (
            dt.timedelta(0),
            dt.timedelta(microseconds=1),
            dt.timedelta(microseconds=-1),
        ),
    ),
)
def test__iterrange__timedelta__err_when_maximum_is_great_than_initial_value__with_n_s(
    initial_value, maximum, step
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(initial_value, maximum, step=step)
    e = e_ctx.value

    assert e.message == (
        "arguments of iterrange() must satisfy maximum <= initial_value if step < 0"
    )


@pytest.mark.parametrize(
    ("initial_value", "resume_from", "maximum"),
    (
        (
            dt.timedelta(days=2),
            dt.timedelta(days=0.5),
            dt.timedelta(days=1),
        ),
    ),
)
def test__iterrange__timedelta__err_when_maximum_is_great_than_resume_from__with_n_step(
    initial_value, resume_from, maximum
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(
            initial_value,
            maximum,
            step=dt.timedelta(seconds=-1),
            cyclic=True,
            resume_from=resume_from,
        )
    e = e_ctx.value

    assert e.message == (
        "arguments of iterrange() must satisfy maximum <= resume_from "
        "if resume_from is specified and step < 0"
    )


@pytest.mark.parametrize(
    ("initial_value", "maximum", "step", "resume_from"),
    (
        (
            dt.timedelta(days=2),
            None,
            None,
            dt.timedelta(days=2),
        ),
        (
            dt.timedelta(days=2),
            dt.timedelta(days=3),
            None,
            dt.timedelta(days=1),
        ),
        (
            dt.timedelta(days=2),
            None,
            dt.timedelta(days=2),
            dt.timedelta(days=1),
        ),
        (
            dt.timedelta(days=2),
            dt.timedelta(days=30),
            dt.timedelta(days=2),
            dt.timedelta(days=10),
        ),
    ),
)
def test__iterrange__timedelta__error_with_resume_from_and_non_cyclic(
    initial_value, maximum, step, resume_from
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(
            initial_value, maximum, step=step, cyclic=False, resume_from=resume_from
        )
    e = e_ctx.value

    assert e.message == "cannot specify 'resume_from' with cyclic=False"
