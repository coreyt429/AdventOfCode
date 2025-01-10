"""
Advent Of Code 2024 day 20

Part 1, my first couple of attempts to find the cheats were not working.  They still exist
in the scratch pad if your curious.  After taking a break, I came back to it and realized
a linked list was the answer.  By converting the path to a linked list, I could easily
calculate the difference between the positions of two nodes in the path.

Part 2, saving for another day

"""
# import system modules
from collections import defaultdict
from functools import lru_cache

# import my modules
from aoc import AdventOfCode # pylint: disable=import-error
from grid import Grid, manhattan_distance # pylint: disable=import-error

def path_to_linked_list(path):
    """Function to convert a path list to linked node list"""
    linked_list = {}
    for i in range(len(path) - 1):
        linked_list[path[i]] = {
            'next': path[i+1],
            'point': path[i],
            'position': i,
            'cheat': None
        }
    linked_list[path[-1]] = {
        'next': None,
        'point': path[-1],
        'position': len(path) - 1,
        'cheat': None
    }
    return linked_list

def path_length(start, linked_list):
    """Function to calculate the length of a path starting at a given node"""
    # print(f"path_length({start}, linked_list)")
    length = -1 # start is not counted
    current = start
    while current is not None:
        # print(f"here current: {current}, next: {linked_list[current]['next']}")
        if linked_list[current]['cheat'] is not None:
            length += manhattan_distance(current, linked_list[current]['cheat'])
            current = linked_list[current]['cheat']
        else:
            length += 1
            current = linked_list[current]['next'] if current in linked_list else None
    return length

def apply_cheat(begin, end, linked_list):
    """Function to apply a cheat to a linked list"""
    linked_list[begin]['cheat'] = end

def clear_cheats(linked_list):
    """Function to clear all cheats from a linked list"""
    for node in linked_list.values():
        node['cheat'] = None

def find_cheats(position, target, linked_list, grid):
    """Function to find all possible cheats from a given position"""
    # print(f"find_cheats({position}, linked_list)")
    cheats = []
    for current in points_within_distance(position, distance=3):
        if current not in linked_list:
            continue
        if linked_list[current]['position'] - linked_list[position]['position'] > target:
            if is_valid_cheat(position, current, grid):
                cheats.append(current)
        current = linked_list[current]['next']
    return cheats

@lru_cache(maxsize=None)
def is_valid_cheat(point, cheat, grid):
    """Function to determine if a cheat is valid"""
    # Check if the manhattan distance is 2 or 3
    distance = manhattan_distance(point, cheat)
    # if distance not in [2, 3]:
    #     return False

    # Check if the path between point and cheat only passes through walls
    x_1, y_1 = point
    x_2, y_2 = cheat

    if x_1 == x_2:  # Same row
        for y_val in range(min(y_1, y_2) + 1, max(y_1, y_2)):
            if grid.get_point((x_1, y_val)) != '#':
                return False
    elif y_1 == y_2:  # Same column
        for x_val in range(min(x_1, x_2) + 1, max(x_1, x_2)):
            if grid.get_point((x_val, y_1)) != '#':
                return False
    else:  # Diagonal
        if distance == 2:
            if grid.get_point((x_1, y_2)) != '#' or grid.get_point((x_2, y_1)) != '#':
                return False
        elif distance == 3:
            if abs(x_1 - x_2) == 1:
                if grid.get_point((x_1, y_2)) != '#' or grid.get_point((x_2, y_1)) != '#':
                    return False
            else:
                if grid.get_point((x_1, y_2)) != '#' or grid.get_point((x_2, y_1)) != '#':
                    return False
    return True

@lru_cache(maxsize=None)
def points_within_distance(point, distance=3):
    """Function to return all points within a given distance of a point"""
    x_val, y_val = point
    points = []
    for i in range(-distance, distance + 1):
        for j in range(-distance, distance + 1):
            if abs(i) + abs(j) <= distance:
                points.append((x_val + i, y_val + j))
    return points

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return part
    target = 99
    grid = Grid(input_value, use_overrides=False)
    start, goal = None, None
    start = next(point for point, value in grid.items() if value == 'S')
    goal = next(point for point, value in grid.items() if value == 'E')
    initial_path = grid.shortest_paths(start, goal)[0]
    path_linked_list = path_to_linked_list(initial_path)
    cheat_stats = defaultdict(set)
    for point, node in path_linked_list.items():
        for cheat in find_cheats(point, target, path_linked_list, grid):
            if not is_valid_cheat(point, cheat, grid):
                continue
            # apply_cheat(point, cheat, path_linked_list)
            # length = path_length(start, path_linked_list)
            savings = path_linked_list[cheat]['position']
            savings -= node['position']
            savings -= manhattan_distance(point, cheat)
            if savings > target:
                cheat_stats[savings].add((point, cheat))
            # clear_cheats(path_linked_list)
    count = 0
    for size in sorted(cheat_stats.keys()):
        if size < 100:
            continue
        count += len(cheat_stats[size])
    # 1415 is too high
    # I wasn't subtracting the manhattan distance between the points from the savings
    return count

if __name__ == "__main__":
    aoc = AdventOfCode(2024,20)
    aoc.load_text()
    # aoc.load_list()
    # correct answers once solved, to validate changes
    aoc.correct[1] = 1404
    aoc.correct[2] = None
    aoc.funcs[1] = solve
    aoc.funcs[2] = solve
    aoc.run()
