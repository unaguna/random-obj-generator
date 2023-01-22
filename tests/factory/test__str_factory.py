import pytest

import ranog.factory
from ranog.exceptions import FactoryConstructionError


def test__random_str__without_options():
    factory = ranog.factory.randstr()

    value = factory.next()

    assert isinstance(value, str)


@pytest.mark.parametrize("length", (0, 1, 2, 3))
def test__random_str__with_length(length):
    factory = ranog.factory.randstr(length=length)

    value = factory.next()

    assert isinstance(value, str)
    assert len(value) == length


@pytest.mark.parametrize(
    ("charset",),
    (
        ("a",),
        ("abc",),
        ("xyz",),
    ),
)
def test__random_str__with_charset(charset):
    factory = ranog.factory.randstr(charset=charset)

    value = factory.next()

    assert isinstance(value, str)
    assert set(value) <= set(charset)


@pytest.mark.parametrize(
    ("charset", "length"),
    (
        ("a", 2),
        ("abc", 3),
        ("xyz", 3),
    ),
)
def test__random_str__with_charset_and_length(charset, length):
    factory = ranog.factory.randstr(length=length, charset=charset)

    value = factory.next()

    assert isinstance(value, str)
    assert len(value) == length
    assert set(value) <= set(charset)


def test__random_str_normal_when_empty_charset_and_zero_length():
    factory = ranog.factory.randstr(length=0, charset="")

    value = factory.next()

    assert isinstance(value, str)
    assert value == ""


def test__random_str__or_none():
    factory = ranog.factory.randstr(length=0).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {"", None}


def test__random_str__or_none_0():
    factory = ranog.factory.randstr(length=0).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {""}


@pytest.mark.parametrize("length", (1, 2))
def test__random_str_error_when_empty_charset_and_nonzero_length(length):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.randstr(length=length, charset="")
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"
