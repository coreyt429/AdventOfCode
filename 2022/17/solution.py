"""
Advent Of Code 2022 day 17

This one works, but I'm not really happy with part 2.

I ran it with 10,000 iterations printing the state where it
when a duplicate state comes out.

That let me capture the rock count, state, and height for a few
iterations so I could manually calculate the loop size, and height increment.

This works for my input, and I doubt it would work for the test data, or other inputs.

A proper solution should include the code that detects the loop, but it is late, so I'm
leaving it as is.

On the positive note, I did rewrite grid.get_map_size() to be more efficient.  That took part 1
from ~ 15 seconds to 1.6 seconds.  So I'm happy with that update, and feel it will speed
up some past solutions that I wasn't happy with performance on.

"""
# import system modules
import time
# import my modules
import aoc # pylint: disable=import-error
from grid import Grid # pylint: disable=import-error

class Rock():
    """Class to represent a falling rock"""

    movements = {
        "d": (0, -1),
        "l": (-1, 0),
        "r": (1, 0),
        "v": (0, -1),
        "<": (-1, 0),
        ">": (1, 0)
    }

    def __init__(self, grid, rocks, jets, state):
        """Init method"""
        self.state = state
        self.grid = grid
        self.rocks = rocks
        self.jets = jets
        self.position = self.find_position()
        self.shape = self.rocks[self.state["rock_idx"]]
        self.state["rock_idx"] = (self.state["rock_idx"] + 1) % len(self.rocks)
        self.points = self.build()
        # self.rocks.rotate(-1)
        # self.draw()

    def can_move(self, direction='d'):
        """Method to check to see if a rock can move"""
        for x_val, y_val in self.points:
            x_val += self.movements[direction][0]
            # hitting wall?
            if x_val < 0 or x_val > 6:
                return False
            y_val += self.movements[direction][1]
            # hitting bottom?
            if y_val < 0:
                return False
            # collision?
            if self.grid.get_point((x_val, y_val)) == '#':
                return False
        return True

    def move(self, direction='d'):
        """Method to move a rock"""
        if not self.can_move(direction):
            return False
        new_points = []
        for x_val, y_val in self.points:
            x_val += self.movements[direction][0]
            y_val += self.movements[direction][1]
            new_points.append((x_val, y_val))
        self.points = new_points
        return True

    def find_position(self):
        """Method to find initial position of a rock"""
        for point in self.grid:
            if self.grid.get_point(point) == '#':
                return (2, point[1] + 4)
        return (2, 3)

    def build(self):
        """Method to build the point collection for a rock"""
        points = []
        for x_val, y_val in self.shape:
            points.append(tuple([self.position[0] + x_val, self.position[1] + y_val]))
        return points

    def draw(self, char='@'):
        """Method to draw a rock"""
        for point in self.points:
            self.grid.set_point(point, char)
        self.grid.update()

    def undraw(self):
        """Method to undraw a rock"""
        self.draw('.')

    def settle(self):
        """Method to draw settled rock"""
        self.draw('#')

    def fire_jet(self):
        """Method to fire a jet to blow the rock left or right"""
        self.move(self.jets[self.state["jet_idx"]])
        self.state["jet_idx"] = (self.state["jet_idx"] + 1) % len(self.jets)

    def drop(self):
        """Method to drop a rock until it settles"""
        self.fire_jet()
        # while it can move down.
        while self.move('d'):
            self.fire_jet()
        self.settle()


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    rocks = (
        ((0, 0), (1, 0), (2, 0), (3, 0)),
        ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)),
        ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
        ((0, 0), (0, 1), (0, 2), (0, 3)),
        ((0, 0), (0, 1), (1, 0), (1, 1))
    )
    jets = list(input_value)
    state = {
        "jet_idx": 0,
        "rock_idx": 0,
    }
    grid = Grid(
        ".......",
        type="infinite",
        coordinate_system="cartesian",
        use_overrides=False,
        default_value="."
    )
    if part == 2:
        # begining of full repeat cycle, identified by manual inspection
        for _ in range(1908):
            rock = Rock(grid, rocks, jets, state)
            rock.drop()
        # this is our state at 1908, this is the beginning of the full repeat cycle
        # the height difference for a cycle is 2785, the height at 1908 is 3023
        # place this structure at  ((count - 1908) // 1745) * 2785 + 3023
        # then run from ((count - 1908) // 1745) * 2785 + 1908 to count
        iter_diff = 1000000000000 - 1908
        iter_count = iter_diff // 1745
        new_y_val = iter_count * 2785 + 3023
        new_iter = iter_count * 1745 + 1908
        for y_val, row in enumerate(reversed(str(grid).splitlines()[:5])):
            for x_val, char in enumerate(row):
                if char == '#':
                    grid.set_point((x_val, new_y_val - 4 + y_val), char)
        grid.update()
        # print(new_y_val, new_iter)
        # run the last few iterations to get the final count
        for _ in range(new_iter, 1000000000000):
            rock = Rock(grid, rocks, jets, state)
            rock.drop()
        # .#....#
        # ###...#
        # .#..###
        # .######
        # .###..#
        # 1595988538653 too low
        # 1595988538692 too high, two changes 1 added +1 iterationin case my count was off,
        #                                     2 grid.update.
        # 1595988538691 was correct, didn't need the +1 iteration, jsut teh grid.uipdate
        return grid.cfg["max"][1] + 1

    # seen = set()
    for _ in range(2022):
        # if str(state)  in seen:
        #     print(f"{counter}, {state}, {grid.cfg['max'][1]}")
        # seen.add(str(state))
        rock = Rock(grid, rocks, jets, state)
        rock.drop()
    return grid.cfg["max"][1] + 1

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022,17)
    input_data = my_aoc.load_text()
    # print(input_text)
    # input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {
        1: 1,
        2: 2
    }
    # dict to store answers
    answer = {
        1: None,
        2: None
    }
    # correct answers once solved, to validate changes
    correct = {
        1: 3224,
        2: 1595988538691
    }
    # dict to map functions
    funcs = {
        1: solve,
        2: solve
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
