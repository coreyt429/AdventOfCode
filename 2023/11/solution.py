"""
Advent Of Code 2023 day 11

"""

# import system modules
import logging
import argparse
import copy

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def print_map(data: list[list[int]], label: str) -> None:
    """Print the map of galaxies"""
    print(label)
    max_row = max(pair[0] for pair in data) + 1
    max_col = max(pair[1] for pair in data) + 1
    for row in range(max_row):
        for col in range(max_col):
            found = False
            for galaxy in data:
                if galaxy[0] == row and galaxy[1] == col:
                    found = True
            if found:
                print("#", end="")
            else:
                print(".", end="")
        print()


def get_galaxies(map_list: list[list[str]]) -> list[list[int]]:
    """Get list of galaxies from map"""
    galaxies = []
    # find galaxies
    for row_idx, row in enumerate(map_list):
        for col_idx, _ in enumerate(row):
            if row[col_idx] == "#":
                galaxies.append([row_idx, col_idx])
    return galaxies


def find_galaxies(sectors: list[list[int]], idx: int, size: int) -> list[list[int]]:
    """Find galaxies in sectors"""
    galaxies = []
    for i in range(size):
        has_galaxy = False
        for sector in sectors:
            if sector[idx] == i:
                has_galaxy = True
        if not has_galaxy:
            galaxies.append(i)
    galaxies.sort(reverse=True)
    return galaxies


def expand_universe(galaxies: list[list[int]], factor: int = 2) -> list[list[int]]:
    """Expand the universe by adding empty rows and columns"""
    factor -= 1
    max_row = max(pair[0] for pair in galaxies) + 1
    max_col = max(pair[1] for pair in galaxies) + 1
    expand_rows = find_galaxies(galaxies, 0, max_row)
    expand_cols = find_galaxies(galaxies, 1, max_col)
    for row in expand_rows:
        for galaxy in galaxies:
            if galaxy[0] > row:
                galaxy[0] += factor
    for col in expand_cols:
        for galaxy in galaxies:
            if galaxy[1] > col:
                galaxy[1] += factor
    return galaxies


def distance(map_list: list[list[int]], g1: int, g2: int) -> int:
    """Calculate the distance between two galaxies"""
    rows = abs(map_list[g1][0] - map_list[g2][0])
    cols = abs(map_list[g1][1] - map_list[g2][1])
    dist = rows + cols
    return dist


def part1(map_list: list[list[int]]) -> int:
    """solve part 1"""
    retval = 0
    galaxies = expand_universe(copy.deepcopy(map_list))
    # print_map(galaxies, "Part1:")

    for g1 in range(len(galaxies)):
        for g2 in range(g1 + 1, len(galaxies)):
            dist = distance(galaxies, g1, g2)
            retval += dist
    return retval


def part2(map_list: list[list[int]]) -> int:
    """solve part 2"""
    retval = 0
    galaxies = expand_universe(copy.deepcopy(map_list), 1000000)
    for g1 in range(len(galaxies)):
        for g2 in range(g1 + 1, len(galaxies)):
            dist = distance(galaxies, g1, g2)
            retval += dist
    return retval


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    parsed_data = [list(line) for line in input_value]
    if part == 1:
        return part1(get_galaxies(parsed_data))
    return part2(get_galaxies(parsed_data))


YEAR = 2023
DAY = 11
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
