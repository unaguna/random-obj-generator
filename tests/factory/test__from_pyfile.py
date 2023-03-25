import randog.factory


def test__from_pyfile():
    # TODO: ファイル指定を堅牢に
    filepath = "./tests/resource/factory_def.py"
    factory = randog.factory.from_pyfile(filepath)

    value = factory.next()

    assert value == 2
