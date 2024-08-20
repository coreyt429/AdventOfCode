"""
Advent Of Code 2018 day 11

Okay I did pretty well on my own, for part 1.

Part 2 needed some math that was rusty in my brain.

Then I saw this numpy solution from u/sciyoshi, and wanted to disect it

I think I have a pretty good grasp of it now, and hope I can remember
these tools if I need them again.

"""
# import system modules
import time
from functools import partial
import numpy
# import my modules
import aoc # pylint: disable=import-error

def get_power_level(x_val, y_val, serial_number):
    """
    Function to calculate power level of a cell
    
    Args:
        x_val, y_val: int() x/y coordinate of cell
        serial_number: int() serial number for grid
    
    Returns:
        power_level: int() result
    """
    # Find the fuel cell's rack ID, which is its X coordinate plus 10.
    rack_id = x_val + 10
    # Begin with a power level of the rack ID times the Y coordinate.
    power_level = rack_id * y_val
    # Increase the power level by the value of the grid serial number (your puzzle input).
    power_level += serial_number
    # Set the power level to itself multiplied by the rack ID
    power_level *= rack_id
    # Keep only the hundreds digit of the power level
    # (so 12345 becomes 3; numbers with no hundreds digit become 0).
    # strip to the left of hundreds digit
    power_level = power_level % 1000
    # zero to the right of hundreds digit
    power_level = power_level // 100
    # Subtract 5 from the power level.
    power_level -= 5
    return power_level

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # grab input and convert to int
    serial_number = int(input_value)
    # partial function to pass serial numver to power_level
    partial_func = partial(get_power_level, serial_number=serial_number)
    # build grid of powerlevels using numpy.fromfunction and our partial function
    grid = numpy.fromfunction(partial_func, (300, 300))
    # part 1
    if part == 1:
        # part 1 has fixed size of 3x3
        width = 3
        # sum up the grid values for width=3
        windows = sum(
            grid[
                x:x - width + 1 or None, y:y - width + 1 or None
            ] for x in range(width) for y in range(width)
        )
        # get max of window sums
        maximum = int(windows.max())
        # get location of max in the grid
        location = numpy.where(windows == maximum)
        # convert x/y values to int
        x_val = int(location[0][0])
        y_val = int(location[1][0])
        # return output string
        return ','.join(str(int(coord)) for coord in [x_val, y_val])
    # init previous_max
    previous_max = -1 * float('infinity')
    # for each width range
    for width in range(1, 300):
        # sum up the grid values for width
        windows = sum(
            grid[
                x:x - width + 1 or None, y:y - width + 1 or None
            ] for x in range(width) for y in range(width)
            )
        # get max of window sums
        maximum = int(windows.max())
        # get location of max in grid
        location = numpy.where(windows == maximum)
        # sample data maximum only had one peak
        # with my input, it had two peaks, so allowing
        # for a greater drop before breaking
        if maximum < previous_max - 100:
            # trip breaker to stop execution
            break
        # if we have a new max
        if maximum > previous_max:
            # update result
            result = (maximum, location[0][0], location[1][0], width)
            # update max
            previous_max = maximum
    # return output string
    return ','.join(str(int(num)) for num in result[1:])

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,11)
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
