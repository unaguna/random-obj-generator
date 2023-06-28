def positive_int(value):
    value_int = int(value)
    if value_int <= 0:
        raise ValueError("must be positive")
    return value_int


def non_negative_int(value):
    value_int = int(value)
    if value_int < 0:
        raise ValueError("must be non-negative")
    return value_int


def probability(value):
    value_float = float(value)
    if 0 <= value_float <= 1:
        return value_float
    else:
        raise ValueError("must be in the range [0, 1]")
