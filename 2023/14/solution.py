"""
Advent Of Code 2023 day 14

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


def parse_input(lines: list[str]) -> tuple[tuple[str]]:
    """Parse input lines into a tuple of tuples representing the map"""
    my_map = []
    for line in lines:
        my_map.append(list(line))
    return tuple(tuple(line) for line in my_map)


def print_map(my_map: tuple[tuple[str]], label: str) -> None:
    """print the map with a label"""
    print(f"{label}:")
    for line in my_map:
        print("".join(line))
    print()


def score_map(my_map: tuple[tuple[str]]) -> int:
    """Score a map based on the position of 'O' characters"""
    score = 0
    for row_idx, row in enumerate(my_map):
        for col in row:
            if col == "O":
                score += len(my_map) - row_idx
    return score


def tilt_north(my_map: tuple[tuple[str]]) -> tuple[tuple[str]]:
    """tilt the map northwards"""
    # Convert the tuple of tuples to a list of lists for easier manipulation
    mutable_map = [list(row) for row in my_map]
    for row_idx, row in enumerate(mutable_map):
        for col_idx, col in enumerate(row):
            if col == ".":
                for row_idx_2 in range(row_idx + 1, len(mutable_map)):
                    if mutable_map[row_idx_2][col_idx] == ".":
                        continue
                    if mutable_map[row_idx_2][col_idx] == "O":
                        mutable_map[row_idx][col_idx] = "O"
                        mutable_map[row_idx_2][col_idx] = "."
                    break

    # Convert the list of lists back to a tuple of tuples before returning
    return tuple(tuple(row) for row in mutable_map)


def rotate_cw(my_map: tuple[tuple[str]]) -> tuple[tuple[str]]:
    """Rotate the map clockwise"""
    retval = []
    for col in range(len(my_map[0])):
        new_col = []
        for row in range(len(my_map)):
            new_col.append(my_map[len(my_map) - row - 1][col])
        retval.append(tuple(new_col))
    return tuple(retval)


def spin_cycle(my_map: tuple[tuple[str]]) -> tuple[tuple[str]]:
    """Run map through a full spin cycle (north, west, south, east)"""
    # north
    my_map = tilt_north(my_map)
    # west
    my_map = rotate_cw(my_map)
    my_map = tilt_north(my_map)
    # south
    my_map = rotate_cw(my_map)
    my_map = tilt_north(my_map)
    # east
    my_map = rotate_cw(my_map)
    my_map = tilt_north(my_map)
    # reorent to north
    my_map = rotate_cw(my_map)
    return my_map


def solve(input_value: list[str], part: int) -> int:
    """
    Function to solve puzzle
    """
    my_map = parse_input(input_value)
    retval = 0
    if part == 1:
        my_map = tilt_north(my_map)
        # print_map(parsed_data,'After')
        retval = score_map(my_map)
        return retval
    seen = set(my_map)
    maps = [my_map]
    idx = 0
    while True:
        idx += 1
        my_map = spin_cycle(my_map)
        if my_map in seen:
            break
        seen.add(my_map)
        maps.append(my_map)

    # First repeated pattern
    first = maps.index(my_map)
    target_idx = (1000000000 - first) % (idx - first) + first
    my_map = maps[target_idx]
    retval = score_map(my_map)
    return retval


YEAR = 2023
DAY = 14
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
