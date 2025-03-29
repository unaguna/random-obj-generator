import base64
import datetime as dt
import filecmp
import itertools
import json
import pickle
import sys
import warnings
from unittest.mock import patch

import pytest

import randog.__main__
from randog.exceptions import RandogWarning
from tests.testtools.envvar import EnvVarSnapshot


class _DummyWarning(Warning):
    pass


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
    ("json_indent", "expected_indent"),
    [
        ("0", ""),
        ("1", " "),
        ("2", "  "),
        ("3", "   "),
        ("", ""),
        (r"\t", "\t"),
    ],
)
def test__main__option_json_indent(capfd, resources, json_indent, expected_indent):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_dict.py")),
        "--json",
        f"--json-indent={json_indent}",
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == (
            f'{{\n{expected_indent}"id": 0,'
            f'\n{expected_indent}"name": "aaa",'
            f'\n{expected_indent}"join_date": "2019-10-14"\n}}\n'
        )
        assert err == ""


@pytest.mark.parametrize("json_indent", ["-1"])
def test__main__error_with_illegal_json_indent(capfd, resources, json_indent):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_dict.py")),
        "--json",
        f"--json-indent={json_indent}",
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            "byfile: error: argument --json-indent: invalid indent value: "
            + repr(json_indent)
            in err
        )


@pytest.mark.parametrize(
    "options",
    [
        [],
        ["--repr"],
    ],
)
def test__main__error_with_json_indent_without_json(capfd, resources, options):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_dict.py")),
        "--json-indent=2",
        *options,
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            "byfile: error: argument --json-indent: not allowed without argument --json"
            in err
        )


def test__main__option_base64(capfd, resources):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_bytes_const.py")),
        "--base64",
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "QIj/\n"
        assert err == ""


def test__main__option_base64__dict(capfd, resources):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_bytes_const_in_dict.py")),
        "--base64",
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "{'int': 1, 'str': 'aaa', 'bytes': 'QIj/'}\n"
        assert err == ""


def test__main__option_base64__list(capfd, resources):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_bytes_const_in_list.py")),
        "--base64",
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "[1, 'aaa', 'QIj/']\n"
        assert err == ""


def test__main__option_base64__error_with_non_bytes(capfd, resources):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        "--base64",
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert "TypeError" in err


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__byfile__pickle(capfd, tmp_path, resources, repeat):
    output_path = tmp_path.joinpath("out.txt")
    expected_values = [
        {
            "id": 0,
            "name": "aaa",
            "join_date": dt.date(2019, 10, 14),
        },
        {
            "id": 1,
            "name": "aaa",
            "join_date": dt.date(2019, 10, 14),
        },
    ]
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_dict.py")),
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

    assert values == expected_values[:repeat]


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__byfile__pickle_base64(capfd, tmp_path, resources, repeat):
    expected_values = [
        {
            "id": 0,
            "name": "aaa",
            "join_date": dt.date(2019, 10, 14),
        },
        {
            "id": 1,
            "name": "aaa",
            "join_date": dt.date(2019, 10, 14),
        },
    ]
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_dict.py")),
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

    assert values == expected_values[:repeat]


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__byfile__pickle_fmt(capfd, tmp_path, resources, repeat):
    expected_values = [
        {
            "id": 0,
            "name": "aaa",
            "join_date": dt.date(2019, 10, 14),
        },
        {
            "id": 1,
            "name": "aaa",
            "join_date": dt.date(2019, 10, 14),
        },
    ]
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_dict.py")),
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

    assert values == expected_values[:repeat]


def test__main__byfile__error_if_fmt_without_pickle(capfd, tmp_path, resources):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        "--fmt=x",
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert "error: --fmt can only be used with --pickle" in err


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
            "byfile: error: argument --repeat/-r: invalid positive_int value: "
            f"'{length}'" in err
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


@pytest.mark.parametrize("regenerate", [0.5, 0])
def test__main__regenerate__with_repeat(capfd, resources, regenerate):
    line_num = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--regenerate",
        str(regenerate),
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
            if regenerate == 0:
                assert i == int(line)
            else:
                assert i <= int(line)
        if regenerate == 0:
            assert line_num - 1 == int(out_lines[-1])
        else:
            assert line_num - 1 < int(out_lines[-1])


