import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


@pytest.mark.parametrize("expected_value", (-1, 0, 1))
def test__random_int(expected_value):
    factory = randog.factory.randint(expected_value, expected_value)

    value = factory.next()

    assert isinstance(value, int)
    assert value == expected_value


def test__random_int__or_none():
    factory = randog.factory.randint(1, 1).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1, None}


def test__random_int__or_none_0():
    factory = randog.factory.randint(1, 1).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1}


def test__random_int_error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randint(2, 1)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"
