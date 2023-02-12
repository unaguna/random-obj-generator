import randog.factory


def test__random_dict():
    factory = randog.factory.randdict(
        a=randog.factory.randint(1, 1),
        b=(randog.factory.randint(2, 2), 1.0),
        c=(randog.factory.randint(26, 26), 0.0),
    )

    value = factory.next()

    assert isinstance(value, dict)
    assert value.get("a") == 1
    assert value.get("b") == 2
    assert "z" not in value


def test__random_dict__items_by_dict():
    factory = randog.factory.randdict(
        {
            "a": randog.factory.randint(1, 1),
            "b": (randog.factory.randint(2, 2), 1.0),
            "z": (randog.factory.randint(26, 26), 0.0),
        }
    )

    value = factory.next()

    assert isinstance(value, dict)
    assert value.get("a") == 1
    assert value.get("b") == 2
    assert "z" not in value


def test__random_dict__or_none():
    factory = randog.factory.randdict(
        a=randog.factory.randint(1, 1),
    ).or_none(0.5)

    values = set(map(lambda x: type(factory.next()), range(200)))

    assert values == {dict, type(None)}


def test__random_dict__or_none_0():
    factory = randog.factory.randdict(
        a=randog.factory.randint(1, 1),
    ).or_none(0)

    values = set(map(lambda x: type(factory.next()), range(200)))

    assert values == {dict}
