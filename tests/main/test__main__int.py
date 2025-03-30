import base64
import filecmp
import pickle
import sys
from unittest import mock
from unittest.mock import patch

import pytest

import randog.__main__


def test__main__int__error_when_miss_args(capfd):
    args = ["randog", "int"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "the following arguments are required: MINIMUM, MAXIMUM" in err


@pytest.mark.parametrize(
    "expected",
    [-1, 0, 1],
)
def test__main__int__min_max(capfd, expected):
    args = ["randog", "int", str(expected), str(expected)]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    "minimum",
    ["0.1", "a", "-"],
)
def test__main__int__error_when_illegal_min(capfd, minimum):
    args = ["randog", "int", minimum, "1000"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "int: error: argument MINIMUM: invalid int value: " in err


@pytest.mark.parametrize(
    "maximum",
    ["0.1", "a", "-"],
)
def test__main__int__error_when_illegal_max(capfd, maximum):
    args = ["randog", "int", "-1000", maximum]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "int: error: argument MAXIMUM: invalid int value: " in err


def test__main__int__error_when_max_lt_min(capfd):
    args = ["randog", "int", "1", "0"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "int: error: arguments must satisfy MINIMUM <= MAXIMUM" in err


@pytest.mark.parametrize(
    ("minimum", "maximum", "options", "expected_kwargs"),
    [
        (1, 8, [], {}),
        (-8, -1, [], {}),
    ],
)
@patch("randog.factory.randint", side_effect=randog.factory.randint)
def test__main__int__weight__exp_uniform(
    mock_func: mock.MagicMock, capfd, minimum, maximum, options, expected_kwargs
):
    args = ["randog", "int", *options, "--exp-uniform", str(minimum), str(maximum)]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        mock_func.assert_called_once()
        assert mock_func.mock_calls[0].args == (minimum, maximum)
        assert mock_func.mock_calls[0].kwargs.get("distribution") == "exp_uniform"
        assert {
            k: mock_func.mock_calls[0].kwargs.get(k) for k in expected_kwargs.keys()
        } == expected_kwargs

        out, err = capfd.readouterr()
        assert out != ""
        assert err == ""


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (["1", "1", "--repr"], "1"),
        (["0", "0", "--repr"], "0"),
        (["-1", "-1", "--repr"], "-1"),
        (["1", "1", "--json"], "1"),
        (["0", "0", "--json"], "0"),
        (["-1", "-1", "--json"], "-1"),
        (["10000", "10000", "--fmt", ","], "10,000"),
        (["10000", "10000", "--fmt", ".2f"], "10000.00"),
        # with --list
        (["10000", "10000", "--fmt", ".2f", "--list=2"], "['10000.00', '10000.00']"),
        # with --list and --json
        (
            ["10000", "10000", "--fmt", ".2f", "--list=2", "--json"],
            '["10000.00", "10000.00"]',
        ),
    ],
)
def test__main__int__fmt(capfd, options, expected):
    args = ["randog", "int", *options]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__int__pickle(capfd, tmp_path, repeat):
    expected_value = 12
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "int",
        str(expected_value),
        str(expected_value),
        "--pickle",
        "--output",
        str(output_path),
        "--repeat",
        str(repeat),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

    with open(output_path, mode="br") as fp:
        values = [pickle.load(fp) for _ in range(repeat)]

    assert values == [expected_value] * repeat


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__int__pickle_base64(capfd, repeat):
    expected_value = 12
    args = [
        "randog",
        "int",
        str(expected_value),
        str(expected_value),
        "--pickle",
        "--base64",
        "--repeat",
        str(repeat),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

    pickle_encoded = [
        base64.b64decode(s, validate=True) for s in out.split("\n") if s != ""
    ]
    values = [pickle.loads(b) for b in pickle_encoded]

    assert values == [expected_value] * repeat


def test__main__int__err_base64_without_pickle(capfd):
    expected_value = 12
    args = [
        "randog",
        "int",
        str(expected_value),
        str(expected_value),
        "--base64",
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert (
            "randog int: error: argument --base64: not allowed without argument "
            "--pickle in this mode" in err
        )


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__int__pickle_fmt(capfd, tmp_path, repeat):
    expected_value = 12
    args = [
        "randog",
        "int",
        str(expected_value),
        str(expected_value),
        "--pickle",
        "--fmt=x",
        "--repeat",
        str(repeat),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

    pickle_encoded = [bytes.fromhex(s) for s in out.split("\n") if s != ""]
    values = [pickle.loads(b) for b in pickle_encoded]

    assert values == [expected_value] * repeat


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__int__pickle_list(capfd, tmp_path, repeat):
    expected_value = 12
    list_length = 2
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "int",
        str(expected_value),
        str(expected_value),
        "--pickle",
        "--list",
        str(list_length),
        "--output",
        str(output_path),
        "--repeat",
        str(repeat),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

    with open(output_path, mode="br") as fp:
        values = [pickle.load(fp) for _ in range(repeat)]

    assert values == [[expected_value] * list_length] * repeat


@pytest.mark.parametrize(
    "expected",
    [-1, 0, 1],
)
@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__int__option_repeat(capfd, resources, expected, option, count):
    args = [
        "randog",
        "int",
        str(expected),
        str(expected),
        option,
        str(count),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n" * count
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--repeat", -1),
        ("-r", 0),
    ],
)
def test__main__int__error_with_negative_repeat(capfd, resources, option, length):
    expected = 100
    args = [
        "randog",
        "int",
        str(expected),
        str(expected),
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            f"int: error: argument --repeat/-r: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    "expected",
    [-1, 0, 1],
)
@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__int__option_list(capfd, resources, expected, option, length):
    args = [
        "randog",
        "int",
        str(expected),
        str(expected),
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == str([expected] * length) + "\n"
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", -1),
        ("-L", 0),
    ],
)
def test__main__int__error_with_negative_list(capfd, resources, option, length):
    expected = 100
    args = [
        "randog",
        "int",
        str(expected),
        str(expected),
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            f"int: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


def test__main__int__option_output(capfd, tmp_path, resources):
    expected = 100
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "int",
        str(expected),
        str(expected),
        "--output",
        str(output_path),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="r") as out_fp:
            assert out_fp.readline() == f"{expected}\n"
            assert out_fp.readline() == ""


def test__main__int__option_output__option_repeat(capfd, tmp_path, resources):
    expected = 100
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "int",
        str(expected),
        str(expected),
        "--output",
        str(output_path),
        "--repeat",
        str(count),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="r") as out_fp:
            for _ in range(count):
                assert out_fp.readline() == f"{expected}\n"
            assert out_fp.readline() == ""


