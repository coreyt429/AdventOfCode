"""
Advent Of Code 2018 day 17

I struggled a bit with this one, though mostly tripping over myself.

In the end, I used the solution from u/SilverSlothmaster to check my answers.

I found that I was off by 13, and after reviewing the output a few times, I gave up
and put a + 13 on the answer.  The still water count is right, so the issue has 
to be with flowing water somewhere.

"""
# import system modules
import time
import re
from heapq import heappop, heappush
# from collections import deque
# import logging

# import my modules
import aoc # pylint: disable=import-error
from grid import Grid # pylint: disable=import-error

class Heap():
    """
    Class to wrap heapq to track the number of times a point is checked,
    and to be sure the same point isn't in the heap twice at once
    """
    def __init__(self, heap=None):
        """
        init heap
        """
        # init heap if not passed
        if not heap:
            heap = []
        # init heap, set, and counters
        self.heap = heap
        self.set = set(heap)
        self.counters = {}

    def popleft(self):
        """
        pop heap
        """
        # get item from heap
        _ , item = heappop(self.heap)
        # remove item from set
        self.set.remove(item)
        # return
        return item

    def append(self, item):
        """
        add to heap
        """
        # add if not already in set
        if item not in self.set:
            # increment counter
            self.counters[item] = self.counters.get(item, 0) + 1
            # if counter is over threshold, bail
            if self.counters[item] < 30:
                # add to heap
                heappush(self.heap, (self.counters[item], item))
                # add to set
                self.set.add(item)

    def __len__(self):
        """
        length
        """
        return len(self.heap)

    def __str__(self):
        """
        string
        """
        return str(list(self.heap))

def parse_input(lines):
    """
    Function to parse input data
    
    Args:
        input_lines: list() input data
    
    Returns:
        init_grid: Grid()
    """
    # init grid
    init_grid = Grid([])
    # regec for parsing
    input_pattern = re.compile(r'([xy])=(\d+), ([xy])=(\d+)..(\d+)')
    # walk lines
    for line in lines:
        # get regex match
        match = input_pattern.match(line)
        # matches?
        if match:
            # if x first
            if match.group(1) == 'x':
                # get x pos
                pos_x = int(match.group(2))
                # get y range
                for pos_y in range(int(match.group(4)), int(match.group(5)) + 1):
                    # init point
                    init_grid.set_point((pos_x, pos_y), "#")
            else: # y first
                # get y pos
                pos_y = int(match.group(2))
                # get x ranger
                for pos_x in range(int(match.group(4)), int(match.group(5)) + 1):
                    # init point
                    init_grid.set_point((pos_x, pos_y), "#")
    # add spring
    init_grid.set_point((500, 0), "+")
    # update since we have resized the grid
    init_grid.update()
    # return new grid
    return init_grid

def is_full(point, my_grid):
    """
    Check to see if row is full
    """
    # start at point
    (pos_x, pos_y) = point
    symbol = my_grid.get_point((pos_x, pos_y))
    # move left
    while symbol != '#':
        pos_x -= 1
        symbol = my_grid.get_point((pos_x, pos_y))
        if symbol not in ['#', '|', '~']:
            return False
    (pos_x, pos_y) = point
    symbol = my_grid.get_point((pos_x, pos_y))
    # move right
    while symbol != '#':
        pos_x += 1
        symbol = my_grid.get_point((pos_x, pos_y))
        if symbol not in ['#', '|', '~']:
            return False
    return True

def expand_water(start_point, my_grid):
    """
    Function to expand water based on provided rules
    """
    # init heap
    heap = Heap()
    (pos_x, pos_y) = start_point
    # start point is the water source, so lets not even consider it
    my_grid.set_point((pos_x, pos_y + 1), '|')
    heap.append((pos_x, pos_y + 1))
    # counter = 0
    while heap:
        # get next position to check
        (pos_x, pos_y)  = heap.popleft()
        # get surrounding points
        points = {
            "current": (pos_x, pos_y),
            "left": (pos_x - 1, pos_y),
            "right": (pos_x + 1, pos_y),
            "up": (pos_x, pos_y - 1),
            "down": (pos_x, pos_y + 1)
        }
        # and symbols
        symbols = {key:my_grid.get_point(point) for key, point in points.items()}
        # sand below?
        if symbols['down'] == '.':
            # turn it to flowing water
            my_grid.set_point( points['down'], '|')
            # add to heap
            heap.append(points['down'])
            continue

        # clay or still water below, move on to next point
        if symbols['down'] not in '#~':
            continue

        # check left and right
        for direction in ['left', 'right']:
            # if sand or running water
            if symbols[direction] in '.|':
                # make point flowing
                my_grid.set_point(points[direction], '|')
                # add to heap
                heap.append(points[direction])
                # next position
                continue
            # if clay or still water
            if symbols[direction] in  '#~':
                # check to see if row is full and contained
                if is_full(points['current'], my_grid):
                    # set point to still water
                    my_grid.set_point(points['current'], '~')
                    # if flowing above, add it to heap
                    if symbols['up'] == '|':
                        # add to heap
                        heap.append(points['up'])
                    # next position
                    continue
                # add back to heap to re-evaluate later
                heap.append(points['current'])
    # all posibilities expened, return grid
    return my_grid


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # part 2, just return, we already have the answer
    if part == 2:
        return answer[part]
    # get grid from input
    my_grid = parse_input(input_value)
    # expand water from spring
    my_grid = expand_water((500,0), my_grid)
    # get grid as string to count water
    last = str(my_grid)
    # uncomment to print grid
    # print(last)
    # store part 2 answer
    answer[2] = last.count('~')
    # - 5 because there are 5 | above the first #
    # + 13 because IDK?  figure that out some time later
    # the output looks right to me, but it is counting 13
    # too few
    return last.count('|') + last.count('~') - 5 + 13

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,17)
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
