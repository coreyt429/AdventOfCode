"""
Advent Of Code 2015 day 24

This was already pretty fast and clean on this one, just needed to refactor into current format.

"""

# import system modules
import logging
import argparse
from heapq import heappop, heappush
import math
from itertools import combinations

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def find_shortest_combinations(big_list, splits):
    """
    find all equal weight three way splits of big_list
    """
    num = len(big_list)
    total = sum(big_list)
    one_third = int(total / splits)
    equal_weight_combinations = []
    # Iterate over possible sizes for the first list
    for i in range(1, num - 1):
        for _ in range(1, num - i):
            # Generate combinations for the first list
            for combo1 in combinations(big_list, i):
                if sum(combo1) == one_third:
                    equal_weight_combinations.append(combo1)
        if len(equal_weight_combinations) > 0:
            break
    return equal_weight_combinations


def solve(presents, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        shortest_combos = find_shortest_combinations(presents, 3)
        heap = []
        for list1 in shortest_combos:
            quantum_entanglement = math.prod(list1)
            leg_room = len(list1)
            heappush(heap, (leg_room, quantum_entanglement, list1))
        return heappop(heap)[1]
    # part 2
    shortest_combos = find_shortest_combinations(presents, 4)
    heap = []
    for list1 in shortest_combos:
        quantum_entanglement = math.prod(list1)
        leg_room = len(list1)
        heappush(heap, (leg_room, quantum_entanglement, list1))
    return heappop(heap)[1]


YEAR = 2015
DAY = 24
input_format = {
    1: "integers",
    2: "integers",
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
