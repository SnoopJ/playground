from __future__ import annotations
from dataclasses import dataclass, field


class ExecutionHalted(Exception):
    """Raised to indicate end of CPU execution"""


@dataclass
class Instruction:
    name: str
    delay: int = field(repr=False)
    register_effect: int


INSTRUCTIONS = {
    "noop": lambda: Instruction("noop", delay=1, register_effect=0),
    "addx": lambda arg: Instruction("addx", delay=2, register_effect=arg)
}


@dataclass
class CPU:
    cycles: int = 1

    # registers
    X: int = 1

    instructions: list[Instruction] = field(default_factory=list)
    curr_i: Instruction = field(default=None)
    curr_delay: int = field(default=None, init=False)
    debug: bool = False

    def load(self, instructions):
        self.instructions.extend(instructions)

    def _load_next(self):
        if not self.instructions:
            raise ExecutionHalted

        self.curr_i = self.instructions.pop(0)
        self.curr_delay = self.curr_i.delay

    @property
    def signal_strength(self):
        return self.cycles * self.X

    def step(self):
        if not self.curr_i:
            self._load_next()

        self.cycles += 1
        self.curr_delay -= 1

        if self.curr_delay == 0:
            self.X += self.curr_i.register_effect
            if self.debug:
                print(f"Effect {self.curr_i.register_effect:+d} applied to register X (new value: {self.X})")
            self.curr_i = self.curr_delay = None
        elif self.curr_delay > 0:
            pass
        else:
            raise ValueError("Invalid delay")
