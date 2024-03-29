import json
import logging
import sys
import typing as t
from unittest.mock import patch

import pytest

import randog.__main__


_PARAM_MODE_OPTIONS = [
    (["bool"],),
    (["int", 0, 0],),
    (["float", 0, 0],),
    (["decimal", 0, 0],),
    (["str"],),
    (["datetime"],),
    (["date"],),
    (["time"],),
    (["timedelta"],),
    (lambda resources: ["byfile", str(resources.joinpath("factory_def.py"))],),
]


@pytest.mark.parametrize(("mode_options",), _PARAM_MODE_OPTIONS)
@pytest.mark.parametrize(
    ("log_options", "include_info", "include_debug"),
    [
        (["--log-stderr=ERROR"], False, False),
        (["--log-stderr=WARNING"], False, False),
        (["--log-stderr=INFO"], True, False),
        (["--log-stderr=DEBUG"], True, True),
        (["--log-stderr=ERROR-full"], False, False),
        (["--log-stderr=WARNING-full"], False, False),
        (["--log-stderr=INFO-full"], True, False),
        (["--log-stderr=DEBUG-full"], True, True),
    ],
)
def test__main__logging__stderr(
    resources, capfd, mode_options, log_options, include_info, include_debug
):
    if isinstance(mode_options, t.Callable):
        mode_options = mode_options(resources)
    args = ["randog", *mode_options, *log_options]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out != ""
        if include_info:
            assert "info: " in err
        else:
            assert "info:" not in err
        if include_debug:
            assert "debug: " in err
        else:
            assert "debug:" not in err

        # TODO: WARNING や ERROR のログを全モードで出すようになったらそのアサーションも追加する。


@pytest.mark.parametrize(
    ("def_filename",),
    [
        ("factory_def_error_on_def.py",),
        ("factory_def_error_on_generation.py",),
    ],
)
@pytest.mark.parametrize(
    ("log_options", "include_traceback"),
    [
        (["--log-stderr=ERROR"], False),
        (["--log-stderr=WARNING"], False),
        (["--log-stderr=INFO"], False),
        (["--log-stderr=DEBUG"], False),
        (["--log-stderr=ERROR-full"], True),
        (["--log-stderr=WARNING-full"], True),
        (["--log-stderr=INFO-full"], True),
        (["--log-stderr=DEBUG-full"], True),
    ],
)
def test__main__logging__stderr_include_traceback(
    resources,
    capfd,
    def_filename,
    log_options,
    include_traceback,
):
    # clear handlers defined by main() in the previous testcase.
    # Skipping this will leave the handler to output with traceback,
    # which will affect the test.
    for logger_name in logging.root.manager.loggerDict:
        logging.getLogger(logger_name).handlers.clear()
    logging.getLogger().handlers.clear()

    args = ["randog", "byfile", str(resources.joinpath(def_filename)), *log_options]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert "error: " in err
        if include_traceback:
            assert "Traceback" in err
        else:
            assert "Traceback" not in err


