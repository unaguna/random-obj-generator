import csv
import json
import sys
import typing as t

import randog.factory
from ._utils.nullsafe import dfor
from .factory import FactoryDef
from ._main import Args, Subcmd, get_subcmd_def


def _build_factories(args: Args) -> t.Iterator[randog.factory.Factory]:
    subcmd_def = get_subcmd_def(args.sub_cmd)

    if args.sub_cmd == Subcmd.Byfile:
        for filepath in args.factories:
            if filepath == "-":
                factory_def = randog.factory.from_pyfile(sys.stdin, full_response=True)
            else:
                factory_def = randog.factory.from_pyfile(filepath, full_response=True)
            factory = factory_def.factory

            post_process = _gen_post_function(args, factory_def)
            if post_process is not None:
                factory = factory.post_process(post_process)

            yield factory
    else:
        iargs, kwargs = subcmd_def.build_args(args)
        yield subcmd_def.get_factory_constructor()(*iargs, **kwargs)


def _get_csv_field(pre_value: t.Mapping, col) -> t.Any:
    if isinstance(col, t.Callable):
        return col(pre_value)
    else:
        return pre_value.get(col)


def _gen_post_function(
    args: Args, factory_def: FactoryDef
) -> t.Optional[t.Callable[[t.Any], t.Any]]:
    """args に応じて、factory_def.factory に適用する post_process 関数を作成する。"""

    if args.get("csv", False):
        if factory_def.csv_columns is not None:

            def _post_function(pre_value):
                if isinstance(pre_value, t.Mapping):
                    return [
                        _get_csv_field(pre_value, col)
                        for col in factory_def.csv_columns
                    ]
                elif isinstance(pre_value, t.Sequence):
                    return pre_value
                else:
                    # TODO: 警告
                    return [pre_value]

        else:

            def _post_function(pre_value):
                if isinstance(pre_value, t.Mapping):
                    # TODO: 警告
                    return list(pre_value.values())
                elif isinstance(pre_value, t.Sequence) and not isinstance(
                    pre_value, str
                ):
                    return pre_value
                else:
                    # TODO: 警告
                    return [pre_value]

        return _post_function
    else:
        return None


class _DummyIO:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def _open_output_fp_only(args: Args) -> t.Union[_DummyIO, t.TextIO]:
    if args.output_path is None or args.multiple_output_path:
        return _DummyIO()
    else:
        options = {
            "mode": "wt",
        }
        if args.get("csv", False):
            options["newline"] = ""
        return open(args.output_path, **options)


def _open_output_fp_numbered(args: Args, number: int) -> t.Union[_DummyIO, t.TextIO]:
    if args.output_path is None or not args.multiple_output_path:
        return _DummyIO()
    else:
        options = {
            "mode": "wt",
        }
        if args.get("csv", False):
            options["newline"] = ""
        return open(args.output_path_for(number), **options)


def _output_generated(generated: t.Any, fp: t.TextIO, args: Args):
    if args.output_fmt == "repr":
        print(repr(generated), file=fp)
    elif args.output_fmt == "json":
        json.dump(generated, fp, default=_json_default(args))
        fp.write("\n")
    else:
        if args.iso and hasattr(generated, "isoformat"):
            print(generated.isoformat(), file=fp)
        elif args.format:
            print(generated.__format__(args.format), file=fp)
        else:
            print(generated, file=fp)


def _json_default(args: Args):
    if args.iso:
        return lambda v: v.isoformat()
    elif args.format:
        return lambda v: v.__format__(args.format)
    else:
        return str


def _output_generated_csv(generated: t.Sequence[t.Sequence[t.Any]], fp: t.TextIO):
    csv_writer = csv.writer(fp, lineterminator="\n")
    csv_writer.writerows(generated)


def main():
    args = Args(sys.argv)

    with _open_output_fp_only(args) as fp_only:
        index = 0
        for factory in _build_factories(args):
            for r_index in range(args.repeat):
                # args.list の指定がある場合、リストを生成する。
                # また、CSV出力の場合は args.list の指定がなくとも、要素数1のリストを生成する。
                if args.list is not None or args.get("csv", False):
                    args_list = dfor(args.list, 1)
                    generated = list(factory.iter(args_list))
                # args.list の指定が無い場合、普通に1つ生成する。
                else:
                    generated = factory.next()

                with _open_output_fp_numbered(args, index) as fp_numbered:
                    if not isinstance(fp_numbered, _DummyIO):
                        fp = fp_numbered
                    elif not isinstance(fp_only, _DummyIO):
                        fp = fp_only
                    else:
                        fp = sys.stdout

                    if args.get("csv", False):
                        _output_generated_csv(generated, fp)
                    else:
                        _output_generated(generated, fp, args=args)

                index += 1


if __name__ == "__main__":
    main()
