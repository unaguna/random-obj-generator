import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__random_union__uses_each_factory():
    factory = randog.factory.union(
        randog.factory.randstr(length=0),
        randog.factory.randint(1, 1),
    )

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {"", 1}


@pytest.mark.parametrize("expected_value", (-1, 0, 1))
def test__random_union__value(expected_value):
    factory = randog.factory.union(
        randog.factory.randint(expected_value, expected_value),
        randog.factory.randint(expected_value, expected_value),
    )

    value = factory.next()

    assert value == expected_value


@pytest.mark.parametrize(
    "weights", ([0.8, 0.2, 0], (0.8, 0.2, 0), [0.8, 0.2, 0, 0][:3])
)
def test__random_union__weight(weights):
    factory = randog.factory.union(
        randog.factory.const(1),
        randog.factory.const(2),
        randog.factory.const(3),
        weights=weights,
    )

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1, 2}


def test__random_union__or_none():
    factory = randog.factory.union(
        randog.factory.const(1),
        randog.factory.const(2),
        randog.factory.const(3),
        weights=[0.5, 0.5, 0],
    ).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1, 2, None}


def test__random_int__or_none_0():
    factory = randog.factory.union(
        randog.factory.const(1),
        randog.factory.const(2),
        randog.factory.const(3),
        weights=[0.5, 0.5, 0],
    ).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1, 2}


def test__random_union__error_when_no_factory_specified():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.union()
    e = e_ctx.value

    assert e.message == "no factory is given to union()"


@pytest.mark.parametrize("weights_len", (0, 1, 3))
def test__random_union__error_when_weights_does_not_match(weights_len):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.union(
            randog.factory.const("1"),
            randog.factory.const("2"),
            weights=[1, 1, 1, 1][:weights_len],
        )
    e = e_ctx.value

    assert e.message == "the number of weights must match the factories"
