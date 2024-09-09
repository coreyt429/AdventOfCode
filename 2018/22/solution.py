"""
Advent Of Code 2018 day 22


Part 1 is complete.   

The rules on this one made it fairly clear that recursion was going to be
necessary, and also repetitive.  So I used functools.lru_cache to cache the
repetitive values.

This assumption paid off, when I ran without it even with the test data, it
was significantly slower.

Time to get to work, so just making some notes for part 2.

Part 2 is a shortest path problem.  However, it is conditional, so the Grid()
built in shortest_path is likely not going to work, unless we implement a callback
to get the conditionals and h_score calculations.  This may pay dividens in the future,
but needs to be done in a manner that doesn't break existing code.

If you go this route, I'm thinking kwargs for:
    h_score_callback - would need to pass grid, pos, and target at minimum
    neighbor_selection_callback - would need to pass grid, pos, target, and possible neighbors

Instead of callbacks, I streamlined the shortest_paths function and Node() class so that
shortest_paths uses methods of Node() to make decisions.  Then I can override those
in a subclass to tweak them for each problem.  Also tweaked the way closed_set was working
to hash the objects instead.  This could improve efficiency in the elf goblin battle if
we revisit it later.

This worked well for the test data, and the input data was just too big for this approach.

Checking the solutions, I was reminded of the networkx library and its dijkstra implementation
in the solution by u/korylprince

I have seen this before, and was not quite ready to understand it.  having a better
understanding now of graphs and the underlying algorithms, I decided to give this
a try.  

"""
# import system modules
import time
import functools
import networkx

# import my modules
import aoc # pylint: disable=import-error
from grid import Grid # pylint: disable=import-error

# map area_types
area_type = {
    0: '.',
    1: '=',
    2: '|'
}

# reverse map to risk_level
risk_level =  {v: k for k, v in area_type.items()}

def parse_input(lines):
    """
    Parse input date
    Args:
        lines: list()
    Returns:
        depth: int()
        target: tuple(x/y)
    """
    depth = int(lines[0].split(' ')[1])
    target = lines[1].split(' ')[1]
    x_pos, y_pos = [int(pos) for pos in target.split(',')]
    return depth, (x_pos, y_pos)

@functools.lru_cache(maxsize=None)
def get_geologic_index(pos, depth, target):
    """
    Funciton to calculate geologic index
    Args:
        pos: tuple() -  int(x), int(y)
        depth: int()
        target: tuple() -  int(x), int(y)
    Returns:
        geologic_index: int()
    """
    # The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    # The region at the coordinates of the target has a geologic index of 0.
    if pos in [(0,0), target]:
        return 0
    if pos[1] == 0:
        # If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
        return pos[0] * 16807
    # If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
    if pos[0] == 0:
        return pos[1] * 48271
    # Otherwise, the region's geologic index is the result of multiplying the erosion levels of
    # the regions at X-1,Y and X,Y-1.
    erosion_level_1 = get_erosion_level((pos[0] - 1, pos[1]), depth, target)
    erosion_level_2 = get_erosion_level((pos[0], pos[1] - 1), depth, target)
    return erosion_level_1 * erosion_level_2

@functools.lru_cache(maxsize=None)
def get_erosion_level(pos, depth, target):
    """
    Function to calculate erosion level for an area
    Args:
        pos: tuple() -  int(x), int(y)
        depth: int()
        target: tuple() -  int(x), int(y)
    
    Returns:
        erosion_level: int()
    """
    # A region's erosion level is its geologic index plus the cave system's depth, all modulo 20183.
    geologic_index = get_geologic_index(pos, depth, target)
    return (geologic_index + depth) % 20183

@functools.lru_cache(maxsize=None)
def get_area_type(pos, depth, target):
    """
    function to get area type
    Args:
        pos: tuple() -  int(x), int(y)
        depth: int()
        target: tuple() -  int(x), int(y)
    Returns:
        area_type: char() '.', '=', or '|'
    """
    # If the erosion level modulo 3 is 0, the region's type is rocky.
    # If the erosion level modulo 3 is 1, the region's type is wet.
    # If the erosion level modulo 3 is 2, the region's type is narrow.
    erosion_level = get_erosion_level(pos, depth, target)
    return area_type[erosion_level % 3]

def get_risk_level(grid, start, goal):
    """
    Function to calculate risk level
    Args:
        grid: Grid() current map
        start: tuple() start position x/y coordinates
        goal: tuple() end position x/y coordinates
    Returns:
        total: int() risk_level total
    """
    total = 0
    min_x = min(start[0], goal[0])
    min_y = min(start[1], goal[1])
    max_x = max(start[0], goal[0])
    max_y = max(start[1], goal[1])
    for point in grid:
        if min_x <= point[0] <= max_x and min_y <= point[1] <= max_y:
            total += risk_level[grid.get_point(point)]
    return total

def init_grid(depth, target, scale_out=6):
    """
    Function to initialize grid and populate data:
    Args:
        depth: int()
        target: tuple(x, y)
    Returns:
        grid: Grid()
    """
    grid = Grid('M', type="infinite", coordinate_system='screen', use_overrides=False)
    # populate grid
    for x_pos in range(target[0] + scale_out):
        for y_pos in range(target[1] + scale_out):
            grid.set_point((x_pos, y_pos), get_area_type((x_pos, y_pos), depth, target))
    grid.update()
    return grid

def dijkstra(grid, target):
    """
    Function to setup and run dijkstra search
    
    Args:
        grid: Grid()
        target: tuple(x, y)
    Returns:
        shortest_path_length: int()
    """
    # init graph
    graph = networkx.Graph()
    # start with torch at (0, 0)
    terrain_equipment_map = {
        '.': ['climbing_gear', 'torch'],
        '=': ['climbing_gear', 'neither'],
        '|': ['neither', 'torch']
    }
    for point in grid:
        point_terrain = grid.get_point(point)
        for eq_1 in terrain_equipment_map[point_terrain]:
            for eq_2 in terrain_equipment_map[point_terrain]:
                if  eq_1 == eq_2:
                    continue
                graph.add_edge((point[0], point[1], eq_1), (point[0], point[1], eq_2), weight=7)
    for point in grid:
        point_terrain = grid.get_point(point)
        for direction, neighbor in grid.get_neighbors(
                point=point, directions=['n','e','s','w']
            ).items():
            if direction not in ['n','e','s','w']:
                continue
            for equipped in terrain_equipment_map[point_terrain]:
                if graph.has_node((neighbor[0], neighbor[1], equipped)):
                    graph.add_edge(
                        (point[0], point[1], equipped),
                        (neighbor[0], neighbor[1], equipped),
                        weight=1
                    )
    return networkx.dijkstra_path_length(graph, (0, 0, 'torch'), (target[0], target[1], 'torch'))


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # load input data
    depth, target = parse_input(input_value)
    scale_out = 1
    if part == 2:
        # part 2 needs a larger grid to cover the path
        scale_out = 50
    # init grid
    grid = init_grid(depth, target, scale_out)
    # part 1 caculate risk level
    if part == 1:
        return get_risk_level(grid, (0,0), target)
    # part 2 calculate shortest path length
    return dijkstra(grid, target)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,22)
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
