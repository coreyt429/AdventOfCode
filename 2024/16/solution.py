"""
Advent Of Code 2024 day 16

"""
# import system modules
import time
from heapq import heappop, heappush

# import my modules
import aoc # pylint: disable=import-error
from grid import Grid # pylint: disable=import-error

def has_duplicates(test_tup):
    """Function to check for duplicates"""
    return len(test_tup) != len(set(test_tup))

def shortest_path(grid, start, goal):
    """Find all shortest paths with the minimum score in the maze."""
    heap = []
    best_paths = []  # Store all paths with the minimum score
    heappush(heap, (0, start, 'e', (start,)))  # Start state
    seen = {}
    min_path_score = float('infinity')

    while heap:
        current = {}
        current["score"], current["point"], current["direction"], current["path"] = heappop(heap)

        # Stop processing paths with scores exceeding the minimum score
        if current['score'] > min_path_score:
            continue

        # Check if we reached the goal
        if current["point"] == goal:
            if current['score'] < min_path_score:
                # New minimum score found
                min_path_score = current["score"]
                best_paths = [current['path']]
            elif current['score'] == min_path_score:
                # Add another valid path
                best_paths.append(current['path'])
            continue

        # Prevent revisits of the same state with a higher or equal score
        signature = (current["point"], current["direction"])
        if signature in seen and seen[signature] < current["score"]:
            continue
        seen[signature] = current["score"]

        # Explore neighbors
        neighbors = grid.get_neighbors(point=current["point"], directions=['n', 's', 'e', 'w'])

        # Forward movement
        forward_point = neighbors[current["direction"]]
        if forward_point not in current['path'] and grid.get_point(point=forward_point) != '#':
            heappush(
                heap,
                (
                    current['score'] + 1,
                    forward_point,
                    current["direction"],
                    current["path"] + (forward_point,)
                )
            )

        # Turning (add turn cost)
        turns = ['e', 'w'] if current["direction"] in ['n', 's'] else ['n', 's']
        for turn in turns:
            neighbor = neighbors[turn]
            if neighbor not in current['path'] and grid.get_point(point=neighbor) != '#':
                heappush(heap, (current['score'] + 1000, current["point"], turn, current["path"]))

    return min_path_score, best_paths

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return answer[part]
        # 541 too low (actually 542 was too low, 541 was my real answer that time)
    maze = Grid(input_value, use_overrides=False)
    start = None
    goal = None
    for point, char in maze.items():
        if char == 'S':
            start = point
        if char == 'E':
            goal = point
        if all([start is not None, goal is not None]):
            break
    score, paths = shortest_path(maze, start, goal)
    points = set()
    print(f"{len(paths)} paths")
    for path in paths:
        for point in path:
            points.add(point)
    answer[2] = len(points)
    return score

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024,16)
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
        1: None,
        2: None
    }
    # correct answers once solved, to validate changes
    correct = {
        1: 123540,
        2: 665
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
