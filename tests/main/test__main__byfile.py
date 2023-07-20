import itertools
import json
import sys
from unittest.mock import patch

import pytest

import randog.__main__


@pytest.mark.parametrize(
    ("def_file", "expected"),
    [
        ("factory_def.py", "aaa\n"),
        ("factory_def_bbb.py", "bbb\n"),
    ],
)
def test__main__spec_factory(capfd, resources, def_file, expected):
    args = ["randog", "byfile", str(resources.joinpath(def_file))]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == expected
        assert err == ""


def test__main__option_repr(capfd, resources):
    args = ["randog", "byfile", str(resources.joinpath("factory_def.py")), "--repr"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "'aaa'\n"
        assert err == ""


def test__main__option_json(capfd, resources):
    args = ["randog", "byfile", str(resources.joinpath("factory_def.py")), "--json"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == '"aaa"\n'
        assert err == ""


@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__option_repeat(capfd, resources, option, count):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        option,
        str(count),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "aaa\n" * count
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--repeat", -1),
        ("-r", 0),
    ],
)
def test__main__error_with_negative_repeat(capfd, resources, option, length):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
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
            f"byfile: error: argument --repeat/-r: invalid positive_int value: '{length}'"
            in err
        )


def test__main__multiple_factories(capfd, resources):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        str(resources.joinpath("factory_def_bbb.py")),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "aaa\nbbb\n"
        assert err == ""


@pytest.mark.parametrize(
    ("option", "r_count", "f_count"),
    [
        ("--repeat", 3, 2),
        ("-r", 2, 5),
    ],
)
def test__main__option_repeat__multiple_factories(
    capfd, resources, option, r_count, f_count
):
    factory_path = str(resources.joinpath("factory_def.py"))
    factory_bbb_path = str(resources.joinpath("factory_def_bbb.py"))
    args = (
        ["randog", "byfile"]
        + (f_count - 1) * [factory_path]
        + [factory_bbb_path]
        + [option, str(r_count)]
    )
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "aaa\n" * (r_count * (f_count - 1)) + "bbb\n" * r_count
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__option_list(capfd, resources, option, length):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == str(["aaa"] * length) + "\n"
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", -1),
        ("-L", 0),
    ],
)
def test__main__error_with_negative_list(capfd, resources, option, length):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
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
            f"byfile: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


def test__main__option_output(capfd, tmp_path, resources):
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        "--output",
        str(output_path),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="r") as out_fp:
            assert out_fp.readline() == "aaa\n"
            assert out_fp.readline() == ""


def test__main__option_output__option_repeat(capfd, tmp_path, resources):
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
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
                assert out_fp.readline() == "aaa\n"
            assert out_fp.readline() == ""


def test__main__option_output__option_repeat__separate(capfd, tmp_path, resources):
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
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
                assert out_fp.readline() == "aaa\n"
                assert out_fp.readline() == ""


def test__main__regenerate__with_repeat(capfd, resources):
    line_num = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--regenerate",
        "0.5",
        "-r",
        str(line_num),
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        out_lines = list(out.splitlines())
        assert len(out_lines) == line_num
        for i, line in enumerate(out_lines):
            assert i <= int(line)
        assert line_num - 1 < int(out_lines[-1])


def test__main__regenerate__with_list(capfd, resources):
    list_size = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--regenerate",
        "0.5",
        "-L",
        str(list_size),
        "--json",
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        out_list = json.loads(out)
        assert len(out_list) == list_size
        for i, value in enumerate(out_list):
            assert i <= value
        assert list_size - 1 < out_list[-1]


def test__main__regenerate__with_repeat_list(capfd, resources):
    line_num = 3
    list_size = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--regenerate",
        "0.5",
        "-r",
        str(line_num),
        "-L",
        str(list_size),
        "--json",
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        out_list_list = list(json.loads(line) for line in out.splitlines())
        out_list_concat = list(itertools.chain(*out_list_list))

        assert len(out_list_list) == line_num
        for out_list in out_list_list:
            assert len(out_list) == list_size
        for i, value in enumerate(out_list_concat):
            assert i <= value
        assert list_size - 1 < out_list_concat[-1]


