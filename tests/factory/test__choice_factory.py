import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__random_choice__uses_each_value():
    factory = randog.factory.randchoice(0, 1)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {0, 1}


@pytest.mark.parametrize("expected_value", (-1, 0, "foo", None))
def test__random_choice__one_value(expected_value):
    factory = randog.factory.randchoice(expected_value)

    value = factory.next()

    assert value == expected_value


@pytest.mark.parametrize("expected_value", (-1, 0, 1))
def test__random_choice__value(expected_value):
    factory = randog.factory.randchoice(expected_value, expected_value)

    value = factory.next()

    assert value == expected_value


@pytest.mark.parametrize(
    "weights", ([0.8, 0.2, 0], (0.8, 0.2, 0), [0.8, 0.2, 0, 0][:3])
)
def test__random_choice__weights(weights):
    factory = randog.factory.randchoice(1, 2, 3, weights=weights)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1, 2}


def test__random_choice__or_none():
    factory = randog.factory.randchoice(0, 1).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(400)))

    assert values == {0, 1, None}


def test__random_choice__or_none_0():
    factory = randog.factory.randchoice(0, 1).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {0, 1}


def test__random_choice__error_when_no_value_specified():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randchoice()
    e = e_ctx.value

    assert e.message == "empty candidate for randchoice"


@pytest.mark.parametrize("weights_len", (0, 1, 3))
def test__random_choice__error_when_weights_does_not_match(weights_len):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randchoice(
            1,
            2,
            weights=[1, 1, 1, 1][:weights_len],
        )
    e = e_ctx.value

    assert e.message == "the number of weights must match the candidates"
