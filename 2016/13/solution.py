"""
Advent Of Code 2016 day 13

"""
from heapq import heappop, heappush
import aoc # pylint: disable=import-error

def is_wall(point,seed):
    """
    Function to determine if a point is a wall or open space
    Find x*x + 3*x + 2*x*y + y + y*y.
    Add the office designer's favorite number (seed).
    Find the binary representation of that sum; count the number of bits that are 1.
    If the number of bits that are 1 is even, it's an open space.
    If the number of bits that are 1 is odd, it's a wall.
    """
    point_x,point_y = point
    int_value = point_x**2 + 3*point_x + 2*point_x*point_y + point_y + point_y**2
    int_value +=seed
    one_count = bin(int_value)[2:].count('1')
    return one_count % 2 == 1

def neighbors(point,seed):
    """
    Funcition to return valid neighbors for a point
    """
    set_neighbors = set()
    for p_x in [point[0]+1,point[0]-1]:
        if p_x >= 0:
            if not is_wall((p_x,point[1]),seed):
                set_neighbors.add((p_x,point[1]))

        for p_y in [point[1]+1,point[1]-1]:
            if p_y >= 0:
                if not is_wall((point[0],p_y),seed):
                    set_neighbors.add((point[0],p_y))
    return set_neighbors

def solve(start=(1,1), seed=10, target=(7,4)):
    """
    Function to dolve part1
    """
    visited = set()
    heap = []
    heappush(heap,(0,start,()))
    min_steps = float('infinity')
    while heap:
        steps, point, path = heappop(heap)
        visited.add(point)
        if point == target:
            if steps < min_steps:
                min_steps = steps
        else:
            new_path = tuple(list(path) + [point])
            for neighbor in neighbors(point, seed):
                if neighbor not in visited:
                    heappush(heap,(steps+1, neighbor, new_path))
    return min_steps

#How many locations (distinct x,y coordinates, including your starting
#location) can you reach in at most 50 steps?
def solve2(start=(1,1), seed=10):
    """
    Function to solve part 2
    """
    visited = set()
    heap = []
    heappush(heap,(0,start))
    while heap:
        steps, point = heappop(heap)
        if steps > 50:
            continue
        visited.add(point)
        for neighbor in neighbors(point, seed):
            if neighbor not in visited:
                heappush(heap,(steps+1, neighbor))
    return len(visited)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016,13)
    print(f"Part 1: {solve((1,1),1358,(31,39))}")
    print(f"Part 2: {solve2((1,1),1358)}")
