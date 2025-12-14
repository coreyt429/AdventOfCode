"""
Advent Of Code 2016 day 21

More regex parsing fun.  Pulled out deque for lazy list rotation.

Scrambling was pretty straight forward.  I over thought unscrambling
and tried to reverse the rules.  That didn't work very well

Then I considered the search space, and realized for once, brute
force is the way to go.  So for part 2, I ended up just iterating
over the permutations of possible passwords, and test until one
scrambled to the target.

"""

import logging
import argparse
import re
import collections
from itertools import permutations
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

# regex patterns to parse instructions
patterns = {
    "swap_position": re.compile(r"swap position (\d+) with position (\d+)"),
    "swap_letter": re.compile(r"swap letter (\w+) with letter (\w+)"),
    "rotate_steps": re.compile(r"rotate (\w+) ([\d]+) steps*"),
    "rotate_letter": re.compile(r"rotate based on position of letter (\w)"),
    "move": re.compile(r"move position (\d+) to position (\d)"),
    "reverse": re.compile(r"reverse positions (\d+) through (\d+)"),
}

# movement functions


def swap_position(chars, positions):
    """
    swap position X with position Y means that the letters at indexes X
    and Y (counting from 0) should be swapped.
    """
    # get i and j as integers
    i, j = [int(position) for position in positions]
    # convert to list
    chars = list(chars)
    # swap i and j
    chars[i], chars[j] = chars[j], chars[i]
    # return string
    return "".join(chars)


def swap_letter(chars, letters):
    """
    swap letter X with letter Y means that the letters X and Y should be
    swapped (regardless of where they appear in the string).
    """
    # swap based on positions of letters
    return swap_position(chars, (chars.find(letters[0]), chars.find(letters[1])))


def rotate_steps(chars, steps):
    """
    rotate left/right X steps means that the whole string should be rotated;
    for example, one right rotation would turn abcd into dabc.
    """
    # get direction and count
    l_r, count = steps

    if l_r == "right":
        # right positive integer
        count = int(count)
    else:
        # left negative integer
        count = int(count) * -1
    # convert to deque
    chars = collections.deque(chars)
    # rotate
    chars.rotate(count)
    # return string
    return "".join(chars)


def rotate_letter(chars, letters):
    """
    rotate based on position of letter X means that the whole string should
    be rotated to the right based on the index of letter X (counting from 0)
    as - determined before this instruction does any rotations. Once the index
    is determined, rotate the string to the right one time, plus a number of
    times equal to that index, plus one additional time if the index was at
    least 4.
    """
    # get letter from tuple
    letter = letters[0]
    # position of letter
    pos = chars.find(letter)
    # rotate the string to the right one time, plus a number of
    # times equal to that index
    steps = pos + 1
    if pos >= 4:
        # plus one additional time if the index was at least 4
        steps += 1
    # return string from rotate_steps
    return rotate_steps(chars, ("right", steps))


def move(chars, positions):
    """
    move position X to position Y means that the letter which
    is at index X should be removed from the string, then inserted
    such that it ends up at index Y.
    """
    # get indexes as ints
    from_idx, to_idx = [int(position) for position in positions]
    # convert to list
    chars = list(chars)
    # pop from and insert at to
    chars.insert(to_idx, chars.pop(from_idx))
    # return string
    return "".join(chars)


def reverse_substring(chars, positions):
    """
    reverse positions X through Y means that the span of letters
    at indexes X through Y (including the letters at X and Y)
    should be reversed in order.
    """
    # get positions as int
    i, j = [int(position) for position in positions]
    # return sliced string, reversing the mid section
    return chars[:i] + chars[i : j + 1][::-1] + chars[j + 1 :]


# function map
handlers = {
    "swap_position": swap_position,
    "swap_letter": swap_letter,
    "rotate_steps": rotate_steps,
    "rotate_letter": rotate_letter,
    "move": move,
    "reverse": reverse_substring,
}


def scramble(input_string, instruction):
    """
    Function to scramble string based on instruction
    """
    # walk patterms
    for key, pattern in patterns.items():
        # check pattern
        match = pattern.match(instruction)
        if match:  # yay, we matches
            # run string through handler
            return handlers[key](input_string, match.groups())
    return "we shouldn't be able to get here, but pylint wants a return"


def run_instructions(input_string, instructions):
    """
    Function to scamble pass based on instructions
    """
    # walk instructions
    for instruction in instructions:
        # scramble based on instruction
        input_string = scramble(input_string, instruction)
    # return string
    return input_string


def parse_input(input_text):
    """
    Return the list of instructions.
    """
    return [line.strip() for line in input_text.splitlines() if line.strip()]


def solve(instructions, part):
    """
    Solve part 1 (scramble) or part 2 (brute-force unscramble).
    """
    if part == 1:
        return run_instructions("abcdefgh", instructions)

    target = "fbgdceah"
    for perm in permutations(target):
        candidate = "".join(perm)
        if run_instructions(candidate, instructions) == target:
            return candidate
    return None


YEAR = 2016
DAY = 21
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
