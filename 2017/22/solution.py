"""
Advent Of Code 2017 day 22

"""

# import system modules
from __future__ import annotations
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


class VirusCarrier:
    """
    class to represent VirusCarrier
    """

    def __init__(self, lines, pos=(1, 1), variant=1):
        """
        Initialize a virus carrier on the infection grid.

        Args:
            lines (Iterable[str]): Initial infection map.
            pos (tuple[int, int]): Starting coordinate.
            variant (int): Puzzle mode (1 or 2).
        """
        self.variant = variant
        self.grid = Grid(lines, coordinate_system="cartesian", type="infinite")
        self.pos = pos
        self.grid.pos = self.pos
        self.stats = {
            "infected": 0,
            "cleaned": 0,
            "weakened": 0,
            "flagged": 0,
            "bursts": 0,
        }
        self.direction = "up"

    def activity_burst(self):
        """
        Execute a single burst of activity following puzzle rules.
        """
        self.stats["bursts"] += 1
        if self.variant == 1:
            if self.grid.map[self.pos] == "#":
                self.turn("right")
                self.clean()
            else:
                self.turn("left")
                self.infect()
        else:
            if self.grid.map[self.pos] == "#":
                self.turn("right")
                self.flag()
            elif self.grid.map[self.pos] == "W":
                self.infect()
            elif self.grid.map[self.pos] == "F":
                self.turn("reverse")
                self.clean()
            else:
                self.turn("left")
                self.weaken()
        self.move()

    def weaken(self):
        """Mark the current node as weakened."""
        self.stats["weakened"] += 1
        self.grid.map[self.pos] = "W"

    def flag(self):
        """Mark the current node as flagged."""
        self.stats["flagged"] += 1
        self.grid.map[self.pos] = "F"

    def clean(self):
        """Mark the current node as clean."""
        self.stats["cleaned"] += 1
        self.grid.map[self.pos] = "."

    def infect(self):
        """Mark the current node as infected."""
        self.stats["infected"] += 1
        self.grid.map[self.pos] = "#"

    def move(self):
        """Advance to the next node in the current direction."""
        if self.grid.move(self.direction):
            self.pos = self.grid.pos

    def turn(self, direction):
        """
        Rotate the carrier according to turn direction keyword.

        Args:
            direction (str): 'left', 'right', or 'reverse'.
        """
        turn_map = {
            "up": {"left": "left", "right": "right", "reverse": "down"},
            "left": {"left": "down", "right": "up", "reverse": "right"},
            "down": {"left": "right", "right": "left", "reverse": "up"},
            "right": {"left": "up", "right": "down", "reverse": "left"},
        }
        self.direction = turn_map[self.direction][direction]

    def __str__(self):
        return f"bursts: {self.stats['bursts']}, infected: {self.stats['infected']}"


def solve(input_value, part):
    """
    Run the virus carrier simulation for the requested part.
    """
    start_y = len(input_value) // 2
    start_x = len(input_value[0]) // 2
    carrier = VirusCarrier(input_value, pos=(start_x, start_y), variant=part)
    cycles = 10000 if part == 1 else 10_000_000
    for _ in range(cycles):
        carrier.activity_burst()
    return carrier.stats["infected"]


YEAR = 2017
DAY = 22
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