@pytest.mark.parametrize(("mode_options",), _PARAM_MODE_OPTIONS)
def test__main__logging__stderr__error_when_illegal_level(
    resources, capfd, mode_options
):
    if isinstance(mode_options, t.Callable):
        mode_options = mode_options(resources)
    args = ["randog", *mode_options, "--log-stderr=AAA"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "error: argument --log-stderr: invalid choice: 'AAA'" in err


@pytest.mark.parametrize(("mode_options",), _PARAM_MODE_OPTIONS)
def test__main__logging__apply_config_file(resources, capfd, mode_options):
    if isinstance(mode_options, t.Callable):
        mode_options = mode_options(resources)
    config_file = resources.joinpath("logging_conf_stderr.json")
    args = ["randog", *mode_options, "--log", str(config_file)]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out != ""
        assert "\tINFO\trandog.cmd\trun randog with args:" in err
        assert "DEBUG:" not in err


@pytest.mark.require_yaml
@pytest.mark.parametrize(("mode_options",), _PARAM_MODE_OPTIONS)
def test__main__logging__apply_config_file_yaml(resources, capfd, mode_options):
    if isinstance(mode_options, t.Callable):
        mode_options = mode_options(resources)
    config_file = resources.joinpath("logging_conf_stderr.yaml")
    args = ["randog", *mode_options, "--log", str(config_file)]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out != ""
        assert "\tINFO\trandog.cmd\trun randog with args:" in err
        assert "DEBUG:" not in err


@pytest.mark.without_yaml
@pytest.mark.parametrize(("mode_options",), _PARAM_MODE_OPTIONS)
def test__main__logging__apply_config_file_yaml__without_yaml(
    resources, capfd, mode_options
):
    if isinstance(mode_options, t.Callable):
        mode_options = mode_options(resources)
    config_file = resources.joinpath("logging_conf_stderr.yaml")
    args = ["randog", *mode_options, "--log", str(config_file)]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert (
            "error: failed to apply the logging configure file; JSONDecodeError: "
            in err
        )
        assert (
            "error: Are you trying to use YAML format logging configuration? "
            "If you want to use YAML format configuration files, "
            "PyYAML must be installed." in err
        )


@pytest.mark.parametrize(("mode_options",), _PARAM_MODE_OPTIONS)
def test__main__logging__apply_config_file__error_when_missing(
    resources, capfd, mode_options
):
    if isinstance(mode_options, t.Callable):
        mode_options = mode_options(resources)
    config_file = resources.joinpath("__dummy_logging_conf.json")
    args = ["randog", *mode_options, "--log", str(config_file)]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert (
            "error: failed to apply the logging configure file; FileNotFoundError: "
            in err
        )


@pytest.mark.parametrize(("mode_options",), _PARAM_MODE_OPTIONS)
def test__main__logging__apply_config_file__error_when_illegal_json(
    resources, tmp_path, capfd, mode_options
):
    if isinstance(mode_options, t.Callable):
        mode_options = mode_options(resources)
    config_file = tmp_path.joinpath("illegal_logging_conf.json")

    # Preparation: Create config file
    with open(config_file, mode="wt") as fp:
        fp.write("{")

    args = ["randog", *mode_options, "--log", str(config_file)]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert "failed to apply the logging configure file; " in err


@pytest.mark.parametrize(("mode_options",), _PARAM_MODE_OPTIONS)
def test__main__logging__apply_config_file__error_when_illegal_config(
    resources, tmp_path, capfd, mode_options
):
    if isinstance(mode_options, t.Callable):
        mode_options = mode_options(resources)
    config_tmp_file = resources.joinpath("logging_conf_stderr.json")
    config_file = tmp_path.joinpath("logging_config.json")

    # Preparation: Create config file
    with open(config_tmp_file, mode="rt") as fp:
        config_dict = json.load(fp)
    del config_dict["formatters"]["fmt_default"]
    with open(config_file, mode="wt") as fp:
        json.dump(config_dict, fp)

    args = ["randog", *mode_options, "--log", str(config_file)]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert (
            "failed to apply the logging configure file; "
            "ValueError: Unable to configure handler 'console'; "
            "ValueError: Unable to set formatter 'fmt_default'; " in err
        )


@pytest.mark.parametrize(("mode_options",), _PARAM_MODE_OPTIONS)
def test__main__logging__apply_config_file__log_file(
    resources, tmp_path, capfd, mode_options
):
    if isinstance(mode_options, t.Callable):
        mode_options = mode_options(resources)
    config_tmp_file = resources.joinpath("logging_conf_stderr.json")
    config_file = tmp_path.joinpath("logging_config.json")
    log_file = tmp_path.joinpath("testcase.log")

    # Preparation: Create config file
    with open(config_tmp_file, mode="rt") as fp:
        config_dict = json.load(fp)
    config_dict["handlers"]["console"] = {
        "class": "logging.FileHandler",
        "filename": str(log_file),
        "formatter": "fmt_default",
        "level": "INFO",
    }
    with open(config_file, mode="wt") as fp:
        json.dump(config_dict, fp)

    args = ["randog", *mode_options, "--log", str(config_file)]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out != ""
        assert err == ""

        with open(log_file, mode="rt") as fp:
            assert "\tINFO\trandog.cmd\trun randog with args:" in fp.readline()


@pytest.mark.parametrize(
    ("disable_existing_loggers", "should_output_to_stderr"),
    [
        (None, True),  # disable_existing_loggers is not explicitly specified
        (False, True),
        (True, False),
    ],
)
def test__main__logging__apply_config_file__error_is_output_to_stderr(
    resources, tmp_path, capfd, disable_existing_loggers, should_output_to_stderr
):
    """

    Case 1:
    Even if logging conf file is applied, error is output into stderr
    if disable_existing_loggers is not explicitly True.

    Case 2:
    Error is not output into stderr
    if logging conf file claims disable_existing_loggers.
    """

    factory_def = resources.joinpath("__dummy_factory_def.py")
    config_tmp_file = resources.joinpath("logging_conf_stderr.json")
    config_file = tmp_path.joinpath("logging_config.json")
    log_file = tmp_path.joinpath("testcase.log")

    # Preparation: Create config file
    with open(config_tmp_file, mode="rt") as fp:
        config_dict = json.load(fp)
    config_dict["handlers"]["console"] = {
        "class": "logging.FileHandler",
        "filename": str(log_file),
        "formatter": "fmt_default",
        "level": "INFO",
    }
    if disable_existing_loggers is not None:
        config_dict["disable_existing_loggers"] = disable_existing_loggers
    with open(config_file, mode="wt") as fp:
        json.dump(config_dict, fp)

    args = ["randog", "byfile", str(factory_def), "--log", str(config_file)]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        if should_output_to_stderr:
            assert (
                "error: FileNotFoundError: [Errno 2] No such file or directory: " in err
            )
            assert "Traceback" not in err
        else:
            assert err == ""

        with open(log_file, mode="rt") as fp:
            assert "INFO\t" in fp.readline()
            assert (
                "ERROR\trandog.cmd\tFileNotFoundError: "
                "[Errno 2] No such file or directory: " in fp.readline()
            )
            assert "Traceback" in fp.readline()
