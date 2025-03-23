from collections import defaultdict
import math
import re
import typing as t

from randog._utils.nullsafe import dforc

STANDARD_FORMAT_SPECIFIER_REGEX = re.compile(
    r"(?:(?P<fill>.+)?(?P<align>[><=^]))?"
    r"(?P<sign>[-+ ])?"
    r"(?P<n_sign>#)?"
    r"(?P<zero>0)?"
    r"(?P<width>[0-9]+)?"
    r"(?P<grouping_option>[_,])?"
    r"(?:\.(?P<precision>[0-9]+))?"
    r"(?P<type>[bcdeEfFgGnosxX%])?"
)

S_TYPE = t.Literal[
    "b", "c", "d", "e", "E", "f", "F", "g", "G", "n", "o", "s", "x", "X", "%"
]
Align = t.Literal["<", ">", "=", "^"]

_SEP_LENGTH = defaultdict(
    lambda: 3,
    {
        "b": 4,
        "o": 4,
        "X": 4,
        "x": 4,
    },
)
"""length of groups separated by '_' or ','"""

_DIGIT_PREFIX: t.Mapping[t.Optional[str], str] = defaultdict(
    lambda: "",
    {
        "b": "0b",
        "o": "0o",
        "X": "0X",
        "x": "0x",
    },
)


class StandardFormatSpec:
    """the format by Standard Format Specification

    ref:
    https://docs.python.org/3.8/library/string.html#format-specification-mini-language
    """

    fill: t.Optional[str]
    align: t.Optional[t.Literal["<", ">", "=", "^"]]
    sign: t.Optional[t.Literal["+", "-", " "]]
    n_sign: bool
    zero: bool
    width: t.Optional[int]
    grouping_option: t.Optional[t.Literal["_", ","]]
    precision: t.Optional[int]
    s_type: t.Optional[S_TYPE]

    def __init__(self, group_dict: t.Dict[str, t.Optional[str]]):
        self.fill = group_dict["fill"]
        self.align = group_dict["align"]
        self.sign = group_dict["sign"]
        self.n_sign = group_dict["n_sign"] is not None
        self.zero = group_dict["zero"] is not None
        self.width = dforc(int, group_dict["width"])
        self.grouping_option = group_dict["grouping_option"]
        self.precision = dforc(int, group_dict["precision"])
        self.s_type = group_dict["type"]

    def __str__(self):
        parts: t.Sequence[t.Optional[str]] = [
            self.fill if self.align is not None else None,
            self.align,
            self.sign,
            "#" if self.n_sign else None,
            "0" if self.zero else None,
            dforc(str, self.width),
            self.grouping_option,
            f".{self.precision}" if self.precision is not None else None,
            self.s_type,
        ]
        return "".join((p for p in parts if p is not None))

    def get_fill_char(self) -> str:
        """returns a char for padding"""
        if self.fill is not None:
            return self.fill
        if self.zero:
            return "0"
        else:
            return " "

    def get_align(self, default: Align = "<") -> Align:
        if self.align is not None:
            return self.align
        if self.zero:
            return "="
        else:
            return default

    def get_align_for_sep(self, default: Align = "<") -> t.Literal["<", ">"]:
        """the align direction for separating by separator such as '_'"""
        align = self.get_align(default)
        if align in "<>":
            return align
        elif default in "<>":
            return default
        else:
            return "<"

    def get_s_type(self, default: S_TYPE = "s") -> S_TYPE:
        if self.s_type is not None:
            return self.s_type
        else:
            return default

    def get_min_width(self) -> int:
        if self.width is not None:
            return self.width
        else:
            return 0

    def get_grp_sep(self) -> str:
        if self.grouping_option is not None:
            return self.grouping_option
        else:
            return ""

    def get_digit_prefix(self) -> str:
        """Returns the prefix such as '0x'."""
        return _DIGIT_PREFIX[self.s_type] if self.n_sign else ""


