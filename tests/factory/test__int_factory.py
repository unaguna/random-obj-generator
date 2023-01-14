import ranog.f


def test__random_int():
    factory = ranog.f.randint(0, 5)

    value = factory.next()

    assert isinstance(value, int)
