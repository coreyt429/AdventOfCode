"""
Advent Of Code 2020 day 4

Nothing really to trip me up here.  This was pretty much
just a regex test. That and fighting with pylint over returns
and if conditions for the validation rules.

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


def value_in_range(value, minimum, maximum):
    """
    Function to determine if a value is in a range
    """
    # print(f"value_in_range({value}, {minimum}, {maximum})")
    return minimum <= int(value) <= maximum


def validate_passport_data(passport):
    """
    Function to validate passport data fields
    """
    # pylint didn't like having so many returns, collapsing these into
    # one check:
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    if not all(
        [
            value_in_range(passport["byr"], 1920, 2002),
            value_in_range(passport["iyr"], 2010, 2020),
            value_in_range(passport["eyr"], 2020, 2030),
        ]
    ):
        #     # print(f"byr invalid: {passport['byr']}")
        return False
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    eye_colors = set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    if passport["ecl"] not in eye_colors:
        # print(f"ecl invalid: {passport['ecl']}")
        return False
    # hgt (Height) - a number followed by either cm or in:
    match = re.match(r"(\d+)(cm|in)", passport["hgt"])
    # pylint didn't like having so many returns, so minimizing the
    # returns for the hgt checks by storing the state in hgt_valid
    hgt_valid = True
    if match:
        # If cm, the number must be at least 150 and at most 193.
        if match.group(2) == "cm":
            if not value_in_range(int(match.group(1)), 150, 193):
                # print(f"hgt invalid cm: {passport['hgt']}")
                hgt_valid = False
        # If in, the number must be at least 59 and at most 76.
        else:
            if not value_in_range(int(match.group(1)), 59, 76):
                # print(f"hgt invalid in: {passport['hgt']}")
                hgt_valid = False
    else:
        # print(f"hgt missed regex: {passport['hgt']}")
        hgt_valid = False
    if not hgt_valid:
        return False
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    match = re.match(r"^(#[a-f0-9]{6})$", passport["hcl"])
    if not match:
        # print(f"hcl missed regex: {passport['hcl']}")
        return False
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    match = re.match(r"^\d{9}$", passport["pid"])
    if not match:
        # print(f"pid missed regex: {passport['pid']}")
        return False
    # cid (Country ID) - ignored, missing or not.
    return True


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    fields = [
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
        # "cid" # Surely, nobody would mind if you made the system temporarily
        # ignore missing cid fields.
    ]
    passports = []
    passport_data = input_value.split("\n\n")
    for passport_entry in passport_data:
        passport = {}
        for passport_datum in passport_entry.replace("\n", " ").split(" "):
            key, value = passport_datum.split(":")
            passport[key] = value
        passports.append(passport)
    valid = 0
    for passport in passports:
        missing_fields = []
        for field in fields:
            if field not in passport:
                missing_fields.append(field)
        if not missing_fields:
            if part == 1:
                valid += 1
            else:
                if validate_passport_data(passport):
                    valid += 1
    return valid


YEAR = 2020
DAY = 4
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
