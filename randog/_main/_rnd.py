import random
import typing as t

from ._logging import logger


def construct_random(seed: t.Any) -> random.Random:
    rnd = random.Random(seed)
    logger.debug(f"seed: {seed}")
    return rnd
