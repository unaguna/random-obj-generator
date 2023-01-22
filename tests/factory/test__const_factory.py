import pytest

import ranog.factory


@pytest.mark.parametrize("expected_value", (-1, 0, "foo", None))
def test__random_const(expected_value):
    factory = ranog.factory.const(expected_value)

    value = factory.next()

    assert value == expected_value


def test__random_const__or_none():
    factory = ranog.factory.const(1).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1, None}


def test__random_const__or_none_0():
    factory = ranog.factory.const(1).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {1}
