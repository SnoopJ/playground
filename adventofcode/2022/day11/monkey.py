from __future__ import annotations  # for forward references

from collections import defaultdict
from dataclasses import dataclass, field
import logging
import operator
import re
from typing import Callable, Literal, Union


LOGGER = logging.getLogger(__name__)

ItemWorry = int
MonkeyId = int


ID = r"\d+"
MONKEY_PATTERN = rf"""
Monkey (?P<ID>{ID}):
  Starting items:(?P<ITEMS>.*)
  Operation: new = (?P<OP_EXPR>.*)
  Test: divisible by (?P<DIVISOR>\d+)
    If true: throw to monkey (?P<TRUE_DEST>{ID})
    If false: throw to monkey (?P<FALSE_DEST>{ID})
""".strip()
MonkeyMatcher = re.compile(MONKEY_PATTERN, re.MULTILINE)

OLD = object()


@dataclass
class MonkeyOperator:
    lhs: Union[Literal[OLD], int]
    rhs: Union[Literal[OLD], int]
    op: Callable[[int, int], int]

    def __call__(self, val: ItemWorry) -> ItemWorry:
        l = val if self.lhs is OLD else self.lhs
        r = val if self.rhs is OLD else self.rhs
        result = self.op(l, r)

        return result



@dataclass
class MonkeyTest:
    divisor: int
    true_dest: Monkey
    false_dest: Monkey

    def __call__(self, val: ItemWorry) -> MonkeyId:
        if (val % self.divisor) == 0:
            LOGGER.debug("    Current worry level is divisible by %s", self.divisor)
            return self.true_dest
        else:
            LOGGER.debug("    Current worry level is not divisible by %s", self.divisor)
            return self.false_dest


@dataclass
class Monkey:
    id: MonkeyId
    op: MonkeyOperator
    test: MonkeyTest

    items: list[ItemWorry] = field(default_factory=list)

    worry_control: bool = True
    inspection_count: int = 0

    @staticmethod
    def _make_op(m: re.Match):
        op_expr = m.group("OP_EXPR")
        lhs, op, rhs = op_expr.split()
        lhs = OLD if lhs == "old" else int(lhs)
        rhs = OLD if rhs == "old" else int(rhs)

        if op == "+":
            op = operator.add
        elif op == "*":
            op = operator.mul
        else:
            raise ValueError(f"Invalid operator {op!r}")

        return MonkeyOperator(
            lhs=lhs,
            rhs=rhs,
            op=op,
        )

    @staticmethod
    def _make_test(m: re.Match):
        divisor = int(m.group("DIVISOR"))
        true_dest = int(m.group("TRUE_DEST"))
        false_dest = int(m.group("FALSE_DEST"))

        return MonkeyTest(
            divisor=divisor,
            true_dest=true_dest,
            false_dest=false_dest,
        )

    @classmethod
    def from_desc(cls, desc: str, **kwargs):
        m = MonkeyMatcher.match(desc)
        assert m, "Invalid Monkey description"

        id = int(m.group("ID"))
        items = [int(it) for it in m.group("ITEMS").split(',') if it]

        op = cls._make_op(m)
        test = cls._make_test(m)

        return cls(
            id=id,
            items=items,
            op=op,
            test=test,
            **kwargs,
        )

    def catch(self, items: list[ItemWorry]):
        self.items.extend(items)

    def compute_throws(self) -> dict[MonkeyId, list[ItemWorry]]:
        LOGGER.debug("Monkey %s:", self.id)
        throws = defaultdict(list)

        for item in self.items:
            LOGGER.debug("  Monkey inspects an item with a worry level of %s", item)
            self.inspection_count += 1
            new_item = self.op(item)
            LOGGER.debug("    Worry level goes from %s to %s", item, new_item)
            if self.worry_control:
                new_item = new_item // 3
                LOGGER.debug("    Monkey gets bored with item. Worry level is divided by 3 to %s", new_item)
            else:
                LOGGER.debug("    Monkey gets bored with item. Worry level is unmodified")
            dest = self.test(new_item)
            throws[dest].append(new_item)
            LOGGER.debug("    Item with worry level %s is thrown to monkey %s", new_item, dest)

        # assumption: every item is thrown
        self.items.clear()

        return throws


@dataclass
class MonkeyBusiness:
    monkeys: list[Monkey]

    def handle_round(self):
        for monkey in self.monkeys:
            throws = monkey.compute_throws()
            for dest, items in throws.items():
                self.monkeys[dest].catch(items)

