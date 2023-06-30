import datetime
import json
import sys
import typing as t

import randog.factory
from ._main import Args, Subcmd, get_subcmd_def


def _build_factories(args: Args) -> t.Iterator[randog.factory.Factory]:
    subcmd_def = get_subcmd_def(args.sub_cmd)

    if args.sub_cmd == Subcmd.Byfile:
        for filepath in args.factories:
            if filepath == "-":
                yield randog.factory.from_pyfile(sys.stdin)
            else:
                yield randog.factory.from_pyfile(filepath)
    else:
        iargs, kwargs = subcmd_def.build_args(args)
        yield subcmd_def.get_factory_constructor()(*iargs, **kwargs)


class _DummyIO:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def _open_output_fp_only(args: Args) -> t.Union[_DummyIO, t.TextIO]:
    if args.output_path is None or args.multiple_output_path:
        return _DummyIO()
    else:
        return open(args.output_path, mode="wt")


def _open_output_fp_numbered(args: Args, number: int) -> t.Union[_DummyIO, t.TextIO]:
    if args.output_path is None or not args.multiple_output_path:
        return _DummyIO()
    else:
        return open(args.output_path_for(number), mode="wt")


def _output_generated(generated: t.Any, fp: t.TextIO, args: Args):
    if args.output_fmt == "repr":
        print(repr(generated), file=fp)
    elif args.output_fmt == "json":
        json.dump(generated, fp, default=_json_default(args))
        fp.write("\n")
    else:
        if args.iso and isinstance(generated, datetime.date):
            print(generated.isoformat(), file=fp)
        elif args.date_fmt and isinstance(generated, datetime.date):
            print(generated.strftime(args.date_fmt), file=fp)
        else:
            print(generated, file=fp)


def _json_default(args: Args):
    if args.iso:
        return lambda v: v.isoformat()
    elif args.date_fmt:
        return lambda v: v.strftime(args.date_fmt)
    else:
        return str


def main():
    args = Args(sys.argv)

    with _open_output_fp_only(args) as fp_only:
        index = 0
        for factory in _build_factories(args):
            for r_index in range(args.repeat):
                if args.list is None:
                    generated = factory.next()
                else:
                    generated = list(factory.iter(args.list))

                with _open_output_fp_numbered(args, index) as fp_numbered:
                    if not isinstance(fp_numbered, _DummyIO):
                        fp = fp_numbered
                    elif not isinstance(fp_only, _DummyIO):
                        fp = fp_only
                    else:
                        fp = sys.stdout

                    _output_generated(generated, fp, args=args)

                index += 1


if __name__ == "__main__":
    main()
