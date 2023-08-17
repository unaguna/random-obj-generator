import logging


def get_logger(name: str = "") -> logging.Logger:
    if name is None or len(name) == 0:
        return logging.getLogger("randog")
    else:
        return logging.getLogger(f"randog.{name}")
