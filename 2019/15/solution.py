"""
Advent Of Code 2019 day 15

I frustrated myself with this one.  By now I should know shortest path means
BFS or dijkstra.  No, I was stuck on the IntCodeComputer state being untouchable
and tried a DFS like attempt that almost worked.  It ended up taking an off map
short cut that I couldn't explain.  Regardless, the BFS approach I ended up with
made filling out the map for part 2 painless.

Part 1 was taking 1.6 seconds, and part 2 1.9 (1.6 of which was rerunning part 1).
So I opted to do everything on the first pass, and store the part 2 answer. So
now they run in 1.9 seconds and 0.9 seconds.

The failed first attempt did shake out an inefficiency in my Grid() class, or rather
in the Node() class for shortest paths.  Node().has_loops was inefficient, and taking
up most of the processing time.  Improved it significantly,  then scrapped the code
that was using it so hopefully that will save the day some other day.

"""

# import system modules
import logging
import argparse
from queue import heappush, heappop
from copy import deepcopy

# import my modules
from intcode import IntCodeComputer  # pylint: disable=import-error
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

opposite = {1: 2, 2: 1, 3: 4, 4: 3}
directions = {1: "n", 2: "s", 3: "w", 4: "e"}

# dict to store answers
answers = {1: None, 2: None}

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


class NodeState:
    """
    NodeState class for encapsulating data in the heapq
    """

    def __init__(self, pos, ptr, program):
        """init"""
        self.pos = pos
        self.ptr = ptr
        self.program = program

    def __lt__(self, other):
        """less than"""
        return 0

    def __str__(self):
        """string"""
        return f"{self.pos}, {self.ptr}"


class RepairDroid(Grid):
    """Class to represent repair droid"""

    # status codes
    WALL = 0
    MOVED = 1
    OXYGEN = 2
    NOOP = 3

    # directions
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    directions = [NORTH, SOUTH, WEST, EAST]
    direction_map = {
        "n": NORTH,
        NORTH: "n",
        "s": SOUTH,
        SOUTH: "s",
        "w": WEST,
        WEST: "w",
        "e": EAST,
        EAST: "e",
    }

    def __init__(self, program):
        # init grid
        super().__init__(
            ["."],
            coordinate_system="cartesian",
            type="infinite",
            default_value="?",
            ob_default_value="?",
            pos_token="D",
        )
        # init icc
        self.icc = IntCodeComputer(program)
        self.icc.output = []
        self.oxygen_system_location = None
        self.debug = False
        self.pos = (0, 0)

    def test_direction(self, direction):
        """
        Method to process a input for movement
        """
        self.icc.inputs.append(direction)
        # wait for output
        while len(self.icc.output) < 1:
            # break when ptr is outside program
            if not 0 <= self.icc.ptr < len(self.icc.program):
                # print(f"ptr: {self.icc.ptr} is OOB")
                break
            self.icc.step()
        # process outputs
        if self.icc.output:
            status_code = self.icc.output.pop(0)
            return status_code
        return None

    def find_oxygen(self):
        """method to find oxygen source"""
        oxygen_steps = 0
        self.icc.output = []
        heap = []
        node = NodeState(
            deepcopy(self.pos), deepcopy(self.icc.ptr), deepcopy(self.icc.program)
        )
        for direction in [1, 2, 3, 4]:
            heappush(heap, (0, direction, node))
        while heap:
            steps, direction, node = heappop(heap)
            self.icc.ptr = deepcopy(node.ptr)
            self.cfg["use_overrides"] = False
            self.icc.program = deepcopy(node.program)
            self.pos = deepcopy(node.pos)

            status_code = self.test_direction(direction)
            if status_code == 2:
                oxygen_steps = steps + 1
                self.move(directions[direction])
                self.set_point(self.pos, "O")
            if status_code == 1:
                self.move(directions[direction])
                self.set_point(self.pos, ".")
                node = NodeState(
                    deepcopy(self.pos),
                    deepcopy(self.icc.ptr),
                    deepcopy(self.icc.program),
                )
                for new_direction in [1, 2, 3, 4]:
                    if new_direction != opposite[direction]:
                        heappush(heap, (steps + 1, new_direction, node))
            if status_code == 0:
                self.move(directions[direction])
                self.set_point(self.pos, "#")
                self.move(directions[opposite[direction]])
        return oxygen_steps

    def fix_unknowns(self):
        """method to replace remaining ? with #"""
        self.update()
        for point in self:
            if self.get_point(point, "?") == "?":
                self.set_point(point, "#")


def _compute_answers(program):
    """
    Explore the area once and cache the answers.
    """
    droid = RepairDroid(program)
    steps = droid.find_oxygen()
    droid.fix_unknowns()
    minutes = 0
    closed_set = set()
    while True:
        new_oxygen = set()
        for point in droid:
            if point in closed_set:
                continue
            if droid.get_point(point, "?") == "O":
                neighbors = droid.get_neighbors(
                    point=point, directions=["n", "s", "e", "w"], invalid="#"
                )
                for neighbor in neighbors.values():
                    if droid.get_point(neighbor) == ".":
                        new_oxygen.add(neighbor)
                closed_set.add(point)
            elif droid.get_point(point, "?") == "#":
                closed_set.add(point)
        if new_oxygen:
            for point in new_oxygen:
                droid.set_point(point, "O")
            minutes += 1
        else:
            break
    answers[1] = steps
    answers[2] = minutes


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if answers[part] is None:
        _compute_answers(input_value)
    return answers[part]


def parse_input(input_text):
    """
    Return stripped intcode program.
    """
    return input_text.strip()


YEAR = 2019
DAY = 15
input_format = {
    1: parse_input,
    2: parse_input,
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
