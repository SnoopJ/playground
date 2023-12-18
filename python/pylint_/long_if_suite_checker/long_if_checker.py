from __future__ import annotations
import astroid
from astroid import nodes
from typing import TYPE_CHECKING, Optional

from pylint.checkers import BaseChecker
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter


Extent = tuple[nodes.NodeNG, int, int]

class LongIfChecker(BaseChecker):

    name = "long-if-clause"
    msgs = {
        # NOTE: pylint code prefixes 51-99 are reserved for external checkers, see:
        # https://github.com/pylint-dev/pylint/blob/v3.0.3/pylint/checkers/__init__.py#L37
        # This prefix was selected randomly
        "W8900": (
            "overlong conditional body",
            "if-body-too-long",
            "If/elif/else clause should be shorter",
        ),
    }
    options = (
        (
            "max-if-clause-length",
            {
                "default": 50,
                "type": "int",
                "metavar": "<int>",
                "help": "Maximum length of an if/elif/else clause",
            },
        ),
        (
            "check-pure-if-length",
            {
                "default": True,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Check the length of if statments without elif/else",
            },
        ),
    )

    def _elif_or_else_extents(self, node: nodes.If) -> list[Extent]:
        result = []
        start = node.fromlineno

        n = node.orelse[0]
        stop = n.fromlineno

        result.append((node, start, stop))

        if not isinstance(n, nodes.If):
            # edge case: `else` clause
            # NOTE: astroid has quirky counting for `else`, so we're
            # effectively off-by-one here
            result.append((n, stop, n.end_lineno))

        # otherwise, `node` is followed by an `elif`, which is an instance of
        # `nodes.If`, and we'll deal with its contents when we visit it later
        return result

    def _clause_extents(self, node: nodes.If) -> list[Extent]:
        if not node.orelse:
            # no `elif, else` clause, end_lineno is the true end of this clause
            start = node.fromlineno
            stop = node.end_lineno
            result = [(node, node.fromlineno, node.end_lineno)]
        else:
            # there is an `elif` or `else` clause to deal with
            result = self._elif_or_else_extents(node)

        return result

    def visit_if(self, node: nodes.If) -> None:
        if not self.linter.config.check_pure_if_length and not node.orelse:
            # user has opted out of checking `if` clauses without an `elif/else`
            return

        for (n, start, stop) in self._clause_extents(node):
            if (stop - start) > self.linter.config.max_if_clause_length:
                self.add_message(
                    "if-body-too-long",
                    node=n,
                    confidence=HIGH,
                )
#         print(f"=== If ===")
#         print(f"{self._clause_extents(node) = }")
#         print("===\n")


def register(linter: "PyLinter") -> None:
    linter.register_checker(LongIfChecker(linter))
