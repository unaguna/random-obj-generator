import pytest

from randog._utils.formatutils import format_bytes


@pytest.mark.parametrize(
    ("fmt", "value", "expected"),
    [
        ("b", b"\x88\xff", "1000100011111111"),
        ("_b", b"\x88\xff", "1000_1000_1111_1111"),
        (">18b", b"\x88\xff", "  1000100011111111"),
        ("<18b", b"\x88\xff", "1000100011111111  "),
        ("L>18b", b"\x88\xff", "LL1000100011111111"),
        ("L<18b", b"\x88\xff", "1000100011111111LL"),
        ("L^18b", b"\x88\xff", "L1000100011111111L"),
        ("018b", b"\x88\xff", "100010001111111100"),
        ("021_b", b"\x88\xff", "1000_1000_1111_1111_0"),
        ("0<21_b", b"\x88\xff", "1000_1000_1111_111100"),
        ("x", b"\x40\x88\xff", "4088ff"),
        ("_x", b"\x40\x88\xff", "4088_ff"),
        (">9x", b"\x40\x88\xff", "   4088ff"),
        ("<9x", b"\x40\x88\xff", "4088ff   "),
        ("L>9x", b"\x40\x88\xff", "LLL4088ff"),
        ("L<9x", b"\x40\x88\xff", "4088ffLLL"),
        ("L^9x", b"\x40\x88\xff", "L4088ffLL"),
        ("09x", b"\x40\x88\xff", "4088ff000"),
        ("011_x", b"\x40\x88\xff", "4088_ff00_0"),
        ("0<11_x", b"\x40\x88\xff", "4088_ff0000"),
        ("X", b"\x40\x88\xff", "4088FF"),
        ("_X", b"\x40\x88\xff", "4088_FF"),
        (">9X", b"\x40\x88\xff", "   4088FF"),
        ("<9X", b"\x40\x88\xff", "4088FF   "),
        ("L>9X", b"\x40\x88\xff", "LLL4088FF"),
        ("L<9X", b"\x40\x88\xff", "4088FFLLL"),
        ("L^9X", b"\x40\x88\xff", "L4088FFLL"),
        ("09X", b"\x40\x88\xff", "4088FF000"),
        ("011_X", b"\x40\x88\xff", "4088_FF00_0"),
        ("0<11_X", b"\x40\x88\xff", "4088_FF0000"),
        ("c", b"\x40\x88\xff", r"@\x88\xff"),
        (">16c", b"\x40\x88\xff", r"       @\x88\xff"),
        ("<16c", b"\x40\x88\xff", r"@\x88\xff       "),
        ("16c", b"\x40\x88\xff", r"@\x88\xff       "),
        ("^16c", b"\x40\x88\xff", r"   @\x88\xff    "),
        ("@>16c", b"\x40\x88\xff", r"@@@@@@@@\x88\xff"),
        ("@<16c", b"\x40\x88\xff", r"@\x88\xff@@@@@@@"),
        ("@^16c", b"\x40\x88\xff", r"@@@@\x88\xff@@@@"),
        ("s", b"\x40\x88\xff", r"b'@\x88\xff'"),
        (">16s", b"\x40\x88\xff", r"    b'@\x88\xff'"),
        ("<16s", b"\x40\x88\xff", r"b'@\x88\xff'    "),
        ("16s", b"\x40\x88\xff", r"b'@\x88\xff'    "),
        ("^16s", b"\x40\x88\xff", r"  b'@\x88\xff'  "),
        ("@>16s", b"\x40\x88\xff", r"@@@@b'@\x88\xff'"),
        ("@<16s", b"\x40\x88\xff", r"b'@\x88\xff'@@@@"),
        ("@^16s", b"\x40\x88\xff", r"@@b'@\x88\xff'@@"),
    ],
)
def test__main__bytes__fmt_value(capfd, fmt, value, expected):
    actual = format_bytes(value, fmt)
    assert actual == expected
