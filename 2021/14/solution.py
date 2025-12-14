"""
Advent Of Code 2021 day 14

Brute force worked for part 1.  Part 2, I'm kicking myself, because after
seeing the solution from u/ThreadsOfCode, I realized I've been down this
road before.  The solution makes sense, and I was able to adapt it to
my solution.  Now will I remember this next time I see one of these?

"""

# import system modules
import logging
import argparse
from collections import Counter, defaultdict

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(text):
    """Function to parse input text and return template and rules"""
    template, rules_text = text.split("\n\n")
    rules = {}
    for rule in rules_text.splitlines():
        pair, insertion = rule.split(" -> ")
        rules[pair] = (pair[0] + insertion, insertion + pair[1])
    return template, rules


def process(template, rules):
    "Function to process template by rules, returning new_template"
    new_template = ""
    for idx, char in enumerate(template):
        if idx == len(template) - 1:
            new_template += char
            continue
        pair = char + template[idx + 1]
        if pair in rules:
            new_template += rules[pair][0]
            continue
        new_template += char
    return new_template


def process_2(template, rules, steps):
    """
    Function to process template rules.

    Improved version maintains pair counter instead of trying
    to build the template.
    """
    pairs = ["".join(pair) for pair in zip(template, template[1:])]
    counter = Counter(pairs)
    for _ in range(steps):
        new_counter = {key: 0 for key in rules.keys()}
        for key, value in counter.items():
            new_counter[rules[key][0]] += value
            new_counter[rules[key][1]] += value
        counter = new_counter
    letters = defaultdict(int)
    for key, value in counter.items():
        letters[key[0]] += value
    letters[template[-1]] += 1
    most_common_letters = Counter(letters).most_common()
    return most_common_letters[0][1] - most_common_letters[-1][1]


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    template, rules = parse_input(input_value)
    passes = 10
    if part == 2:
        passes = 40
    return process_2(template, rules, passes)


YEAR = 2021
DAY = 14
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
