"""
Advent Of Code 2023 day 19

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


def parse_input(
    data: str,
) -> tuple[dict[str, tuple[str, ...]], list[tuple[str, str, str, str]]]:
    """parse input data into rules and parts"""
    # Split the data into lines
    rule_block, part_block = data.strip().split("\n\n")

    rules = {}
    parts = []
    # 'px{a<2006:qkq,m>2090:A,rfg}'split('{|}')
    # {x=2127,m=1623,a=2188,s=1013}
    for rule in rule_block.split("\n"):
        split_characters = r"\{|\}"  # Escaping '{' and '}' and using '|' for 'or'
        # Splitting the string
        rule_name, rule_tests, dummy = re.split(split_characters, rule)
        rule_list = rule_tests.split(",")
        rules[rule_name] = tuple(rule_list)

    pattern = r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}"
    parts = [match.groups() for match in re.finditer(pattern, part_block) if match]
    return rules, parts


def accepted_part(
    part: tuple[str, str, str, str], rules: dict[str, tuple[str, ...]], current="in"
):
    """determine if part is accepted according to rules"""
    if current == "A":
        return True
    if current == "R":
        return False
    logger.debug("Evaluating part %s with rule %s", part, current)
    logger.debug("Current rules: %s", rules)
    rule = rules[current]
    for test in rule:
        matches = re.match(r"^([a-zA-Z]+)$", test)
        if matches:
            label = matches.group(1)
            return accepted_part(part, rules, label)
        comparison, label = test.split(":")
        matches = re.match(r"([xmas])([<>])(\d+)", comparison)
        mykey = {"x": 0, "m": 1, "a": 2, "s": 3}
        if matches:
            prop = matches.group(1)
            oper = matches.group(2)
            value = int(matches.group(3))
            if oper == "<":
                if int(part[mykey[prop]]) < value:
                    return accepted_part(part, rules, label)
            elif oper == ">":
                if int(part[mykey[prop]]) > value:
                    return accepted_part(part, rules, label)
            else:
                logger.warning(
                    "unkown operator in comparison: %s, label: %s",
                    comparison,
                    label,
                )
    return None


def part_value(parts: tuple[str, str, str, str]):
    """calculate part value"""
    pattern = r"(\d+)"
    total_sum = 0
    for part in parts:
        total_sum += sum(int(match.group()) for match in re.finditer(pattern, part))
    return total_sum


def both(
    ch: str,
    gt: bool,
    val: int,
    ranges: list[
        tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]
    ],
) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]]:
    """Apply both conditions to ranges"""
    ch = "xmas".index(ch)
    ranges2 = []
    for rng in ranges:
        rng = list(rng)
        lo, hi = rng[ch]
        if gt:
            lo = max(lo, val + 1)
        else:
            hi = min(hi, val - 1)
        if lo > hi:
            continue
        rng[ch] = (lo, hi)
        ranges2.append(tuple(rng))
    return ranges2


def acceptance_ranges_outer(
    work: str, rules: dict[str, tuple[str, ...]]
) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]]:
    """Get acceptance ranges for a workflow"""
    logger.debug("acceptance_ranges_outer: %s %s", work, rules[work])
    return acceptance_ranges_inner(rules[work], rules)


def acceptance_ranges_inner(
    w: tuple[str, ...], rules: dict[str, tuple[str, ...]]
) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]]:
    """Get acceptance ranges for a workflow inner"""
    logger.debug("acceptance_ranges_outer(%s)", w)
    # acceptance_ranges_outer(('s<1351:px', 'qqz'))
    it = w[0]
    logger.debug("it: %s", it)
    if it == "R":
        return []
    if it == "A":
        return [((1, 4000), (1, 4000), (1, 4000), (1, 4000))]
    if ":" not in it:
        return acceptance_ranges_outer(it, rules)
    cond = it.split(":")[0]
    logger.debug("cond: %s", cond)
    gt = ">" in cond
    logger.debug("gt: %s", gt)
    ch = cond[0]
    logger.debug("ch: %s", ch)
    val = int(cond[2:])
    logger.debug("val: %d", val)
    val_inverted = val + 1 if gt else val - 1
    logger.debug("val_inverted: %d", val_inverted)
    if_cond_is_true = both(
        ch, gt, val, acceptance_ranges_inner([it.split(":")[1]], rules)
    )
    if_cond_is_false = both(
        ch, not gt, val_inverted, acceptance_ranges_inner(w[1:], rules)
    )
    return if_cond_is_true + if_cond_is_false


def part1(parts: list[tuple[str, str, str, str]], rules: dict[str, tuple[str, ...]]):
    """solve part 1 of puzzle"""
    retval = 0
    for part in parts:
        if accepted_part(part, rules):
            value = part_value(part)
            retval += value
    return retval


def part2(rules: dict[str, tuple[str, ...]]):
    """solve part 2 of puzzle"""
    retval = 0
    for rng in acceptance_ranges_outer("in", rules):
        logger.debug("Range: %s", rng)
        v = 1
        for lo, hi in rng:
            logger.debug("%d - %d", hi, lo)
            v *= hi - lo + 1
            logger.debug("%d *= %d - %d + 1", v, hi, lo)
        retval += v
    return retval


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    rules, parts = parse_input(input_value)
    logger.debug("Parsed rules: %s", rules)
    logger.debug("Parsed parts: %s", parts)
    retval = 0
    if part == 1:
        retval = part1(parts, rules)
    else:
        retval = part2(rules)
    return retval


YEAR = 2023
DAY = 19
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