@pytest.mark.parametrize("regenerate", [0.5, 0])
def test__main__regenerate__with_list(capfd, resources, regenerate):
    list_size = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--regenerate",
        str(regenerate),
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
            if regenerate == 0:
                assert i == value
            else:
                assert i <= value
        if regenerate == 0:
            assert list_size - 1 == out_list[-1]
        else:
            assert list_size - 1 < out_list[-1]


@pytest.mark.parametrize("regenerate", [0.5, 0])
def test__main__regenerate__with_repeat_list(capfd, resources, regenerate):
    line_num = 3
    list_size = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--regenerate",
        str(regenerate),
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
            if regenerate == 0:
                assert i == value
            else:
                assert i <= value
        if regenerate == 0:
            assert list_size * line_num - 1 == out_list_concat[-1]
        else:
            assert list_size * line_num - 1 < out_list_concat[-1]


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
            "byfile: error: argument --regenerate: "
            "must be lower than or equal to 1023/1024" in err
        )


@pytest.mark.parametrize("discard", [0.5, 0])
def test__main__discard__with_repeat(capfd, resources, discard):
    line_num = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--discard",
        str(discard),
        "-r",
        str(line_num),
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        out_lines = list(out.splitlines())
        if discard == 0:
            assert len(out_lines) == line_num
        else:
            assert len(out_lines) < line_num
        for i, line in enumerate(out_lines):
            if discard == 0:
                assert i == int(line)
            else:
                assert i <= int(line)
        if discard == 0:
            assert len(out_lines) - 1 == int(out_lines[-1])
        else:
            assert len(out_lines) - 1 < int(out_lines[-1]) < line_num


def test__main__discard__max__with_repeat(capfd, resources):
    line_num = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--discard",
        "1",
        "-r",
        str(line_num),
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""


@pytest.mark.parametrize("discard", [0.5, 0])
def test__main__discard__with_list(capfd, resources, discard):
    list_size = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--discard",
        str(discard),
        "-L",
        str(list_size),
        "--json",
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        out_list = json.loads(out)
        if discard == 0:
            assert len(out_list) == list_size
        else:
            assert len(out_list) < list_size
        for i, value in enumerate(out_list):
            if discard == 0:
                assert i == int(value)
            else:
                assert i <= int(value)
        if discard == 0:
            assert len(out_list) - 1 == int(out_list[-1])
        else:
            assert len(out_list) - 1 < int(out_list[-1]) < list_size


def test__main__discard__max__with_list(capfd, resources):
    list_size = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--discard",
        "1",
        "-L",
        str(list_size),
        "--json",
    ]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

        out_list = json.loads(out)
        assert len(out_list) == 0


@pytest.mark.parametrize("discard", [0.5, 0])
def test__main__discard__with_repeat_list(capfd, resources, discard):
    line_num = 3
    list_size = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--discard",
        str(discard),
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
            if discard == 0:
                assert len(out_list) == list_size
            else:
                assert len(out_list) < list_size
        for i, value in enumerate(out_list_concat):
            if discard == 0:
                assert i == value
            else:
                assert i <= value
        if discard == 0:
            assert len(out_list_concat) - 1 == out_list_concat[-1]
        else:
            assert len(out_list_concat) - 1 < out_list_concat[-1] < list_size * line_num


