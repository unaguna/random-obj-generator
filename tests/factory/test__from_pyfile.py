import randog.factory


def test__from_pyfile(resources):
    filepath = resources.joinpath("factory_def.py")
    factory = randog.factory.from_pyfile(filepath)

    value = factory.next()

    assert value == 2
