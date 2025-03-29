import base64
import filecmp
import ipaddress
import pickle
import sys
from unittest.mock import patch

import pytest

import randog.__main__


def test__main__ipv4(capfd):
    args = ["randog", "ipv4"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out != ""
        assert err == ""


def test__main__ipv4__default(capfd):
    args = ["randog", "ipv4", "-r", "100"]
    with patch.object(sys, "argv", args):
        expected_network = ipaddress.ip_network("192.0.2.0/24")
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out != ""
        assert err == ""

        actual_values = [ipaddress.ip_address(line) for line in out.splitlines()]
        assert all(value in expected_network for value in actual_values)


@pytest.mark.parametrize(
    ("args_network",),
    [
        (["192.168.0.0/30"],),
        (["192.168.0.0/24", "8.8.8.0/24"],),
    ],
)
def test__main__ipv4__network(capfd, args_network):
    expected_network = [ipaddress.ip_network(arg) for arg in args_network]

    args = ["randog", "ipv4", *args_network, "--repeat=300"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        actual_values = [ipaddress.ip_address(line) for line in out.splitlines()]
        assert all(
            any(value in network for network in expected_network)
            for value in actual_values
        )
        assert err == ""


@pytest.mark.parametrize(
    ("args_network",),
    [
        (["192.168.0.256/30"],),
        (["192.168.256.0/30"],),
        (["192.256.0.0/30"],),
        (["256.168.0.0/30"],),
        (["192.168.0.0/"],),
        (["192.168.0.0/33"],),
        (["192.168.0.0/-1"],),
    ],
)
def test__main__ipv4__error_when_illegal_network(capfd, args_network):
    args = ["randog", "ipv4", *args_network]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "ipv4: error: argument NETWORK: invalid ipv4_network value: " in err


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (["192.168.0.1/32"], "IPv4Address('192.168.0.1')"),
    ],
)
def test__main__ipv4__option_repr(capfd, options, expected):
    args = ["randog", "ipv4", *options, "--repr"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (["192.168.0.1/32"], '"192.168.0.1"'),
    ],
)
def test__main__ipv4__option_json(capfd, options, expected):
    args = ["randog", "ipv4", *options, "--json"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.require_python(">=3.9.0")
@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (["192.168.0.1/32", "--fmt", "s"], "192.168.0.1"),
        (["192.168.0.1/32", "--fmt", "b"], "11000000101010000000000000000001"),
        (["192.168.0.1/32", "--fmt", "#b"], "0b11000000101010000000000000000001"),
        (["192.168.0.1/32", "--fmt", "_b"], "1100_0000_1010_1000_0000_0000_0000_0001"),
        (["192.168.0.1/32", "--fmt", "x"], "c0a80001"),
        (["192.168.0.1/32", "--fmt", "X"], "C0A80001"),
    ],
)
def test__main__ipv4__fmt(capfd, options, expected):
    args = ["randog", "ipv4", *options]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.require_python("<3.9.0")
@pytest.mark.parametrize(
    ("options",),
    [
        (["192.168.0.1/32", "--fmt", "s"],),
        (["192.168.0.1/32", "--fmt", "b"],),
        (["192.168.0.1/32", "--fmt", "#b"],),
        (["192.168.0.1/32", "--fmt", "_b"],),
        (["192.168.0.1/32", "--fmt", "x"],),
        (["192.168.0.1/32", "--fmt", "X"],),
    ],
)
def test__main__ipv4__fmt__error__lt_3_9(capfd, options):
    args = ["randog", "ipv4", *options]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert (
            "ipv4: error: argument --fmt: python>=3.9.0 is required "
            "to use --fmt for ipv4"
        ) in err


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__ipv4__pickle(capfd, tmp_path, repeat):
    expected_value = ipaddress.ip_address("127.0.0.5")
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "ipv4",
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
def test__main__ipv4__pickle_base64(capfd, repeat):
    expected_value = ipaddress.ip_address("127.0.0.5")
    args = [
        "randog",
        "ipv4",
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


@pytest.mark.require_python(">=3.9.0")
@pytest.mark.parametrize("repeat", [1, 2])
def test__main__ipv4__pickle_fmt(capfd, tmp_path, repeat):
    expected_value = ipaddress.ip_address("127.0.0.5")
    args = [
        "randog",
        "ipv4",
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


@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__ipv4__option_repeat(capfd, resources, option, count):
    args = [
        "randog",
        "ipv4",
        "192.168.0.1/32",
        option,
        str(count),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "192.168.0.1\n" * count
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--repeat", -1),
        ("-r", 0),
    ],
)
def test__main__ipv4__error_with_negative_repeat(capfd, resources, option, length):
    args = [
        "randog",
        "ipv4",
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
            f"ipv4: error: argument --repeat/-r: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__ipv4__option_list(capfd, resources, option, length):
    args = [
        "randog",
        "ipv4",
        "192.168.0.1/32",
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == str([ipaddress.IPv4Address("192.168.0.1")] * length) + "\n"
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", -1),
        ("-L", 0),
    ],
)
def test__main__ipv4__error_with_negative_list(capfd, resources, option, length):
    args = [
        "randog",
        "ipv4",
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
            f"ipv4: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


def test__main__ipv4__option_output(capfd, tmp_path, resources):
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "ipv4",
        "192.168.0.1/32",
        "--output",
        str(output_path),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="r") as out_fp:
            assert out_fp.readline() == "192.168.0.1\n"
            assert out_fp.readline() == ""


def test__main__ipv4__option_output__option_repeat(capfd, tmp_path, resources):
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "ipv4",
        "192.168.0.1/32",
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
                assert out_fp.readline() == "192.168.0.1\n"
            assert out_fp.readline() == ""


def test__main__ipv4__option_output__option_repeat__separate(
    capfd, tmp_path, resources
):
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "ipv4",
        "192.168.0.1/32",
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
                assert out_fp.readline() == "192.168.0.1\n"
                assert out_fp.readline() == ""


@pytest.mark.parametrize(
    ("options",),
    [
        (["--json", "--repr"],),
    ],
)
def test__main__ipv4__error_duplicate_format(capfd, resources, options):
    args = ["randog", "ipv4", *options]
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
def test__main__ipv4__seed(capfd, tmp_path, seed0, seed1, expect_same_output):
    output_path0 = tmp_path.joinpath("out_0.txt")
    output_path1 = tmp_path.joinpath("out_1.txt")
    args_base = ["randog", "ipv4", "--repeat=50"]
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


def test__main__ipv4__help(capfd):
    args = ["randog", "ipv4", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: randog ipv4")
        assert err == ""
