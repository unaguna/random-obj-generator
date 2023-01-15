import ranog.factory


def test__random_dict():
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
