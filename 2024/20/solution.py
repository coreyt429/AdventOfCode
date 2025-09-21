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
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid, manhattan_distance  # pylint: disable=import-error


def path_to_linked_list(path):
    """Function to convert a path list to linked node list"""
    linked_list = {}
    for i in range(len(path) - 1):
        linked_list[path[i]] = {
            "next": path[i + 1],
            "point": path[i],
            "position": i,
        }
    linked_list[path[-1]] = {
        "next": None,
        "point": path[-1],
        "position": len(path) - 1,
    }
    return linked_list


def find_cheats(position, target, linked_list, grid, **kwargs):
    """Function to find all possible cheats from a given position"""
    distance = kwargs.get("distance", 3)
    part = kwargs.get("part", 1)
    cheats = []
    for current in points_within_distance(position, distance):
        if current not in linked_list:
            continue
        if (
            linked_list[current]["position"]
            - linked_list[position]["position"]
            - manhattan_distance(position, current)
            > target
        ):
            if part == 2 or is_valid_cheat(position, current, grid):
                cheats.append(current)
        # current = linked_list[current]["next"]
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
            if grid.get_point((x_1, y_val)) != "#":
                return False
    elif y_1 == y_2:  # Same column
        for x_val in range(min(x_1, x_2) + 1, max(x_1, x_2)):
            if grid.get_point((x_val, y_1)) != "#":
                return False
    else:  # Diagonal
        if distance == 2:
            if grid.get_point((x_1, y_2)) != "#" or grid.get_point((x_2, y_1)) != "#":
                return False
        elif distance == 3:
            if abs(x_1 - x_2) == 1:
                if (
                    grid.get_point((x_1, y_2)) != "#"
                    or grid.get_point((x_2, y_1)) != "#"
                ):
                    return False
            else:
                if (
                    grid.get_point((x_1, y_2)) != "#"
                    or grid.get_point((x_2, y_1)) != "#"
                ):
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
    distance = 3
    if part == 2:
        distance = 20
        # return part
    target = 99
    grid = Grid(input_value, use_overrides=False)
    # start, goal = None, None
    start = next(point for point, value in grid.items() if value == "S")
    goal = next(point for point, value in grid.items() if value == "E")
    path_linked_list = path_to_linked_list(grid.shortest_paths(start, goal)[0])
    cheat_stats = {1: defaultdict(set), 2: {}}
    for point, node in path_linked_list.items():
        # print(f"\r{point=}, position={node['position']}, of {len(path_linked_list)},", end="")
        for cheat in find_cheats(
            point, target, path_linked_list, grid, distance=distance, part=part
        ):
            if not part == 2 and not is_valid_cheat(point, cheat, grid):
                continue
            savings = (
                path_linked_list[cheat]["position"]
                - node["position"]
                - manhattan_distance(point, cheat)
            )
            if savings > target:
                cheat_stats[1][savings].add((point, cheat))
                cheat_stats[2][(point, cheat)] = max(
                    cheat_stats[2].get((point, cheat), 0), savings
                )
    count = 0
    if part == 2:
        for size in cheat_stats[2].values():
            if size >= 100:
                count += 1
        return count
    for size, cheat in cheat_stats[1].items():
        if size < 100:
            continue
        count += len(cheat)

    # 1415 is too high
    # I wasn't subtracting the manhattan distance between the points from the savings
    # part 2
    # 904905 is too low
    # 916903 is too low - dijkstra for cheat - really slow
    # 1010981 - bingo
    # 1029553 is too high - manhattan distance for cheat
    # 1141785 is too high
    return count


if __name__ == "__main__":
    aoc = AdventOfCode(2024, 20)
    aoc.load_text()
    # aoc.load_list()
    # correct answers once solved, to validate changes
    aoc.correct[1] = 1404
    aoc.correct[2] = 1010981
    aoc.funcs[1] = solve
    aoc.funcs[2] = solve
    aoc.run()
