"""
Advent Of Code 2020 day 15

I played around with data structures on this one.

I started with a big deque for the numbers.  worked great for
test data and part 1.  way to big and slow for part 2.

Converted that to a defaultdict(deque) keyed on the number and
queing its appearances.  Worked, solved the problem, slow.

Optimized deque to only store the last two values.  This got it
down to 22 seconds.

Dropped both, and went with a dict(tuple) keyed on number with
value as a tuple of the last two instances.  time is doen to 13
seconds for part 2, so leaving it at that.

"""

# import system modules
import logging
import argparse
# from collections import deque
# from collections import defaultdict

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    numbers = [int(num) for num in input_value[0].split(",")]
    seen = {}
    current = numbers[-1]
    seen = {num: (idx + 1, None) for idx, num in enumerate(numbers)}
    target = 2020 + 1
    if part == 2:
        target = 30000000 + 1
    for turn in range(len(numbers) + 1, target):
        # print(turn, current, seen[current])
        if current not in seen or seen[current][1] is None:
            next_number = 0
        else:
            next_number = seen[current][0] - seen[current][1]
        if next_number in seen:
            seen[next_number] = (turn, seen[next_number][0])
        else:
            seen[next_number] = (turn, None)
        current = next_number
        # if turn % 1000000 == 0:
        # print(f"turn: {turn}, spoken: {current}")
    # attempts:
    # 1: 104 too low
    # 2: 371 got it.  helps if you remember to parse the input
    # part 2:
    # 1: 175594 too high.   ah, input matters, that was using the test input
    # 2: 352, got it.
    return current


YEAR = 2020
DAY = 15
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
