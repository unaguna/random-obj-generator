from ._cmn import analyze_standard_fmt, StandardFormatSpec, apply_format_char

_BINARY_STR = tuple(format(v, "08b") for v in range(0, 256))
_HEX_UPPER_STR = tuple(format(v, "02X") for v in range(0, 256))
_HEX_LOWER_STR = tuple(format(v, "02x") for v in range(0, 256))

_BYTE_STR_MAPS = {
    "b": _BINARY_STR,
    "X": _HEX_UPPER_STR,
    "x": _HEX_LOWER_STR,
}

_STR_LENGTH_OF_BYTE = {
    "b": 8,
    "X": 2,
    "x": 2,
}


def format_bytes(value: bytes, fmt: str) -> str:
    """custom formatter of bytes objects"""
    try:
        fmt_ana = analyze_standard_fmt(fmt)
        _validate(fmt_ana)

        if fmt_ana.s_type in (None, "s"):
            return format(str(value), fmt)
        elif fmt_ana.s_type == "c":
            fmt_ana.s_type = "s"
            return format(str(value)[2:-1], str(fmt_ana))
    except ValueError as e:
        raise ValueError(
            f"Invalid format specifier '{fmt}' for object of type 'bytes'"
        ) from e

    pre_str = _get_pre_str(value, fmt_ana)
    return apply_format_char(
        pre_str, fmt_ana, default_type="s", default_align="<", zero_padding_align="<"
    )


def _validate(fmt_ana: StandardFormatSpec):
    if fmt_ana.align == "=":
        raise ValueError()
    if fmt_ana.sign is not None:
        raise ValueError()
    if fmt_ana.s_type is not None and fmt_ana.s_type not in "bcdXxs":
        raise ValueError()
    if fmt_ana.grouping_option == ",":
        raise ValueError()
    if fmt_ana.fill not in (None, "0") and fmt_ana.zero:
        raise ValueError()


def _get_pre_str(value: bytes, fmt_ana: StandardFormatSpec) -> str:
    try:
        byte_str_map = _BYTE_STR_MAPS[fmt_ana.s_type]
    except KeyError:
        raise ValueError()

    return "".join(byte_str_map[b] for b in value)