def test__main__discard__max__with_repeat_list(capfd, resources):
    line_num = 3
    list_size = 100
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_sequential.py")),
        "--discard",
        "1",
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

        assert len(out_list_list) == 3
        assert len(out_list_concat) == 0


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
        ("factory_def_list.py", 1, "0,aaa,2019-10-14\n"),
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
    ("hide_warning", "q_options"),
    [
        (False, []),
        (True, ["--quiet"]),
        (True, ["-q"]),
    ],
)
@pytest.mark.parametrize(
    ("def_file", "line_num", "expected", "warning_msg"),
    [
        (
            "factory_def.py",
            1,
            "aaa\n",
            "--csv is recommended for only collections (such as dict, list, tuple, "
            "etc.); In CSV output, one generated value is treated as one row, so the "
            "result is the same as --repeat except for collections.",
        ),
        (
            "factory_def_date.py",
            1,
            "2019-10-14\n",
            "--csv is recommended for only collections (such as dict, list, tuple, "
            "etc.); In CSV output, one generated value is treated as one row, so the "
            "result is the same as --repeat except for collections.",
        ),
        (
            "factory_def_useless_col.py",
            1,
            "aaa\n",
            "--csv is recommended for only collections (such as dict, list, tuple, "
            "etc.); In CSV output, one generated value is treated as one row, so the "
            "result is the same as --repeat except for collections; "
            "CSV_COLUMNS in the definition file is ignored.",
        ),
        (
            "factory_def_dict_without_col.py",
            1,
            "0,aaa,2019-10-14\n",
            "Since CSV_COLUMNS is not defined in the definition file, "
            "the fields are inserted in the order returned by the "
            "dictionary; In this case, fields may not be aligned "
            "depending on the FACTORY definition, "
            "so it is recommended to define CSV_COLUMNS.",
        ),
    ],
)
def test__main__csv__with_warning(
    capfd, resources, hide_warning, q_options, def_file, line_num, expected, warning_msg
):
    args = [
        "randog",
        "byfile",
        "--csv",
        str(line_num),
        str(resources.joinpath(def_file)),
        *q_options,
    ]

    with patch.object(sys, "argv", args):
        with pytest.warns((RandogWarning, _DummyWarning)) as w_ctx:
            warnings.warn("dummy for test", _DummyWarning)
            randog.__main__.main()

        if hide_warning:
            assert len(w_ctx.list) == 1
            assert isinstance(w_ctx.list[0].message, _DummyWarning)
        else:
            assert len(w_ctx.list) == 2
            assert isinstance(w_ctx.list[0].message, _DummyWarning)
            assert isinstance(w_ctx.list[1].message, RandogWarning)
            assert len(w_ctx.list[1].message.args) == 1
            assert w_ctx.list[1].message.args[0] == warning_msg

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


@pytest.mark.parametrize(
    ("output_fmt", "output"),
    [
        ("out.txt", "out.txt"),
        ("out_{}.txt", "out_0.txt"),
    ],
)
@pytest.mark.parametrize("x_option", ["--output-encoding", "-X"])
@pytest.mark.parametrize("encoding", ["utf_8", "utf_16_le", "shift_jis"])
@pytest.mark.parametrize(
    ("options", "expected"),
    [
        ([], "テスト\n"),
        (["--csv=1", "--quiet"], "テスト\n"),
        (["--json"], '"テスト"\n'),
        (["--list=1"], "['テスト']\n"),
        (["--repeat=1"], "テスト\n"),
    ],
)
def test__main__option_output__encoding(
    capfd,
    tmp_path,
    resources,
    output_fmt,
    output,
    x_option,
    encoding,
    options,
    expected,
):
    output_path_fmt = tmp_path.joinpath(output_fmt)
    output_path = tmp_path.joinpath(output)
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_ja.py")),
        "--output",
        str(output_path_fmt),
        x_option,
        encoding,
        *options,
        "--output-linesep=LF",
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="rb") as out_fp:
            assert out_fp.read(50) == expected.encode(encoding=encoding)


@pytest.mark.parametrize(
    ("x_options",),
    [
        (["--output-encoding", "AAA"],),
        (["-X", "AAA"],),
    ],
)
def test__main__option_output__error_with_illegal_encoding(
    capfd, tmp_path, resources, x_options
):
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_ja.py")),
        "--output",
        str(output_path),
        *x_options,
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            f"byfile: error: argument --output-encoding/-X: invalid encoding value: "
            f"'{x_options[1]}'" in err
        )


