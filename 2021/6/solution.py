"""
Advent Of Code 2021 day 6

I started this one out actually spawning the fish, and trying to
find patterns.

In part two, I realized this was just too slow, and we only needed
the fish count in the end.  So I switched to just counting the
number of fish in each state each day.
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


def spawn_fish(start, days):
    """
    Function to spawn lantern fish over a number of days

    This will work for part 1, and can be used two ways:
    1) slow way, pass the whole start fish list to it
    2) faster way, run one unique fish number at a time, then
       add up the totals
    Both are two slow for part 2, so this is just here for information
    """
    fishes = list(start)
    # print(f"Initial state: {','.join((str(fish) for fish in fishes))}")
    for _ in range(days):
        new_fishes = []
        for idx, fish in enumerate(fishes):
            fish -= 1
            if fish < 0:
                new_fishes.append(8)
                fish = 6
            fishes[idx] = fish
        fishes.extend(new_fishes)
        # print(f"After {day:2} days:  {','.join((str(fish) for fish in fishes))}")
    return fishes


def spawn_fish_2(start_fishes, days):
    """
    Function to simulate spawning lantern fish.
    """
    # init fish states -1 to 8
    fishes = {}
    for key in range(-1, 9):
        fishes[key] = 0
    # set initial state counts based on input
    for key in start_fishes:
        fishes[key] += 1
    # iterate over days
    for _ in range(days):
        # set state to the count above it
        for key in range(0, 9):
            fishes[key - 1] = fishes[key]
        # -1 is not a valid state, these are the fish that are spawning
        # so add them to 6 and set 8 to that number
        fishes[6] += fishes[-1]
        fishes[8] = fishes[-1]
        fishes[-1] = 0
        # print(f"After {day:2} days:  {sum(fishes.values())}")
    # return fish counts
    return sum(fishes.values())


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    initial_fishes = [int(num) for num in input_value.split(",")]
    # if part == 1:
    #     fishes = spawn_fish(initial_fish, 80)
    #     return len(fishes)
    days = 80
    if part == 2:
        days = 256
    return spawn_fish_2(initial_fishes, days)
    # original method, too slow for part 2
    # counts = {}
    # for num in set(initial_fish):
    #     counts[num] = len(spawn_fish([num], days))
    # total = 0
    # for num in initial_fish:
    #     total += counts[num]
    # return total


YEAR = 2021
DAY = 6
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