@pytest.mark.parametrize(
    "regenerate",
    [
        "-0.1",
        "1.1",
    ],
)
def test__main__regenerate__error_when_illegal_probability(
    capfd, resources, regenerate
):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--regenerate",
        regenerate,
        "-r",
        "100",
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            "byfile: error: argument --regenerate: invalid probability value: " in err
        )


@pytest.mark.parametrize(
    "regenerate",
    [
        # 2047/2048; it is greater than 1023/1024
        "0.99951171875",
    ],
)
def test__main__regenerate__error_when_illegal_probability2(
    capfd, resources, regenerate
):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--regenerate",
        regenerate,
        "-r",
        "100",
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            "byfile: error: argument --regenerate: must be lower than or equal to 1023/1024"
            in err
        )


def test__main__discard__with_repeat(capfd, resources):
    line_num = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--discard",
        "0.5",
        "-r",
        str(line_num),
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        out_lines = list(out.splitlines())
        assert len(out_lines) < line_num
        for i, line in enumerate(out_lines):
            assert i <= int(line)
        assert len(out_lines) - 1 < int(out_lines[-1]) < line_num


def test__main__discard__with_list(capfd, resources):
    list_size = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--discard",
        "0.5",
        "-L",
        str(list_size),
        "--json",
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        out_list = json.loads(out)
        assert len(out_list) < list_size
        for i, value in enumerate(out_list):
            assert i <= value
        assert len(out_list) - 1 < out_list[-1] < list_size


def test__main__discard__with_repeat_list(capfd, resources):
    line_num = 3
    list_size = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--discard",
        "0.5",
        "-r",
        str(line_num),
        "-L",
        str(list_size),
        "--json",
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        out_list_list = list(json.loads(line) for line in out.splitlines())
        out_list_concat = list(itertools.chain(*out_list_list))

        assert len(out_list_list) == line_num
        for out_list in out_list_list:
            assert len(out_list) < list_size
        for i, value in enumerate(out_list_concat):
            assert i <= value
        assert len(out_list_concat) - 1 < out_list_concat[-1] < list_size * line_num


@pytest.mark.parametrize(
    "regenerate",
    [
        "-0.1",
        "1.1",
    ],
)
def test__main__discard__error_when_illegal_probability(capfd, resources, regenerate):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--discard",
        regenerate,
        "-r",
        "100",
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "byfile: error: argument --discard: invalid probability value: " in err


@pytest.mark.parametrize(
    ("options",),
    [
        (["--json", "--repr"],),
        (["--json", "--csv", "1"],),
        (["--repr", "--csv", "1"],),
        (["--csv", "1", "--list", "1"],),
        (["--csv", "1", "-L", "1"],),
    ],
)
def test__main__error_duplicate_format(capfd, resources, options):
    args = ["randog", "byfile", str(resources.joinpath("factory_def.py")), *options]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "not allowed with argument" in err


