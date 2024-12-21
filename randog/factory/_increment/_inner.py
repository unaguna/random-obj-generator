import typing as t

from .._logging import logger


def _increment(initial_value, maximum, step, resume_value) -> t.Iterator:
    next_value = initial_value
    while True:
        yield next_value
        next_value += step

        if next_value > maximum:
            logger.debug(
                "increment() has reached its maximum value and resumes "
                f"from {resume_value}"
            )
            next_value = resume_value
