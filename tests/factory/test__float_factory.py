import pytest

import ranog.factory
from ranog.exceptions import FactoryConstructionError


@pytest.mark.parametrize("expected_value", (-1, 0, 1))
def test__random_float(expected_value):
    factory = ranog.factory.randfloat(expected_value, expected_value)

    value = factory.next()

    assert isinstance(value, float)
    assert value == expected_value


def test__random_float_error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.randint(2, 1)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"
