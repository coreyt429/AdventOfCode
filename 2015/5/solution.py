"""
Advent Of Code 2015 day 5

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


def part1(lines, _part=None):
    """
    Function to solve part 1
    It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or
      aabbccdd (aa, bb, cc, or dd).
    It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the
      other requirements.
    """
    retval = {"nice": 0, "naughty": 0}

    forbidden_strings = ["ab", "cd", "pq", "xy"]
    vowels = ["a", "e", "i", "o", "u"]
    for line in lines:
        vowel_count = 0
        double = 0
        bad = 0
        for idx, char in enumerate(line):
            if char in vowels:
                vowel_count += 1
            if idx < len(line) - 1:
                if char == line[idx + 1]:
                    double += 1
                elif line[idx : idx + 2] in forbidden_strings:
                    bad += 1
        if bad > 0:
            retval["naughty"] += 1
        elif vowel_count > 2:
            if double > 0:
                retval["nice"] += 1
        else:
            retval["naughty"] += 1
    return retval["nice"]


def part2(lines, _part=None):
    """
    Function to solve part 2
    It contains a pair of any two letters that appears at least twice in the string without
      overlapping,
    like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    It contains at least one letter which repeats with exactly one letter between them, like
      xyx, abcdefeghi (efe), or even aaa.
    """
    retval = {"nice": 0, "naughty": 0}
    for line in lines:
        pairs = 0
        skips = 0
        for idx in range(0, len(line) - 2):
            if line[idx] == line[idx + 2]:
                skips += 1
            for idx2 in range(idx + 2, len(line) - 1):
                if line[idx : idx + 2] == line[idx2 : idx2 + 2]:
                    pairs += 1
        if skips > 0:
            if pairs > 0:
                # print(f'nice: {line}')
                retval["nice"] += 1
            else:
                retval["naughty"] += 1
                # print(f'naughty: {line}')
        else:
            retval["naughty"] += 1
            # print(f'naughty: {line}')
    return retval["nice"]


YEAR = 2015
DAY = 5
input_format = {
    1: "lines",
    2: "lines",
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
