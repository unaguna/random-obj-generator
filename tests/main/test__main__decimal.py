import decimal
import filecmp
import sys
from unittest.mock import patch

import pytest

import randog.__main__


def test__main__decimal__without_min_max(capfd):
    args = ["randog", "decimal"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert 0 <= float(out) <= 1
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("1", "1"),
        ("0", "0"),
        ("-1", "-1"),
        ("1.25", "1.25"),
    ],
)
def test__main__decimal__min_max(capfd, arg, expected):
    args = ["randog", "decimal", arg, arg]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    "minimum",
    ["a", "-"],
)
def test__main__decimal__error_when_illegal_min(capfd, minimum):
    args = ["randog", "decimal", minimum, "1000"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "decimal: error: argument MINIMUM: invalid float value: " in err


@pytest.mark.parametrize(
    "maximum",
    ["a", "-"],
)
def test__main__decimal__error_when_illegal_max(capfd, maximum):
    args = ["randog", "decimal", "-1000", maximum]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "decimal: error: argument MAXIMUM: invalid float value: " in err


def test__main__decimal__error_when_max_lt_min(capfd):
    args = ["randog", "decimal", "1", "0"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "decimal: error: arguments must satisfy MINIMUM <= MAXIMUM" in err


@pytest.mark.parametrize(
    ("dec_length", "expected"),
    [
        ("0", "0"),
        ("1", "0.0"),
        ("2", "0.00"),
    ],
)
def test__main__decimal__dec_length(capfd, dec_length, expected):
    args = [
        "randog",
        "decimal",
        "0",
        "0",
        "--decimal-len",
        dec_length,
        "--repeat=100",
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert set(out.splitlines(keepends=False)) == {expected}
        assert err == ""


@pytest.mark.parametrize(
    "length",
    ["0.1", "a", "-1", "-"],
)
def test__main__decimal__error_when_illegal_dec_length(capfd, length):
    args = ["randog", "decimal", "--decimal-len", length]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            "decimal: error: argument --decimal-len: invalid non_negative_int value: "
            in err
        )


@pytest.mark.parametrize(
    ("prob_p_inf", "contains_inf", "contains_fin"),
    [
        ("1", True, False),
        ("0", False, True),
        ("0.5", True, True),
    ],
)
def test__main__decimal__p_inf(capfd, prob_p_inf, contains_inf, contains_fin):
    args = ["randog", "decimal", "0", "0", "--p-inf", prob_p_inf, "--repeat=100"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        if contains_inf:
            assert "Infinity" in out
            assert "-Infinity" not in out
        else:
            assert "Infinity" not in out

        if contains_fin:
            assert "0" in out
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
def test__main__decimal__n_inf(capfd, prob_n_inf, contains_inf, contains_fin):
    args = ["randog", "decimal", "0", "0", "--n-inf", prob_n_inf, "--repeat=100"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        if contains_inf:
            assert "-Infinity" in out
            assert " Infinity" not in out
        else:
            assert "Infinity" not in out

        if contains_fin:
            assert "0" in out
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
def test__main__decimal__nan(capfd, prob_nan, contains_nan, contains_non_nan):
    args = ["randog", "decimal", "0", "0", "--nan", prob_nan, "--repeat=100"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        if contains_nan:
            assert "NaN" in out
        else:
            assert "NaN" not in out

        if contains_non_nan:
            assert "0" in out
        else:
            assert "0" not in out


@pytest.mark.parametrize(
    ("option", "expected"),
    [
        ("--p-inf=1", "Infinity"),
        ("--n-inf=1", "-Infinity"),
        ("--nan=1", "NaN"),
    ],
)
def test__main__decimal__special__without_min_max(capfd, option, expected):
    args = ["randog", "decimal", option, "--repeat=100"]
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
def test__main__decimal__error_when_illegal_prop(capfd, option, prop_p_inf):
    args = ["randog", "decimal", "0", "0", option, prop_p_inf]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert f"decimal: error: argument {option}: invalid probability value: " in err


@pytest.mark.parametrize(
    ("prob_nan", "prob_p_inf", "prob_n_inf"),
    [
        ("0.6", "0.6", "0"),
        ("0.6", "0", "0.6"),
        ("0", "0.6", "0.6"),
        ("0.4", "0.4", "0.4"),
    ],
)
def test__main__decimal__error_when_too_large_inf_nan(
    capfd, prob_nan, prob_p_inf, prob_n_inf
):
    args = [
        "randog",
        "decimal",
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
    ("arg", "expected"),
    [
        ("0", "Decimal('0')"),
        ("0.25", "Decimal('0.25')"),
        ("1", "Decimal('1')"),
        ("-1", "Decimal('-1')"),
    ],
)
def test__main__decimal__option_repr(capfd, arg, expected):
    args = ["randog", "decimal", arg, arg, "--repr"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [("0", '"0"'), ("0.25", '"0.25"'), ("1", '"1"'), ("-1", '"-1"')],
)
def test__main__decimal__option_json(capfd, arg, expected):
    args = ["randog", "decimal", arg, arg, "--json"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (["10000", "10000", "--fmt", ","], "10,000"),
        (["10000", "10000", "--fmt", ".0f"], "10000"),
        (["10000", "10000", "--fmt", ".2f"], "10000.00"),
    ],
)
def test__main__decimal__fmt(capfd, options, expected):
    args = ["randog", "decimal", *options]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    "expected",
    [-1, 0, 1, 0.25],
)
@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__decimal__option_repeat(capfd, resources, expected, option, count):
    args = [
        "randog",
        "decimal",
        str(expected),
        str(expected),
        option,
        str(count),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{decimal.Decimal(expected)}\n" * count
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--repeat", -1),
        ("-r", 0),
    ],
)
def test__main__decimal__error_with_negative_repeat(capfd, resources, option, length):
    expected = 100
    args = [
        "randog",
        "decimal",
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
            "decimal: error: argument --repeat/-r: invalid positive_int value: "
            f"'{length}'" in err
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
def test__main__decimal__option_list(capfd, resources, expected, option, length):
    args = [
        "randog",
        "decimal",
        str(expected),
        str(expected),
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == str([decimal.Decimal(expected)] * length) + "\n"
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", -1),
        ("-L", 0),
    ],
)
def test__main__decimal__error_with_negative_list(capfd, resources, option, length):
    expected = 100
    args = [
        "randog",
        "decimal",
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
            "decimal: error: argument --list/-L: invalid positive_int value: "
            f"'{length}'" in err
        )


def test__main__decimal__option_output(capfd, tmp_path, resources):
    expected = 100
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "decimal",
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


def test__main__decimal__option_output__option_repeat(capfd, tmp_path, resources):
    expected = 100
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "decimal",
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


def test__main__decimal__option_output__option_repeat__separate(
    capfd, tmp_path, resources
):
    expected = 100
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "decimal",
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
def test__main__decimal__error_duplicate_format(capfd, resources, options):
    args = ["randog", "decimal", "1", "100", *options]
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
def test__main__decimal__seed(capfd, tmp_path, seed0, seed1, expect_same_output):
    output_path0 = tmp_path.joinpath("out_0.txt")
    output_path1 = tmp_path.joinpath("out_1.txt")
    args_base = ["randog", "decimal", "0", "100", "--repeat=50"]
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


def test__main__decimal__help(capfd):
    args = ["randog", "decimal", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: python -m randog decimal")
        assert err == ""
