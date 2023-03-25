import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


@pytest.mark.parametrize(
    ("prop_true", "expected_values"),
    (
        (0, {False}),
        (1, {True}),
        (0.5, {True, False}),
    ),
)
def test__random_bool(prop_true, expected_values):
    factory = randog.factory.randbool(prop_true)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == expected_values


@pytest.mark.parametrize("prop_true", (-0.1, 1.1))
def test__random_int_error_when_illegal_probability(prop_true):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randbool(prop_true)
    e = e_ctx.value

    assert e.message == "the probability `prob_true` must range from 0 to 1"