def analyze_standard_fmt(fmt: str) -> StandardFormatSpec:
    match = re.fullmatch(STANDARD_FORMAT_SPECIFIER_REGEX, fmt)
    if match is None:
        raise ValueError("illegal format specifier")

    return StandardFormatSpec(match.groupdict())


def apply_format_char(
    pre_str: str,
    fmt_ana: StandardFormatSpec,
    *,
    default_type: S_TYPE = "s",
    default_align: t.Literal["<", ">", "^"] = "<",
    zero_padding_align: t.Literal["<", ">"] = ">",
) -> str:
    """

    Parameters
    ----------
    pre_str
        string expression of formatted value
    fmt_ana
        analyzed format
    default_type
    default_align
    zero_padding_align
        align in align="=" and fill="0". If ">", left-padding such as '000123'.
        If "<", right-padding such as '123000'.

    Returns
    -------
        formatted value with group separator and padding
    """
    s_type = fmt_ana.get_s_type(default_type)
    min_width = fmt_ana.get_min_width()
    # min_widthに到達するために埋める際に使う文字
    fill_char = fmt_ana.get_fill_char()
    # 1グループあたりの長さ（セパレータを除く）
    grp_len = _SEP_LENGTH[s_type]
    # グループのセパレータ
    grp_sep = fmt_ana.get_grp_sep()
    # グループのセパレータの長さ
    sep_len = len(grp_sep)
    # 何進数かを表す接頭辞
    dig_prefix = fmt_ana.get_digit_prefix()
    # 何進数かを表す接頭辞の長さ
    dig_prefix_len = len(dig_prefix)

    # 0埋め箇所も込みでグループごとに _ や , で区切る場合
    if fill_char == "0" and fmt_ana.get_align() == "=":
        # min_width を満たすために必要なグループ数 (セパレータとprefixは除く)
        min_group_num = math.ceil(
            (min_width + sep_len - dig_prefix_len) / (grp_len + sep_len)
        )
        # min_width を満たすために必要な桁数 (セパレータとprefixは除く)
        min_len_exclude_sep_prefix = (
            min_width - dig_prefix_len - (min_group_num - 1) * sep_len
        )

        filled_str = fill(
            pre_str, fill_char, min_len_exclude_sep_prefix, zero_padding_align
        )
        separated_filled_str = separate_grp(
            filled_str, grp_sep, grp_len, align=zero_padding_align
        )
        separated_filled_str = dig_prefix + separated_filled_str
    # グループごとに _ や , で区切った後に fill する場合
    else:
        separated_str = separate_grp(
            pre_str, grp_sep, grp_len, align=fmt_ana.get_align_for_sep(default_align)
        )
        separated_filled_str = fill(
            dig_prefix + separated_str,
            fill_char,
            min_width,
            fmt_ana.get_align(default_align),
        )

    return separated_filled_str


def separate_grp(
    value: str, sep: str, grp_len: int, align: t.Literal["<", ">"] = ">"
) -> str:
    if align == "<":
        return sep.join(value[i : i + grp_len] for i in range(0, len(value), grp_len))
    else:
        dummy_padding_len = -len(value) % grp_len
        dummy_val = " " * dummy_padding_len + value
        dummy_result = separate_grp(dummy_val, sep, grp_len, align="<")
        return dummy_result[dummy_padding_len:]


def fill(
    value: str,
    fill_char: str,
    min_width: int,
    align: Align,
    default_align: t.Literal["<", ">", "^"] = "<",
) -> str:
    if align == "=":
        align = default_align

    fill_len = min_width - len(value)

    if len(value) >= min_width:
        return value
    elif align == ">":
        return fill_char * fill_len + value
    elif align == "<":
        return value + fill_char * fill_len
    else:
        fill_len_l = fill_len // 2
        fill_len_r = fill_len - fill_len_l
        return fill_char * fill_len_l + value + fill_char * fill_len_r
