"""
Advent Of Code 2020 day 12

Part 1 was quick and easy.  Part 2, I needed to revisit some math skills.

I initially laid out test points on paper, and came up with the swap x/y and
adjust signs based on quadrant method since we are working in 90 degree increments.
A quick google search reinforced that this is the easy way to do it manually.

We aren't doing it manually, and there is a better mathematical solution. So,
I dropped the 90 degrees from the search to learn how to move it an arbitrary
angle.  That method is a lot simpler to read in code, and the math module is
better at sine and cosine than me.  So this method makes more sense in code.

"""

# import system modules
import time
import math

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid, manhattan_distance  # pylint: disable=import-error


class Ship(Grid):
    """
    Class to represent our ship on the ocean (Grid)
    """

    headings = {0: "e", 180: "w", 90: "s", 270: "n"}

    def __init__(self):
        """init method"""
        super().__init__(
            "S",
            coordinate_system="cartesian",
            type="infinite",
            ob_default_value=".",
            default_value=".",
        )
        # pylint didn't like me using self.pos without defining it here
        # likely due to pylint not reading Grid from grid.
        # no harm in reassigning here, so rolling with it.
        self.pos = (0, 0)
        self.heading = 0
        self.move_handler = {
            "F": lambda distance: [
                self.move(self.headings[self.heading]) for _ in range(distance)
            ],
            "N": lambda distance: [self.move("n") for _ in range(distance)],
            "S": lambda distance: [self.move("s") for _ in range(distance)],
            "E": lambda distance: [self.move("e") for _ in range(distance)],
            "W": lambda distance: [self.move("w") for _ in range(distance)],
            "L": lambda degrees: self.set_heading((self.heading - degrees) % 360),
            "R": lambda degrees: self.set_heading((self.heading + degrees) % 360),
        }
        self.waypoint = (10, 1)

    def set_heading(self, heading):
        """method to set heading"""
        self.heading = heading

    def goto_waypoint(self):
        """method to move the ship to the next waypoint"""
        x_val, y_val = self.pos
        x_val += self.waypoint[0]
        y_val += self.waypoint[1]
        self.pos = (x_val, y_val)

    def rotate_point(self, point, degrees):
        """Method to rotate the waypoint around the ship"""
        radians = math.radians(degrees)
        x_val, y_val = point
        new_x_val = (x_val * math.cos(radians)) - (y_val * math.sin(radians))
        new_y_val = (y_val * math.cos(radians)) + (x_val * math.sin(radians))
        return (round(new_x_val), round(new_y_val))

    def move_waypoint(self, command, magnitude):
        """Method to move the waypoint relative to the ship"""
        x_val, y_val = self.waypoint
        offsets = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
        # north, south, east, and west we simply increment x or y
        if command in offsets:
            x_val += offsets[command][0] * magnitude
            y_val += offsets[command][1] * magnitude
        # right and left, we rotate around the ship
        elif command == "R":
            x_val, y_val = self.rotate_point(self.waypoint, -1 * magnitude)
        elif command == "L":
            x_val, y_val = self.rotate_point(self.waypoint, magnitude)
        self.waypoint = (x_val, y_val)

    def make_move(self, instruction, mode=1):
        """Method to process move instruction"""
        # print(f"make_move(self, {instruction}, {mode})")
        command = instruction[0]
        magnitude = int(instruction[1:])
        # Part/mode 1 simple movement commands
        if mode == 1:
            self.move_handler[command](magnitude)
            return
        # Part/mode 2 waypoint commands
        if command == "F":
            for _ in range(magnitude):
                self.goto_waypoint()
            return
        # mode 2 and not moving to waypoint, so lets move the waypoint
        self.move_waypoint(command, magnitude)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # Starting point is (0, 0)
    origin = (0, 0)
    ship = Ship()
    for instruction in input_value:
        ship.make_move(instruction, part)
        # print(ship.pos, ship.waypoint)
    # ship.update()
    # print(ship.pos, ship)
    # 49186 too low (correct on test data)
    # 78826 too low (flipped L and R, incorrect on test data)
    # What is the Manhattan distance between that location and the ship's starting position?
    return manhattan_distance(origin, ship.pos)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020, 12)
    input_lines = my_aoc.load_lines()
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 1838, 2: 89936}
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
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
