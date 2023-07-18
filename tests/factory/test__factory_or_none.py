from unittest.mock import MagicMock

import randog.factory


def test__or_none__no_lazy_choice():
    iter_num = 200

    child_fac = randog.factory.const(1)
    child_fac.next = MagicMock(return_value=1)
    factory = child_fac.or_none()

    values = set(factory.iter(iter_num))

    assert values == {None, 1}
    assert child_fac.next.call_count < iter_num


def test__or_none__lazy_choice():
    iter_num = 200

    child_fac = randog.factory.const(1)
    child_fac.next = MagicMock(return_value=1)
    factory = child_fac.or_none(lazy_choice=True)

    values = set(factory.iter(iter_num))

    assert values == {None, 1}
    assert child_fac.next.call_count == iter_num
