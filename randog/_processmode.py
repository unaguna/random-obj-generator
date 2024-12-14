from enum import Enum
import os
import typing as t

ENV_PROCESS_MODE = "RANDOG_PROCESS_MODE"


class Subcmd(Enum):
    Byfile = "byfile"
    Bool = "bool"
    Int = "int"
    Float = "float"
    String = "str"
    Decimal = "decimal"
    Datetime = "datetime"
    Date = "date"
    Time = "time"
    Timedelta = "timedelta"


def set_process_mode(mode: t.Optional[Subcmd]):
    os.environ[ENV_PROCESS_MODE] = str(mode.value)


def get_process_mode() -> Subcmd:
    mode_str = os.environ[ENV_PROCESS_MODE]
    return Subcmd(mode_str)