@pytest.mark.parametrize(
    ("output_fmt", "output"),
    [
        ("out.txt", "out.txt"),
        ("out_{}.txt", "out_0.txt"),
    ],
)
@pytest.mark.parametrize("encoding", ["utf8", "shift_jis"])
@pytest.mark.parametrize(
    ("options", "expected"),
    [
        ([], "テスト\n"),
        (["--csv=1", "--quiet"], "テスト\n"),
        (["--json"], '"テスト"\n'),
        (["--list=1"], "['テスト']\n"),
        (["--repeat=1"], "テスト\n"),
    ],
)
def test__main__option_output__default_encoding(
    capfd,
    tmp_path,
    resources,
    output_fmt,
    output,
    encoding,
    options,
    expected,
):
    output_path_fmt = tmp_path.joinpath(output_fmt)
    output_path = tmp_path.joinpath(output)
    args = [
        "randog",
        "byfile",
        str(resources.joinpath(f"factory_def_ja_{encoding}.py")),
        "--output",
        str(output_path_fmt),
        *options,
        "--output-linesep=LF",
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="rb") as out_fp:
            assert out_fp.read(50) == expected.encode(encoding=encoding)


@pytest.mark.parametrize(
    "input_file",
    ["factory_def_ja_illegal_encoding.py", "factory_def_ja_illegal_encoding2.py"],
)
def test__main__option_output__error_with_illegal_default_encoding(
    capfd, tmp_path, resources, input_file
):
    output_path = tmp_path.joinpath("out.txt")
    pyfile = str(resources.joinpath(input_file))
    args = [
        "randog",
        "byfile",
        pyfile,
        "--output",
        str(output_path),
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert (
            "attribute 'OUTPUT_ENCODING' of factory file "
            f"'{pyfile}' MUST be None or an encoding string" in err
        )


@pytest.mark.parametrize(
    ("output_fmt", "output"),
    [
        ("out.txt", "out.txt"),
        ("out_{}.txt", "out_0.txt"),
    ],
)
@pytest.mark.parametrize("x_option", ["--output-encoding", "-X"])
@pytest.mark.parametrize("encoding", ["utf_8", "utf_16_le", "shift_jis"])
@pytest.mark.parametrize("def_encoding", ["utf8", "shift_jis"])
@pytest.mark.parametrize(
    ("options", "expected"),
    [
        ([], "テスト\n"),
        (["--csv=1", "--quiet"], "テスト\n"),
        (["--json"], '"テスト"\n'),
        (["--list=1"], "['テスト']\n"),
        (["--repeat=1"], "テスト\n"),
    ],
)
def test__main__option_output__ignore_default_encoding(
    capfd,
    tmp_path,
    resources,
    output_fmt,
    output,
    x_option,
    encoding,
    def_encoding,
    options,
    expected,
):
    output_path_fmt = tmp_path.joinpath(output_fmt)
    output_path = tmp_path.joinpath(output)
    args = [
        "randog",
        "byfile",
        str(resources.joinpath(f"factory_def_ja_{def_encoding}.py")),
        "--output",
        str(output_path_fmt),
        x_option,
        encoding,
        *options,
        "--output-linesep=LF",
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="rb") as out_fp:
            assert out_fp.read(50) == expected.encode(encoding=encoding)


@pytest.mark.parametrize(
    ("output_fmt", "output"),
    [
        ("out.txt", "out.txt"),
        ("out_{}.txt", "out_0.txt"),
    ],
)
@pytest.mark.parametrize(
    ("ls_options", "ls_expected"),
    [
        (["--output-linesep", "CRLF"], b"\r\n"),
        (["--output-linesep", "LF"], b"\n"),
        (["--output-linesep", "CR"], b"\r"),
        (["--O-ls", "CRLF"], b"\r\n"),
        (["--O-ls", "LF"], b"\n"),
        (["--O-ls", "CR"], b"\r"),
    ],
)
@pytest.mark.parametrize(
    ("options", "expected"),
    [
        ([], b"aaa"),
        (["--csv=1", "--quiet"], b"aaa"),
        (["--json"], b'"aaa"'),
        (["--list=1"], b"['aaa']"),
        (["--repeat=1"], b"aaa"),
    ],
)
def test__main__option_output__linesep(
    capfd,
    tmp_path,
    resources,
    output_fmt,
    output,
    ls_options,
    ls_expected,
    options,
    expected,
):
    output_path_fmt = tmp_path.joinpath(output_fmt)
    output_path = tmp_path.joinpath(output)
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        "--output",
        str(output_path_fmt),
        *ls_options,
        *options,
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        # mode="r" だと改行コードが '\n' に変換されてしまうため、mode="rb" でバイナリを取得する。
        with open(output_path, mode="rb") as out_fp:
            assert out_fp.read(50) == expected + ls_expected


@pytest.mark.parametrize(
    ("ls_options",),
    [
        (["--output-linesep", "CRLF"],),
        (["--output-linesep", "LF"],),
        (["--output-linesep", "CR"],),
        (["--O-ls", "CRLF"],),
        (["--O-ls", "LF"],),
        (["--O-ls", "CR"],),
    ],
)
@pytest.mark.parametrize(
    ("options", "expected"),
    [
        ([], b"aaa"),
        (["--csv=1", "--quiet"], b"aaa"),
        (["--json"], b'"aaa"'),
        (["--list=1"], b"['aaa']"),
        (["--repeat=1"], b"aaa"),
    ],
)
def test__main__option_output_linesep__without_output(
    capfdbinary,
    tmp_path,
    resources,
    ls_options,
    options,
    expected,
):
    # --output がないと、--output-linesep が無効である（標準出力への出力に --output-linesep は影響しない）

    ls_expected = b"\n"
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        *ls_options,
        *options,
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfdbinary.readouterr()
        assert out == expected + ls_expected
        assert err == b""


@pytest.mark.parametrize(
    ("ls_options",),
    [
        (["--output-linesep", "AAA"],),
        (["--O-ls", "AAA"],),
    ],
)
def test__main__option_output__error_with_illegal_linesep(
    capfd, tmp_path, resources, ls_options
):
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        "--output",
        str(output_path),
        *ls_options,
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        # Since different versions of python no longer enclose choices in single quotes,
        # remove the single quotes before comparison to ensure
        # that the assertion will succeed whether single quotes are attached.
        assert (
            f"byfile: error: argument --output-linesep/--O-ls: invalid choice: "
            f"{ls_options[1]} (choose from LF, CRLF, CR)" in err.replace("'", "")
        )


@pytest.mark.parametrize(
    ("output_fmt", "output"),
    [
        ("out.txt", "out.txt"),
        ("out_{}.txt", "out_0.txt"),
    ],
)
@pytest.mark.parametrize(
    ("ls_filename", "ls_expected"),
    [
        ("crlf", b"\r\n"),
        ("lf", b"\n"),
        ("cr", b"\r"),
        ("crlf2", b"\r\n"),
        ("lf2", b"\n"),
        ("cr2", b"\r"),
    ],
)
@pytest.mark.parametrize(
    ("options", "expected"),
    [
        ([], b"aaa"),
        (["--csv=1", "--quiet"], b"aaa"),
        (["--json"], b'"aaa"'),
        (["--list=1"], b"['aaa']"),
        (["--repeat=1"], b"aaa"),
    ],
)
def test__main__option_output__default_linesep(
    capfd,
    tmp_path,
    resources,
    output_fmt,
    output,
    ls_filename,
    ls_expected,
    options,
    expected,
):
    output_path_fmt = tmp_path.joinpath(output_fmt)
    output_path = tmp_path.joinpath(output)
    args = [
        "randog",
        "byfile",
        str(resources.joinpath(f"factory_def_ls_{ls_filename}.py")),
        "--output",
        str(output_path_fmt),
        *options,
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        # mode="r" だと改行コードが '\n' に変換されてしまうため、mode="rb" でバイナリを取得する。
        with open(output_path, mode="rb") as out_fp:
            assert out_fp.read(50) == expected + ls_expected


@pytest.mark.parametrize(
    ("ls_filename",),
    [
        ("aaa",),
    ],
)
@pytest.mark.parametrize(
    ("options", "expected"),
    [
        ([], b"aaa"),
        (["--csv=1", "--quiet"], b"aaa"),
        (["--json"], b'"aaa"'),
        (["--list=1"], b"['aaa']"),
        (["--repeat=1"], b"aaa"),
    ],
)
def test__main__option_output__error_with_illegal_default_linesep(
    capfd,
    tmp_path,
    resources,
    ls_filename,
    options,
    expected,
):
    output_path_fmt = tmp_path.joinpath("output.txt")
    pyfile = str(resources.joinpath(f"factory_def_ls_{ls_filename}.py"))
    args = [
        "randog",
        "byfile",
        pyfile,
        "--output",
        str(output_path_fmt),
        *options,
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert (
            "attribute 'OUTPUT_LINESEP' of factory file "
            f"'{pyfile}' MUST be None or LF, CRLF, CR" in err
        )


@pytest.mark.parametrize(
    ("output_fmt", "output"),
    [
        ("out.txt", "out.txt"),
        ("out_{}.txt", "out_0.txt"),
    ],
)
@pytest.mark.parametrize(
    ("ls_options", "ls_expected"),
    [
        (["--output-linesep", "CRLF"], b"\r\n"),
        (["--output-linesep", "LF"], b"\n"),
        (["--output-linesep", "CR"], b"\r"),
        (["--O-ls", "CRLF"], b"\r\n"),
        (["--O-ls", "LF"], b"\n"),
        (["--O-ls", "CR"], b"\r"),
    ],
)
@pytest.mark.parametrize(
    ("ls_filename",),
    [
        ("crlf",),
        ("lf",),
        ("cr",),
        ("crlf2",),
        ("lf2",),
        ("cr2",),
    ],
)
@pytest.mark.parametrize(
    ("options", "expected"),
    [
        ([], b"aaa"),
        (["--csv=1", "--quiet"], b"aaa"),
        (["--json"], b'"aaa"'),
        (["--list=1"], b"['aaa']"),
        (["--repeat=1"], b"aaa"),
    ],
)
def test__main__option_output__ignore_default_linesep(
    capfd,
    tmp_path,
    resources,
    output_fmt,
    output,
    ls_options,
    ls_expected,
    ls_filename,
    options,
    expected,
):
    output_path_fmt = tmp_path.joinpath(output_fmt)
    output_path = tmp_path.joinpath(output)
    args = [
        "randog",
        "byfile",
        str(resources.joinpath(f"factory_def_ls_{ls_filename}.py")),
        "--output",
        str(output_path_fmt),
        *ls_options,
        *options,
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        # mode="r" だと改行コードが '\n' に変換されてしまうため、mode="rb" でバイナリを取得する。
        with open(output_path, mode="rb") as out_fp:
            assert out_fp.read(50) == expected + ls_expected


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
        with pytest.warns(RandogWarning, match="--csv *"):
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
        with pytest.warns(RandogWarning, match="--csv *"):
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


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (["--env=VALUE=AAA"], "AAA"),
        (["--env=VALUE=bbb"], "bbb"),
        (["--env=VALUE="], ""),
        (["--env=VALUE"], ""),
        (["--env=VALUE=AAA", "--env=VALUE2=bbb"], "AAA"),
        (["--env=VALUE=AAA", "--env=VALUE2="], "AAA"),
        (["--env=VALUE=AAA", "--env=VALUE2"], "AAA"),
    ],
)
def test__main__env(capfd, tmp_path, resources, options, expected):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def_env.py")),
        *options,
    ]
    with patch.object(sys, "argv", args), EnvVarSnapshot():
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


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
@pytest.mark.parametrize(
    ("seed0", "seed1", "expect_same_output"),
    [
        (["--seed=100"], ["--seed=100"], True),
        (["--seed=100"], ["--seed=1000"], False),
        ([], ["--seed=1000"], False),
        ([], [], False),
    ],
)
def test__main__byfile__seed(
    capfd, tmp_path, resources, filename, seed0, seed1, expect_same_output
):
    filepath = resources.joinpath(filename)
    output_path0 = tmp_path.joinpath("out_0.txt")
    output_path1 = tmp_path.joinpath("out_1.txt")
    args_base = ["randog", "byfile", str(filepath), "--repeat=50"]
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


def test__main__byfile__help(capfd):
    args = ["randog", "byfile", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: randog byfile")
        assert err == ""
