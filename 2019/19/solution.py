"""
Advent Of Code 2019 day 19

Part 1 was easy, Grid() + IntCodeComputer() quickly mapped it out.

Part 2 was a bit tricker.  I established a pattern that held through the first
250+ lines, and thought I had a path to a mathematical solution.  However something
changed in the pattern after that.

Not seeing a quick math solution, that left me with actually scanning, which was
time consuming.  So I kicked off a big scan and took a break.  When I got back,
I searched for '#'*100 in the scan to see where our potential search space was.
Then worked on tweaking my search to minimize intcode processing.

The final solution runs reasonably fast enough, optimizations for part 2 also sped
up part 1 significantly:

(base) PS AdventOfCode> run
Part 1: 197, took 0.31675004959106445 seconds
Part 2: 9181022, took 7.902804851531982 seconds
"""
# import system modules
import time

# import my modules
from intcode import IntCodeComputer # pylint: disable=import-error
import aoc # pylint: disable=import-error
from grid import Grid # pylint: disable=import-error

class Drone(Grid):
    """
    Class to represent drone

    subclass of Grid() with bolted on IntCodeComputer() for processing intcode input
    """

    def __init__(self, program, height=10, width=10):
        """Init"""
        start_map = '.'
        super().__init__(start_map, use_overrides=False, default_value='.')
        self.icc = IntCodeComputer(program)
        self.icc.output = []
        self.scan_position((0,0))
        self.scan_position((height - 1,width - 1))
        self.update()

    def scan_position(self, position):
        """
        Method to scan a particular location
        """
        tiles = '.#'
        # Retore icc to initial state each time
        self.icc.restore()

        for value in position:
            self.icc.inputs.append(value)

        while not self.icc.output and 0 <= self.icc.ptr < len(self.icc.program):
            self.icc.step()

        if self.icc.output:
            result = self.icc.output.pop(0)
            self.set_point(position, tiles[result])

    def scan_row(self, y_val):
        """
        Method to scan a particular row
        
        To minimize scan time, we only look at specific rows.
        """
        line_dict = {}
        # start at a position known to me to the right of the beam x=y+1
        x_val = y_val + 1
        point = (x_val , y_val)
        self.scan_position(point)
        # Here we use two passes. First scan until the drone is in the beam,
        # then scan until the drone exits the beam
        for value in '#.':
            while x_val >= 0 and self.get_point(point) != value:
                x_val -= 1
                if x_val < 0:
                    continue
                point = (x_val , y_val)
                self.scan_position(point)
                # store value in line_dict t quickly reconstruct for return value
                line_dict[point] = self.get_point(point)
        line = ''
        for x_val in range(self.cfg['min'][0], self.cfg['max'][0] + 1):
            line += line_dict.get((x_val, y_val), '.')
        return line

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        # However, you'll need to scan a larger area to understand the shape of the beam.
        drone = Drone(input_value, 50, 50)
        for row in range(50):
            drone.scan_row(row)
        # How many points are affected by the tractor beam in the 50x50 area closest to the emitter?
        return str(drone).count('#')
    # Find the 100x100 square closest to the emitter that fits entirely within the tractor beam;
    # within that square, find the point closest to the emitter.
    # manual inspection of a scan showed that the answer should be in a 1150 x 1150 grid
    size=1150
    drone = Drone(input_text, size, size)
    target='#'*100
    # manual inspection also showed that it would not be in the first 1000 rows
    for y_val in range(1000, size + 1):
        # scan each row, if it has target in it, then scan the last row of the potential box
        # if both left hand corners of our potential box are '#', then we found the answer.
        line = drone.scan_row(y_val)
        if target in line:
            drone.scan_row(y_val + 99)
            point_1 = (line.rindex(target), y_val)
            point_3 = (line.rindex(target), y_val + 99)
            if drone.get_point(point_1) == drone.get_point(point_3) == '#':
                break
    # What value do you get if you take that point's X coordinate,
    # multiply it by 10000, then add the point's Y coordinate?
    return point_1[0]*10000 + point_1[1]

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019,19)
    input_text = my_aoc.load_text()
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
        1: 197,
        2: 9181022
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
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
