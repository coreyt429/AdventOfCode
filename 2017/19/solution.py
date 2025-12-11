"""
Advent Of Code 2017 day 19

This one was tougher than it should have been.  I had the beginnings of a grid system
in my aoc module, which would handle different coordinate systems, data stores, and
position identifiers.  It worked well for another puzzle, and was not fully tested.

So I spent more time rewriting that and testing it thoroughly  before working on
this puzzle.

I'm happy with the new Grid() class.  It worked well.

I'm a bit slow on this puzzle, I think it could be dramatically sped up by just noting
the position of all of the + and letters as well as the directions you can travel from
them.  Then we would just need to find the next one on the same line, and get the
manhattan distance between the points to count steps.  Maybe I can work on that later.

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


class Packet:
    """
    Class to represent our packet
    """

    def __init__(self, grid, pos, direction, **kwargs):
        """
        Initialize packet state for the ASCII maze.

        Args:
            grid (Iterable[str]): Raw maze rows.
            pos (tuple[int, int]): Starting coordinate.
            direction (str): Initial movement direction.
            **kwargs: Additional Grid constructor arguments.
        """
        self.pos = pos
        self.direction = direction
        self.letters = []
        self.grid = Grid(
            grid, start_pos=pos, coordinate_system="screen", datastore="dict", **kwargs
        )
        self.pos = self.grid.pos
        self.steps = 0

    def __str__(self):
        return f"{self.grid}"

    def get_square(self, pos):
        """
        Return the character at the requested coordinate.

        Args:
            pos (tuple[int, int]): Coordinate lookup.
        """
        return self.grid.map[pos]

    def step_forward(self):
        """
        Advance one step following the packet path rules.

        Returns:
            bool: True while more movement is possible.
        """
        current = self.get_square(self.pos)
        if current.isalpha():
            self.letters.append(current)
        if current != "+":
            if self.grid.move(self.direction, invalid=" "):
                self.steps += 1
                self.pos = self.grid.pos
                return True
            return False
        options = {
            "s": {"directions": ["e", "w"], "invalid": " |"},
            "n": {"directions": ["e", "w"], "invalid": " |"},
            "e": {"directions": ["n", "s"], "invalid": " -"},
            "w": {"directions": ["n", "s"], "invalid": " -"},
        }
        neighbors = self.grid.get_neighbors(
            directions=options[self.direction]["directions"],
            invalid=options[self.direction]["invalid"],
        )
        if len(neighbors) == 1:
            for direction in neighbors.keys():
                if self.grid.move(direction):
                    self.direction = direction
                    self.steps += 1
                    self.pos = self.grid.pos
                    return True
        if len(neighbors) == 0:
            logger.debug("end of the line: %s", self.pos)
            return False
        logger.debug("too many options: %s", self.pos)
        return False


def traverse_path(grid_lines):
    """
    Walk the ASCII path recording collected letters and step count.

    Args:
        grid_lines (list[str]): Puzzle grid rows.

    Returns:
        tuple[str, int]: Letter string and number of steps taken.
    """
    start = (grid_lines[0].index("|"), 0)
    pack = Packet(grid_lines, start, "s")
    sentinel = 0
    while pack.step_forward():
        sentinel += 1
        if sentinel > 100000:
            logger.warning("Breaking loop due to sentinel")
            break
    return "".join(pack.letters), pack.steps + 1


def solve(input_value, part):
    """
    Execute the tube traversal for the requested part.
    """
    letters, steps = traverse_path(input_value)
    if part == 1:
        return letters
    return steps


YEAR = 2017
DAY = 19
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
