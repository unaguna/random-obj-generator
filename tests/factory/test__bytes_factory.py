import random

import pytest

import randog.factory


def test__random_bytes__without_options():
    factory = randog.factory.randbytes()

    value = factory.next()

    assert isinstance(value, bytes)


@pytest.mark.parametrize("length", (0, 1, 2, 3))
def test__random_bytes__with_fix_length(length):
    factory = randog.factory.randbytes(length=length)

    values = list(factory.iter(100))

    assert {type(v) for v in values} == {bytes}
    assert {len(v) for v in values} == {length}


@pytest.mark.parametrize("length", (0, 1, 2, 3))
def test__random_bytes__with_random_length(length):
    length_factory = randog.factory.randint(length, length)
    factory = randog.factory.randbytes(length=length_factory)

    values = list(factory.iter(100))

    assert {type(v) for v in values} == {bytes}
    assert {len(v) for v in values} == {length}


def test__random_bytes__or_none():
    factory = randog.factory.randbytes(length=0).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {b"", None}


def test__random_bytes__or_none_0():
    factory = randog.factory.randbytes(length=0).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {b""}


@pytest.mark.parametrize(
    ("rnd1", "rnd2", "expect_same_output"),
    [
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(12)}, True),
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(13)}, False),
        (lambda: {"rnd": random.Random(12)}, lambda: {}, False),
        (lambda: {}, lambda: {}, False),
    ],
)
def test__random_bytes__seed(rnd1, rnd2, expect_same_output):
    repeat = 20
    factory1 = randog.factory.randbytes(**rnd1(), length=10)
    factory2 = randog.factory.randbytes(**rnd2(), length=10)

    generated1 = list(factory1.iter(repeat))
    generated2 = list(factory2.iter(repeat))

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
