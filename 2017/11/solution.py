"""
Advent Of Code 2017 day 11

I may have over designed this one.  I'm pretty sure the object structure is unecessary, and
keeping track of the Hex()s in the HexGrid() is pointless, but I had fun with this one,
and it runs fast.  So be it.

My first attempt was using axial coordinates, and the calculations were unreliable. Switched
to cube coordinates, and it seems more accurate.

"""

# import system modules
from __future__ import annotations
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


class Hex:
    """
    Class to represent a hex tile
    """

    directions = {
        "n": (0, 1, -1),
        "s": (0, -1, 1),
        "ne": (1, 0, -1),
        "nw": (-1, 1, 0),
        "se": (1, -1, 0),
        "sw": (-1, 0, 1),
    }

    def __init__(self, parent, x_val, y_val, z_val):
        self.parent = parent
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val

    def __str__(self):
        return f"Hex Tile ({self.x_val},{self.y_val},{self.z_val})"

    def step(self, direction):
        """Move one step in the given direction"""
        dx_val, dy_val, dz_val = self.directions[direction]
        return self.parent.get_neighbor(
            self.x_val + dx_val, self.y_val + dy_val, self.z_val + dz_val
        )


class HexGrid:
    """
    Class to represent a grid of hex tiles
    """

    def __init__(self):
        self.tiles = {(0, 0, 0): Hex(self, 0, 0, 0)}
        self.start = self.tiles[(0, 0, 0)]
        self.current = self.tiles[(0, 0, 0)]

    def get_neighbor(self, x_val, y_val, z_val):
        """Get the neighbor tile at the given coordinates"""
        if (x_val, y_val, z_val) not in self.tiles:
            self.tiles[(x_val, y_val, z_val)] = Hex(self, x_val, y_val, z_val)
        self.current = self.tiles[(x_val, y_val, z_val)]

    def distance(self):
        """Calculate distance from start to current tile"""
        return 0.5 * (
            abs(self.current.x_val - self.start.x_val)
            + abs(self.current.y_val - self.start.y_val)
            + abs(self.current.z_val - self.start.z_val)
        )


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = HexGrid()
    max_distance = 0
    last_distance = 0
    for direction in input_value.split(","):
        grid.current.step(direction)
        last_distance = grid.distance()
        max_distance = max(max_distance, last_distance)
    if part == 2:
        return max_distance
    return last_distance


YEAR = 2017
DAY = 11
input_format = {
    1: "text",
    2: "text",
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
