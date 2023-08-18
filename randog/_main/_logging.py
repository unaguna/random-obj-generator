import logging

from .._logging import get_logger as _get_logger

logger = _get_logger("cmd")


class CmdLogFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = record.levelname.lower()
        return logging.Formatter.format(self, record)
