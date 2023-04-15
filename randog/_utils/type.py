def positive_int(value):
    value_int = int(value)
    if value_int <= 0:
        raise ValueError("must be positive")
    return value_int
