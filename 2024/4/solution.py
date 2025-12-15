"""
Advent Of Code 2024 day 4

Grid() made this one fairly easy. I extended it to at an items() method that I ended
up not using.  I think that will come in handy in the future though, as I usually
end up doing something like this:
for point in grid:
    char = grid.get_point(point)
    # do something with char

Now I can just do this:
for point, char in grid.items():
    # do something with char

The only trip ups on this one were typo's ([all_directions]  !- all_directions),
and bad assumptions

"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid, all_directions, diagonal_directions  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def count_words(grid, word, point, index=0, directions=all_directions):
    """Function to count the instances of word for a point"""
    if grid.get_point(point) != word[index]:
        return 0
    if index == len(word) - 1:
        return 1
    total = 0
    for direction, neighbor in grid.get_neighbors(
        point=point, directions=directions
    ).items():
        total += count_words(grid, word, neighbor, index + 1, [direction])
    return total


def check_x_mas(grid, point):
    """
    Function to find X-MAS in the grid

    This one is a bit more hard coded to find MAS,
    unlike count_words, which should work with any word
    """
    if grid.get_point(point) != "A":
        return False
    neighbors = grid.get_neighbors(point=point, directions=diagonal_directions)
    opposite_pairs = (("ne", "sw"), ("nw", "se"))
    valid = set()
    for pair in opposite_pairs:
        chars = ""
        for direction in pair:
            if direction in neighbors:
                chars += grid.get_point(neighbors[direction])
        if chars in ["MS", "SM"]:
            valid.add(pair)
    if len(valid) < 2:
        return False
    return True


def find_words(grid, word, part=1):
    """Function to find a word in the grid"""
    words = 0
    for point in grid:
        if part == 1:
            words += count_words(grid, word, point)
        else:
            if check_x_mas(grid, point):
                words += 1
    return words


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    return find_words(grid, "XMAS", part)


YEAR = 2024
DAY = 4
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
