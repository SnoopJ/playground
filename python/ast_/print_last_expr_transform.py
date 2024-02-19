import ast


class LastExprPrintTransformer(ast.NodeVisitor):
    """A helper class for finding `print()` and storing the last `Expr` in an AST"""
    def __init__(self):
        self.print_seen = False

    def visit_Expr(self, node):
        self.lastexpr = node

        if isinstance(node.value, ast.Call) and getattr(node.value.func, "id", "") == "print":
            self.print_seen = True


def wrap_node_print(node: ast.Expr) -> None:
    """Helper to transform an `Expr` into the equivalent form wrapped in `print()`"""

    val = node.value
    # NOTE: the below is being pretty lazy about column offsets, pretending that the
    # print() is basically not present. The Right Way™ to do this is to add an additional
    # offset to the old node's column offsets. The main side effect of this is that error
    # reports that refer to a particular location in a line will be wrong if a print() was added to that line
    node.value = ast.Call(
        lineno=node.lineno,
        col_offset=node.lineno,
        end_lineno=node.end_lineno,
        end_col_offset=node.end_col_offset,
        func=ast.Name(
            lineno=node.lineno,
            col_offset=-1,
            end_lineno=node.end_lineno,
            end_col_offset=-1,
            id='print',
            ctx=ast.Load(),
        ),
        args=[val],
        keywords=[],
    )



def maybe_print_last(src: str) -> str:
    """Wrap a `print()` around the last expression in the given source code, if no other `print()` is present"""
    module = ast.parse(src)

    lept = LastExprPrintTransformer()

    new_module = lept.visit(module)
    if not lept.print_seen:
        wrap_node_print(lept.lastexpr)

    new_src = ast.unparse(module)
    return new_src


if __name__ == "__main__":
    TEST_PROGRAMS = [
        "1 + 1",
        "1 + 1\nprint(42)",
    ]

    for src in TEST_PROGRAMS:
        print("Input source:\n=============")
        print(src)

        print("\nOutput source:\n=============")
        print(maybe_print_last(src))
