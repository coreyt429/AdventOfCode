"""
Advent Of Code 2023 day 2

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


def parse_games(lines):
    """
    Function to parse input
    """
    games = {}
    for line in lines:
        [game, str_rolls] = line.split(":", 2)
        game_id = int(game.replace("Game ", ""))
        games[game_id] = {}
        games[game_id]["turns"] = {}
        turn = 0
        for roll in str_rolls.split(";"):
            turn += 1
            games[game_id]["turns"][turn] = {}
            for cube in roll.split(","):
                cube = cube.strip()
                [qty, color] = cube.split(" ")
                games[game_id]["turns"][turn][color] = int(qty)
    return games


def part1(games):
    """
    Function to solve part 1
    """
    cubes = {"red": 12, "green": 13, "blue": 14}
    result = 0
    for game_id in games:
        valid = 1
        for turn in games[game_id]["turns"]:
            for color in games[game_id]["turns"][turn]:
                if games[game_id]["turns"][turn][color] > cubes[color]:
                    valid = 0
        # print(valid)
        if valid:
            result += game_id
    return result


def part2(games):
    """
    function to solve part 2
    """
    result = 0
    # find minimum number of cubes of each color for each game
    # calculate power of cube set for game red * green * blue
    # sum up power as answer
    for game_id in games:
        min_set = {"red": 0, "green": 0, "blue": 0}
        for turn in games[game_id]["turns"]:
            for color in games[game_id]["turns"][turn]:
                if games[game_id]["turns"][turn][color] > min_set[color]:
                    min_set[color] = games[game_id]["turns"][turn][color]
        power = min_set["red"] * min_set["blue"] * min_set["green"]
        result += power
    return result


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    games = parse_games(input_value)
    if part == 1:
        return part1(games)
    return part2(games)


YEAR = 2023
DAY = 2
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
