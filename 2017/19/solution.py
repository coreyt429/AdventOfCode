"""
Advent Of Code 2017 day 19

This one was tougher than it should have been.  I had the beginnings of a grid system
in my aoc module, which would handle different coordinate systems, data stores, and
position identifiers.  It worked well for another puzzle, and was not fully tested.

So I spent more time rewriting that and testing it thoroughly  before working on
this puzzle.

I'm happy with the new Grid() class.  It worked well.

I'm a bit slow on this puzzle, I think it could be dramatically sped up by just noting
the position of all of the + and letters as well as the directions you can travel from
them.  Then we would just need to find the next one on the same line, and get the
manhattan distance between the points to count steps.  Maybe I can work on that later.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

# dict to store answers
answer = {1: None, 2: None}


class Packet:
    """
    Class to represent our packet
    """

    def __init__(self, grid, pos, direction, **kwargs):
        """
        init function
        """
        # init position
        self.pos = pos
        # init direction
        self.direction = direction
        # init letters
        self.letters = []
        # init grid
        # need to test dict vs list for performance.  I think get_square would have to update
        # for list though
        self.grid = Grid(
            grid, start_pos=pos, coordinate_system="screen", datastore="dict", **kwargs
        )
        # reset self.pos (needed if changing the pos_type)
        self.pos = self.grid.pos
        # init steps
        self.steps = 0

    def __str__(self):
        """String for debugging"""
        my_str = f"{self.grid}"
        return my_str

    def get_square(self, pos):
        """get value of square"""
        return self.grid.map[pos]

    def step_forward(self):
        """
        Function to move forward or turn
        """
        # get current value
        current = self.get_square(self.pos)
        # is it a letter
        if current.isalpha():
            # add to letters
            self.letters.append(current)
        # is it not a +?
        if current != "+":
            # try moving forward
            if self.grid.move(self.direction, invalid=" "):
                # increment steps, and update position
                self.steps += 1
                self.pos = self.grid.pos
                return True
            # can't move forward and not a at a decision point
            # must be the end of the line
            return False
        # can't go forward
        # init options
        options = {
            "s": {"directions": ["e", "w"], "invalid": " |"},
            "n": {"directions": ["e", "w"], "invalid": " |"},
            "e": {"directions": ["n", "s"], "invalid": " -"},
            "w": {"directions": ["n", "s"], "invalid": " -"},
        }
        # get neighbors from grid
        neighbors = self.grid.get_neighbors(
            directions=options[self.direction]["directions"],
            invalid=options[self.direction]["invalid"],
        )
        # if only one option, take it
        if len(neighbors) == 1:
            # walk neighbors
            for direction in neighbors.keys():
                # try moving to neighbor
                if self.grid.move(direction):
                    # update direction
                    self.direction = direction
                    # increment steps
                    self.steps += 1
                    # update pos
                    self.pos = self.grid.pos
                    return True
        # if no neighbors, then end of the line
        if len(neighbors) == 0:
            print(f"end of the line: {self.pos}")
            return False
        # else, too many options, and we need code to try multiple paths
        # this doesn't seem to be the case with our input
        print(f"too many options: {self.pos}")
        return False


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # part 2, just return the answer
    if part == 2:
        return answer[2]
    # init my_map
    my_map = input_value
    # find start location
    start = (my_map[0].index("|"), 0)
    # init packet
    pack = Packet(my_map, start, "s")
    # init sentinel
    sentinel = 0
    # step forward until we can't
    while pack.step_forward():
        # increment sentinel
        sentinel += 1
        # check sentinel
        if sentinel > 100000:
            print("Breaking loop")
            break
    # store steps for part 2
    # I'm not sure why I'm off by one here, maybe revisit
    answer[2] = pack.steps + 1
    # return part1 answer
    return "".join(pack.letters)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 19)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
