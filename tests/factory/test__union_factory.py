import pytest

import ranog.factory
from ranog.exceptions import FactoryConstructionError


def test__random_union__uses_each_factory():
    factory = ranog.factory.union(
        ranog.factory.randstr(length=0),
        ranog.factory.randint(1, 1),
    )

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {"", 1}


@pytest.mark.parametrize("expected_value", (-1, 0, 1))
def test__random_union__value(expected_value):
    factory = ranog.factory.union(
        ranog.factory.randint(expected_value, expected_value),
        ranog.factory.randint(expected_value, expected_value),
    )

    value = factory.next()

    assert value == expected_value


def test__random_union__weight():
    factory = ranog.factory.union(
        ranog.factory.const(1),
        ranog.factory.const(2),
        ranog.factory.const(3),
        weights=[0.8, 0.2, 0],
    )

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1, 2}


def test__random_union__error_when_no_factory_specified():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.union()
    e = e_ctx.value

    assert (
        e.message
        == "the generating conditions are inconsistent: specify at least one factory"
    )
