"""
Advent Of Code 2023 day 22

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


class Brick:
    """
    Class representing a brick in 3D space
    """

    def __init__(self, line: str):
        a, b = line.strip().split("~")
        a = tuple(map(int, a.split(",")))
        b = tuple(map(int, b.split(",")))
        self.x = (min(a[0], b[0]), max(a[0], b[0]))
        self.y = (min(a[1], b[1]), max(a[1], b[1]))
        self.z = (min(a[2], b[2]), max(a[2], b[2]))

        # Keep track of bricks directly above and below (ie which are supported by this
        # brick and which are supporting this brick)
        self.below = set()
        self.above = set()

    def is_below(self, other: "Brick") -> bool:
        """
        Returns True if self and other overlap in the x-y plane and self
        is below other along the z-axis.
        """
        return (
            (self.x[0] <= other.x[1] and other.x[0] <= self.x[1])
            and (self.y[0] <= other.y[1] and other.y[0] <= self.y[1])
            and (self.z[1] <= other.z[0])
        )

    def drop(self, newz: int):
        """
        Drops this brick down so the new lower z-value is newz. No checking
        is done for collisions.
        """
        length = self.z[1] - self.z[0]
        self.z = (newz, newz + length)

    def collapse(self):
        """
        Checks if the current brick is supported by a subset of <removed>.
        If so, add this brick to remove and all
        bricks above it that would fall (check recursively).
        """
        removed = {self}
        for other in self.above:
            other.collapse2(removed)
        removed.remove(self)
        return removed

    def collapse2(self, removed):
        """
        Helper function for collapse, checks if all supporting bricks are in
        <removed>. If so, add this brick to <removed> and check all bricks
        above it recursively.
        """
        if self.below.issubset(removed):
            removed.add(self)
            for other in self.above:
                other.collapse2(removed)

    def __str__(self):
        return f"Brick coordinates: X{self.x}, Y{self.y}, Z{self.z}"


def parse_input(lines: list[str]) -> list[Brick]:
    """parse input lines into list of Brick objects"""
    # Split the data into lines
    bricks = [Brick(line) for line in lines]
    return bricks


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    bricks = parse_input(input_value)
    #  Keep bricks sorted by z-value, also, after settling, keep track of
    # the bricks by lower z-value, to keep track of neighbours
    bricks.sort(key=lambda v: v.z[0])
    by_zval = [[] for _ in range(bricks[-1].z[0])]
    base = Brick("0,0,0~1000,1000,0")
    settled = [base]
    for brick in bricks:
        # compare to settled bricks, put it in lowest place possible and add to settled
        # Start by getting the highest z-value for the x,y footprint of brick
        top_z = max((other.z[1] for other in settled if other.is_below(brick)))
        brick.drop(top_z + 1)
        settled.append(brick)
        by_zval[top_z + 1].append(brick)
    for brick in bricks:
        for other in by_zval[brick.z[1] + 1]:
            if brick.is_below(other):
                other.below.add(brick)
                brick.above.add(other)

    remove_count = 0
    chain_count = 0
    for brick in bricks:
        if len(brick.above) == 0 or all(len(other.below) > 1 for other in brick.above):
            # Each brick supported by the current brick is also supported by yet others
            # Therefor we can safely remove this one
            remove_count += 1
        else:
            supported = brick.collapse()
            chain_count += len(supported)
    if part == 1:
        return remove_count
    return chain_count


YEAR = 2023
DAY = 22
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
