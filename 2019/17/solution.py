"""
Advent Of Code 2019 day 17

This one was fun.  I IntCodeComputer() worked without modification.  Grid()
was useful for part 1.

I printed grid in part 1, and used that output to figure out the path
the robot would need to take.  From there, I just had to find the repeating
patterns, and make them A, B, and C.  I had an extra R4 in that was throwing
me off.  Stepping through the first few steps proved it was an error and I
removed it.

Finding the final output could probably have been more graceful, but I
noticed it was printing an unprintable character, and assumed it was > 256.
I initially tested by printing the value if it was > 256, and that proved
to be the correct answer, so I modified it to a return.

"""

# import system modules
import logging
import argparse

# import my modules
from intcode import IntCodeComputer  # pylint: disable=import-error
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def find_intersections(grid):
    """
    Function to find intersections in scaffolding
    """
    # init intersections
    intersections = []
    # iterate over points in grid
    for point in grid:
        # if point is scaffolding, take a closer look
        if grid.get_point(point) == "#":
            # init intersection as true
            intersection = True
            # get neightbors of point
            neighbors = grid.get_neighbors(point=point, directions=["n", "s", "e", "w"])
            # iterate over neighbors
            for neighbor in neighbors.values():
                # if neghbor is not scaffolding, then not an intersection
                if grid.get_point(neighbor, "?") != "#":
                    # set intersection false, and move to next point
                    intersection = False
                    break
            # if intersection, then add to inetersections
            if intersection:
                intersections.append(point)
    # return intersection points
    return intersections


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init IntCodeComputer
    icc = IntCodeComputer(input_value)
    # init output
    icc.output = []
    if part == 1:
        # run program
        icc.run()
        # get grid text from output
        grid_text = "".join([chr(num) for num in icc.output])
        # init grid
        grid = Grid(grid_text, use_overrides=False)
        # find intersections
        intersections = find_intersections(grid)
        # calculate result
        return sum(point[0] * point[1] for point in intersections)
    # define main_program, and sub routines based on manual map examination
    main_text = "A,B,A,C,A,B,A,C,B,C\n"
    a_text = "R,4,L,12,L,8,R,4\n"
    b_text = "L,8,R,10,R,10,R,6\n"
    c_text = "R,4,R,10,L,12\n"
    # live feed, to enable set use_live_feed to True
    use_live_feed = False
    live_feed = "n\n"
    if use_live_feed:
        live_feed = "y\n"
    # iterate over input strings
    for input_string in [main_text, a_text, b_text, c_text, live_feed]:
        # convert strings to ascii values and add to inputs
        icc.inputs.extend([ord(char) for char in input_string])
    # Force the vacuum robot to wake up by changing the value in your ASCII program
    # at address 0 from 1 to 2.
    icc.program[0] = 2
    # loop indefinitely
    while True:
        # break if out of bounds
        if not 0 <= icc.ptr < len(icc.program):
            break
        # step through program
        icc.step()
        # if there are outputs, check them
        while len(icc.output) > 0:
            # get next output
            output = icc.output.pop(0)
            # if output is outside of printable characters
            if output > 256:
                # return
                return output
            if use_live_feed:
                # print feed if enabled
                print(chr(output), end="")
    return None


def parse_input(input_text):
    """
    Return stripped intcode program.
    """
    return input_text.strip()


YEAR = 2019
DAY = 17
input_format = {
    1: parse_input,
    2: parse_input,
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
