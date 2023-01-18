import math
from decimal import Decimal
from fractions import Fraction

import pytest

import ranog.factory
from ranog.exceptions import FactoryConstructionError


def test__random_decimal():
    factory = ranog.factory.randdecimal()

    value = factory.next()

    assert isinstance(value, Decimal)


@pytest.mark.parametrize(
    "expected_value",
    (
        Decimal("0.25"),
        Decimal("0.125"),
    ),
)
def test__random_decimal__by_decimal(expected_value):
    factory = ranog.factory.randdecimal(expected_value, expected_value)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "expected_value"),
    (
        (-1.0, Decimal(-1)),
        (0.0, Decimal(0)),
        (1.0, Decimal(1)),
    ),
)
def test__random_decimal__by_float(condition, expected_value):
    factory = ranog.factory.randdecimal(condition, condition)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "expected_value"),
    (
        (1, Decimal(1)),
        (2, Decimal(2)),
    ),
)
def test__random_decimal__by_int(condition, expected_value):
    factory = ranog.factory.randdecimal(condition, condition)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "expected_value"),
    (
        (Fraction("1/4"), Decimal(0.25)),
        (Fraction("1/8"), Decimal(0.125)),
    ),
)
def test__random_decimal__by_fraction(condition, expected_value):
    factory = ranog.factory.randdecimal(condition, condition)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


@pytest.mark.parametrize(
    ("p_inf", "n_inf", "expected_value"),
    (
        (1.0, 0.0, Decimal("inf")),
        (0.0, 1.0, Decimal("-inf")),
    ),
)
def test__random_decimal__inf(p_inf, n_inf, expected_value):
    factory = ranog.factory.randdecimal(p_inf=p_inf, n_inf=n_inf)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


def test__random_decimal__nan():
    factory = ranog.factory.randdecimal(nan=1.0)

    value = factory.next()

    assert isinstance(value, Decimal)
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
def test__random_decimal__inf_zero(p_inf, n_inf):
    factory = ranog.factory.randdecimal(p_inf=p_inf, n_inf=n_inf)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert math.isfinite(value)


def test__random_decimal__error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.randdecimal(2, 1)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"


def test__random_decimal__error_when_probability_gt_1():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.randdecimal(p_inf=0.625, n_inf=0.5)
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
def test__random_decimal__error_when_negative_probability(p_inf, n_inf, nan):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.randdecimal(p_inf=p_inf, n_inf=n_inf, nan=nan)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"
