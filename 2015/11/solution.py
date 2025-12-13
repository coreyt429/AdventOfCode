"""
Advent Of Code 2015 day 11

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


def next_char(char):
    """
    Function to get next character
    """
    # get int vslue of char
    int_char = ord(char)
    # increment by 1
    int_char += 1
    # loop around if past last valid character
    if int_char > 122:
        int_char = 97
    # increment if banned letter
    if int_char in [105, 108, 111]:  # banned letters i, l, and o
        int_char += 1
    # return new character
    return chr(int_char)


def next_password(input_string):
    """
    Function to calculate next password
    """
    # convert to list
    password = list(input_string)
    # walk list backwards
    for idx in range(len(password) - 1, 0, -1):
        # replace current character with net character
        password[idx] = next_char(password[idx])
        # break if not 'a' (only increment up to the
        # least significant position that needs to increment
        if password[idx] != "a":
            break
    # return joined list
    return "".join(password)


def three_consecutive(ints):
    """
    Function to test for three consecutive incrementing chars
    Passwords must include one increasing straight of at least three letters,
    like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
    """
    # walk first n-2 characters
    for idx in range(len(ints) - 2):
        # if idx, idx+1, and idx2 are consecutive
        if ints[idx + 1] == ints[idx] + 1 and ints[idx + 2] == ints[idx + 1] + 1:
            return True
    return False


def two_matched_pairs(ints):
    """
    Function to test for two matched pairs
    Passwords must contain at least two different, non-overlapping pairs of letters,
    like aa, bb, or zz.
    """
    # two matched pairs
    # reset to False
    pairs = set()
    for idx in range(len(ints) - 1):
        if ints[idx + 1] == ints[idx]:
            pair = (ints[idx], ints[idx + 1])
            if not pair in pairs:
                pairs.add(pair)
                if len(pairs) == 2:
                    return True
    return False


def is_valid(password):
    """
    Function to check a passwords validty
    """
    # get int values for chars in password
    ints = [ord(char) for char in password]

    # 3 consecutive letters
    if not three_consecutive(ints):
        return False

    # 2 matched pairs
    if not two_matched_pairs(ints):
        return False

    # banned letters i, o, l
    # Passwords may not contain the letters i, o, or l, as these letters can be mistaken
    # for other characters and are therefore confusing.
    if any(char in password for char in ["i", "o", "l"]):
        return False
    return True


def solve(password):
    """
    Function to solve puzzle
    """
    # get next password
    password = next_password(password)
    # if not valid, loop until valid
    while not is_valid(password):
        password = next_password(password)
    # return password
    return password


def part1(password, _part=None):
    """
    Function to solve part 1
    """
    return solve(password.strip())


def part2(password, _part=None):
    """
    Function to solve part 2
    """
    first = solve(password.strip())
    return solve(first)


YEAR = 2015
DAY = 11
input_format = {
    1: "text",
    2: "text",
}

funcs = {
    1: part1,
    2: part2,
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
