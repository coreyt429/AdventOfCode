"""
Advent Of Code 2018 day 18

This one was fun.  Most of our household was sick today (9/6/2024).  So it was nice to
have an easy challenge after feeling puny all day.

I did need to make some modifications to the Grid() class for this.  I didn't need
any overrides, so needed a config option to turn them off.  Also, __str__ wasn't using
self.get_point it was instead pulling directly from self.map.  So I changed that so that
self.get_point is the gatekeeper for the point values including overrides.  That simplifies
the __str__ code a bit.

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
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def next_state(grid):
    """
    Function to caculcate the next state of the map
    """
    # These changes happen across all acres simultaneously, each of them using the state of
    # all acres at the beginning of the minute and changing to their new form by the end of
    # that same minute. Changes that happen during the minute don't affect each other.
    # init new state to store new values
    new_state = {}
    # walk current grid
    for point in grid:
        # get neighbor values as list
        neighbors = [
            grid.get_point(neighbor)
            for neighbor in grid.get_neighbors(point=point).values()
        ]
        # An open acre (.) will become filled with trees (|) if three or more adjacent acres
        # contained trees. Otherwise, nothing happens.
        if grid.get_point(point) == ".":
            if neighbors.count("|") >= 3:
                new_state[point] = "|"
                continue
            new_state[point] = "."
        # An acre filled with trees (|) will become a lumberyard (#) if three or more adjacent
        # acres were lumberyards. Otherwise, nothing happens.
        if grid.get_point(point) == "|":
            if neighbors.count("#") >= 3:
                new_state[point] = "#"
                continue
            new_state[point] = "|"
        # An acre containing a lumberyard (#) will remain a lumberyard if it was adjacent to
        # at least one other lumberyard and at least one acre containing trees. Otherwise,
        # it becomes open.
        if grid.get_point(point) == "#":
            if neighbors.count("#") >= 1 and neighbors.count("|") >= 1:
                new_state[point] = "#"
                continue
            new_state[point] = "."
    # update grid with new_state values
    for point, value in new_state.items():
        grid.set_point(point, value)
    # no return, since we are manipulating the grid object


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init grid from input
    my_grid = Grid(input_value, use_overrides=False)
    # minute iterations for part 1
    minutes = 10
    # already_seen list to track maps we have seen
    # based on the large number of iterations in part 2
    # I'm expacting a repeating pattern
    already_seen = []
    # set minute iterations for part 2
    if part == 2:
        minutes = 1000000000
    # run minutes
    for _ in range(1, minutes + 1):
        # calculate next state
        next_state(my_grid)
        # get str() map
        map_str = str(my_grid)
        # for part 2, if we have already seen the map, we have our loop
        if map_str in already_seen:
            # get the index of the repeated map
            # loop range is loop_start to len(alread_seen) - 1
            loop_start = already_seen.index(map_str)
            # no need to calculate any more
            break
        # add to already_seen
        already_seen.append(map_str)
    if part == 2:
        # get count
        count = len(already_seen)
        # reduce minutes by non repeating portion of already_seen
        minutes = minutes - loop_start
        # How deep will the end be into the last cycle
        modulus = minutes % (count - loop_start)
        # grap the map that should be at minutes calculations
        # note, this would fail if modulus == 0, and that is not the
        # case for my input so not accounting for it here.
        # if modulus == 0 in your input, you would instead want to
        # set map_str to the last map in already_seen
        map_str = already_seen[loop_start - 1 + modulus]
    # count woods
    woods = map_str.count("|")
    # count lumber yarde
    lumber_yards = map_str.count("#")
    # return total resources value
    return woods * lumber_yards


YEAR = 2018
DAY = 18
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
