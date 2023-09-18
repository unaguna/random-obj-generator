import random
import re

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__random_str__without_options():
    factory = randog.factory.randstr()

    value = factory.next()

    assert isinstance(value, str)


@pytest.mark.parametrize("length", (0, 1, 2, 3))
def test__random_str__with_fix_length(length):
    factory = randog.factory.randstr(length=length)

    value = factory.next()

    assert isinstance(value, str)
    assert len(value) == length


@pytest.mark.parametrize("length", (0, 1, 2, 3))
def test__random_str__with_random_length(length):
    length_factory = randog.factory.randint(length, length)
    factory = randog.factory.randstr(length=length_factory)

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
    factory = randog.factory.randstr(charset=charset)

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
    factory = randog.factory.randstr(length=length, charset=charset)

    value = factory.next()

    assert isinstance(value, str)
    assert len(value) == length
    assert set(value) <= set(charset)


def test__random_str_normal_when_empty_charset_and_zero_length():
    factory = randog.factory.randstr(length=0, charset="")

    value = factory.next()

    assert isinstance(value, str)
    assert value == ""


@pytest.mark.parametrize("length", (0, 1, 2, 3))
def test__random_str_error_when_empty_charset_and_random_length(length):
    length_factory = randog.factory.randint(length, length)
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randstr(length=length_factory, charset="")
    e = e_ctx.value

    assert (
        e.message
        == "the charset for randstr() must not be empty if length is at random"
    )


@pytest.mark.require_rstr
@pytest.mark.parametrize("regex", [r"[\d]+BC", re.compile(r"[abc]+")])
def test__random_str__regex(regex):
    factory = randog.factory.randstr(regex=regex)

    value = factory.next()

    assert isinstance(value, str)
    assert re.fullmatch(regex, value)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"length": 1},
        {"charset": "a"},
        {"length": 1, "charset": "a"},
    ],
)
def test__random_str_error_when_specify_regex_and_length_charset(kwargs):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randstr(regex=r"\d", **kwargs)
    e = e_ctx.value

    assert (
        e.message
        == "cannot specify argument 'regex' for randstr() with 'length' or 'charset'"
    )


def test__random_str__or_none():
    factory = randog.factory.randstr(length=0).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {"", None}


def test__random_str__or_none_0():
    factory = randog.factory.randstr(length=0).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {""}


@pytest.mark.parametrize("length", (1, 2))
def test__random_str_error_when_empty_charset_and_nonzero_length(length):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randstr(length=length, charset="")
    e = e_ctx.value

    assert (
        e.message == "the charset for randstr() must not be empty if length is positive"
    )


@pytest.mark.parametrize(
    ("rnd1", "rnd2", "expect_same_output"),
    [
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(12)}, True),
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(13)}, False),
        (lambda: {"rnd": random.Random(12)}, lambda: {}, False),
        (lambda: {}, lambda: {}, False),
    ],
)
@pytest.mark.parametrize(
    "kwargs",
    [
        {"length": 10},
        {"length": 5, "charset": "abcdef"},
        {"regex": "[a-fA-F]{1,5}"},
    ],
)
def test__random_str__seed(rnd1, rnd2, expect_same_output, kwargs):
    if "regex" in kwargs:
        pytest.importorskip("rstr")

    repeat = 20
    factory1 = randog.factory.randstr(**rnd1(), **kwargs)
    factory2 = randog.factory.randstr(**rnd2(), **kwargs)

    generated1 = list(factory1.iter(repeat))
    generated2 = list(factory2.iter(repeat))

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
