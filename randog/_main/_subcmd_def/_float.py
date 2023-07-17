import argparse
import typing as t

import randog.factory
from ..._utils.type import probability
from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments


class SubcmdDefFloat(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Float

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        float_parser = subparsers.add_parser(
            Subcmd.Float.value,
            usage="python -m randog float [MINIMUM MAXIMUM] [--p-inf PROB_P_INF] [--n-inf PROB_N_INF] [--nan PROB_NAN] "
            "[common-options]",
            description="It generates values of type float.",
            add_help=False,
        )
        float_args_group = float_parser.add_argument_group("arguments")
        float_args_group.add_argument(
            "minimum",
            type=float,
            nargs="?",
            metavar="MINIMUM",
            help="the minimum value. "
            "If not specified, the behavior is left to the specification of randog.factory.randfloat.",
        )
        float_args_group.add_argument(
            "maximum",
            type=float,
            nargs="?",
            metavar="MAXIMUM",
            help="the maximum value. "
            "If not specified, the behavior is left to the specification of randog.factory.randfloat.",
        )
        float_args_group.add_argument(
            "--p-inf",
            type=probability,
            default=0.0,
            metavar="PROB_P_INF",
            help="the probability of positive infinity; default=0.0",
        )
        float_args_group.add_argument(
            "--n-inf",
            type=probability,
            default=0.0,
            metavar="PROB_N_INF",
            help="the probability of negative infinity; default=0.0",
        )
        float_args_group.add_argument(
            "--nan",
            type=probability,
            default=0.0,
            metavar="PROB_NAN",
            help="the probability of NaN; default=0.0",
        )
        add_common_arguments(float_parser)

        return float_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        if args.sub_cmd != Subcmd.Float:
            return

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
        return (args.get("minimum"), args.get("maximum")), {
            "p_inf": args.get("p_inf"),
            "n_inf": args.get("n_inf"),
            "nan": args.get("nan"),
        }

    def get_factory_constructor(self) -> t.Callable:
        return randog.factory.randfloat
