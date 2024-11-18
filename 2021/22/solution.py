"""
Advent Of Code 2021 day 22

The first time I looked at this one, I was essentially trying to do part 2 first, by not reading
the 50x50x50 limit in part 1.

The second time, I realized that mistake, and made a working solution for part 1.

Then I made several failed solutions for part 2.  Gave up, and worked with ChatGPT to make even
worse solutions.

Checked the reddit solutions, and found one from u/Dullstar that used some concepts I was not
overly familiar with, so took on the task of understanding it as a learning experience.

  - collections.namedtuple - I had been exposed to named tuples in an online, class and never
        really utilized them
  - @property - This I was not aware of, and actually wanted this funcitionality for a few things,
        so good to learn
  - __repr__ - likewise, I was not previously exposed to this.  I like the concept, and fixed this
        one to accurately reproduce the object in eval()

The only other thing in this solution that I was totally overlooking in my attempts, was to reverse
the instructions so you don't have to keep track of the stack below the current cube.

"""
# import system modules
import time
import re
import math
import operator
import itertools
import collections


# import my modules
import aoc # pylint: disable=import-error


Point = collections.namedtuple("Point", ["x", "y", "z"])
Instruction = collections.namedtuple("Instruction", ["value", "cuboid"])

class Cuboid:
    """Class to represent a Cuboid"""
    def __init__(self, corner1: Point, corner2: Point):
        """Init method"""
        self.corner_1: Point = corner1
        self.corner_2: Point = corner2

    def __repr__(self):
        """object representation method"""
        return f"Cuboid({repr(self.corner_1)},{repr(self.corner_2)})"

    def is_valid(self) -> bool:
        """Method to determine if a Cuboid is ordered correctly"""
        return all(
            (c_1 < c_2 for c_1, c_2 in zip(self.corner_1, self.corner_2))
        )

    @property
    def volume(self):
        """Method to calculate the volume of a cuboid"""
        return math.prod(
            (c_2 - c_1 + 1 for c_1, c_2 in zip(self.corner_1, self.corner_2))
        )

def cuboid_get_overlap(cube_a: Cuboid, cube_b: Cuboid) -> Cuboid or None:
    """Function to compare two Cuboids and return the overlapping Cuboid"""
    # I'm not sure about a good way to explain where this formula comes from other than to draw
    # it out with squares (it'll extend out to 3 dimensions trivially), but if we do this process,
    # and we get a cuboid that fits the format that Cuboid.is_valid() expects in order for it to
    # return True, then it's the cuboid that describes where the overlap occurs, while if it
    # returns False, then that tells us there's no overlap and we can safely discard the cuboid we
    # found.
    overlap = Cuboid(
        Point(
            max(cube_a.corner_1.x, cube_b.corner_1.x),
            max(cube_a.corner_1.y, cube_b.corner_1.y),
            max(cube_a.corner_1.z, cube_b.corner_1.z)),
        Point(
            min(cube_a.corner_2.x, cube_b.corner_2.x),
            min(cube_a.corner_2.y, cube_b.corner_2.y),
            min(cube_a.corner_2.z, cube_b.corner_2.z))
    )
    return overlap if overlap.is_valid() else None

pattern_input = re.compile(
    r'(on|off) x=(\-*\d+)\.\.(\-*\d+),y=(\-*\d+)\.\.(\-*\d+),z=(\-*\d+)\.\.(\-*\d+)'
    )


def parse_data(lines):
    """Function to parse input data for part 1"""
    data = []
    for line in lines:
        values = pattern_input.findall(line)[0]
        data.append({
            'state': values[0],
            'x_range': (int(values[1]), int(values[2])),
            'y_range': (int(values[3]), int(values[4])),
            'z_range': (int(values[5]), int(values[6])),
            'points': points_in_cube(
                    (int(values[1]), int(values[2])),
                    (int(values[3]), int(values[4])),
                    (int(values[5]), int(values[6]))
            )
        })
    return data

def parse_input(lines: list) -> list[Instruction]:
    """function to parse input for part 2"""
    instructions = []
    for line in lines:
        if match := pattern_input.search(line):
            value = match[1] == "on"
            point_1 = Point(int(match[2]), int(match[4]), int(match[6]))
            point_2 = Point(int(match[3]), int(match[5]), int(match[7]))
            # nice check to be sure the input is what we expected.  I was just using
            # min/max everywhere, but this lets us trust the input
            assert point_1 == Point(
                min(point_1.x, point_2.x), min(point_1.y, point_2.y), min(point_1.z, point_2.z)
                ), \
                "Input data ordering doesn't comply with expected min..max format"
            assert point_2 == Point(
                max(point_1.x, point_2.x), max(point_1.y, point_2.y), max(point_1.z, point_2.z)
                ), \
                "Input data ordering doesn't comply with expected min..max format"
            # Commented this out, because I don't agree that the +1 should be here
            # added it in the volume calculation instead
            # point_2 = Point(point_2.x + 1, point_2.y + 1, point_2.z + 1)
            cuboid = Cuboid(point_1, point_2)
            instructions.append(Instruction(value, cuboid))
        else:
            # Complain if the assumption regarding the order of inputs is violated so those
            # values aren't just silently discarded.
            assert False, f"Error reading line: {line} -- are the coordinates out of order?"
    return instructions

