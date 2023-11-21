import argparse
from pathlib import Path

import libcst as cst


parser = argparse.ArgumentParser()
parser.add_argument("source_files", nargs="+")


class SourceAttributeTransformer(cst.CSTTransformer):
    def _append_source(self, node):
        src = cst.Module([node]).code
        new_stmt = cst.parse_statement(f"{node.name.value}.__acme_source__ = {src!r}")
        return cst.FlattenSentinel([node, cst.Newline(), new_stmt, cst.Newline()])

    def leave_ClassDef(self, original_node, updated_node):
        return self._append_source(updated_node)

    def leave_FunctionDef(self, original_node, updated_node):
        return self._append_source(updated_node)


def transform(fn: str) -> str:
    src = Path(fn).read_text()
    tree = cst.parse_module(src)
    visitor = SourceAttributeTransformer()
    modified_tree = tree.visit(visitor)
    return modified_tree.code


def main():
    args = parser.parse_args()

    for fn in args.source_files:
        print(transform(fn))


if __name__ == "__main__":
    main()
