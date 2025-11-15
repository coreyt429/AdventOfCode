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
import time

# import my modules
import aoc  # pylint: disable=import-error
from grid import linear_distance  # pylint: disable=import-error


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


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022, 9)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 6087, 2: 2493}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
