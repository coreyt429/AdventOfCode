"""
Advent Of Code 2019 day 6

This one was pretty easy.  Part 1, used a simple class structure
to establish parent/child relationships, then just had calc_orbits
recurse the tree to update values.  There are some unnecessary redundant
calculations, and it runs in 0.04 seconds, so not worth the effort
to reduce these.

Part 2, had to add __lt__ to the class to use heapq for Dijkstra
algorithm.  I probably should have used networkx here, and again
it runs in 0.05 seconds with a manual Dijkstra solution so I'll take
it as good that I remember teh algorithm.
"""
# import system modules
import time
from heapq import heappop, heappush

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

    def __lt__(self, other):
        """less than, needed for heapq"""
        return self.oid < other.oid

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


def shortest_path(start, goal):
    """
    Function to find shortest path
    """
    # init heap
    heap = []
    # init visited
    visited = set()
    # add start point
    heappush(heap, (0, start))
    # init min_steps
    min_steps = float('infinity')
    # process heap
    while heap:
        # get next item
        steps, current = heappop(heap)
        # did we find the end?
        if current == goal:
            # update min_steps
            min_steps = min(min_steps, steps)
            # next item
            continue

        # have we already processed this node?
        if current in visited:
            # next item
            continue

        # have we gone too far?
        if steps > min_steps:
            # next item
            continue

        # add to visited
        visited.add(current)
        # add parent
        if current.parent:
            heappush(heap, (steps + 1, current.parent))
        # add children
        for child in current.children:
            heappush(heap, (steps + 1, child))
    return min_steps

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # parse input
    objects = load_objects(input_value)
    # orbit_count = objects['COM'].calc_orbits()
    orbit_count = 0
    for obj in objects.values():
        # orbit_count += obj.direct_orbits + obj.indirect_orbits
        orbit_count += obj.calc_orbits()
    # part 2
    if part == 2:
        # return shortest_path
        return shortest_path(
            objects['YOU'].parent,
            objects['SAN'].parent
        )
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
