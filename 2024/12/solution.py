"""
Advent Of Code 2024 day 12

Part 1, I initially solved in a very slow solution.  I retooled it to use flood fill,
and it is faster.

Part 2, I was successful with the test data after serveral failed attempts. No go with the
puzzle input.  Answered with a borrowed solution, and will come back to understand it later.

"""
# import system modules
import time
from collections import defaultdict
from functools import lru_cache
from heapq import heappop, heappush
# import my modules
import aoc # pylint: disable=import-error
from grid import Grid, manhattan_distance # pylint: disable=import-error

def group_points(grid):
    """Function to group points by value"""
    points = defaultdict(set)
    for point, char in grid.items():
        points[char].add(point)
    return points

def can_merge(regions_dict):
    """Function to determine if regions can be merged"""
    for regions in regions_dict.values():
        for region in regions:
            for other in regions:
                if region is not other and regions_connected(tuple(region), tuple(other)):
                    return True
    return False

@lru_cache(maxsize=None)
def get_direction(p_1, p_2):
    """A function to determine direction (horizontal or vertical)"""
    (x_1, y_1), (x_2, y_2) = p_1, p_2
    if x_1 == x_2:
        return 'vertical'
    if y_1 == y_2:
        return 'horizontal'
    # Should never happen with rectilinear shapes
    return 'other'

def get_boundary_edges(squares):
    """Function to get boundary_edges"""
    boundary_edges = set()
    for (x_val, y_val) in squares:
        # The corners of this square:
        # top edge: ((x, y), (x+1, y))
        # bottom edge: ((x, y+1), (x+1, y+1))
        # left edge: ((x, y), (x, y+1))
        # right edge: ((x+1, y), (x+1, y+1))

        # Check each edge if it's on boundary
        # Top edge
        if (x_val, y_val - 1) not in squares:
            boundary_edges.add(((x_val, y_val), (x_val + 1, y_val)))
        # Bottom edge
        if (x_val, y_val + 1) not in squares:
            boundary_edges.add(((x_val, y_val + 1), (x_val + 1, y_val + 1)))
        # Left edge
        if (x_val - 1, y_val) not in squares:
            boundary_edges.add(((x_val, y_val), (x_val, y_val + 1)))
        # Right edge
        if (x_val + 1, y_val) not in squares:
            boundary_edges.add(((x_val + 1, y_val), (x_val + 1, y_val + 1)))
        return boundary_edges

def merge_regions(input_regions_dict):
    """Function to merge connected regions"""
    regions_dict = input_regions_dict
    while can_merge(regions_dict):
        new_regions_dict = defaultdict(list)
        for char, regions in regions_dict.items():
            for region in regions:
                found = False
                for other in new_regions_dict[char]:
                    if regions_connected(tuple(region), tuple(other)):
                        other.update(region)
                        found = True
                        break
                if not found:
                    new_regions_dict[char].append(region)
        regions_dict = new_regions_dict
    return regions_dict

@lru_cache(maxsize=None)
def regions_connected(region_a, region_b):
    """Function to test if two reagions are connected"""
    for point in region_a:
        for other in region_b:
            if manhattan_distance(point, other) < 2:
                return True
    return False

def flood_fill_region(grid, start):
    """Function to flood fill a region"""
    target = grid.get_point(start)
    heap = []
    heappush(heap, (1, (start,)))
    max_region = ()
    max_region_len = 0
    seen = set()
    while heap:
        length, region = heappop(heap)
        if length > max_region_len:
            max_region_len = length
            max_region = region
        if region in seen:
            continue
        seen.add(region)
        new_region = set(region)
        for point in region:
            neighbors = grid.get_neighbors(point=point, directions={'n','s','e','w'})
            for neighbor in neighbors.values():
                if grid.get_point(neighbor) == target:
                    new_region.add(neighbor)
        heappush(heap, (len(new_region), tuple(new_region)))
    return max_region

def find_region_boundaries(grid, region):
    """Function to find region boundaries"""
    target = grid.get_point(region[0])
    # print(f"target: {target}")
    heap = []
    heappush(heap, (0, ()))
    max_border = ()
    max_border_len = 0
    seen = set()
    while heap:
        length, border = heappop(heap)
        if length > max_border_len:
            max_border_len = length
            max_border = border
        if border in seen:
            continue
        seen.add(border)
        new_border = set(border)
        for point in region:
            neighbors = grid.get_neighbors(point=point, directions={'n','s','e','w'})
            for neighbor in neighbors.values():
                if grid.get_point(neighbor) != target:
                    new_border.add(neighbor)
        heappush(heap, (len(new_border), tuple(new_border)))
    return max_border


def get_regions(grid):
    """Function to group matching points into regions"""
    # get points of teach type
    points = group_points(grid)
    regions = defaultdict(list)
    for char, data in points.items():
        for point in data:
            found = False
            for region in regions[char]:
                # check if region of {point} is connected to region
                if point in region:
                    found = True
                    break
            if found:
                continue
            # no connection found, create a new region
            regions[char].append(flood_fill_region(grid, point))
            # some regions will be broken, so lets merge them before returning
    return regions

