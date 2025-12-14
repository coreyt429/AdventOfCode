"""
Advent Of Code 2019 day 4

This one was pretty straight forward, not much to say.


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


def check_passcode(int_in, mode=1):
    """
    Function to check a passcode
    Args:
        int_in: int()
    Returns:
        bool()
    """
    # convert to string
    work_str = str(int_in)
    # init rool flags
    has_repeating_digit = False
    no_incrementing_values = True
    # get length
    length = len(work_str)
    # walk characters
    for idx, char in enumerate(work_str):
        # if not the last char
        if idx < length - 1:
            # if the next char is smaller
            if work_str[idx + 1] < char:
                # set flag
                no_incrementing_values = False
                # no need to test this num further
                break
            # if next char is the same
            if char == work_str[idx + 1]:
                # part 2
                if mode == 2:
                    # if the char after next matches, no go
                    if idx < length - 2 and char == work_str[idx + 2]:
                        continue
                    # if the previous character matches, no go
                    if idx > 0 and char == work_str[idx - 1]:
                        continue
                # set flag
                has_repeating_digit = True
    # return true if all conditions met
    return all([has_repeating_digit, no_incrementing_values])


def parse_input(input_text):
    """
    Parse range bounds.
    """
    start_num, end_num = [int(num) for num in input_text.strip().split("-")]
    return start_num, end_num


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    start_num, end_num = input_value
    passwords = []
    for num in range(start_num, end_num + 1):
        if check_passcode(num, part):
            passwords.append(num)
    return len(passwords)


YEAR = 2019
DAY = 4
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
