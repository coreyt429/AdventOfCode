"""
Advent Of Code 2019 day 6

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

class CelestialObject():
    """
    Class to represent celestial objects
    """
    def __init__(self, oid):
        """init"""
        self.oid = oid
        self.parent = None
        self.children = set()
        self.direct_orbits = 0
        self.indirect_orbits = 0

    def orbits(self, other):
        """Method to set orbit for a CE"""
        self.parent = other
        other.has_orbiter(self)

    def has_orbiter(self, other):
        """Method to add orbiter to a CE"""
        self.children.add(other)

    def calc_orbits(self):
        """Method to calculate orbits for a CE"""
        self.direct_orbits = len(self.children)
        self.indirect_orbits = 0
        for child in self.children:
            self.indirect_orbits += child.calc_orbits()
        return self.direct_orbits + self.indirect_orbits

    def __str__(self):
        """string"""
        return f"{self.oid}: direct {self.direct_orbits}, indirect {self.indirect_orbits}"

def load_objects(lines):
    """
    Function to parse input and load objects
    """
    # init empty set
    objects = {}
    # walk lines
    for line in lines:
        # get parent and child ids
        parent_id, child_id = line.split(')')
        # create objects if they don't already exist
        for obj_id in (parent_id, child_id):
            if obj_id not in objects:
                objects[obj_id] = CelestialObject(obj_id)
        # add parent child relationship
        objects[child_id].orbits(objects[parent_id])
    # return set
    return objects

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        # some madness
        return part
    objects = load_objects(input_value)
    # orbit_count = objects['COM'].calc_orbits()
    orbit_count = 0
    for obj in objects.values():
        # orbit_count += obj.direct_orbits + obj.indirect_orbits
        orbit_count += obj.calc_orbits()
    return orbit_count

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019,6)
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
