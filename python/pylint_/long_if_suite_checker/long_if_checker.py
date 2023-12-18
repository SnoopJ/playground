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

    name = "long-if-suite"
    msgs = {
        # NOTE: pylint code prefixes 51-99 are reserved for external checkers, see:
        # https://github.com/pylint-dev/pylint/blob/v3.0.3/pylint/checkers/__init__.py#L37
        # This prefix was selected randomly
        "W8900": (
            "overlong conditional body",
            "if-body-too-long",
            "If/elif/else suite should be shorter",
        ),
    }
    options = (
        (
            "max-if-suite-length",
            {
                "default": 50,
                "type": "int",
                "metavar": "<int>",
                "help": "Maximum length of an if/elif/else suite",
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

    def _suite_extents(self, node: nodes.If) -> list[Extent]:
        start = node.body[0].fromlineno
        stop = node.body[-1].end_lineno
        result = [(node, start, stop)]

        if node.orelse:
            # `elif` or `else` suite is present
            n = node.orelse[0]
            if not isinstance(n, nodes.If):
                # there is an `else` suite, we must also count its body here
                result.append((n, n.fromlineno, n.end_lineno))
            # otherwise, `node` is followed by an `elif`, which is an instance of
            # `nodes.If`, and we'll deal with its contents when we visit it later

        return result

    def visit_if(self, node: nodes.If) -> None:
        if not self.linter.config.check_pure_if_length and not node.orelse:
            # user has opted out of checking `if` suites without an `elif/else`
            return

        for (n, start, stop) in self._suite_extents(node):
            if (stop - start) + 1 > self.linter.config.max_if_suite_length:
                self.add_message(
                    "if-body-too-long",
                    node=n,
                    confidence=HIGH,
                )
#         print(f"=== If ===")
#         print(f"{self._suite_extents(node) = }")
#         print("===\n")


def register(linter: "PyLinter") -> None:
    linter.register_checker(LongIfChecker(linter))
