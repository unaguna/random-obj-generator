from datetime import timedelta

import pytest

from randog.timedelta_util import from_str, to_iso, TimedeltaExpressionError, to_fmt


@pytest.mark.parametrize(
    ("input_str", "expected"),
    [
        # each units
        ("1d", timedelta(days=1)),
        ("1h", timedelta(hours=1)),
        ("1m", timedelta(minutes=1)),
        ("1s", timedelta(seconds=1)),
        ("1ms", timedelta(milliseconds=1)),
        ("1us", timedelta(microseconds=1)),
        ("-1d", timedelta(days=-1)),
        ("-1h", timedelta(hours=-1)),
        ("-1m", timedelta(minutes=-1)),
        ("-1s", timedelta(seconds=-1)),
        ("-1ms", timedelta(milliseconds=-1)),
        ("-1us", timedelta(microseconds=-1)),
        # combined term
        ("1h20m", timedelta(hours=1, minutes=20)),
        ("1h20s", timedelta(hours=1, seconds=20)),
        ("-1h20m", timedelta(hours=-1, minutes=-20)),
        ("-1h20s", timedelta(hours=-1, seconds=-20)),
        ("1h1m20s", timedelta(hours=1, minutes=1, seconds=20)),
        ("1h80s", timedelta(hours=1, minutes=1, seconds=20)),
        # calc
        ("1h+20m", timedelta(hours=1, minutes=20)),
        ("1h-20m", timedelta(minutes=40)),
        ("1h-20m+30m", timedelta(minutes=70)),
        ("1h-20m-30m", timedelta(minutes=10)),
        ("-1h+20m", timedelta(hours=-1, minutes=20)),
        ("-1h-20m", timedelta(minutes=-80)),
        ("-1h-20m+30m", timedelta(minutes=-50)),
        ("-1h-20m-30m", timedelta(minutes=-110)),
        ("1h-20m30s", timedelta(minutes=39, seconds=30)),
        ("-1h-20m30s", timedelta(hours=-1, minutes=-20, seconds=-30)),
        ("-1h+20m30s", timedelta(minutes=-40, seconds=30)),
    ],
)
def test__timedelta_util__from_str(input_str, expected):
    generated = from_str(input_str)
    assert generated == expected


@pytest.mark.parametrize(
    "input_str",
    ["1", "d", "10", "10dd", "10h+10x"],
)
def test__timedelta_util__from_str__error_by_illegal_arg(input_str):
    with pytest.raises(TimedeltaExpressionError) as e_ctx:
        from_str(input_str)
    e = e_ctx.value
    message = e.args[0]

    assert isinstance(message, str)
    assert message.startswith("illegal timedelta expression: ")


@pytest.mark.parametrize(
    ("input_td", "expected"),
    [
        (timedelta(days=1), "P1D"),
        (timedelta(hours=1), "PT1H"),
        (timedelta(minutes=1), "PT1M"),
        (timedelta(seconds=1), "PT1S"),
        (timedelta(milliseconds=1), "PT0.001S"),
        (timedelta(microseconds=1), "PT0.000001S"),
        (timedelta(0), "PT0S"),
        (timedelta(days=1000), "P1000D"),
        (timedelta(hours=26, minutes=30), "P1DT2H30M"),
        (-timedelta(hours=26, minutes=30), "-P1DT2H30M"),
        (timedelta(hours=20, minutes=30, seconds=55), "PT20H30M55S"),
        (
            timedelta(hours=20, minutes=30, seconds=55, microseconds=51200),
            "PT20H30M55.0512S",
        ),
    ],
)
def test__timedelta_util__to_iso(input_td, expected):
    generated = to_iso(input_td)
    assert generated == expected


@pytest.mark.parametrize(
    ("input_td", "expected"),
    [
        (timedelta(hours=20, minutes=30, seconds=55), "PT20H30M55S"),
        (
            timedelta(hours=20, minutes=30, seconds=55, microseconds=51200),
            "PT20H30M55S",
        ),
    ],
)
def test__timedelta_util__to_iso__exclude_milliseconds(input_td, expected):
    generated = to_iso(input_td, exclude_milliseconds=True)
    assert generated == expected


@pytest.mark.parametrize(
    ("input_td", "point_char", "expected"),
    [
        (
            timedelta(hours=20, minutes=30, seconds=55, microseconds=51200),
            ".",
            "PT20H30M55.0512S",
        ),
        (
            timedelta(hours=20, minutes=30, seconds=55, microseconds=51200),
            ",",
            "PT20H30M55,0512S",
        ),
    ],
)
def test__timedelta_util__to_iso__point_char(input_td, point_char, expected):
    generated = to_iso(input_td, point_char=point_char)
    assert generated == expected


@pytest.mark.parametrize(
    ("input_td", "fmt", "expected"),
    [
        # %D
        (timedelta(days=1), "%D", "1"),
        (timedelta(days=2), "%D", "2"),
        # %tH
        (timedelta(hours=3), "%tH", "3"),
        (timedelta(days=1), "%tH", "24"),
        (timedelta(days=1, hours=12), "%tH", "36"),
        # %H
        (timedelta(hours=3), "%H", "03"),
        (timedelta(days=1), "%H", "00"),
        (timedelta(days=1, hours=12), "%H", "12"),
        # %tM
        (timedelta(minutes=3), "%tM", "3"),
        (timedelta(days=1, hours=12), "%tM", "2160"),
        (timedelta(days=1, hours=12, minutes=5), "%tM", "2165"),
        # %M
        (timedelta(minutes=3), "%M", "03"),
        (timedelta(days=1, hours=12), "%M", "00"),
        (timedelta(days=1, hours=12, minutes=5), "%M", "05"),
        # %tS
        (timedelta(seconds=3), "%tS", "3"),
        (timedelta(days=1, hours=12), "%tS", "129600"),
        (timedelta(days=1, hours=12, seconds=5), "%tS", "129605"),
        (timedelta(seconds=5, milliseconds=800), "%tS", "5"),
        # %S
        (timedelta(seconds=3), "%S", "03"),
        (timedelta(days=1, hours=12, minutes=13), "%S", "00"),
        (timedelta(days=1, hours=12, seconds=5), "%S", "05"),
        (timedelta(seconds=5, milliseconds=800), "%S", "05"),
        # %f
        (timedelta(days=1, hours=12, seconds=5), "%f", "000000"),
        (timedelta(seconds=5, milliseconds=800), "%f", "800000"),
        (timedelta(seconds=5, microseconds=800), "%f", "000800"),
        # combine
        (timedelta(days=1), "%D %H:%M:%S", "1 00:00:00"),
        (timedelta(days=1), "%tH:%M:%S", "24:00:00"),
        (
            timedelta(days=1, hours=12, minutes=13, seconds=14),
            "%D %H:%M:%S",
            "1 12:13:14",
        ),
        (timedelta(days=1, hours=12, minutes=13, seconds=14), "%tH:%M:%S", "36:13:14"),
        (
            timedelta(days=1, hours=12, microseconds=123),
            "%tH:%M:%S.%f",
            "36:00:00.000123",
        ),
    ],
)
def test__timedelta_util__to_fmt(input_td, fmt, expected):
    generated = to_fmt(input_td, fmt)
    assert generated == expected


def test__timedelta_util__to_fmt__error_by_illegal_fmt():
    with pytest.raises(ValueError) as e_ctx:
        to_fmt(timedelta(), "%A")
    e = e_ctx.value
    message = e.args[0]

    assert message == "Invalid format string"
