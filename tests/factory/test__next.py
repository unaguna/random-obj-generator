import pytest

import randog.factory


def _only_2_times():
    _only_2_times.count += 1
    if _only_2_times.count >= 3:
        raise StopIteration
    return 0


_only_2_times.count = 0


@pytest.mark.parametrize(
    "factory",
    [
        randog.factory.by_callable(_only_2_times),
        randog.factory.by_iterator(iter(range(1, 3))),
        randog.factory.randdict(
            a=randog.factory.by_iterator(iter(range(1, 3))),
            b=randog.factory.randint(0, 10),
        ),
        randog.factory.randlist(
            randog.factory.by_iterator(iter(range(1, 3))),
            randog.factory.randint(0, 10),
        ),
    ],
)
def test__next__stop_iteration(factory):
    factory.next()
    factory.next()

    with pytest.raises(StopIteration):
        factory.next()