def test__main__int__option_output__option_repeat__separate(capfd, tmp_path, resources):
    expected = 100
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "int",
        str(expected),
        str(expected),
        "--output",
        str(output_fmt_path),
        "--repeat",
        str(count),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        for i in range(count):
            with open(output_paths[i], mode="r") as out_fp:
                assert out_fp.readline() == f"{expected}\n"
                assert out_fp.readline() == ""


@pytest.mark.parametrize(
    ("options",),
    [
        (["--json", "--repr"],),
    ],
)
def test__main__int__error_duplicate_format(capfd, resources, options):
    args = ["randog", "int", "1", "100", *options]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "not allowed with argument" in err


@pytest.mark.parametrize(
    ("seed0", "seed1", "expect_same_output"),
    [
        (["--seed=100"], ["--seed=100"], True),
        (["--seed=100"], ["--seed=1000"], False),
        ([], ["--seed=1000"], False),
        ([], [], False),
    ],
)
@pytest.mark.parametrize(
    ("distribution",),
    [
        ([],),
        (["--exp-uniform"],),
    ],
)
def test__main__int__seed(
    capfd, tmp_path, seed0, seed1, expect_same_output, distribution
):
    output_path0 = tmp_path.joinpath("out_0.txt")
    output_path1 = tmp_path.joinpath("out_1.txt")
    args_base = ["randog", "int", "0", "100", "--repeat=50", *distribution]
    args0 = [*args_base, *seed0, "--output", str(output_path0)]
    args1 = [*args_base, *seed1, "--output", str(output_path1)]

    with patch.object(sys, "argv", args0):
        randog.__main__.main()
    with patch.object(sys, "argv", args1):
        randog.__main__.main()

    if expect_same_output:
        assert filecmp.cmp(output_path0, output_path1, shallow=False)
    else:
        assert not filecmp.cmp(output_path0, output_path1, shallow=False)

    out, err = capfd.readouterr()
    assert out == ""
    assert err == ""


def test__main__int__help(capfd):
    args = ["randog", "int", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: randog int")
        assert err == ""
