"""
Advent Of Code 2017 day 18

I struggled too much with this one.

My initial implementation wasn't working, it may have worked if I had found the bug,
but after reviewing a few other implementations, I realized mathcing instruction
for instruction was going to be inefficient.  So I changed the processing to batch
processing for each computer.  So now each computer runs the program until it terminates
or is io blocked.  That still led me to a loop, that I was struggling with. My logic
flow looked like others, and I was getting to the same state in about the same time,
I was just looping past the answer.  Stepping back through the instruction handlers,
I found that I had coded jgz to jump on non-zero values instead of greater than zero
values.  Changed that condition, and it worked like magic.
"""

# import system modules
from __future__ import annotations
import logging
import argparse
from collections import deque

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


class SoundPlayer:
    """
    Class SoundPlayer,  this turned out to be pretty useless,
    but a was still fun.  Just commenting out the slow parts now
    """

    def __init__(self):
        """Initialize playback history."""
        self.history = []

    def last(self):
        """Return the last played frequency."""
        return self.history[-1]

    def play(self, frequency):
        """
        Log a frequency playback to history (tone generation disabled).

        Args:
            frequency (int): Frequency to "play".
        """
        if 37 <= frequency <= 32767:
            pass
        self.history.append(frequency)


class Computer:
    """
    Class to represent a computer
    """

    def __init__(self, program=None, comp_id=None):
        """
        Initialize a duet computer.

        Args:
            program (Iterable[str] | str | None): Program source.
            comp_id (int | None): Identifier to preload register `p`.
        """
        self.handlers = {
            "snd": self.do_snd,
            "set": self.do_set,
            "add": self.do_add,
            "mul": self.do_mul,
            "mod": self.do_mod,
            "rcv": self.do_rcv,
            "jgz": self.do_jgz,
        }
        self.registers = {
            "pointer": 0,
            "sent": 0,
            "received": 0,
            "recover": None,
            "iowait": False,
        }
        self.program = []
        self.player = SoundPlayer()
        self.partner = None
        self.buffer = deque([])
        self.comp_id = comp_id
        if program:
            self.load_program(program)
        if self.comp_id is not None:
            self.registers["p"] = self.comp_id

    def __str__(self):
        """Debug string showing execution state."""
        my_string = f"{self.comp_id}: running {self.running()}, "
        my_string = f"iowait: {self.registers['iowait']}, "
        my_string += f"pointer: {self.registers['pointer']}/{len(self.program)}, "
        my_string += f"sent: {self.registers['sent']}, buffer: {len(self.buffer)}, "
        my_string += f"registers: {self.registers}"
        return my_string

    def load_program(self, program):
        """
        Parse program text into instruction dictionaries.

        Args:
            program (Iterable[str] | str): Program source.
        """
        if isinstance(program, str):
            program = program.split("\n")
        self.program = []
        for line in program:
            inputs = line.split(" ")
            instruction = {"instruction": inputs[0]}
            try:
                instruction["x"] = int(inputs[1])
            except ValueError:
                instruction["x"] = inputs[1]
                self.registers[inputs[1]] = 0
            try:
                instruction["y"] = int(inputs[2])
            except ValueError:
                instruction["y"] = inputs[2]
                self.registers[inputs[2]] = 0
            except IndexError:
                pass
            self.program.append(instruction)

    def value(self, test_value):
        """
        Resolve a literal or register name into an integer value.

        Args:
            test_value (int | str): Value reference.
        """
        if isinstance(test_value, int):
            return test_value
        return self.registers[test_value]

    def running(self):
        """Return True while the instruction pointer remains in bounds."""
        return 0 <= self.registers["pointer"] < len(self.program)

    def run_next_instruction(self):
        """Execute the next instruction if still running."""
        if self.running():
            current = self.program[self.registers["pointer"]]
            instruction = current["instruction"]
            return self.handlers[instruction](current)
        return self.running()

    def run_program(self):
        """Execute instructions until halted or blocked."""
        while self.run_next_instruction():
            pass
        return self.running()

    def do_send(self, instruction):
        """Part-2 send handler; enqueue value for partner."""
        self.partner.buffer.append(self.value(instruction["x"]))
        self.partner.registers["iowait"] = False
        self.registers["pointer"] += 1
        self.registers["sent"] += 1
        return True

    def do_receive(self, instruction):
        """Part-2 receive handler; block when no data is available."""
        if len(self.buffer) == 0:
            self.registers["iowait"] = True
            return False
        self.registers["iowait"] = False
        self.registers[instruction["x"]] = self.buffer.popleft()
        self.registers["pointer"] += 1
        return True

    def do_snd(self, instruction):
        """Part-1 sound instruction."""
        frequency = self.value(instruction["x"])
        self.registers["sent"] += 1
        self.player.play(frequency)
        self.registers["pointer"] += 1
        return True

    def do_set(self, instruction):
        """Set register to the operand value."""
        self.registers[instruction["x"]] = self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_add(self, instruction):
        """Add operand value to the register."""
        self.registers[instruction["x"]] += self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_mul(self, instruction):
        """Multiply register by operand value."""
        self.registers[instruction["x"]] *= self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_mod(self, instruction):
        """Modulo the register by operand value."""
        self.registers[instruction["x"]] %= self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_rcv(self, instruction):
        """Recover last frequency when operand is non-zero."""
        value = self.value(instruction["x"])
        if value:
            self.registers["recover"] = self.player.last()
            self.registers["pointer"] += len(self.program)
        self.registers["pointer"] += 1
        return True

    def do_jgz(self, instruction):
        """Conditional jump for positive operand."""
        if self.value(instruction["x"]) > 0:
            self.registers["pointer"] += self.value(instruction["y"])
        else:
            self.registers["pointer"] += 1
        return True


def solve(input_value, part):
    """
    Execute the duet program for the requested part.

    Args:
        input_value (Iterable[str]): Puzzle input lines.
        part (int): Part selector (1 or 2).

    Returns:
        int: Recovered frequency (part 1) or sends from program 1 (part 2).
    """
    if part == 1:
        computer = Computer(input_value)
        computer.run_program()
        return computer.registers["recover"]
    computers = {0: Computer(input_value, 0), 1: Computer(input_value, 1)}
    computers[0].partner = computers[1]
    computers[1].partner = computers[0]
    for comp in computers.values():
        comp.handlers["snd"] = comp.do_send
        comp.handlers["rcv"] = comp.do_receive
    while True:
        running = False
        for comp in computers.values():
            if not comp.running():
                break
            running = True
            comp.run_program()
        if not running:
            break
        if all(comp.registers["iowait"] for comp in computers.values()):
            break
    return computers[1].registers["sent"]


YEAR = 2017
DAY = 18
input_format = {
    1: "lines",
    2: "lines",
}

funcs = {
    1: solve,
    2: solve,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
