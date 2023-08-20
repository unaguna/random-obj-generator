import sys
from unittest.mock import patch

import pytest

import randog.__main__


@pytest.mark.parametrize(
    ("def_file_name", "options", "expected_out"),
    [
        ("factory_def_raise_stop.py", [], ""),
        ("factory_def_only_3_times.py", ["--repeat", "4"], "0\n1\n2\n"),
        ("factory_def_only_3_times.py", ["--list", "4"], ""),
        ("factory_def_only_3_times.py", ["--repeat", "2", "--list", "2"], "[0, 1]\n"),
        ("factory_def_only_3_times.py", ["--csv", "4", "--quiet"], "0\n1\n2\n"),
        (
            "factory_def_only_3_times.py",
            ["--repeat", "2", "--csv", "2", "--quiet"],
            "0\n1\n2\n",
        ),
    ],
)
def test__main__error_on_factory_stopped(
    capfd, resources, def_file_name, options, expected_out
):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath(def_file_name)),
        "--error-on-factory-stopped",
        *options,
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == expected_out
        assert (
            "error: the factory stopped generating before the process was complete"
            in err
        )


@pytest.mark.parametrize(
    ("def_file_name", "options", "expected_out"),
    [
        ("factory_def_raise_stop.py", [], ""),
        ("factory_def_only_3_times.py", ["--repeat", "4"], "0\n1\n2\n"),
        ("factory_def_only_3_times.py", ["--list", "4"], "[0, 1, 2]\n"),
        (
            "factory_def_only_3_times.py",
            ["--repeat", "2", "--list", "2"],
            "[0, 1]\n[2]\n",
        ),
        ("factory_def_only_3_times.py", ["--csv", "4", "--quiet"], "0\n1\n2\n"),
        (
            "factory_def_only_3_times.py",
            ["--repeat", "2", "--csv", "2", "--quiet"],
            "0\n1\n2\n",
        ),
    ],
)
def test__main__without_error_on_factory_stopped(
    capfd, resources, def_file_name, options, expected_out
):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath(def_file_name)),
        *options,
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == expected_out
        assert err == ""


@pytest.mark.parametrize(
    ("def_file_name", "options", "expected_out"),
    [
        ("factory_def_sequential.py", ["--repeat", "3"], "0\n1\n2\n"),
        ("factory_def_sequential.py", ["--list", "3"], "[0, 1, 2]\n"),
        (
            "factory_def_sequential.py",
            ["--repeat", "3", "--list", "1"],
            "[0]\n[1]\n[2]\n",
        ),
        ("factory_def_sequential.py", ["--csv", "3", "--quiet"], "0\n1\n2\n"),
        (
            "factory_def_sequential.py",
            ["--repeat", "3", "--csv", "1", "--quiet"],
            "0\n1\n2\n",
        ),
        ("factory_def_only_3_times.py", ["--repeat", "3"], "0\n1\n2\n"),
        ("factory_def_only_3_times.py", ["--list", "3"], "[0, 1, 2]\n"),
        (
            "factory_def_only_3_times.py",
            ["--repeat", "3", "--list", "1"],
            "[0]\n[1]\n[2]\n",
        ),
        ("factory_def_only_3_times.py", ["--csv", "3", "--quiet"], "0\n1\n2\n"),
        (
            "factory_def_only_3_times.py",
            ["--repeat", "3", "--csv", "1", "--quiet"],
            "0\n1\n2\n",
        ),
    ],
)
def test__main__error_on_factory_stopped__no_error_with_enough_long_factory(
    capfd, resources, def_file_name, options, expected_out
):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath(def_file_name)),
        "--error-on-factory-stopped",
        *options,
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == expected_out
        assert err == ""


@pytest.mark.parametrize(
    ("def_file_name", "options", "expected_out"),
    [
        ("factory_def_raise_stop.py", [], ""),
    ],
)
def test__main__no_error__without_error_on_factory_stopped(
    capfd, resources, def_file_name, options, expected_out
):
    args = [
        "randog",
        "byfile",
        str(resources.joinpath(def_file_name)),
        *options,
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == expected_out
        assert err == ""
