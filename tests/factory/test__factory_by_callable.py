import pytest

import randog.factory


@pytest.mark.parametrize("expected_value", (-1.0, "a", {}, None))
def test__by_callable(expected_value):
    factory = randog.factory.by_callable(lambda: expected_value)

    value = factory.next()

    assert value == expected_value
