"""
Advent Of Code 2016 day 7

already fast, refactored, simplifying main logic and moving to current format

"""

# import system modules
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

supernet_pattern = re.compile(r"(\[\w+\])")


def contains_abba(my_string):
    """
    Checks for abba pattern in string
    """
    for idx in range(len(my_string) - 3):
        if (
            my_string[idx] == my_string[idx + 3]
            and my_string[idx + 1] == my_string[idx + 2]
            and my_string[idx] != my_string[idx + 1]
        ):
            return True
    return False


def contains_aba(my_string):
    """
    checks for aba patterns
    """
    abas = []
    retval = False
    for idx in range(len(my_string) - 2):
        if (
            my_string[idx] == my_string[idx + 2]
            and my_string[idx] != my_string[idx + 1]
        ):
            retval = True
            abas.append(my_string[idx : idx + 3])
    return retval, abas


def contains_bab(my_string, aba):
    """
    contains reverse of aba
    """
    bab = aba[1] + aba[0] + aba[1]
    return bab in my_string


def supports_ssl(my_string):
    """
    check for ssl suport ABA outside [] and BAB inside []
    """
    supernets = supernet_pattern.findall(my_string)
    for supernet in supernets:
        my_string = my_string.replace(supernet, "-")

    has_aba, my_abas = contains_aba(my_string)
    if has_aba:
        for aba in my_abas:
            for supernet in supernets:
                if contains_bab(supernet, aba):
                    return True
    return False


def supports_tls(my_string):
    """
    check for tls support (abba outside of square brackets, but not inside)
    """
    for my_str in supernet_pattern.findall(my_string):
        if contains_abba(my_str):
            return False
    if contains_abba(my_string):
        return True
    return False


def solve(lines, part):
    """
    Function to solve puzzle
    """
    counter = 0
    func_map = {1: supports_tls, 2: supports_ssl}
    for line in lines:
        if func_map[part](line):
            counter += 1
    return counter


YEAR = 2016
DAY = 7
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
