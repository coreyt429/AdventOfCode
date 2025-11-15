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
import time
from queue import heappush, heappop
from copy import deepcopy

# import my modules
from intcode import IntCodeComputer  # pylint: disable=import-error
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

opposite = {1: 2, 2: 1, 3: 4, 4: 3}
directions = {1: "n", 2: "s", 3: "w", 4: "e"}

# dict to store answers
answer = {1: None, 2: None}


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


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # part 2 return answer we calculated in the first pass
    if part == 2:
        return answer[2]
    # init droid
    droid = RepairDroid(input_value)
    # get steps to oxygen source
    steps = droid.find_oxygen()
    # part 2 continue
    # repair unkown walls
    droid.fix_unknowns()
    # init minutes
    minutes = 0
    # init closed_set
    closed_set = set()
    # loop until break
    while True:
        # init new_oxygen each pass
        new_oxygen = set()
        # iterate over points in map
        for point in droid:
            # skip id already closed
            if point in closed_set:
                continue
            # oxygen
            if droid.get_point(point, "?") == "O":
                # get neighbors
                neighbors = droid.get_neighbors(
                    point=point, directions=["n", "s", "e", "w"], invalid="#"
                )
                # iterate over neighbors
                for neighbor in neighbors.values():
                    # if neighbor is empty
                    if droid.get_point(neighbor) == ".":
                        # add to new_oxygen
                        new_oxygen.add(neighbor)
                # add point to closed set
                closed_set.add(point)
            # add walls to closed_set
            elif droid.get_point(point, "?") == "#":
                closed_set.add(point)
        # did we find any new rooms to oxygenate?
        if new_oxygen:
            # iterate over new rooms
            for point in new_oxygen:
                # set to oxygen
                droid.set_point(point, "O")
            # increment minutes
            minutes += 1
        else:
            # break if no new rooms
            break
    # store part 2 answer for the next pass
    answer[2] = minutes
    # part 1, return steps to oxygen source
    return steps


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019, 15)
    input_text = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # correct answers once solved, to validate changes
    correct = {1: 354, 2: 370}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
