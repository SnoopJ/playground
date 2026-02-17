from __future__ import annotations

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.interfaces import HIGH
from pylint.lint import PyLinter


class NameReuseChecker(BaseChecker):

    name = "reused-name"
    msgs = {
        # NOTE: pylint code prefixes 51-99 are reserved for external checkers, see:
        # https://github.com/pylint-dev/pylint/blob/v3.0.3/pylint/checkers/__init__.py#L37
        # This prefix was selected randomly
        "W8901": (
            "name assigned to multiple times",
            "multiple-name-assignment",
            "names should be assigned to one time",
        ),
    }
    options = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._assignments_per_scope = {}

    def _check_target(self, tgt):
        if hasattr(tgt, "elts"):
            for t in tgt.elts:
                # NOTE:2026-02-17:SnoopJ:Probably a way to do this without recursing, but target lists aren't commonly very deep, so let's keep it simple
                self._check_target(t)
            return

        scope_assignments_by_name = self._assignments_per_scope.setdefault(tgt.scope(), set())

        if tgt.name in scope_assignments_by_name:
            self.add_message(
                "multiple-name-assignment",
                node=tgt,
                confidence=HIGH,
            )
        else:
            scope_assignments_by_name.add(tgt.name)

    def visit_assign(self, node: nodes.Assign) -> None:
        for tgt in node.targets:
            self._check_target(tgt)


def register(linter: PyLinter) -> None:
    linter.register_checker(NameReuseChecker(linter))
