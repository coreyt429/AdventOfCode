"""
Advent Of Code 2023 day 24

"""

# import system modules
import logging
import argparse
from z3 import Solver, Real, Reals, sat

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

X = 0
Y = 1
solver = Solver()
x, y, z = Reals("x y z")
vx, vy, vz = Reals("vx vy vz")


def parse_input(lines: list) -> list:
    """parse input into list of hailstones with position and velocity"""
    hail = []
    for line in lines:
        str_pos, str_vel = line.split(" @ ")
        pos = [int(x) for x in str_pos.split(", ")]
        vel = [int(x) for x in str_vel.split(", ")]
        hail.append({"pos": pos, "vel": vel})
    return hail


def find_intersection_and_check_time(pointa: dict, pointb: dict) -> tuple:
    """find intersection point of two hailstones and check if in past"""
    pos = {
        "a": tuple(pointa["pos"][a] for a in (X, Y)),
        "b": tuple(pointb["pos"][b] for b in (X, Y)),
    }
    vel = {
        "a": tuple(pointa["vel"][a] for a in (X, Y)),
        "b": tuple(pointb["vel"][b] for b in (X, Y)),
    }
    a, b, c, d = vel["a"][X], -vel["b"][X], vel["a"][Y], -vel["b"][Y]
    e, f = pos["b"][X] - pos["a"][X], pos["b"][Y] - pos["a"][Y]
    denominator = a * d - b * c

    if denominator == 0:
        return None, False, False  # Lines are parallel or coincident

    t = (e * d - b * f) / denominator
    s = (a * f - e * c) / denominator

    intersection = {
        X: pos["a"][X] + vel["a"][X] * t,
        Y: pos["a"][Y] + vel["a"][Y] * t,
    }
    past = {
        "a": t < 0,
        "b": s < 0,
    }
    return (intersection[X], intersection[Y]), past["a"], past["b"]


def part1(parsed_data: list) -> int:
    """solve part 1"""
    # for idx in hail
    # calculate times both x and y are within test_area[0] and test_area[1] inclusive
    retval = 0
    for i, pointa in enumerate(parsed_data):
        for j in range(i + 1, len(parsed_data)):
            pointb = parsed_data[j]
            if pointa == pointb:
                continue
            intersection, past_for_pointa, past_for_pointb = (
                find_intersection_and_check_time(pointa, pointb)
            )
            if intersection:
                if past_for_pointa and past_for_pointb:
                    continue
                if past_for_pointa:
                    continue
                if past_for_pointb:
                    continue
                if (
                    test_area[0] <= intersection[X] <= test_area[1]
                    and test_area[0] <= intersection[Y] <= test_area[1]
                ):
                    retval += 1
    return retval


def part2(line_data: list) -> int:
    """solve part 2"""
    for idx, line in enumerate(line_data[:3]):
        x0, y0, z0 = line["pos"]
        xv, yv, zv = line["vel"]

        t = Real("t" + str(idx))

        solver.add(x + vx * t == x0 + xv * t)
        solver.add(y + vy * t == y0 + yv * t)
        solver.add(z + vz * t == z0 + zv * t)

    if solver.check() == sat:
        model = solver.model()
        # Extracting the solution
        return (
            int(model[x].as_decimal(10))
            + int(model[y].as_decimal(10))
            + int(model[z].as_decimal(10))
        )
    raise RuntimeError("No solution found")


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    hail = parse_input(input_value)
    if part == 1:
        return part1(hail)
    return part2(hail)


YEAR = 2023
DAY = 24
input_format = {
    1: "lines",
    2: "lines",
}

funcs = {
    1: solve,
    2: solve,
}

test_area = [200000000000000, 400000000000000]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    if args.test:
        test_area.clear()
        test_area.extend([20, 30])
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
