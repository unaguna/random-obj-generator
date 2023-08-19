import json
import logging
import logging.config
import os
import typing as t

from .._logging import get_logger as _get_logger

logger = _get_logger("cmd")


class CmdLogFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = record.levelname.lower()
        return logging.Formatter.format(self, record)


def apply_default_logging_config():
    root_logger = logging.getLogger()
    root_logger.setLevel("WARNING")
    root_logger.addHandler(logging.NullHandler())


def apply_stderr_logging_config(level: str):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.formatter = CmdLogFormatter("%(levelname)s: %(message)s")
    root_logger.addHandler(handler)


def apply_logging_config_file(config_file: t.Union[str, os.PathLike]):
    try:
        import yaml

        with open(config_file, mode="rt") as fp:
            config = yaml.load(fp, yaml.Loader)
    except ModuleNotFoundError:
        with open(config_file, mode="rt") as fp:
            config = json.load(fp)

    logging.config.dictConfig(config)