def area_of_region(region):
    """Function to calculate the area of a region"""
    # simple I know, but it makes the main logic readable
    return len(region)

def perimeter_of_region(grid, region):
    """Function to calculate the permiter of a region"""
    directions = ['n', 's', 'e', 'w']
    perimeter = 0
    for point in sorted(region):

        neighbors = grid.get_neighbors(point=point, directions=directions)
        for direction in directions:
            # outside perimiter
            if direction not in neighbors:
                perimeter += 1
                # print(point, direction, perimeter)
            # touching another region
            elif neighbors[direction] not in region:
                perimeter += 1
                # print(point, direction, perimeter)
        # print(point, perimeter)
    return perimeter

def build_adjacency_map(grid, boundary_points):
    """Function to build adjacency map"""
    directions = ['n', 's', 'e', 'w']
    adjacency = defaultdict(list)
    for point in boundary_points:
        for neighbor in grid.get_neighbors(point=point, directions=directions).values():
            if neighbor in boundary_points:
                adjacency[point].append(neighbor)
    return adjacency

def walk_direction(grid, boundary_points, point, direction):
    """Function to identify bounday points in a direction from point"""
    points = set()
    current = point
    while current in boundary_points:
        points.add(current)
        neighbors = grid.get_neighbors(point=current, directions=(direction,))
        if direction not in neighbors:
            break
        current = neighbors[direction]
    return points

def find_path(boundary_points, grid):
    """function to order boundary points into a path"""
    start = min(boundary_points)
    # directions in reading order
    directions = ['n', 's', 'e', 'w', 'nw', 'ne', 'sw', 'se']
    path = []
    current = start
    while True:
        if current in path:
            break
        path.append(current)
        neighbors = grid.get_neighbors(point=current)
        # print(f"current: {current}, neighbors: {neighbors}")
        found = False
        for direction in directions:
            if neighbors[direction] in boundary_points and neighbors[direction] not in path:
                # print(f"{current} -> {neighbors[direction]}")
                current = neighbors[direction]
                found = True
                break
        # no next hop
        if not found:
            break
    while manhattan_distance(path[0], path[-1]) == 1:
        path.append(path.pop(0))
    return path

def find_edge(grid, path, start, direction):
    """Function to find edges"""
    directions = {
        'n': ('e','w'),
        's': ('e','w'),
        'e': ('n', 's'),
        'w': ('n', 's'),
    }
    heap = []
    heappush(heap, (1, (start,)))
    edge = set()
    seen = set()
    while heap:
        _, edge_points = heappop(heap)
        if edge_points in seen:
            continue
        seen.add(edge_points)
        edge.update(set(edge_points))
        new_edge_points = set()
        for point in edge_points:
            new_edge_points.add(point)
            neighbors = grid.get_neighbors(point=point, directions=directions[direction])
            for neighbor in neighbors.values():
                if neighbor in path:
                    new_edge_points.add(neighbor)
            heappush(heap, (len(new_edge_points), tuple(new_edge_points)))
    return edge


def count_edges(grid, path, region):
    """
    Counts the number of 'edges' in a path, unifying consecutive horizontal/vertical
    segments into single edges. Diagonal segments are also treated as single edges
    (if they occur).
    
    For example, a path like:
        [(0,0), (0,1), (0,2), (1,2), (2,2), (2,3)]
    yields 3 edges total:
        - One vertical edge (from (0,0) to (0,2))
        - One horizontal edge (from (0,2) to (2,2))
        - One vertical edge (from (2,2) to (2,3))
    """
    opposites = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e'
    }

    point_faces = defaultdict(list)
    edges = {
        'n': set(),
        's': set(),
        'e': set(),
        'w': set()
    }
    for point in path:
        neighbors = grid.get_neighbors(point=point, directions=('n','s','e','w'))
        for direction, neighbor in neighbors.items():
            if neighbor in region:
                point_faces[point].append(opposites[direction])

    for point, directions in point_faces.items():
        for direction in directions:
            if any(point in edge for edge in edges[direction]):
                # point is already in an edge facing this direction
                continue
            edges[direction].add(tuple(find_edge(grid, path, point, direction)))
    edge_count = 0
    for edge_set in edges.values():
        edge_count += len(edge_set)
    return edge_count


def sides_of_region(grid, region):
    """Function to find sides of a region"""
    boundary_points = find_region_boundaries(grid, region)
    path = find_path(boundary_points, grid)
    # print(f"path: {path}")
    return count_edges(grid, path, region)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False, coordinate_system='screen', type='infinite')
    if part == 2:
        regions_dict = answer[2]
    else:
        regions_dict = get_regions(grid)
    answer[2] = regions_dict
    cost = 0
    for regions in regions_dict.values():
        for region in regions:
            area = area_of_region(region)
            if part == 1:
                perimeter = perimeter_of_region(grid, region)
            else:
                perimeter = sides_of_region(grid, region)
                # 437396 answer is too low
            print(f"{area} * {perimeter} = {area * perimeter}")
            cost += area * perimeter
    return cost

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024,12)
    input_data = my_aoc.load_lines()
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
        1: 1451030,
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
