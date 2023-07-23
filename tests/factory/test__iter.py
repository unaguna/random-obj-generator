import itertools
from fractions import Fraction

import pytest

import randog.factory


def test__iter():
    factory = randog.factory.by_iterator(itertools.count(0))
    generated = list(factory.iter(10))

    assert isinstance(generated, list)
    assert generated == list(range(10))


def test__iter__regenerate():
    list_len = 100
    factory = randog.factory.by_iterator(itertools.count(0))
    generated = list(factory.iter(list_len, regenerate=0.5))

    assert len(generated) == list_len
    for prev_value, value in zip(generated[:-1], generated[1:]):
        assert prev_value < value
    assert list_len - 1 < generated[-1]


def test__iter__regenerate__zero():
    list_len = 100
    factory = randog.factory.by_iterator(itertools.count(0))
    generated = list(factory.iter(list_len, regenerate=0))

    assert len(generated) == list_len
    for prev_value, value in zip(generated[:-1], generated[1:]):
        assert value - prev_value == 1


@pytest.mark.parametrize(
    "regenerate",
    [
        -0.1,
        1.1,
        float(Fraction(2047, 2048)),
    ],
)
def test__iter__regenerate__error_when_illegal_probability(regenerate):
    factory = randog.factory.by_iterator(itertools.count(0))
    with pytest.raises(ValueError) as e_ctx:
        factory.iter(100, regenerate=regenerate)
    e = e_ctx.value
    message = e.args[0]

    assert message == "the probability `regenerate` must range from 0 to 1023/1024"


def test__iter__discard():
    list_len = 100
    factory = randog.factory.by_iterator(itertools.count(0))
    generated = list(factory.iter(list_len, discard=0.5))

    assert len(generated) < list_len
    for prev_value, value in zip(generated[:-1], generated[1:]):
        assert prev_value < value
    assert len(generated) - 1 < generated[-1] < list_len


def test__iter__discard__zero():
    list_len = 100
    factory = randog.factory.by_iterator(itertools.count(0))
    generated = list(factory.iter(list_len, discard=0))

    assert len(generated) == list_len
    for prev_value, value in zip(generated[:-1], generated[1:]):
        assert value - prev_value == 1


def test__iter__discard__full():
    list_len = 100
    factory = randog.factory.by_iterator(itertools.count(0))
    generated = list(factory.iter(list_len, discard=1.0))

    assert len(generated) == 0


@pytest.mark.parametrize(
    "discard",
    [
        -0.1,
        1.1,
    ],
)
def test__iter__discard__error_when_illegal_probability(discard):
    factory = randog.factory.by_iterator(itertools.count(0))
    with pytest.raises(ValueError) as e_ctx:
        factory.iter(100, discard=discard)
    e = e_ctx.value
    message = e.args[0]

    assert message == "the probability `discard` must range from 0 to 1"


def test__iter__error_when_duplicate_regenerate_discord():
    factory = randog.factory.by_iterator(itertools.count(0))
    with pytest.raises(ValueError) as e_ctx:
        factory.iter(100, regenerate=0.1, discard=0.1)
    e = e_ctx.value
    message = e.args[0]

    assert message == "`regenerate` and `discard` cannot be specified at the same time"


def test__infinity_iter():
    factory = randog.factory.randint(10, 10)
    inf_iter = factory.infinity_iter()

    for i in range(20):
        generated = next(inf_iter)
        assert generated == 10


def test__infinity_iter__regenerate():
    list_len = 100
    factory = randog.factory.by_iterator(itertools.count(0))
    iterator = factory.infinity_iter(regenerate=0.5)
    generated = [next(iterator) for _ in range(list_len)]

    assert len(generated) == list_len
    for prev_value, value in zip(generated[:-1], generated[1:]):
        assert prev_value < value
    assert list_len - 1 < generated[-1]


@pytest.mark.parametrize(
    "regenerate",
    [
        -0.1,
        1.1,
        float(Fraction(2047, 2048)),
    ],
)
def test__infinity_iter__regenerate__error_when_illegal_probability(regenerate):
    factory = randog.factory.by_iterator(itertools.count(0))
    with pytest.raises(ValueError) as e_ctx:
        factory.infinity_iter(regenerate=regenerate)
    e = e_ctx.value
    message = e.args[0]

    assert message == "the probability `regenerate` must range from 0 to 1023/1024"