@pytest.mark.parametrize(
    ("def_file", "line_num", "expected"),
    [
        # Tests outputting various types
        ("factory_def_dict.py", 1, "0,aaa,2019-10-14\n"),
        ("factory_def_dict_without_col.py", 1, "0,aaa,2019-10-14\n"),
        ("factory_def_list.py", 1, "0,aaa,2019-10-14\n"),
        ("factory_def.py", 1, "aaa\n"),
        ("factory_def_date.py", 1, "2019-10-14\n"),
        # Test for multiple lines of output
        ("factory_def_dict.py", 2, "0,aaa,2019-10-14\n1,aaa,2019-10-14\n"),
        (
            "factory_def_dict.py",
            3,
            "0,aaa,2019-10-14\n1,aaa,2019-10-14\n2,aaa,2019-10-14\n",
        ),
        # Test for specifying column by lambda
        ("factory_def_dict_with_lambda_column.py", 1, "0,N-aaa,2019/10/14\n"),
        # Test for skipping none
        ("factory_def_dict_half_none.py", 4, "0,aaa,2019-10-14\n2,aaa,2019-10-14\n"),
    ],
)
def test__main__csv(capfd, resources, def_file, line_num, expected):
    args = [
        "randog",
        "byfile",
        "--csv",
        str(line_num),
        str(resources.joinpath(def_file)),
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == expected
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--csv", -1),
        ("--csv", 0),
    ],
)
def test__main__error_with_negative_csv(capfd, resources, option, length):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_dict.py")),
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
            f"byfile: error: argument --csv: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (
            ["--repeat", "3", "--csv", "1"],
            "0,aaa,2019-10-14\n1,aaa,2019-10-14\n2,aaa,2019-10-14\n",
        ),
        (
            ["--repeat", "2", "--csv", "2"],
            "0,aaa,2019-10-14\n1,aaa,2019-10-14\n2,aaa,2019-10-14\n3,aaa,2019-10-14\n",
        ),
    ],
)
def test__main__csv__option_repeat(capfd, resources, options, expected):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_dict.py")),
        *options,
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == expected
        assert err == ""


def test__main__csv__option_output__option_repeat(capfd, tmp_path, resources):
    output_path = tmp_path.joinpath("out.txt")
    line_num = 2
    count = 3
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_dict.py")),
        "--output",
        str(output_path),
        "--repeat",
        str(count),
        "--csv",
        str(line_num),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="r") as out_fp:
            for i in range(count * line_num):
                assert out_fp.readline() == f"{i},aaa,2019-10-14\n"
            assert out_fp.readline() == ""


def test__main__csv__option_output__option_repeat__separate(capfd, tmp_path, resources):
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    line_num = 2
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_dict.py")),
        "--output",
        str(output_fmt_path),
        "--repeat",
        str(count),
        "--csv",
        str(line_num),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        for repeat_i in range(count):
            with open(output_paths[repeat_i], mode="r") as out_fp:
                for row_i in range(line_num):
                    i = repeat_i * line_num + row_i
                    assert out_fp.readline() == f"{i},aaa,2019-10-14\n"
                assert out_fp.readline() == ""


def test__main__csv__with_regenerate_repeat(capfd, tmp_path, resources):
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    line_num = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--output",
        str(output_fmt_path),
        "--regenerate",
        "0.5",
        "-r",
        str(count),
        "--csv",
        str(line_num),
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        out_list_list = []
        for repeat_i in range(count):
            with open(output_paths[repeat_i], mode="r") as out_fp:
                out_list = [int(line) for line in out_fp.readlines()]
            out_list_list.append(out_list)
        out_list_concat = list(itertools.chain(*out_list_list))

        assert len(out_list_list) == count
        for out_list in out_list_list:
            assert len(out_list) == line_num
        for i, value in enumerate(out_list_concat):
            assert i <= value
        assert line_num - 1 < out_list_concat[-1]


def test__main__csv__with_discard_repeat(capfd, tmp_path, resources):
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    line_num = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--output",
        str(output_fmt_path),
        "--discard",
        "0.5",
        "-r",
        str(count),
        "--csv",
        str(line_num),
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        out_list_list = []
        for repeat_i in range(count):
            with open(output_paths[repeat_i], mode="r") as out_fp:
                out_list = [int(line) for line in out_fp.readlines()]
            out_list_list.append(out_list)
        out_list_concat = list(itertools.chain(*out_list_list))

        assert len(out_list_list) == count
        for out_list in out_list_list:
            assert len(out_list) < line_num
        for i, value in enumerate(out_list_concat):
            assert i <= value
        assert len(out_list_concat) - 1 < out_list_concat[-1] < line_num * count


def test__main__byfile__help(capfd):
    args = ["randog", "byfile", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: python -m randog byfile")
        assert err == ""
