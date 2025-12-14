"""
Advent Of Code 2020 day 7

Pretty simple recursion task.  I used default dict to initialize my
dict(dict) structure for the rules. regex would have been more
elegant for the parsing, but this method works.



"""

# import system modules
import logging
import argparse
from collections import defaultdict

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_bag_rules(bag_rules):
    """Function to parse input into defaultdict"""
    rules = defaultdict(dict)
    for rule in bag_rules:
        bag_type, contents = rule.split(" bags contain ")
        for inner_bag in contents.split(", "):
            if "no other bags" in inner_bag:
                rules[bag_type] = {}
            else:
                count, inner_bag_type = inner_bag.split(" ", 1)
                inner_bag_type = inner_bag_type.replace(" bags", "")
                inner_bag_type = inner_bag_type.replace(" bag", "")
                inner_bag_type = inner_bag_type.replace(".", "")
                # print(f"count: {count}, inner_bag_type: {inner_bag_type}")
                rules[bag_type][inner_bag_type] = int(count.replace(" ", ""))
    return rules


def can_contain(outer, inner, rules):
    """
    Recursive function to determine if a bag_type can hold another
    bag_type
    """
    # print(f"can_contain({outer}, {inner}, rules)")
    for child_bag_type in rules[outer].keys():
        if child_bag_type == inner:
            return True
        if can_contain(child_bag_type, inner, rules):
            return True
    return False


def bags_needed(bag_type, qty, rules):
    """
    Recursive function to identify the number of bags needed
    """
    # print(f"bags_needed({bag_type}, {qty}, rules)")
    total = qty
    for _ in range(qty):
        for inner_bag_type, inner_qty in rules[bag_type].items():
            total += bags_needed(inner_bag_type, inner_qty, rules)
    # print(f"bags_needed({bag_type}, {qty}, rules): {total}")
    return total


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    rules = parse_bag_rules(input_value)
    target = "shiny gold"
    if part == 1:
        count = 0
        for bag_type in rules.keys():
            # print(f"Trying {bag_type}")
            if can_contain(bag_type, target, rules):
                # print('Yes')
                count += 1
        # How many bag colors can eventually contain at least one shiny gold bag?
        return count
    # part 2
    # How many individual bags are required inside your single shiny gold bag?
    # -1 because we don't count the shiny gold bag
    return bags_needed(target, 1, rules) - 1


YEAR = 2020
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
