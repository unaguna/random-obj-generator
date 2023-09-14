import random

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


@pytest.mark.parametrize(
    ("rnd1", "rnd2", "expect_same_output"),
    [
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(12)}, True),
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(13)}, False),
        (lambda: {"rnd": random.Random(12)}, lambda: {}, False),
        (lambda: {}, lambda: {}, False),
    ],
)
@pytest.mark.parametrize(
    ("filename",),
    [
        ("factory_def_rnd_bool.py",),
        ("factory_def_rnd_int.py",),
        ("factory_def_rnd_float.py",),
        ("factory_def_rnd_str.py",),
        ("factory_def_rnd_list.py",),
        ("factory_def_rnd_dict.py",),
        ("factory_def_rnd_decimal.py",),
        ("factory_def_rnd_datetime.py",),
        ("factory_def_rnd_date.py",),
        ("factory_def_rnd_time.py",),
        ("factory_def_rnd_timedelta.py",),
        ("factory_def_rnd_enum.py",),
    ],
)
def test__from_pyfile__seed(resources, rnd1, rnd2, expect_same_output, filename):
    filepath = resources.joinpath(filename)
    repeat = 20
    factory1 = randog.factory.from_pyfile(filepath, **rnd1())
    factory2 = randog.factory.from_pyfile(filepath, **rnd2())

    # NaN != NaN となってしまうため、repr 文字列で比較する
    generated1 = [repr(v) for v in factory1.iter(repeat)]
    generated2 = [repr(v) for v in factory2.iter(repeat)]

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
