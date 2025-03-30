import random

import pytest

import randog.factory


def test__random_bytearray__without_options():
    factory = randog.factory.randbytearray()

    value = factory.next()

    assert isinstance(value, bytearray)


@pytest.mark.parametrize("length", (0, 1, 2, 3))
def test__random_bytearray__with_fix_length(length):
    factory = randog.factory.randbytearray(length=length)

    values = list(factory.iter(100))

    assert {type(v) for v in values} == {bytearray}
    assert {len(v) for v in values} == {length}


@pytest.mark.parametrize("length", (0, 1, 2, 3))
def test__random_bytearray__with_random_length(length):
    length_factory = randog.factory.randint(length, length)
    factory = randog.factory.randbytearray(length=length_factory)

    values = list(factory.iter(100))

    assert {type(v) for v in values} == {bytearray}
    assert {len(v) for v in values} == {length}


def test__random_bytearray__or_none():
    factory = randog.factory.randbytearray(length=0).or_none(0.5)

    values = set(type(v) for v in factory.iter(200))

    assert values == {bytearray, type(None)}


def test__random_bytearray__or_none_0():
    factory = randog.factory.randbytearray(length=0).or_none(0)

    values = set(type(v) for v in factory.iter(200))

    assert values == {bytearray}


@pytest.mark.parametrize(
    ("rnd1", "rnd2", "expect_same_output"),
    [
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(12)}, True),
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(13)}, False),
        (lambda: {"rnd": random.Random(12)}, lambda: {}, False),
        (lambda: {}, lambda: {}, False),
    ],
)
def test__random_bytearray__seed(rnd1, rnd2, expect_same_output):
    repeat = 20
    factory1 = randog.factory.randbytearray(**rnd1(), length=10)
    factory2 = randog.factory.randbytearray(**rnd2(), length=10)

    generated1 = list(factory1.iter(repeat))
    generated2 = list(factory2.iter(repeat))

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
