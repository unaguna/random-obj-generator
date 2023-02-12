import randog.factory


def test__iter():
    factory = randog.factory.randint(10, 10)
    generated = list(factory.iter(3))

    assert isinstance(generated, list)
    assert generated == [10, 10, 10]


def test__iter2():
    factory = randog.factory.randint(0, 1000000)
    generated = set(factory.iter(10))

    assert isinstance(generated, set)
    assert len(generated) >= 2


def test__infinity_iter():
    factory = randog.factory.randint(10, 10)
    inf_iter = factory.infinity_iter()

    for i in range(20):
        generated = next(inf_iter)
        assert generated == 10
