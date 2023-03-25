import math
from decimal import Decimal
from fractions import Fraction

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__random_decimal():
    factory = randog.factory.randdecimal()

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
    factory = randog.factory.randdecimal(expected_value, expected_value)

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
    factory = randog.factory.randdecimal(condition, condition)

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
    factory = randog.factory.randdecimal(condition, condition)

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
    factory = randog.factory.randdecimal(condition, condition)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


@pytest.mark.parametrize(
    ("condition", "decimal_len", "expected_value"),
    (
        (1.0, 0, Decimal("1")),
        (1.0, 1, Decimal("1.0")),
        (1.0, 2, Decimal("1.00")),
        (0.2, 0, Decimal("0")),
        (0.2, 1, Decimal("0.2")),
        (0.2, 2, Decimal("0.20")),
        (15.0, 0, Decimal("15")),
        (15.0, 1, Decimal("15.0")),
        (15.0, 2, Decimal("15.00")),
    ),
)
def test__random_decimal__decimal_len(condition, decimal_len, expected_value):
    factory = randog.factory.randdecimal(condition, condition, decimal_len=decimal_len)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value
    assert value.as_tuple() == expected_value.as_tuple()  # check decimal length


@pytest.mark.parametrize(
    ("p_inf", "n_inf", "expected_value"),
    (
        (1.0, 0.0, Decimal("inf")),
        (0.0, 1.0, Decimal("-inf")),
    ),
)
def test__random_decimal__inf(p_inf, n_inf, expected_value):
    factory = randog.factory.randdecimal(p_inf=p_inf, n_inf=n_inf)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert value == expected_value


def test__random_decimal__nan():
    factory = randog.factory.randdecimal(nan=1.0)

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
    factory = randog.factory.randdecimal(p_inf=p_inf, n_inf=n_inf)

    value = factory.next()

    assert isinstance(value, Decimal)
    assert math.isfinite(value)


def test__random_decimal__or_none():
    factory = randog.factory.randdecimal(1, 1).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {Decimal("1"), None}
    value = next(filter(lambda x: x is not None, values))
    assert isinstance(value, Decimal)


def test__random_decimal__or_none_0():
    factory = randog.factory.randdecimal(1, 1).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {Decimal("1")}
    value = next(filter(lambda x: x is not None, values))
    assert isinstance(value, Decimal)


def test__random_decimal__error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randdecimal(2, 1)
    e = e_ctx.value

    assert e.message == "empty range for randfloat"


def test__random_decimal__error_when_probability_gt_1():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randdecimal(p_inf=0.625, n_inf=0.5)
    e = e_ctx.value

    assert (
        e.message
        == "the sum of probabilities `p_inf`, `n_inf`, and `nan` must range from 0 to 1"
    )


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
        randog.factory.randdecimal(p_inf=p_inf, n_inf=n_inf, nan=nan)
    e = e_ctx.value

    assert (
        e.message
        == "the probabilities `p_inf`, `n_inf`, and `nan` must range from 0 to 1"
    )
