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
        (["--log-stderr=CRITICAL"], False, False),
        (["--log-stderr=ERROR"], False, False),
        (["--log-stderr=WARNING"], False, False),
        (["--log-stderr=INFO"], True, False),
        (["--log-stderr=DEBUG"], True, True),
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
