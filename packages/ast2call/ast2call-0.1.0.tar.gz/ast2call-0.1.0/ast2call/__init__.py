#! /usr/bin/env python

import ast
import sys

ignore = ["end_lineno", "col_offset", "end_col_offset"]


def ast2call(node: ast.AST) -> ast.AST:
    if not isinstance(node, ast.AST):
        return ast.Constant(node)

    args = []
    for k, v in node.__dict__.items():
        if k in ignore:
            continue
        if k == "lineno":
            v = None
        if isinstance(v, list):
            args.append(ast.keyword(arg=k, value=ast.List(elts=[ast2call(vs) for vs in v])))
        else:
            args.append(ast.keyword(arg=k, value=ast2call(v)))

    return ast.Call(
        func=ast.Attribute(value=ast.Name('ast'), attr=node.__class__.__name__),
        args=[],
        keywords=args,
    )


def astprint(f: str) -> str:
    return ast.unparse(ast2call(ast.parse(f)))


def main() -> int:
    if len(sys.argv) != 2:
        return 1

    with open(sys.argv[1], 'r') as in_f:
        data = in_f.read()

    print(astprint(data))
    return 0


if __name__ == '__main__':
    sys.exit(main())
