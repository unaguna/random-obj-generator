import math
from decimal import Decimal
from fractions import Fraction

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__random_float():
    factory = randog.factory.randfloat()

    value = factory.next()

    assert isinstance(value, float)


@pytest.mark.parametrize("expected_value", (-1.0, 0.0, 1.0))
def test__random_float__by_float(expected_value):
    factory = randog.factory.randfloat(expected_value, expected_value)

    value = factory.next()

    assert isinstance(value, float)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "expected_value"),
    (
        (1, 1.0),
        (2, 2.0),
    ),
)
def test__random_float__by_int(condition, expected_value):
    factory = randog.factory.randfloat(condition, condition)

    value = factory.next()

    assert isinstance(value, float)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "expected_value"),
    (
        (Decimal("0.25"), 0.25),
        (Decimal("0.125"), 0.125),
    ),
)
def test__random_float__by_decimal(condition, expected_value):
    factory = randog.factory.randfloat(condition, condition)

    value = factory.next()

    assert isinstance(value, float)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "expected_value"),
    (
        (Fraction("1/4"), 0.25),
        (Fraction("1/8"), 0.125),
    ),
)
def test__random_float__by_fraction(condition, expected_value):
    factory = randog.factory.randfloat(condition, condition)

    value = factory.next()

    assert isinstance(value, float)
    assert value == expected_value


@pytest.mark.parametrize(
    ("p_inf", "n_inf", "expected_value"),
    (
        (1.0, 0.0, float("inf")),
        (0.0, 1.0, float("-inf")),
    ),
)
def test__random_float__inf(p_inf, n_inf, expected_value):
    factory = randog.factory.randfloat(p_inf=p_inf, n_inf=n_inf)

    value = factory.next()

    assert isinstance(value, float)
    assert value == expected_value


def test__random_float__nan():
    factory = randog.factory.randfloat(nan=1.0)

    value = factory.next()

    assert isinstance(value, float)
    assert math.isnan(value)


@pytest.mark.parametrize(
    ("p_inf", "n_inf"),
    (
        (0.0, 0.0),
        (-0.0, 0.0),
        (0.0, -0.0),
        (-0.0, -0.0),
    ),
)
def test__random_float__inf_zero(p_inf, n_inf):
    factory = randog.factory.randfloat(p_inf=p_inf, n_inf=n_inf)

    value = factory.next()

    assert isinstance(value, float)
    assert math.isfinite(value)


def test__random_float__or_none():
    factory = randog.factory.randfloat(1, 1).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1.0, None}


def test__random_float__or_none_0():
    factory = randog.factory.randfloat(1, 1).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1.0}


def test__random_float_error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randfloat(2, 1)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"


def test__random_float_error_when_probability_gt_1():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randfloat(p_inf=0.625, n_inf=0.5)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"


@pytest.mark.parametrize(
    ("p_inf", "n_inf", "nan"),
    (
        (-0.1, 0.1, 0.1),
        (0.1, -0.1, 0.1),
        (-0.1, -0.1, 0.1),
        (0.1, 0.1, -0.1),
        (-0.1, 0.1, -0.1),
        (0.1, -0.1, -0.1),
        (-0.1, -0.1, -0.1),
    ),
)
def test__random_float__error_when_negative_probability(p_inf, n_inf, nan):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randfloat(p_inf=p_inf, n_inf=n_inf, nan=nan)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"
