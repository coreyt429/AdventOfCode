"""
Advent Of Code 2021 day 5

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


def solve(lines, part):
    """Function to solve puzzle"""
    points = defaultdict(int)
    data = {"p": [], "x": [0, 0], "y": [0, 0]}
    for line in lines:
        data["p"] = line.split(" -> ")
        for idx, value in enumerate(data["p"]):
            data["x"][idx], data["y"][idx] = (int(num) for num in value.split(","))
        # if x's match or y's match, then we have a vertical or horizontal line
        if any([len(set(data["x"])) == 1, len(set(data["y"])) == 1]):
            # Consider only horizontal and vertical lines.
            for x_val in range(min(data["x"]), max(data["x"]) + 1):
                for y_val in range(min(data["y"]), max(data["y"]) + 1):
                    points[(x_val, y_val)] += 1
        elif part == 2:
            # Consider all of the lines.
            d_x = 1
            if data["x"][1] - data["x"][0] < 0:
                d_x = -1
            # d_y = d_x * slope
            d_y = d_x * int(
                (data["y"][1] - data["y"][0]) / (data["x"][1] - data["x"][0])
            )
            x_val = data["x"][0]
            y_val = data["y"][0]
            while x_val != data["x"][1]:
                points[(x_val, y_val)] += 1
                x_val += d_x
                y_val += d_y
            points[(data["x"][1], data["y"][1])] += 1
    # At how many points do at least two lines overlap?
    counter = 0
    for _, count in points.items():
        if count > 1:
            counter += 1
    # 11690 - too low
    return counter


YEAR = 2021
DAY = 5
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
