"""
Advent Of Code 2017 day 22

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error


class VirusCarrier:
    """
    class to represent VirusCarrier
    """

    def __init__(self, lines, pos=(1, 1), variant=1):
        self.variant = variant
        self.grid = Grid(lines, coordinate_system="cartesian", type="infinite")
        self.pos = pos
        self.grid.pos = self.pos
        self.stats = {
            "infected": 0,
            "cleaned": 0,
            "weakened": 0,
            "flagged": 0,
            "bursts": 0,
        }
        self.direction = "up"

    def activity_burst(self):
        """
        If the current node is infected, it turns to its right. Otherwise, it turns to its left.
        (Turning is done in-place; the current node does not change.)
        If the current node is clean, it becomes infected. Otherwise, it becomes cleaned.
        (This is done after the node is considered for the purposes of changing direction.)
        The virus carrier moves forward one node in the direction it is facing.
        """
        self.stats["bursts"] += 1
        if self.variant == 1:
            if self.grid.map[self.pos] == "#":
                self.turn("right")
                self.clean()
            else:
                self.turn("left")
                self.infect()
        else:
            if self.grid.map[self.pos] == "#":
                # If it is infected, it turns right.
                self.turn("right")
                # Infected nodes become flagged.
                self.flag()
            elif self.grid.map[self.pos] == "W":
                # Weakened nodes become infected.
                self.infect()
                # If it is weakened, it does not turn, and
                # will continue moving in the same direction.
            elif self.grid.map[self.pos] == "F":
                # If it is flagged, it reverses direction, and will go back the way it came.
                self.turn("reverse")
                # Flagged nodes become clean.
                self.clean()
            else:
                # If it is clean, it turns left.
                self.turn("left")
                # Clean nodes become weakened.
                self.weaken()
        self.move()

    def weaken(self):
        """weaken cell"""
        self.stats["weakened"] += 1
        self.grid.map[self.pos] = "W"

    def flag(self):
        """flag cell"""
        self.stats["flagged"] += 1
        self.grid.map[self.pos] = "F"

    def clean(self):
        """clean ccell"""
        self.stats["cleaned"] += 1
        self.grid.map[self.pos] = "."

    def infect(self):
        """infect cell"""
        self.stats["infected"] += 1
        self.grid.map[self.pos] = "#"

    def move(self):
        """move to next cell"""
        if self.grid.move(self.direction):
            self.pos = self.grid.pos

    def turn(self, direction):
        """turn in place"""
        turn_map = {
            "up": {"left": "left", "right": "right", "reverse": "down"},
            "left": {"left": "down", "right": "up", "reverse": "right"},
            "down": {"left": "right", "right": "left", "reverse": "up"},
            "right": {"left": "up", "right": "down", "reverse": "left"},
        }
        self.direction = turn_map[self.direction][direction]

    def __str__(self):
        """string"""
        return f"bursts: {self.stats['bursts']}, infected: {self.stats['infected']}"


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # The virus carrier begins in the middle of the map facing up.
    start_y = len(input_value) // 2
    start_x = len(input_value[0]) // 2
    carrier = VirusCarrier(input_value, pos=(start_x, start_y), variant=part)
    # print(carrier)
    # print()
    if part == 1:
        cycles = 10000
    else:
        cycles = 10000000
    for _ in range(cycles):
        carrier.activity_burst()
        # if part == 2:
        #    print(carrier)
    return carrier.stats["infected"]


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 22)
    # fetch input
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
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
