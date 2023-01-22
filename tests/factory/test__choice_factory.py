import pytest

import ranog.factory
from ranog.exceptions import FactoryConstructionError


def test__random_choice__uses_each_value():
    factory = ranog.factory.randchoice(0, 1)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {0, 1}


@pytest.mark.parametrize("expected_value", (-1, 0, "foo", None))
def test__random_choice__one_value(expected_value):
    factory = ranog.factory.randchoice(expected_value)

    value = factory.next()

    assert value == expected_value


@pytest.mark.parametrize("expected_value", (-1, 0, 1))
def test__random_choice__value(expected_value):
    factory = ranog.factory.randchoice(expected_value, expected_value)

    value = factory.next()

    assert value == expected_value


def test__random_choice__or_none():
    factory = ranog.factory.randchoice(0, 1).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(400)))

    assert values == {0, 1, None}


def test__random_choice__or_none_0():
    factory = ranog.factory.randchoice(0, 1).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {0, 1}


def test__random_choice__error_when_no_value_specified():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.randchoice()
    e = e_ctx.value

    assert (
        e.message
        == "the generating conditions are inconsistent: specify at least one value"
    )
