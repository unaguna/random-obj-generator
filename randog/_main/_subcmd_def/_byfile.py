import argparse
import typing as t

from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments


class SubcmdDefByfile(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Byfile

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        byfile_parser = subparsers.add_parser(
            Subcmd.Byfile.value,
            usage="python -m randog byfile FACTORY_PATH [FACTORY_PATH ...] [--csv] [common-options]",
            description="It generates values according to factory definition files.",
            add_help=False,
        )
        byfile_args_group = byfile_parser.add_argument_group("arguments")
        byfile_args_group.add_argument(
            "factories",
            nargs="+",
            metavar="FACTORY_PATH",
            help="path of factory definition files",
        )
        byfile_args_group.add_argument(
            "--csv",
            action="store_true",
            help="if specified, it outputs generated object as CSV. "
            "When using this option, it is recommended to use a factory that generates dictionaries and "
            "to define CSV_COLUMNS in the definition file to specify the fields of the CSV.",
        )
        add_common_arguments(byfile_parser)

        return byfile_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        pass

    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        pass

    def get_factory_constructor(self) -> t.Callable:
        pass
