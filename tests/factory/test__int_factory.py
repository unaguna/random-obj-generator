import pytest

import ranog.factory
from ranog.exceptions import FactoryConstructionError


@pytest.mark.parametrize("expected_value", (-1, 0, 1))
def test__random_int(expected_value):
    factory = ranog.factory.randint(expected_value, expected_value)

    value = factory.next()

    assert isinstance(value, int)
    assert value == expected_value


def test__random_int__or_none():
    factory = ranog.factory.randint(1, 1).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1, None}


def test__random_int__or_none_0():
    factory = ranog.factory.randint(1, 1).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1}


def test__random_int_error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.randint(2, 1)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"