def points_in_cube(*ranges):
    """Function to count the points in a cube"""
    return math.prod((abs(operator.sub(*range)) + 1 for range in ranges))

def cubes_overlap(c_1, c_2):
    """Function to determine if two cubes overlap"""
    overlap = get_overlap(c_1, c_2)
    if not overlap:
        return False
    return True

def get_overlap(c_1, c_2):
    """Function to return the overlap of two cubes"""
    overlap = {}
    for dim in ['x_range', 'y_range', 'z_range']:
        if (
            min(c_1[dim]) <= max(c_2[dim]) and max(c_1[dim]) >= min(c_2[dim])
        ):
            overlap[dim] = (
                max(min(c_1[dim]), min(c_2[dim])),
                min(max(c_1[dim]), max(c_2[dim]))
            )
        else:
            return {}
    return overlap

def find_overlapping_cubes(cubes):
    """Function to find overlapping cubes from a cube list"""
    overlaps = {}
    for c_1, c_2 in itertools.combinations(range(len(cubes)), 2):
        if cubes_overlap(cubes[c_1], cubes[c_2]):
            overlap = get_overlap(cubes[c_1], cubes[c_2])
            overlap_id = tuple(sorted((c_1, c_2)))
            overlap['points'] = points_in_cube(
                overlap['x_range'],
                overlap['y_range'],
                overlap['z_range']
            )
            overlaps[overlap_id] = overlap
    return overlaps

def initialization_test(cubes):
    """Function to run intialization test (part 1)"""
    target = {
        "x_range": (-50, 50),
        "y_range": (-50, 50),
        "z_range": (-50, 50)
    }

    answer_cube = {}
    for cube in cubes:
        if not cubes_overlap(cube, target):
            continue
        overlap = get_overlap(cube, target)
        for x_val in range(min(overlap['x_range']), max(overlap['x_range']) + 1):
            for y_val in range(min(overlap['y_range']), max(overlap['y_range']) + 1):
                for z_val in range(min(overlap['z_range']), max(overlap['z_range']) + 1):
                    answer_cube[(x_val, y_val, z_val)] = cube['state']
    counter = collections.Counter(answer_cube.values())
    return counter.get('on')

def run_instructions(instructions: list[Instruction]):
    """Function to execut instruction list.  Mostly untouched rom borrowed solution"""
    placed = []
    volume = 0
    # Reversing the list makes it so we don't have to treat OFF values any differently from ON
    # values, except their volume doesn't change the total when they're first encountered: the
    # last cuboid always contributes its full volume to the final volume, then each subsequent
    # ON cuboid contributes whatever portion of its volume doesn't overlap with any other cuboids.
    # Thus, both ON and OFF cuboids cut into the contributions by earlier cuboids (the ones we
    # visit last) in identical ways. If we went forward, we'd have to keep closer track of
    # ON vs. OFF when determining how much extra volume each additional cuboid contributes.
    #
    # In the special case where all the cuboids are ON (well, probably OFF too, but that doesn't
    # actually happen), then it doesn't make a difference. This comes up when we determine how
    # much to subtract from a given cuboid's volume later.
    for instruction in reversed(instructions):
        # We only need to add the volume if the cuboid is ON, i.e. instruction.value == True;
        # otherwise we don't need to worry about the volume.
        if instruction.value:
            overlaps = []
            for cuboid in placed:
                if (
                    overlapping := cuboid_get_overlap(cuboid, instruction.cuboid)
                ) is not None:
                    # Since we'll be checking these overlaps for more overlaps to get the volume
                    # of overlap, we want to always treat the result of cuboid_get_overlap as ON.
                    # If it were OFF we'd fail to cut into the volume.
                    overlaps.append(Instruction(True, overlapping))
            # The overlaps can be overlapping themselves, so we'll need to handle that to
            # figure out exactly how much we should be subtracting from the volume.
            volume += instruction.cuboid.volume - run_instructions(overlaps)
        # The cuboid still needs to be remembered either way because both ON and OFF cuboids
        # already placed will both mask pieces from whatever cuboids are behind them.
        placed.append(instruction.cuboid)
    assert volume >= 0, "Negative volume shouldn't happen"
    return volume


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        cubes = parse_data(input_value)
        return initialization_test(cubes)
    instructions = parse_input(input_value)
    return run_instructions(instructions)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021,22)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {
        1: 1,
        2: 2
    }
    # dict to store answers
    answer = {
        1: 577205,
        2: 1197308251666843
    }
    # correct answers once solved, to validate changes
    correct = {
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
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
