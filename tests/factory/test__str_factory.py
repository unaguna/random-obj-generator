import pytest

import ranog.f
from ranog.exceptions import FactoryConstructionError


@pytest.mark.parametrize(
    ("charset", "length"),
    (
        ("a", 2),
        ("abc", 3),
        ("xyz", 3),
    ),
)
def test__random_str(charset, length):
    factory = ranog.f.randstr(length=length, charset=charset)

    value = factory.next()

    assert isinstance(value, str)
    assert len(value) == length
    assert set(value) <= set(charset)


def test__random_str_normal_when_empty_charset_and_zero_length():
    factory = ranog.f.randstr(length=0, charset="")

    value = factory.next()

    assert isinstance(value, str)
    assert value == ""


@pytest.mark.parametrize("length", (1, 2))
def test__random_str_error_when_empty_charset_and_nonzero_length(length):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.f.randstr(length=length, charset="")
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"
