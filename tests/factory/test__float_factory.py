from decimal import Decimal
from fractions import Fraction

import pytest

import ranog.factory
from ranog.exceptions import FactoryConstructionError


@pytest.mark.parametrize("expected_value", (-1.0, 0.0, 1.0))
def test__random_float(expected_value):
    factory = ranog.factory.randfloat(expected_value, expected_value)

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
    factory = ranog.factory.randfloat(condition, condition)

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
    factory = ranog.factory.randfloat(condition, condition)

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
    factory = ranog.factory.randfloat(condition, condition)

    value = factory.next()

    assert isinstance(value, float)
    assert value == expected_value


def test__random_float_error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.randint(2, 1)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"
