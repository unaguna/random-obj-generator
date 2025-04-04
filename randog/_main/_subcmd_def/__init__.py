import typing as t

from ..._processmode import Subcmd
from ._base import SubcmdDef
from ._bool import SubcmdDefBool
from ._byfile import SubcmdDefByfile
from ._date import SubcmdDefDate
from ._datetime import SubcmdDefDatetime
from ._decimal import SubcmdDefDecimal
from ._dice import SubcmdDefDice
from ._float import SubcmdDefFloat
from ._int import SubcmdDefInt
from ._str import SubcmdDefString
from ._bytes import SubcmdDefBytes
from ._time import SubcmdDefTime
from ._timedelta import SubcmdDefTimedelta
from ._ipv4 import SubcmdDefIPV4

_subcmd_def_list: t.Sequence[SubcmdDef] = (
    SubcmdDefBool(),
    SubcmdDefByfile(),
    SubcmdDefDate(),
    SubcmdDefDatetime(),
    SubcmdDefDecimal(),
    SubcmdDefDice(),
    SubcmdDefFloat(),
    SubcmdDefInt(),
    SubcmdDefString(),
    SubcmdDefBytes(),
    SubcmdDefTime(),
    SubcmdDefTimedelta(),
    SubcmdDefIPV4(),
)

_subcmd_def_dict: t.Mapping[Subcmd, SubcmdDef] = {
    subcmd_def.cmd(): subcmd_def for subcmd_def in _subcmd_def_list
}


def iter_subcmd_def() -> t.Iterator[SubcmdDef]:
    return iter(_subcmd_def_list)


def get_subcmd_def(subcmd: Subcmd) -> SubcmdDef:
    return _subcmd_def_dict[subcmd]
