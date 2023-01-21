import pytest

import ranog.factory


@pytest.mark.parametrize("expected_value", (-1, 0, "foo", None))
def test__random_const(expected_value):
    factory = ranog.factory.const(expected_value)

    value = factory.next()

    assert value == expected_value
