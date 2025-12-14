"""
Advent Of Code 2022 day 2

Easy enough.  I only tripped on one small bug in part 2.  For some reason, I was
expecting 3 % 3 to be 3 instead of 0. Which is especially bad since I explicitly
tested that and still did it wrong.

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


def play_round(elf, player, part):
    """Function to play round of rock paper scissors"""
    moves = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
    # convert move to score
    elf = moves[elf]
    if part == 1:
        player = moves[player]
    else:
        # Anyway, the second column says how the round needs to end:
        # X means you need to lose,
        if player == "X":
            player = (elf - 1) % 3
        # Y means you need to end the round in a draw, and
        elif player == "Y":
            player = elf
        # Z means you need to win. Good luck!
        elif player == "Z":
            player = (elf + 1) % 3
        # fix scissors
        if player == 0:
            player = 3
    # get diff
    diff = abs(elf - player)

    if diff == 0:  # draw
        return elf + 3, player + 3
    if diff == 1:  # 1,2 or 2, 3 higher score wins
        if elf > player:
            return elf + 6, player
        return elf, player + 6
    if player == 1:  # 1, 3 - 1 wins
        return elf, player + 6
    return elf + 6, player
    # part 2:
    # 13662 too low


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    elf_total = 0
    player_total = 0
    for line in input_value:
        elf_score, player_score = play_round(*line.split(" "), part)
        elf_total += elf_score
        player_total += player_score
    return player_total


YEAR = 2022
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
