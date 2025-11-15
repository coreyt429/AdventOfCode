"""
Advent Of Code 2019 day 11

This one was fun.  For once I didn't have to tweak IntCodeComputer much.

Robot() extends Grid(), and adds an IntCodeComputer() for logic

I did need to tweak Grid() a bit.  get_point I added an early check to see
if the point exists and has a value.  Without running frequent update() calls,
the existing logic was letting OOB override the point actually existing. Previous
puzzles have shown that update() is slow, and should only be run when needed (before
iteration, or string functions (__str__ iterates the Grid)).  Otherwise, on an
infinite grid, we should be able to just move freely, and set arbitrary points.
Once a point is set, we should get its value, not a default_value or ob_default_value.
Hopefully this fix doesn't break any old puzzles, but I still have todo item to check
anything that uses Grid() to be sure it wasn't broken by previous updates.

I grabbed the screen reading code from 2016.8, and modified it to "OCR" the part 2
output.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error
from intcode import IntCodeComputer  # pylint: disable=import-error,wrong-import-order


class Robot(Grid):
    """Class to represent a robot"""

    # init color map
    colors = {".": 0, 0: ".", "#": 1, 1: "#"}
    # init directions
    directions = ["n", "e", "s", "w"]

    def __init__(self, program):
        """
        Init Method
        """
        super().__init__(
            ["."], coordinate_system="cartesian", type="infinite", use_overrides=False
        )
        # set default_value ob_default_value to black.
        self.cfg["default_value"] = "."
        self.cfg["ob_default_value"] = "."
        # The robot starts facing up.
        self.direction = "n"
        # init IntCodecomputer
        self.icc = IntCodeComputer(program)
        # redefine self.icc.output.  It is None by default
        self.icc.output = []
        # init set of painted points
        self.painted = set()

    def process_square(self):
        """
        Method to process a square the robot enters
        """
        # The program uses input instructions to access the robot's camera:
        # provide 0 if the robot is over a black panel or 1 if the robot is over a white panel.
        initial_color = self.get_point(self.pos, ".")
        # print(f"Current square {self.pos} is '{initial_color}': {self.colors[initial_color]}")
        self.icc.inputs.append(self.colors[initial_color])
        # Then, the program will output two values:
        while len(self.icc.output) < 2:
            if not 0 <= self.icc.ptr < len(self.icc.program):
                # print(f"ptr: {self.icc.ptr} is OOB")
                break
            self.icc.step()
        # print(f"outputs: {self.icc.output}")
        if self.icc.output:
            # First, it will output a value indicating the color to paint
            # the panel the robot is over:
            self.paint(color=self.icc.output.pop(0))
        if self.icc.output:
            # Second, it will output a value indicating the direction the robot should turn:
            self.turn(direction=self.icc.output.pop(0))
            # After the robot turns, it should always move forward exactly one panel.
            self.move(self.direction)
            # print(f"Moved, new location: {self.pos}")
            # curious why this is needed, but we'll roll with it.
            # it is a known slow process though, so we may speedup if we can kill it.
            # I suspect it has to do with neighbor selection in self.move()
            # self.update()
            # print(self)

    def paint(self, color):
        """
        Method to paint a square
        Args:
            color: int() 0 means to paint the panel black, and 1 means to paint the panel white.
        """
        # set current location point based on color map
        # print(f"painting {self.pos}: {self.colors[color]}")
        self.set_point(self.pos, self.colors[color])

        # add current location to painted
        self.painted.add(self.pos)

    def turn(self, direction):
        """
        Method to turn robot
        """
        # 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.
        # convert direction - to direction -1
        if direction == 0:
            direction = -1
        # get index of current directions
        curr_idx = self.directions.index(self.direction)
        # add offset and normalize to valid index
        new_idx = (curr_idx + direction) % 4
        # get new_direction
        new_direction = self.directions[new_idx]
        # print(f"direction {direction}, from {self.direction} to {new_direction}")
        self.direction = new_direction

    def get_reg_id(self):
        """
        Function to read registration id
        """
        input_string = str(self)
        # Split the string into lines
        lines = input_string.replace(".", " ").strip().split("\n")

        # Define the width and height of each character
        char_width = 5
        # needed for fix below, for strings ending in O (maybe other letters)
        # char_height = 6  # Including the space between rows

        # Calculate the number of characters in the message
        num_chars = len(lines[0]) // char_width

        # Initialize the result string
        result = ""
        # printed output to covert
        # .#....###....##.#..#.####.#..#.#....#..#...
        # .#....#..#....#.#..#.#....#.#..#....#..#...
        # .#....###.....#.####.###..##...#....####...
        # .#....#..#....#.#..#.#....#.#..#....#..#...
        # .#....#..#.#..#.#..#.#....#.#..#....#..#...
        # .####.###...##..#..#.####.#..#.####.#..#...
        # LBJHEKLH
        char_map = {
            "####  #    ###  #    #    ####": "E",
            "#     #    #    #    #    ####": "L",
            "#  #  #  # #### #  # #  # #  #": "H",
            "###   #  # ###  #  # #  # ### ": "B",
            "  ##     #    #    # #  #  ## ": "J",
            "#  #  # #  ##   # #  # #  #  #": "K",
        }
        # Iterate through each character
        for i in range(num_chars):
            # Extract the 5x5 grid for this character
            char_grid = [line[i * char_width : (i + 1) * char_width] for line in lines]
            # Convert the grid to a single string for easier comparison
            char_string = "".join(char_grid)
            # the last O was missing a couple spaces, issue was in a previous
            # puzzle and didn't affect this one, leaving in case it is needed in the
            # future
            # while len(char_string) < char_height*char_width:
            #     char_string += ' '
            # match to char_map
            # print(f"[{char_string}]")
            result += char_map.get(char_string, "?")
        return result


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init robot
    robot = Robot(input_value)
    # part 2
    if part == 2:
        # start on white instead
        robot.set_point(robot.pos, "#")
    # while program is on a valid instruction
    while 0 <= robot.icc.ptr < len(robot.icc.program):
        # process square
        robot.process_square()
    if part == 2:
        robot.update()
        # print(robot)
        return robot.get_reg_id()
    # part 1
    return len(robot.painted)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019, 11)
    input_text = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 2021, 2: "LBJHEKLH"}
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
