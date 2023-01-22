import ranog.factory


def test__random_dict():
    factory = ranog.factory.randdict(
        a=ranog.factory.randint(1, 1),
        b=(ranog.factory.randint(2, 2), 1.0),
        c=(ranog.factory.randint(26, 26), 0.0),
    )

    value = factory.next()

    assert isinstance(value, dict)
    assert value.get("a") == 1
    assert value.get("b") == 2
    assert "z" not in value


def test__random_dict__items_by_dict():
    factory = ranog.factory.randdict(
        {
            "a": ranog.factory.randint(1, 1),
            "b": (ranog.factory.randint(2, 2), 1.0),
            "z": (ranog.factory.randint(26, 26), 0.0),
        }
    )

    value = factory.next()

    assert isinstance(value, dict)
    assert value.get("a") == 1
    assert value.get("b") == 2
    assert "z" not in value


def test__random_dict__or_none():
    factory = ranog.factory.randdict(
        a=ranog.factory.randint(1, 1),
    ).or_none(0.5)

    values = set(map(lambda x: type(factory.next()), range(200)))

    assert values == {dict, type(None)}


def test__random_dict__or_none_0():
    factory = ranog.factory.randdict(
        a=ranog.factory.randint(1, 1),
    ).or_none(0)

    values = set(map(lambda x: type(factory.next()), range(200)))

    assert values == {dict}
