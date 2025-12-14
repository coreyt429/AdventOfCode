"""
Advent Of Code 2021 day 10

I tripped a couple times on this one.  My first attempt to identify corrupted lines
didn't work because it also matched incomplete lines.  My second attempt didn't
take into account the last open set being the one that needed to close first.  I
modified that for the final is_corrupted version.

Part 2 was fairly easy, the logic I used for part 1 was already identifying the expected
closings.  I could probably return them from is_corrupted, and not have to find them
in auto_complete, but part 2 is already running in 0.001 seconds, so no real need
to optimize.  I failed my first answer, because I didn't copy scores.sort() from
my test code to solve() function.

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


def score_auto_complete(auto_complete_list):
    """Function to score an auto complete ending"""
    points = {")": 1, "]": 2, "}": 3, ">": 4}
    score = 0
    for char in auto_complete_list:
        score *= 5
        score += points[char]
    return score


def auto_complete(line):
    """Function to auto complete the chunk closing"""
    opens = {"(": ")", "[": "]", "{": "}", "<": ">"}
    expecting = []
    for _, char in enumerate(line):
        if char in opens:
            expecting.append(opens[char])
            continue
        if char == expecting[-1]:
            # remove it from expecting, this closes the last open set
            expecting.pop(-1)
            continue
        print(f"We shouldn't get here: {char}")
    auto_complete_list = list(reversed(expecting))
    return auto_complete_list, score_auto_complete(auto_complete_list)


def is_corrupted(line):
    """Function to identify corrupted lines"""
    # this initially failed because it was too simplistic.
    # {([(<{}[<>[]}>{[]{[(<()> - Expected ], but found } instead.
    #             ^  was in expecting because of 0
    #        ^ but not the last open set, so need to add to test
    #          to see if it is the last open set expecting[-1]
    #          also need to prune the last if it is
    # with that added logic, it seems to pass the test data at least.
    opens = {"(": ")", "[": "]", "{": "}", "<": ">"}
    corrupted = False
    expecting = []
    char = None
    for _, char in enumerate(line):
        if char in opens:
            expecting.append(opens[char])
            continue
        if char not in expecting:
            # print(f"{line}: not expecting {char} at {idx}")
            corrupted = True
            break
        if char == expecting[-1]:
            # remove it from expecting, this closes the last open set
            expecting.pop(-1)
            continue
        # now it is in expecting, but not the last, so valid == False
        # print(f"{line}: {char} at {idx} doesn't close last set {expecting[-1]}")
        corrupted = True
        break
    return corrupted, char


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    score = 0
    scores = []
    for line in input_value:
        corrupted, bad_char = is_corrupted(line)
        if corrupted:
            # Find the first illegal character in each corrupted line of the navigation subsystem.
            score += points[bad_char]
        elif part == 2:
            _, score = auto_complete(line)
            scores.append(score)
    if part == 2:
        # Find the completion string for each incomplete line, score the completion strings,
        # and sort the scores. What is the middle score?
        # 85929366 too low, hehe forgot to sort the scores
        scores.sort()
        return scores[len(scores) // 2]
    # What is the total syntax error score for those errors?
    return score


YEAR = 2021
DAY = 10
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
