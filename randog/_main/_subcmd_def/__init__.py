import typing as t

from .. import Subcmd
from ._base import SubcmdDef
from ._bool import SubcmdDefBool
from ._byfile import SubcmdDefByfile
from ._datetime import SubcmdDefDatetime
from ._decimal import SubcmdDefDecimal
from ._float import SubcmdDefFloat
from ._int import SubcmdDefInt
from ._str import SubcmdDefString

_subcmd_def_list: t.Sequence[SubcmdDef] = (
    SubcmdDefBool(),
    SubcmdDefByfile(),
    SubcmdDefDatetime(),
    SubcmdDefDecimal(),
    SubcmdDefFloat(),
    SubcmdDefInt(),
    SubcmdDefString(),
)

_subcmd_def_dict: t.Mapping[Subcmd, SubcmdDef] = {
    subcmd_def.cmd(): subcmd_def for subcmd_def in _subcmd_def_list
}


def iter_subcmd_def() -> t.Iterator[SubcmdDef]:
    return iter(_subcmd_def_list)


def get_subcmd_def(subcmd: Subcmd) -> SubcmdDef:
    return _subcmd_def_dict[subcmd]
