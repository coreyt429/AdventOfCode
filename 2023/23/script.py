import sys
from functools import cache
from collections import defaultdict, deque


def parse_input(data):
    # Split the data into lines
    lines = data.strip().split("\n")
    grid = []
    for line in lines:
        grid.append(tuple(list(line)))
    return tuple(grid)


def print_map(grid, label, path=[]):
    print(f"{label}:")
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if row == 0 and grid[row][col] == ".":
                print("S", end="")
            elif path and (row, col) in path:
                print("O", end="")
            else:
                print(grid[row][col], end="")
        print()
    print()


@cache
def get_neighbor_coordinates_old(grid, row, col, ignore_slopes=False):
    cType = grid[row][col]
    neighbors = [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]
    if not ignore_slopes:
        if cType == ">":
            neighbors = [(row, col + 1)]
        elif cType == "<":
            neighbors = [(row, col - 1)]
        elif cType == "v":
            neighbors = [(row + 1, col)]
        elif cType == "^":
            neighbors = [(row - 1, col)]
    valid_neighbors = []
    for r, c in neighbors:
        if 0 <= r < len(grid) and 0 <= c < len(grid[r]):
            valid_neighbors.append((r, c))
    return valid_neighbors


@cache
def get_neighbor_coordinates(grid, row, col, ignore_slopes=False):
    cType = grid[row][col]
    valid_neighbors = []

    if not ignore_slopes and cType in (">", "<", "v", "^"):
        delta = {">": (0, 1), "<": (0, -1), "v": (1, 0), "^": (-1, 0)}
        dr, dc = delta[cType]
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[new_row]):
            valid_neighbors.append((new_row, new_col))
    else:
        for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[new_row]):
                valid_neighbors.append((new_row, new_col))

    return valid_neighbors


def longest_path_old(grid, start, destination, path, ignore_slopes=False):
    stack = [(start, set([start]))]
    longest = 0
    retval = []
    while stack:
        current, path = stack.pop(0)
        # print(f'longest_path(grid,{current},{destination},{len(path)})')
        if current == destination:
            print(f"Found path: {len(path)}")
            if len(path) > longest:
                retval = path
        else:
            neighbors = get_neighbor_coordinates(grid, *current, ignore_slopes)
            for n in neighbors:
                nType = grid[n[0]][n[1]]
                if nType in [".", ">", "<", "v", "^"]:
                    # print(f' Checking {n},{nType}')
                    if not n in path:
                        moved = True
                        stack.append([n, tuple([*path, n])])
    return retval


def longest_path(grid, start, destination, path, ignore_slopes=False):
    stack = [(start, path | {start})]
    longest_path = set()
    longest_length = 0

    while stack:
        current, current_path = stack.pop()
        if current == destination:
            if len(current_path) > longest_length:
                longest_length = len(current_path)
                longest_path = current_path
        else:
            neighbors = get_neighbor_coordinates(grid, *current, ignore_slopes)
            for n in neighbors:
                nType = grid[n[0]][n[1]]
                if nType != "#" and n not in current_path:
                    stack.append((n, current_path | {n}))

    return longest_path


def neighbors(grid, r, c, ignore_slopes):
    cell = grid[r][c]

    if ignore_slopes or cell == ".":
        for r, c in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if grid[r][c] != "#":
                yield r, c
    elif cell == "v":
        yield (r + 1, c)
    elif cell == "^":
        yield (r - 1, c)
    elif cell == ">":
        yield (r, c + 1)
    elif cell == "<":
        yield (r, c - 1)


def num_neighbors(grid, r, c, ignore_slopes):
    if ignore_slopes or grid[r][c] == ".":
        return sum(
            grid[r][c] != "#"
            for r, c in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
        )
    return 1


def is_node(grid, rc, src, dst, ignore_slopes):
    return rc == src or rc == dst or num_neighbors(grid, *rc, ignore_slopes) > 2


def adjacent_nodes(grid, rc, src, dst, ignore_slopes):
    q = deque([(rc, 0)])
    seen = set()

    while q:
        rc, dist = q.popleft()
        seen.add(rc)

        for n in neighbors(grid, *rc, ignore_slopes):
            if n in seen:
                continue

            if is_node(grid, n, src, dst, ignore_slopes):
                yield (n, dist + 1)
                continue

            q.append((n, dist + 1))


def graph_from_grid(grid, src, dst, ignore_slopes=False):
    g = defaultdict(list)
    q = deque([src])
    seen = set()

    while q:
        rc = q.popleft()
        if rc in seen:
            continue

        seen.add(rc)

        for n, weight in adjacent_nodes(grid, rc, src, dst, ignore_slopes):
            g[rc].append((n, weight))
            q.append(n)

    return g


def part1_old(myMap):
    retval = 0
    start = (0, myMap[0].index("."))
    end = (len(myMap) - 1, myMap[-1].index("."))
    path = longest_path(myMap, start, end, {start})
    retval = len(path) - 1
    # print_map(parsed_data,'Part1',path)
    return retval


def part1(myMap):
    start = (0, myMap[0].index("."))
    end = (len(myMap) - 1, myMap[-1].index("."))
    graph = graph_from_grid(myMap, start, end)
    print(graph)


def part2(myMap):
    retval = 0
    start = (0, myMap[0].index("."))
    end = (len(myMap) - 1, myMap[-1].index("."))
    path = longest_path(myMap, start, end, {start}, True)
    retval = len(path) - 1
    # print_map(parsed_data,'Part2',path)

    return retval


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        parsed_data = parse_input(f.read())

    # print(parsed_data1)
    # print_map(parsed_data,'Start')

    # print("Part 1")
    answer1 = part1(parsed_data)

    # print("Part 2")
    # answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    # print(f"Part2: {answer2}")
