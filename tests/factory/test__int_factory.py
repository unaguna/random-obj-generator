import pytest

import ranog.f
from ranog.exceptions import FactoryConstructionError


@pytest.mark.parametrize("expected_value", (-1, 0, 1))
def test__random_int(expected_value):
    factory = ranog.f.randint(expected_value, expected_value)

    value = factory.next()

    assert isinstance(value, int)
    assert value == expected_value


def test__random_int_error_when_edges_inverse():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.f.randint(2, 1)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"
