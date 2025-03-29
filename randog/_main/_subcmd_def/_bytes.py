import argparse
import typing as t

import randog.factory
from ..._utils.type import non_negative_int
from ..._processmode import Subcmd
from .. import Args
from ._base import SubcmdDef, add_common_arguments
from .._rnd import construct_random
from ...factory import Factory
from .fmt_wrapper.bytes import BytesWrapper


class SubcmdDefBytes(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Bytes

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        bytes_parser = subparsers.add_parser(
            Subcmd.Bytes.value,
            usage="randog bytes [--length LENGTH] [--fmt FORMAT] [common-options]",
            description="It generates values of type bytes.",
            add_help=False,
        )
        bytes_args_group = bytes_parser.add_argument_group("arguments")
        bytes_args_group.add_argument(
            "--length",
            type=non_negative_int_range,
            default=None,
            metavar="LENGTH",
            help=(
                "the length of generated bytes. "
                "You can specify an integer such as '--length 5' or a range such as "
                "'--length 3:8'."
            ),
        )
        bytes_args_group.add_argument(
            "--fmt",
            dest="format",
            metavar="FORMAT",
            help="if specified, it outputs generated value as string "
            "with the specified format, such as 'b'",
        )
        add_common_arguments(bytes_parser)

        return bytes_parser

    def _validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        # --json is available only if generated value is converted to str
        if (
            args.output_fmt == "json"
            and args.format is None
            and args.binary_fmt is None
        ):
            subparser.error(
                "argument --json can only be used with --fmt or --base64 in bytes mode."
            )

    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        rnd = construct_random(args.seed)
        kwargs = {
            "rnd": rnd,
        }
        length = args.get("length")
        if length is not None:
            if length[0] == length[1]:
                kwargs["length"] = length[0]
            else:
                kwargs["length"] = randog.factory.randint(*length)

        return tuple(), kwargs

    def get_factory_constructor(self) -> t.Callable[..., Factory[bytes]]:
        return lambda *a, **kw: randog.factory.randbytes(*a, **kw).post_process(
            BytesWrapper
        )


# TODO: _str.py と重複する定義なので、統一する
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
