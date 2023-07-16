import argparse
import typing as t

import randog.factory
from ..._utils.type import time
from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments


class SubcmdDefTime(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Time

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        time_parser = subparsers.add_parser(
            Subcmd.Time.value,
            usage="python -m randog time [MINIMUM MAXIMUM] [--iso | --fmt FORMAT] [common-options]",
            description="It generates values of type datetime.time.",
            add_help=False,
        )
        time_args_group = time_parser.add_argument_group("arguments")
        time_args_group.add_argument(
            "minimum",
            type=time,
            nargs="?",
            metavar="MINIMUM",
            help="the minimum value with the ISO-8601 format. "
            "If not specified, the behavior is left to the specification of randog.factory.randtime.",
        )
        time_args_group.add_argument(
            "maximum",
            type=time,
            nargs="?",
            metavar="MAXIMUM",
            help="the maximum value with the ISO-8601 format. "
            "If not specified, the behavior is left to the specification of randog.factory.randtime.",
        )
        group_date_fmt = time_args_group.add_mutually_exclusive_group()
        group_date_fmt.add_argument(
            "--iso",
            action="store_true",
            help="if specified, it outputs generated object with ISO-8601 format"
            "Since the str of datetime.time is identical to the iso-8601 format, this option is meaningless.",
        )
        group_date_fmt.add_argument(
            "--fmt",
            dest="format",
            metavar="FORMAT",
            help="if specified, it outputs generated object with the specified format, such as '%%H:%%M:%%S.%%f'",
        )
        add_common_arguments(time_parser)

        return time_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        if args.sub_cmd != Subcmd.Time:
            return

        if args.output_fmt == "repr" and args.iso:
            subparser.error("argument --iso: not allowed with argument --repr")
        elif args.output_fmt == "repr" and args.format:
            subparser.error("argument --fmt: not allowed with argument --repr")

    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        return (args.get("minimum"), args.get("maximum")), {}

    def get_factory_constructor(self) -> t.Callable:
        return randog.factory.randtime
