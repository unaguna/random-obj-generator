import argparse
import typing as t
from decimal import Decimal

import randog.factory
from ..._utils.type import decimal, non_negative_int, probability
from ..._processmode import Subcmd
from .. import Args
from ._base import SubcmdDef, add_common_arguments
from .._rnd import construct_random
from ...factory import Factory


class SubcmdDefDecimal(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Decimal

    def generate_bytes_only_with_pickle(self) -> bool:
        return True

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        decimal_parser = subparsers.add_parser(
            Subcmd.Decimal.value,
            usage=(
                "randog decimal [MINIMUM MAXIMUM] "
                "[--decimal-len DECIMAL_LENGTH] [--p-inf PROB_P_INF] "
                "[--n-inf PROB_N_INF] [--nan PROB_NAN] [--exp-uniform] [--fmt FORMAT] "
                "[common-options]"
            ),
            description="It generates values of type decimal.Decimal.",
            add_help=False,
        )
        decimal_args_group = decimal_parser.add_argument_group("arguments")
        decimal_args_group.add_argument(
            "minimum",
            type=decimal,
            nargs="?",
            metavar="MINIMUM",
            help=(
                "the minimum value. "
                "If not specified, the behavior is left to the specification of "
                "randog.factory.randdecimal."
            ),
        )
        decimal_args_group.add_argument(
            "maximum",
            type=decimal,
            nargs="?",
            metavar="MAXIMUM",
            help=(
                "the maximum value. "
                "If not specified, the behavior is left to the specification of "
                "randog.factory.randdecimal."
            ),
        )
        decimal_args_group.add_argument(
            "--decimal-len",
            type=non_negative_int,
            default=None,
            metavar="DECIMAL_LENGTH",
            help="the length of decimal part of generated values",
        )
        decimal_args_group.add_argument(
            "--p-inf",
            type=probability,
            default=0.0,
            metavar="PROB_P_INF",
            help="the probability of positive infinity; default=0.0",
        )
        decimal_args_group.add_argument(
            "--n-inf",
            type=probability,
            default=0.0,
            metavar="PROB_N_INF",
            help="the probability of negative infinity; default=0.0",
        )
        decimal_args_group.add_argument(
            "--nan",
            type=probability,
            default=0.0,
            metavar="PROB_NAN",
            help="the probability of NaN; default=0.0",
        )
        decimal_args_group.add_argument(
            "--exp-uniform",
            dest="distribution",
            action="store_const",
            const="exp_uniform",
            help=(
                "if specified, the distribution of digits (log with a base of 10) is "
                "uniform."
            ),
        )
        decimal_args_group.add_argument(
            "--fmt",
            dest="format",
            metavar="FORMAT",
            help="if specified, it outputs generated value with the specified format, "
            "such as '011.2f'",
        )
        add_common_arguments(decimal_parser)

        return decimal_parser

    def _validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        iargs, kwargs = self.build_args(args)
        minimum, maximum = iargs
        nan = kwargs["nan"]
        p_inf = kwargs["p_inf"]
        n_inf = kwargs["n_inf"]

        if minimum is not None and maximum is not None and minimum > maximum:
            subparser.error("arguments must satisfy MINIMUM <= MAXIMUM")

        if nan + p_inf + n_inf > 1.0:
            subparser.error(
                "arguments must satisfy that PROB_P_INF + PROB_N_INF + PROB_NAN <= 1.0"
            )

    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        rnd = construct_random(args.seed)
        return (args.get("minimum"), args.get("maximum")), {
            "decimal_len": args.get("decimal_len"),
            "p_inf": args.get("p_inf"),
            "n_inf": args.get("n_inf"),
            "nan": args.get("nan"),
            "distribution": args.get("distribution"),
            "rnd": rnd,
        }

    def get_factory_constructor(self) -> t.Callable[..., Factory[Decimal]]:
        return randog.factory.randdecimal
