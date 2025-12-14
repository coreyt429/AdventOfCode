"""
Advent Of Code 2016 day 14

I struggled with this one. After running someone else's solution,
I discovered that I was counting a key as discovered when it was verified
rather than when it was detected.

So I had to search deeper to be sure the 64th detected key was verified,
then sort by index

"""

import logging
import argparse
import hashlib
import re
from collections import deque

from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

# patterns for matching 3 and 5 chars in a row
pattern_chars = {3: re.compile(r"(.)\1\1"), 5: re.compile(r"(.)\1\1\1\1")}


def parse_input(input_text):
    """
    Return stripped salt string.
    """
    return input_text.strip()


def checksum(number, seed):
    """
    Function to generate the first checksum for a seed
    """
    check_string = f"{seed}{number}"
    return hashlib.md5(check_string.encode("utf-8")).hexdigest()


def expanded_checksum(number, seed):
    """
    function to execute part 2 checksum expansion
    """
    # get first checksum from checksum()
    tmp_checksum = checksum(number, seed)
    # rehash 2016 times
    for _ in range(2016):
        tmp_checksum = hashlib.md5(tmp_checksum.encode("utf-8")).hexdigest()
    return tmp_checksum


def find_chars(input_string, count):
    """
    Function to find 3 or 5 character patterns
    """
    # Define the regex pattern for exactly count consecutive identical characters
    if count not in pattern_chars:
        return None
    # fetch pattern
    pattern = pattern_chars[count]
    # init matched_chars
    matched_chars = []
    # for each match in the input_string
    for match in pattern.finditer(input_string):
        # Test character before (this shouldn't really happen, but checking anyway)
        matched_chars.append(match.group(1))
        if count == 3:
            # short circuit 3's
            break
    return matched_chars


def find_key(seed, protocol):
    """
    Function to find keys, and return the index of the 64th key
    """
    # my_keys: list of tuple(idx,char,checksum)
    my_keys = set()

    # potentials: set of tuple(idx,char,checksum)
    potentials = deque(maxlen=1001)

    # initialize idx
    idx = 0
    # okay, just a bit frustrated here, I was stopping at 64,
    # and you need to go a bit beyond then sort the results
    while len(my_keys) < 72:
        # get md5sum
        if protocol == 1:
            my_checksum = checksum(idx, seed)
        else:
            my_checksum = expanded_checksum(idx, seed)
        # get all matching 5 char set
        my_chars = find_chars(my_checksum, 5)
        # did we match?
        if my_chars:
            # walk potentials to see if there is a match
            for potential in potentials:
                # is it stale?
                if (
                    potential[0] < idx <= potential[0] + 1001
                    and potential[1] in my_chars
                ):
                    # yes, add it to my_keys
                    # my_keys.add((potential,(idx,tuple(my_chars),my_checksum)))
                    my_keys.add(potential)
        # get first matching 3 char set
        my_chars = find_chars(my_checksum, 3)
        # did we match?
        if my_chars:
            # yes, add it to potentials
            potentials.append((idx, my_chars[0], my_checksum))
        idx += 1
    return sorted(list(my_keys))[63][0]


YEAR = 2016
DAY = 14
input_format = {
    1: parse_input,
    2: parse_input,
}

funcs = {
    1: find_key,
    2: find_key,
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
