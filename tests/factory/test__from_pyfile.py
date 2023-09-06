import pytest

import randog.factory


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("factory_def.py", "aaa"),
        # assert __name__ == "__randog__"
        ("factory_def_name.py", "__randog__"),
    ],
)
def test__from_pyfile(resources, filename, expected):
    filepath = resources.joinpath(filename)
    factory = randog.factory.from_pyfile(filepath)

    value = factory.next()

    assert value == expected


def test__from_pyfile__full_response__without_csv_col(resources):
    filepath = resources.joinpath("factory_def.py")
    factory_def = randog.factory.from_pyfile(filepath, full_response=True)

    factory = factory_def.factory
    csv_columns = factory_def.csv_columns

    assert isinstance(factory, randog.factory.Factory)
    assert csv_columns is None

    value = factory.next()

    assert value == "aaa"


def test__from_pyfile__full_response__with_csv_col(resources):
    filepath = resources.joinpath("factory_def_dict.py")
    factory_def = randog.factory.from_pyfile(filepath, full_response=True)

    factory = factory_def.factory
    csv_columns = factory_def.csv_columns

    assert isinstance(factory, randog.factory.Factory)
    assert csv_columns == ["id", "name", "join_date"]

    value = factory.next()

    assert isinstance(value, dict)
    assert value["id"] == 0
