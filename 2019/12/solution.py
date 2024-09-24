"""
Advent Of Code 2019 day 12

part 1 was pretty straight forward.

part 2, I realized quickly was an LCM solution.  I struggled for a bit, then looked to
reddit solutions The solution u/ConstantGazelle pointed out that the answer was to get
the cycle for X, Y, and Z repitition individually.  Then calculate the LCM of period[X],
period[Y], and period[Z].
"""
# import system modules
import time
import re
from itertools import permutations
import math
from functools import reduce

# import my modules
import aoc # pylint: disable=import-error

# axis ids
X=0
Y=1
Z=2

# regex to extract numbers
pattern_nums = re.compile(r'(-*\d+)')

def parse_input(lines):
    """
    Function to parse input
    """
    # init items
    items = []
    # iterate over lines
    for idx, line in enumerate(lines):
        # extract position
        position = [int(num) for num in pattern_nums.findall(line)]
        # append moon item
        items.append({"id": idx, "position": position, "velocity": [0, 0, 0]})
    # returm moon items
    return items

def moon_string(moon):
    """
    function to print moon data
    used in early debugging of move_moons
    """
    pos = moon["position"]
    vel = moon["velocity"]
    return f"pos=<x={pos[X]}, y={pos[Y]}, {pos[Z]}>, vel=<x={vel[X]}, y={vel[Y]}, z={vel[Z]}>"

def get_velocities(moons):
    """
    Function to calculate velocities
    """
    # iterate over pair permutations
    for moon_a, moon_b in permutations(moons, 2):
        # iterate over axes
        for axis in (X, Y, Z):
            # For example, if Ganymede(a) has an x position of 3,
            # and Callisto(b) has a x position of 5,
            # then Ganymede's(a) x velocity changes by +1 (because 5 > 3) and
            # Callisto's(b) x velocity changes by -1 (because 3 < 5).
            if moon_a["position"][axis] < moon_b["position"][axis]:
                moon_a["velocity"][axis] += 1
                moon_b["velocity"][axis] -= 1
            # However, if the positions on a given axis are the same, the velocity on that
            # axis does not change for that pair of moons.
    return moons

def move_moons(moons):
    """
    Function to move moons
    """
    # get velocities
    moons = get_velocities(moons)
    # iterate over moons
    for moon in moons:
        # iterate over axes
        for axis in (X, Y, Z):
            # update position
            moon["position"][axis] +=  moon["velocity"][axis]
    return moons

def potential_energy(moon):
    """
    Function to calculate potential energy
    """
    # A moon's potential energy is the sum of the absolute values
    # of its x, y, and z position coordinates.
    return sum(abs(val) for val in moon["position"])

def kinetic_energy(moon):
    """
    Function to calculate kinetic energy
    """
    # A moon's kinetic energy is the sum of the absolute values of its velocity coordinates.
    return sum(abs(val) for val in moon["velocity"])

def lcm_of_list(numbers):
    """
    Function to calculate LCM (least common multiple)
    of a list of values
    """
    return reduce(math.lcm, numbers)

def moon_state(moon):
    """
    function to get the state of a moon
    """
    return tuple([moon["id"],tuple(moon["position"]),tuple(moon["velocity"])])

def plane_state(moons, axis):
    """
    Function to get the state of an axis
    """
    # init state
    state = [axis]
    # iterate over moons
    for moon in moons:
        # add position to state
        state.append(moon["position"][axis])
        # add velocity to state
        state.append(moon["velocity"][axis])
    return tuple(state)

def calculate_energy(moons):
    """
    Funciton to calculate energy of moons
    """
    # init total
    total = 0
    # Then, it might help to calculate the total energy in the system.
    # iterate over moons
    for moon in moons:
        # The total energy for a single moon is its potential energy
        # multiplied by its kinetic energy.
        energy = potential_energy(moon) * kinetic_energy(moon)
        # add energy to total
        total += energy
    return total

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # parse input data
    moons = parse_input(input_value)
    # part 1
    if part == 1:
        # iterate 1000 times
        for _ in range(1000):
            # move moons
            moons = move_moons(moons)
        # return energy
        return calculate_energy(moons)
    # init closed set
    seen = set()
    # init counter
    counter = 0
    # init keep going
    keep_going = True
    # init period
    periods = {}
    # loop until done
    while keep_going:
        # iterate over axes
        for axis in [X, Y, Z]:
            # if we have already got the cycle for this axis, no need to get state
            if axis in periods:
                continue
            # get axis state
            state = plane_state(moons, axis)
            # Is this the first repeat for this axis?
            if state in seen and axis not in periods:
                # set period for axis
                periods[axis] = counter
                # if all 3 axes are set
                if len(periods) == 3:
                    # stop loop
                    keep_going = False
            else:
                # add to seen
                seen.add(state)
        # move moons
        moons = move_moons(moons)
        # increment counter
        counter += 1
    # return LCM
    return lcm_of_list(periods.values())

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019,12)
    input_lines = my_aoc.load_lines()
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
        1: 6220,
        2: 548525804273976
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
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
