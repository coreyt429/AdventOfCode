"""
Advent Of Code 2015 day 2

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def parse_input(lines):
    """
    Function to parse input
    """
    # Split each line by whitespace and remove the first element (the label)
    presents = []
    for line in lines:
        presents.append(line.split("x"))
    for present in presents:
        for idx, dimension in enumerate(present):
            present[idx] = int(dimension)
    return presents


def area_plus_side(present):
    """
    Function to calculate the surface area
    """
    present.sort()
    sides = []
    sides.append(2 * present[0] * present[1])  # l*w*2
    sides.append(2 * present[1] * present[2])  # w*h*2
    sides.append(2 * present[0] * present[2])  # l*h*2
    sides.append(present[0] * present[1])  # area of smallest side
    return sum(sides)


def ribbon(present):
    """
    Function to calculate ribbon length
    """
    # sort present dimensions so shortest sides are first
    present.sort()
    # calculate and return length
    return 2 * present[0] + 2 * present[1] + present[0] * present[1] * present[2]


def part1(parsed_data):
    """
    Funciton to solve part 1
    """
    retval = 0
    for present in parsed_data:
        retval += area_plus_side(present)
    return retval


def part2(parsed_data):
    """
    Function to solve part 2
    A present with dimensions 2x3x4 requires 2+2+3+3 = 10 feet of ribbon to wrap the present
    plus 2*3*4 = 24 feet of ribbon for the bow,
    for a total of 34 feet.
    """
    retval = 0
    for present in parsed_data:
        retval += ribbon(present)
    return retval


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015, 2)
    input_lines = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: part1, 2: part2}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](parse_input(input_lines))
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
