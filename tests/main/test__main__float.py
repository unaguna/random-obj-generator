import sys
from unittest.mock import patch

import pytest

import randog.__main__


def test__main__float__without_min_max(capfd):
    args = ["randog", "float"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert 0 <= float(out) <= 1
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("1", "1.0"),
        ("0", "0.0"),
        ("-1", "-1.0"),
        ("1.0", "1.0"),
        ("0.1", "0.1"),
    ],
)
def test__main__float__min_max(capfd, arg, expected):
    args = ["randog", "float", arg, arg]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    "minimum",
    ["a", "-"],
)
def test__main__float__error_when_illegal_min(capfd, minimum):
    args = ["randog", "float", minimum, "1000"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "float: error: argument MINIMUM: invalid float value: " in err


@pytest.mark.parametrize(
    "maximum",
    ["a", "-"],
)
def test__main__float__error_when_illegal_max(capfd, maximum):
    args = ["randog", "float", "-1000", maximum]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "float: error: argument MAXIMUM: invalid float value: " in err


def test__main__float__error_when_max_lt_min(capfd):
    args = ["randog", "float", "1", "0"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "float: error: arguments must satisfy MINIMUM <= MAXIMUM" in err


@pytest.mark.parametrize(
    ("prob_p_inf", "contains_inf", "contains_fin"),
    [
        ("1", True, False),
        ("0", False, True),
        ("0.5", True, True),
    ],
)
def test__main__float__p_inf(capfd, prob_p_inf, contains_inf, contains_fin):
    args = ["randog", "float", "0", "0", "--p-inf", prob_p_inf, "--repeat=100"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        if contains_inf:
            assert "inf" in out
            assert "-inf" not in out
        else:
            assert "inf" not in out

        if contains_fin:
            assert "0.0" in out
        else:
            assert "0" not in out


@pytest.mark.parametrize(
    ("prob_n_inf", "contains_inf", "contains_fin"),
    [
        ("1", True, False),
        ("0", False, True),
        ("0.5", True, True),
    ],
)
def test__main__float__n_inf(capfd, prob_n_inf, contains_inf, contains_fin):
    args = ["randog", "float", "0", "0", "--n-inf", prob_n_inf, "--repeat=100"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        if contains_inf:
            assert "-inf" in out
            assert " inf" not in out
        else:
            assert "inf" not in out

        if contains_fin:
            assert "0.0" in out
        else:
            assert "0" not in out


@pytest.mark.parametrize(
    ("prob_nan", "contains_nan", "contains_non_nan"),
    [
        ("1", True, False),
        ("0", False, True),
        ("0.5", True, True),
    ],
)
def test__main__float__nan(capfd, prob_nan, contains_nan, contains_non_nan):
    args = ["randog", "float", "0", "0", "--nan", prob_nan, "--repeat=100"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        if contains_nan:
            assert "nan" in out
        else:
            assert "nan" not in out

        if contains_non_nan:
            assert "0.0" in out
        else:
            assert "0" not in out


@pytest.mark.parametrize(
    ("option", "expected"),
    [
        ("--p-inf=1", "inf"),
        ("--n-inf=1", "-inf"),
        ("--nan=1", "nan"),
    ],
)
def test__main__float__special__without_min_max(capfd, option, expected):
    args = ["randog", "float", option, "--repeat=100"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert {*out.splitlines(keepends=False)} == {expected}
        assert err == ""


@pytest.mark.parametrize(
    "option",
    ["--p-inf", "--n-inf", "--nan"],
)
@pytest.mark.parametrize(
    "prop_p_inf",
    ["-1", "-0.1", "1.1", "INF", "foo"],
)
def test__main__float__error_when_illegal_prop(capfd, option, prop_p_inf):
    args = ["randog", "float", "0", "0", option, prop_p_inf]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert f"float: error: argument {option}: invalid probability value: " in err


@pytest.mark.parametrize(
    ("prob_nan", "prob_p_inf", "prob_n_inf"),
    [
        ("0.6", "0.6", "0"),
        ("0.6", "0", "0.6"),
        ("0", "0.6", "0.6"),
        ("0.4", "0.4", "0.4"),
    ],
)
def test__main__float__error_when_too_large_inf_nan(
    capfd, prob_nan, prob_p_inf, prob_n_inf
):
    args = [
        "randog",
        "float",
        "0",
        "0",
        "--nan",
        prob_nan,
        "--p-inf",
        prob_p_inf,
        "--n-inf",
        prob_n_inf,
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            "arguments must satisfy that PROB_P_INF + PROB_N_INF + PROB_NAN <= 1.0"
            in err
        )


@pytest.mark.parametrize(
    "expected",
    [-1, 0, 1, 0.1],
)
@pytest.mark.parametrize(
    "fmt",
    ["--repr", "--json"],
)
def test__main__float__option_repr_json(capfd, expected, fmt):
    args = ["randog", "float", str(expected), str(expected), fmt]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{float(expected)}\n"
        assert err == ""


@pytest.mark.parametrize(
    "expected",
    [-1, 0, 1, 0.1],
)
@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__float__option_repeat(capfd, resources, expected, option, count):
    args = [
        "randog",
        "float",
        str(expected),
        str(expected),
        option,
        str(count),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{float(expected)}\n" * count
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--repeat", -1),
        ("-r", 0),
    ],
)
def test__main__float__error_with_negative_repeat(capfd, resources, option, length):
    expected = 100
    args = [
        "randog",
        "float",
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
            f"float: error: argument --repeat/-r: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    "expected",
    [-1, 0, 1, 0.1],
)
@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__float__option_list(capfd, resources, expected, option, length):
    args = [
        "randog",
        "float",
        str(expected),
        str(expected),
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == str([float(expected)] * length) + "\n"
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", -1),
        ("-L", 0),
    ],
)
def test__main__float__error_with_negative_list(capfd, resources, option, length):
    expected = 100
    args = [
        "randog",
        "float",
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
            f"float: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


def test__main__float__option_output(capfd, tmp_path, resources):
    expected = 100.0
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "float",
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


def test__main__float__option_output__option_repeat(capfd, tmp_path, resources):
    expected = 100.0
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "float",
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


def test__main__float__option_output__option_repeat__separate(
    capfd, tmp_path, resources
):
    expected = 100.0
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "float",
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
def test__main__float__error_duplicate_format(capfd, resources, options):
    args = ["randog", "float", "1", "100", *options]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "not allowed with argument" in err
