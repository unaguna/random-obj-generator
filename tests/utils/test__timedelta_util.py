from datetime import timedelta

import pytest

from randog.timedelta_util import from_str, TimedeltaExpressionError


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
