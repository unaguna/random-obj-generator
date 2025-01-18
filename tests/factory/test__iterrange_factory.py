import logging

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__iterrange():
    factory = randog.factory.iterrange()

    values = (*factory.iter(10),)

    assert values == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    assert set(map(type, values)) == {int}


def test__iterrange__or_none():
    factory = randog.factory.iterrange().or_none()

    values = set(map(lambda x: factory.next(), range(200)))

    assert set(map(type, values)) == {int, type(None)}


def test__iterrange__or_none_0():
    factory = randog.factory.iterrange().or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert set(map(type, values)) == {int}


@pytest.mark.parametrize(
    ("initial_value", "expected"), ((None, (1, 2, 3)), (1, (1, 2, 3)), (3, (3, 4, 5)))
)
def test__iterrange__initial_value(initial_value, expected):
    factory = randog.factory.iterrange(initial_value)

    values = (*factory.iter(3),)

    assert values == expected


@pytest.mark.parametrize(
    ("maximum", "expected", "resume"),
    (
        (None, (1, 2, 3), False),
        (3, (1, 2, 3), False),
        (2, (1, 2), True),
    ),
)
def test__iterrange__maximum(maximum, expected, resume, caplog):
    caplog.set_level(logging.DEBUG)
    factory = randog.factory.iterrange(maximum=maximum)

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
        (None, (1, 2, 3), False),
        (3, (1, 2, 3), False),
        (2, (1, 2, 1), True),
    ),
)
def test__iterrange__maximum__cyclic(maximum, expected, resume, caplog):
    caplog.set_level(logging.DEBUG)
    factory = randog.factory.iterrange(maximum=maximum, cyclic=True)

    values = (*factory.iter(3),)

    assert values == expected

    # assert logging
    if resume:
        assert len(caplog.record_tuples) == 1
        assert caplog.record_tuples[0] == (
            "randog.factory",
            logging.DEBUG,
            "iterrange() has reached its maximum value and resumes from 1",
        )
    else:
        assert len(caplog.records) == 0


@pytest.mark.parametrize(
    ("step", "expected"),
    (
        (None, (1, 2, 3)),
        (2, (1, 3, 5)),
        (-1, (1, 0, -1)),
    ),
)
def test__iterrange__step(step, expected, caplog):
    caplog.set_level(logging.DEBUG)
    factory = randog.factory.iterrange(step=step)

    values = (*factory.iter(3),)

    assert values == expected

    # assert logging
    assert len(caplog.records) == 0


@pytest.mark.parametrize(
    ("step", "maximum", "cyclic", "expected"),
    (
        (-1, -4, False, (1, 0, -1, -2)),
        (-2, -4, False, (1, -1, -3)),
        (-1, -4, True, (1, 0, -1, -2)),
        (-2, -4, True, (1, -1, -3, 1)),
    ),
)
def test__iterrange__negative_step__maximum(step, maximum, cyclic, expected, caplog):
    caplog.set_level(logging.DEBUG)
    factory = randog.factory.iterrange(maximum=maximum, step=step, cyclic=cyclic)

    values = (*factory.iter(4),)

    assert values == expected


@pytest.mark.parametrize(
    ("initial_value", "maximum", "expected", "resume"),
    (
        (None, None, (1, 2, 3), False),
        (1, None, (1, 2, 3), False),
        (None, 3, (1, 2, 3), False),
        (4, 5, (4, 5), True),
        (5, 5, (5,), True),
    ),
)
def test__iterrange__initial_value__maximum(
    initial_value, maximum, expected, resume, caplog
):
    caplog.set_level(logging.DEBUG)
    factory = randog.factory.iterrange(initial_value, maximum)

    values = (*factory.iter(3),)

    assert values == expected

    # assert logging
    if resume:
        assert len(caplog.records) == 1
        assert caplog.record_tuples[0] == (
            "randog.factory",
            logging.DEBUG,
            "iterrange() has reached its maximum value. "
            "This factory no longer generates values.",
        )
    else:
        assert len(caplog.records) == 0


@pytest.mark.parametrize(
    ("initial_value", "maximum", "resume_from", "expected", "resume", "resume_cnt"),
    (
        (None, None, None, (1, 2, 3, 4), False, 0),
        (1, None, None, (1, 2, 3, 4), False, 0),
        (None, 4, None, (1, 2, 3, 4), False, 0),
        (4, 5, None, (4, 5, 4, 5), True, 1),
        (5, 5, None, (5, 5, 5, 5), True, 3),
        (4, 5, 1, (4, 5, 1, 2), True, 1),
        (3, 5, 4, (3, 4, 5, 4), True, 1),
        (4, 5, 5, (4, 5, 5, 5), True, 2),
    ),
)
def test__iterrange__initial_value__maximum__cyclic(
    initial_value, maximum, resume_from, expected, resume, resume_cnt, caplog
):
    caplog.set_level(logging.DEBUG)
    factory = randog.factory.iterrange(
        initial_value, maximum, cyclic=True, resume_from=resume_from
    )
    expected_resume_by = resume_from if resume_from is not None else initial_value

    values = (*factory.iter(4),)

    assert values == expected

    # assert logging
    assert len(caplog.record_tuples) == resume_cnt
    if resume:
        assert (
            tuple(caplog.record_tuples)
            == (
                (
                    "randog.factory",
                    logging.DEBUG,
                    "iterrange() has reached its maximum value and resumes "
                    f"from {expected_resume_by}",
                ),
            )
            * resume_cnt
        )
    else:
        assert len(caplog.records) == 0


@pytest.mark.parametrize(("initial_value", "maximum"), ((4, 3), (5, 3)))
def test__iterrange__error_when_maximum_is_lower_than_initial_value(
    initial_value, maximum
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(initial_value, maximum)
    e = e_ctx.value

    assert e.message == (
        "arguments of iterrange() must satisfy initial_value <= maximum"
    )


@pytest.mark.parametrize(("initial_value", "resume_from", "maximum"), ((2, 4, 3),))
def test__iterrange__error_when_maximum_is_lower_than_resume_value(
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


@pytest.mark.parametrize(("initial_value", "maximum", "step"), ((3, 4, -1), (2, 4, -1)))
def test__iterrange__error_when_maximum_is_greater_than_initial_value__with_neg_step(
    initial_value, maximum, step
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(initial_value, maximum, step=step)
    e = e_ctx.value

    assert e.message == (
        "arguments of iterrange() must satisfy maximum <= initial_value if step < 0"
    )


@pytest.mark.parametrize(
    ("initial_value", "resume_from", "maximum"), ((6, 4, 5), (2, -2, -1))
)
def test__iterrange__error_when_maximum_is_greater_than_resume_value__with_neg_step(
    initial_value, resume_from, maximum
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(
            initial_value, maximum, step=-1, cyclic=True, resume_from=resume_from
        )
    e = e_ctx.value

    assert e.message == (
        "arguments of iterrange() must satisfy maximum <= resume_from "
        "if resume_from is specified and step < 0"
    )


@pytest.mark.parametrize(
    ("initial_value", "maximum", "step", "resume_from"),
    (
        (2, None, None, 1),
        (2, 4, None, 1),
        (2, None, 2, 1),
        (3, 4, -1, 0),
    ),
)
def test__iterrange__error_with_resume_from_and_non_cyclic(
    initial_value, maximum, step, resume_from
):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.iterrange(
            initial_value, maximum, step=step, cyclic=False, resume_from=resume_from
        )
    e = e_ctx.value

    assert e.message == "cannot specify 'resume_from' with cyclic=False"
