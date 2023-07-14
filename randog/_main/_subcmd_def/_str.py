import argparse
import typing as t

import randog.factory
from ..._utils.type import non_negative_int
from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments


class SubcmdDefString(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.String

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        str_parser = subparsers.add_parser(
            Subcmd.String.value,
            usage="python -m randog str [--length LENGTH] [--charset CHARSET] [common-options]",
            description="It generates values of type str.",
            add_help=False,
        )
        str_args_group = str_parser.add_argument_group("arguments")
        str_args_group.add_argument(
            "--length",
            type=non_negative_int_range,
            default=None,
            metavar="LENGTH",
            help="the length of generated strings. "
            "You can specify an integer such as '--length 5' or a range such as '--length 3:8'.",
        )
        str_args_group.add_argument(
            "--charset",
            type=str,
            default=None,
            metavar="CHARSET",
            help="the characters which contained by generated strings",
        )
        add_common_arguments(str_parser)

        return str_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        pass

    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        kwargs = {"charset": args.get("charset")}
        length = args.get("length")
        if length is not None:
            if length[0] == length[1]:
                kwargs["length"] = length[0]
            else:
                kwargs["length"] = randog.factory.randint(*length)

        return tuple(), kwargs

    def get_factory_constructor(self) -> t.Callable:
        return randog.factory.randstr


def non_negative_int_range(value: str) -> t.Tuple[int, int]:
    if ":" in value:
        value_s_str, value_e_str = value.split(":", 1)
        value_s = non_negative_int(value_s_str)
        value_e = non_negative_int(value_e_str)

        if value_s > value_e:
            raise ValueError("range must not be empty")

    else:
        value_s = value_e = non_negative_int(value)

    return value_s, value_e
