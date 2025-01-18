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
    ("maximum", "expected", "resume"),
    (
        (
            dt.datetime(2000, 1, 2, 3, 4, 59, 999),
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 59),
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
def test__iterrange__datetime__maximum(maximum, expected, resume, caplog):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.datetime(2000, 1, 2, 3, 4, 58)
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
            dt.datetime(2000, 1, 2, 3, 4, 59, 999),
            None,
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 59),
                dt.datetime(2000, 1, 2, 3, 4, 58),
            ),
            True,
        ),
        (
            dt.datetime(2000, 1, 2, 4, 0, 0, 999),
            None,
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 59),
                dt.datetime(2000, 1, 2, 3, 5, 0),
            ),
            False,
        ),
        # resume_from < initial_value
        (
            dt.datetime(2000, 1, 2, 3, 4, 59, 999),
            dt.datetime(2000, 1, 2, 3, 4, 0),
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 59),
                dt.datetime(2000, 1, 2, 3, 4, 0),
            ),
            True,
        ),
        # initial_value < resume_from
        (
            dt.datetime(2000, 1, 2, 3, 4, 59, 999),
            dt.datetime(2000, 1, 2, 3, 4, 58, 500),
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 59),
                dt.datetime(2000, 1, 2, 3, 4, 58, 500),
            ),
            True,
        ),
    ),
)
def test__iterrange__datetime__maximum__cyclic(
    maximum, resume_from, expected, resume, caplog
):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.datetime(2000, 1, 2, 3, 4, 58)
    expected_resume_by = resume_from if resume_from is not None else initial_value
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
            f"from {expected_resume_by}",
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
        (
            dt.timedelta(seconds=-1),
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 57),
                dt.datetime(2000, 1, 2, 3, 4, 56),
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
    ("step", "maximum", "cyclic", "expected"),
    (
        (
            dt.timedelta(seconds=-1),
            dt.datetime(2000, 1, 2, 3, 4, 55),
            False,
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 57),
                dt.datetime(2000, 1, 2, 3, 4, 56),
                dt.datetime(2000, 1, 2, 3, 4, 55),
            ),
        ),
        (
            dt.timedelta(seconds=-2),
            dt.datetime(2000, 1, 2, 3, 4, 54),
            False,
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 56),
                dt.datetime(2000, 1, 2, 3, 4, 54),
            ),
        ),
        (
            dt.timedelta(seconds=-1),
            dt.datetime(2000, 1, 2, 3, 4, 55),
            True,
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 57),
                dt.datetime(2000, 1, 2, 3, 4, 56),
                dt.datetime(2000, 1, 2, 3, 4, 55),
            ),
        ),
        (
            dt.timedelta(seconds=-2),
            dt.datetime(2000, 1, 2, 3, 4, 54),
            True,
            (
                dt.datetime(2000, 1, 2, 3, 4, 58),
                dt.datetime(2000, 1, 2, 3, 4, 56),
                dt.datetime(2000, 1, 2, 3, 4, 54),
                dt.datetime(2000, 1, 2, 3, 4, 58),
            ),
        ),
    ),
)
def test__iterrange__datetime__negative_step__maximum(
    step, maximum, cyclic, expected, caplog
):
    caplog.set_level(logging.DEBUG)
    initial_value = dt.datetime(2000, 1, 2, 3, 4, 58)
    factory = randog.factory.iterrange(initial_value, maximum, step=step, cyclic=cyclic)

    values = (*factory.iter(4),)

    assert values == expected


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

    assert e.message == (
        "arguments of iterrange() must satisfy initial_value <= maximum"
    )


@pytest.mark.parametrize(
    ("initial_value", "resume_from", "maximum"),
    (
        (
            dt.datetime(2000, 1, 2, 3, 4, 58),
            dt.datetime(2000, 1, 2, 3, 5, 0),
            dt.datetime(2000, 1, 2, 3, 4, 59),
        ),
    ),
)
def test__iterrange__datetime__error_when_maximum_is_lower_than_resume_value(
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
            dt.datetime(2000, 1, 2, 3, 4, 57),
            dt.datetime(2000, 1, 2, 3, 4, 58),
            dt.timedelta(seconds=-1),
        ),
        (
            dt.datetime(2000, 1, 2, 3, 4, 56),
            dt.datetime(2000, 1, 2, 3, 4, 58),
            dt.timedelta(days=-1),
        ),
    ),
)
def test__iterrange__datetime__err_when_maximum_is_great_than_initial_value__with_neg_s(
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
            dt.datetime(2000, 1, 2, 3, 4, 58),
            dt.datetime(2000, 1, 2, 3, 4, 56),
            dt.datetime(2000, 1, 2, 3, 4, 57),
        ),
    ),
)
def test__iterrange__date__err_when_maximum_is_greater_than_resume_value__with_neg_step(
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
            dt.datetime(2000, 1, 29),
            None,
            None,
            dt.datetime(2000, 1, 29),
        ),
        (
            dt.datetime(2000, 1, 29),
            dt.datetime(2000, 1, 30),
            None,
            dt.datetime(2000, 1, 29),
        ),
        (
            dt.datetime(2000, 1, 29),
            None,
            dt.timedelta(days=2),
            dt.datetime(2000, 1, 30),
        ),
        (
            dt.datetime(2000, 1, 29),
            dt.datetime(2000, 1, 31),
            dt.timedelta(days=2),
            dt.datetime(2000, 1, 30),
        ),
    ),
)
def test__iterrange__datetime__error_with_resume_from_and_non_cyclic(
    initial_value, maximum, step, resume_from
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(
            initial_value, maximum, step=step, cyclic=False, resume_from=resume_from
        )
    e = e_ctx.value

    assert e.message == "cannot specify 'resume_from' with cyclic=False"
