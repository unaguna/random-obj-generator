import os
import re
import sys
from pathlib import Path
import typing as t

import pytest


def pytest_runtest_setup(item):
    for marker in item.iter_markers(name="require_python"):
        __require_python(*marker.args)
    for marker in item.iter_markers(name="require_sqlalchemy"):
        __require_sqlalchemy(*marker.args)
    for _ in item.iter_markers(name="require_rstr"):
        __require_rstr()
    for _ in item.iter_markers(name="without_rstr"):
        __without_rstr()
    for _ in item.iter_markers(name="require_yaml"):
        __require_yaml()
    for _ in item.iter_markers(name="without_yaml"):
        __without_yaml()


def __require_python(*version_requirements: str):
    ranges = [_PythonVersionRange(text) for text in version_requirements]
    actual_version = sys.version_info[:3]

    if all(actual_version in r for r in ranges):
        pass
    else:
        pytest.skip(reason="need python " + ", ".join(version_requirements))


def __require_sqlalchemy(*variants: t.Literal[1, 2]):
    require1 = 1 in variants
    require2 = 2 in variants

    ver_sqlalchemy = __get_version_of_sqlalchemy()

    if require1 and require2:
        if ver_sqlalchemy is None or ver_sqlalchemy[0] not in "12":
            pytest.skip(reason="need sqlalchemy 1 or 2")
    elif require1:
        if ver_sqlalchemy is None or ver_sqlalchemy[0] != "1":
            pytest.skip(reason="need sqlalchemy 1")
    elif require2:
        if ver_sqlalchemy is None or ver_sqlalchemy[0] != "2":
            pytest.skip(reason="need sqlalchemy 2")
    else:
        pass


def __require_rstr():
    if not __exists_rstr():
        pytest.skip(reason="need rstr")


def __without_rstr():
    if __exists_rstr():
        pytest.skip(reason="rstr is installed")


def __require_yaml():
    if not __exists_yaml():
        pytest.skip(reason="need yaml")


def __without_yaml():
    if __exists_yaml():
        pytest.skip(reason="yaml is installed")


def __get_version_of_sqlalchemy() -> t.Optional[str]:
    try:
        import sqlalchemy

        return sqlalchemy.__version__
    except (ModuleNotFoundError, AttributeError):
        return None


def __exists_rstr() -> bool:
    try:
        import rstr

        return True
    except (ModuleNotFoundError, AttributeError):
        return False


def __exists_yaml() -> bool:
    try:
        import yaml

        return True
    except (ModuleNotFoundError, AttributeError):
        return False


@pytest.fixture
def resources():
    return Path(os.path.dirname(__file__), "tests/resources")


class _PythonVersionRange:
    _min: t.Tuple[int, int, int]
    _exclude_min: bool
    _max: t.Tuple[int, int, int]
    _exclude_max: bool

    _REGEX_INIT = re.compile(r"([<>]?=?)([0-9]+)\.([0-9]+)\.([0-9]+)")

    def __init__(self, requirement: str):
        match = re.fullmatch(self._REGEX_INIT, requirement)
        compare_mode = match.group(1)
        major = int(match.group(2))
        minor = int(match.group(3))
        micro = int(match.group(4))

        if compare_mode == "=" or compare_mode == "":
            self._min = (major, minor, micro)
            self._exclude_min = False
            self._max = (major, minor, micro)
            self._exclude_max = False
        elif compare_mode == ">=":
            self._min = (major, minor, micro)
            self._exclude_min = False
            self._max = (999, 999, 999)
            self._exclude_max = False
        elif compare_mode == ">":
            self._min = (major, minor, micro)
            self._exclude_min = True
            self._max = (999, 999, 999)
            self._exclude_max = False
        elif compare_mode == "<=":
            self._min = (0, 0, 0)
            self._exclude_min = False
            self._max = (major, minor, micro)
            self._exclude_max = False
        elif compare_mode == "<":
            self._min = (0, 0, 0)
            self._exclude_min = False
            self._max = (major, minor, micro)
            self._exclude_max = True
        else:
            raise ValueError(compare_mode)

    def __contains__(self, item):
        if self._exclude_min:
            if not self._min < item:
                return False
        else:
            if not self._min <= item:
                return False
        if self._exclude_max:
            if not item < self._max:
                return False
        else:
            if not item <= self._max:
                return False

        return True
