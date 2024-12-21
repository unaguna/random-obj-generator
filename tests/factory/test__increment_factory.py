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
        (2, (1, 2, 1), True),
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
            "iterrange() has reached its maximum value and resumes from 1",
        )
    else:
        assert len(caplog.records) == 0


@pytest.mark.parametrize(
    ("step", "expected"),
    (
        (None, (1, 2, 3)),
        (2, (1, 3, 5)),
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
    ("initial_value", "maximum", "expected", "resume", "resume_cnt"),
    (
        (None, None, (1, 2, 3), False, 0),
        (1, None, (1, 2, 3), False, 0),
        (None, 3, (1, 2, 3), False, 0),
        (4, 5, (4, 5, 4), True, 1),
        (5, 5, (5, 5, 5), True, 2),
    ),
)
def test__iterrange__initial_value__maximum(
    initial_value, maximum, expected, resume, resume_cnt, caplog
):
    caplog.set_level(logging.DEBUG)
    factory = randog.factory.iterrange(initial_value, maximum)

    values = (*factory.iter(3),)

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
                    f"from {initial_value}",
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

    assert (
        e.message == "arguments of iterrange(initial_value, maximum) must satisfy "
        "initial_value <= maximum"
    )
