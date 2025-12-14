"""
Advent Of Code 2021 day 25

nice simple puzzle to end.  Nice win after the brutality of the 24th.


"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def move_sea_cucumbers(in_map):
    """Function to move sea cucumbers one step"""
    # Every step, the sea cucumbers in the east-facing herd attempt to move forward one location,
    # then the sea cucumbers in the south-facing herd attempt to move forward one location. When
    # a herd moves forward, every sea cucumber in the herd first simultaneously considers whether
    # there is a sea cucumber in the adjacent location it's facing (even another sea cucumber
    # facing the same direction), and then every sea cucumber facing an empty location
    # simultaneously moves into that location.
    out_map = [["."] * len(line) for line in in_map]
    row_count = len(in_map)
    col_count = len(in_map[0])
    move_count = 0
    # move east
    for row, line in enumerate(in_map):
        for col, char in enumerate(line):
            if char == ">":
                if line[(col + 1) % col_count] == ".":
                    out_map[row][(col + 1) % col_count] = ">"
                    out_map[row][col] = "."
                    move_count += 1
                else:
                    out_map[row][col] = ">"
    # move south
    for row, line in enumerate(in_map):
        for col, char in enumerate(line):
            if char == "v":
                # if slot is open in the current map, and not already occupied in the new map
                if all(
                    [
                        in_map[(row + 1) % row_count][col] != "v",
                        out_map[(row + 1) % row_count][col] == ".",
                    ]
                ):
                    out_map[(row + 1) % row_count][col] = "v"
                    out_map[row][col] = "."
                    move_count += 1
                else:
                    out_map[row][col] = "v"
    return move_count, out_map


def print_map(in_map, title):
    """Function to print map for debug"""
    print(f"{title}:")
    for line in in_map:
        print("".join(line))
    print()


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return "Remote Start Sleigh"
    current_map = [list(line) for line in input_value]
    # print_map(current_map, "Initial state")
    idx = 0
    while True:
        idx += 1
        moves, current_map = move_sea_cucumbers(current_map)
        if moves == 0:
            return idx
            # print(f"No movement at {idx}")
            # break
        # ess = 's'
        # if idx == 1:
        #     ess = ''
        # print_map(current_map, f"After {idx} step{ess}")


YEAR = 2021
DAY = 25
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
