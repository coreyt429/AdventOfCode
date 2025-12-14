"""
Advent Of Code 2022 day 9

My approach to part 1 set me up pretty well for part 2.

I just split the head/tail entities into a new Knot() class
with a parent child relationship, and defined tail as the
last child in the link.  So the only change between part
1 and part 2 is the number of rope segments.

I'm glad I didn't try to work this into Grid() instead first, that
would have been more complex.

"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import linear_distance  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


class Knot:
    """class to represent a knot"""

    def __init__(self, knot_id=0, parent=None, children=0):
        self.knot_id = knot_id
        self.parent = parent
        self.child = None
        self.position = (0, 0)
        self.history = [(0, 0)]
        if children > 0:
            self.child = Knot(knot_id + 1, self, children - 1)

    def move(self, direction):
        """Method to move head"""
        moves = {"u": (0, 1), "d": (0, -1), "l": (-1, 0), "r": (1, 0)}
        self.position = (
            self.position[0] + moves[direction][0],
            self.position[1] + moves[direction][1],
        )
        self.history.append(self.position)
        if self.child is not None:
            self.child.check()

    def check(self):
        """Method to check to see if a knot needs to be moved"""
        parent = self.parent
        # manhattan distance won't work, need to check distance instead
        # use the integer value of the linear distance instead.
        # diagonals are 1.4142135623730951 so don't use float()
        if int(linear_distance(self.position, parent.position)) > 1:
            vector = [0, 0]
            for dim in [0, 1]:
                if parent.position[dim] > self.position[dim]:
                    vector[dim] = 1
                    continue
                if parent.position[dim] < self.position[dim]:
                    vector[dim] = -1
            self.position = (
                self.position[0] + vector[0],
                self.position[1] + vector[1],
            )
            self.history.append(self.position)
            if self.child is not None:
                self.child.check()


class Rope:
    """Class to represent a rope"""

    def __init__(self, segments=2):
        """Init method"""
        self.head = Knot(children=segments - 1)
        current = self.head
        self.segments = segments
        while current.child is not None:
            current = current.child
        self.tail = current

    def make_move(self, move_str):
        """Function to make a move like U 4"""
        direction, count = move_str.split(" ")
        count = int(count)
        direction = direction.lower()
        for _ in range(count):
            self.head.move(direction)

    def __str__(self):
        """string method"""
        my_string = f"Head: {self.head.position}, Tail: {self.tail.position}"
        return my_string


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    segments = 2
    if part == 2:
        segments = 10
    rope = Rope(segments=segments)
    for move in input_value:
        rope.make_move(move)
    return len(set(rope.tail.history))


YEAR = 2022
DAY = 9
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
