import ast


class LastExprPrintTransformer(ast.NodeTransformer):
    """A helper class for finding `print()` and storing the last `Expr` in an AST"""
    def __init__(self):
        self.lastexpr = None
        self.print_seen = False

    def visit_Expr(self, node):
        self.lastexpr = node

        if isinstance(node.value, ast.Call) and getattr(node.value.func, "id", "") == "print":
            self.print_seen = True

        return node


def wrap_node_print(node: ast.Expr) -> None:
    """Helper to transform an `Expr` into the equivalent form wrapped in `print(repr(…))`"""

    val = node.value
    # NOTE:the column offsets here are pretty wrong, but the result of this helper is passed pretty much
    # directly into `ast.unparse()` which doesn't use the column offset information anyway. When the transformed
    # program is run through the WASI CPython's parser, the column offsets will be *correct*, so despite the mild
    # evil on display here, errors reported by the bot include correct column indicators
    repr_node = ast.Call(
        lineno=node.lineno,
        col_offset=-1,
        end_lineno=node.end_lineno,
        end_col_offset=-1,
        func=ast.Name(
            lineno=node.lineno,
            col_offset=-1,
            end_lineno=node.end_lineno,
            end_col_offset=-1,
            id='repr',
            ctx=ast.Load(),
        ),
        args=[val],
        keywords=[],
    )

    node.value = ast.Call(
        lineno=node.lineno,
        col_offset=-1,
        end_lineno=node.end_lineno,
        end_col_offset=-1,
        func=ast.Name(
            lineno=node.lineno,
            col_offset=-1,
            end_lineno=node.end_lineno,
            end_col_offset=-1,
            id='print',
            ctx=ast.Load(),
        ),
        args=[repr_node],
        keywords=[ast.keyword(arg="end", value=ast.Constant(""))],
    )



def maybe_print_last(src: str) -> str:
    """Wrap a `print(repr(…))` around the last expression in the given source code, if no other `print()` is present"""
    module = ast.parse(src)

    lept = LastExprPrintTransformer()

    new_module = lept.visit(module)
    if not lept.lastexpr:
        # edge case: there is no last expression!
        return src

    if not lept.print_seen:
        wrap_node_print(lept.lastexpr)

    new_src = ast.unparse(module)
    return new_src


if __name__ == "__main__":
    TEST_PROGRAMS = [
        "1 + 1",
        "1 + 1\nprint(42)",
        "import os",
    ]

    for src in TEST_PROGRAMS:
        print("Input source:\n==============")
        print(src)

        print("\nOutput source:\n==============")
        print(maybe_print_last(src))
        print("\n--------------\n")
