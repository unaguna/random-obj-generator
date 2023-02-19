import pytest

import randog.factory


def test__by_iterator():
    factory = randog.factory.by_iterator(iter(range(3)))
    assert factory.next() == 0
    assert factory.next() == 1
    assert factory.next() == 2
    with pytest.raises(StopIteration):
        factory.next()


def test__by_iterator__generator():
    def generator():
        for i in range(3):
            yield i

    factory = randog.factory.by_iterator(generator())
    assert factory.next() == 0
    assert factory.next() == 1
    assert factory.next() == 2
    with pytest.raises(StopIteration):
        factory.next()
