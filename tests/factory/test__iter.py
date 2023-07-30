import itertools
from fractions import Fraction

import pytest

import randog.factory


def _get_callable_only_2_times():
    def _only_2_times():
        _only_2_times.count += 1
        if _only_2_times.count >= 3:
            raise StopIteration
        return 0

    _only_2_times.count = 0

    return _only_2_times


def test__iter():
    factory = randog.factory.by_iterator(itertools.count(0))
    generated = list(factory.iter(10))

    assert isinstance(generated, list)
    assert generated == list(range(10))


# get_factory, iter_length
_CASES_STOP_ITER = [
    (lambda: randog.factory.by_callable(_get_callable_only_2_times()), 2),
    (lambda: randog.factory.by_iterator(iter(range(1, 3))), 2),
    (
        lambda: randog.factory.randdict(
            a=randog.factory.by_iterator(iter(range(1, 3))),
            b=randog.factory.randint(0, 10),
        ),
        2,
    ),
    (
        lambda: randog.factory.randlist(
            randog.factory.by_iterator(iter(range(1, 3))),
            randog.factory.randint(0, 10),
        ),
        2,
    ),
    (
        lambda: randog.factory.randlist(
            randog.factory.randint(0, 10),
            length=randog.factory.by_iterator(iter(range(1, 3))),
        ),
        2,
    ),
]


@pytest.mark.parametrize(
    ("get_factory", "iter_length"),
    _CASES_STOP_ITER,
)
@pytest.mark.parametrize(
    "options_raise_on_factory_stopped",
    [
        # default
        {},
        # Same behavior with explicit default values.
        {"raise_on_factory_stopped": False},
    ],
)
def test__iter__stop_iteration(
    get_factory, iter_length, options_raise_on_factory_stopped
):
    factory = get_factory()
    generated = list(factory.iter(iter_length + 5, **options_raise_on_factory_stopped))
    assert len(generated) == iter_length


@pytest.mark.parametrize(
    ("get_factory", "iter_length"),
    _CASES_STOP_ITER,
)
def test__iter__raise_on_factory_stopped__true__error(get_factory, iter_length):
    factory = get_factory()
    with pytest.raises(randog.factory.FactoryStopException) as e_ctx:
        list(factory.iter(iter_length + 5, raise_on_factory_stopped=True))
    e = e_ctx.value
    message = e.args[0]

    assert message == "the factory stopped generating"


@pytest.mark.parametrize(
    ("get_factory", "iter_length"),
    _CASES_STOP_ITER,
)
def test__iter__raise_on_factory_stopped__true__no_error(get_factory, iter_length):
    factory = get_factory()
    generated = list(factory.iter(iter_length, raise_on_factory_stopped=True))

    assert isinstance(generated, list)
    assert len(generated) == iter_length


@pytest.mark.parametrize(
    ("get_factory", "iter_length"),
    _CASES_STOP_ITER,
)
def test__iter__raise_on_factory_stopped__true__error__regenerate(
    get_factory, iter_length
):
    factory = get_factory()
    with pytest.raises(randog.factory.FactoryStopException) as e_ctx:
        list(factory.iter(iter_length, regenerate=0.99, raise_on_factory_stopped=True))
    e = e_ctx.value
    message = e.args[0]

    assert message == "the factory stopped generating"


@pytest.mark.parametrize(
    ("get_factory", "iter_length"),
    _CASES_STOP_ITER,
)
def test__iter__raise_on_factory_stopped__true__error__discard(
    get_factory, iter_length
):
    factory = get_factory()
    with pytest.raises(randog.factory.FactoryStopException) as e_ctx:
        list(factory.iter(iter_length + 1, discard=0.99, raise_on_factory_stopped=True))
    e = e_ctx.value
    message = e.args[0]

    assert message == "the factory stopped generating"


@pytest.mark.parametrize(
    ("get_factory", "iter_length"),
    _CASES_STOP_ITER,
)
def test__iter__raise_on_factory_stopped__true__no_error__discard(
    get_factory, iter_length
):
    factory = get_factory()
    generated = list(
        factory.iter(iter_length, discard=0.99, raise_on_factory_stopped=True)
    )

    assert isinstance(generated, list)
    assert len(generated) <= iter_length


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


@pytest.mark.parametrize(
    ("get_factory", "iter_length"),
    _CASES_STOP_ITER,
)
@pytest.mark.parametrize(
    "options_raise_on_factory_stopped",
    [
        # default
        {},
        # Same behavior with explicit default values.
        {"raise_on_factory_stopped": False},
    ],
)
def test__infinity_iter__stop_iteration(
    get_factory, options_raise_on_factory_stopped, iter_length
):
    factory = get_factory()
    generated = list(factory.infinity_iter(**options_raise_on_factory_stopped))
    assert len(generated) == iter_length


@pytest.mark.parametrize(
    ("get_factory", "iter_length"),
    _CASES_STOP_ITER,
)
def test__infinity_iter__raise_on_factory_stopped__true__error(
    get_factory, iter_length
):
    factory = get_factory()
    with pytest.raises(randog.factory.FactoryStopException) as e_ctx:
        list(factory.infinity_iter(raise_on_factory_stopped=True))
    e = e_ctx.value
    message = e.args[0]

    assert message == "the factory stopped generating"


@pytest.mark.parametrize(
    ("get_factory", "iter_length"),
    _CASES_STOP_ITER,
)
def test__infinity_iter__raise_on_factory_stopped__true__error__regenerate(
    get_factory, iter_length
):
    factory = get_factory()
    with pytest.raises(randog.factory.FactoryStopException) as e_ctx:
        list(factory.infinity_iter(regenerate=0.99, raise_on_factory_stopped=True))
    e = e_ctx.value
    message = e.args[0]

    assert message == "the factory stopped generating"


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
