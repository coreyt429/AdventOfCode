"""
Advent Of Code 2017 day 3

This one was a bit more fun.  I went with a more mathematical solution for part 1,
and that didn't work well for part 2. So I tried building a traversal routine to
make the grid, but that was too slow for part 1.  So taking different approaches
for each part.

"""

# import system modules
import time
import logging
import sys
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import manhattan_distance, Grid

# x/y constants
X = 0
Y = 1


def get_target_coordinates(target):
    """
    Part 1 solution.  Calculates values instead of building large grid
    """
    # init total, n and new
    total = 1
    counter = 1
    new = 0
    # loop until we find our target
    while total < target:
        # step n up by 2
        counter += 2
        # count of items for this layer
        new = (counter - 1) * 4
        # total count
        total += new
    # find lower right hand corner
    corner = counter // 2
    point = [corner, -1 * corner]
    # get difference between lower right hand corner and target
    diff = total - target
    # if diff is < counter, then target is on the bottom row
    if diff < counter:
        offset = diff
        point[X] -= offset
    # if diff is in the next counter-2 then target is on the left side
    elif diff < counter + (counter - 2):
        offset = diff - counter
        point[X] -= counter - 1
        point[Y] += offset + 1
    # if diff is in the next counter, then target is on the top row
    elif diff < counter * 2 + (counter - 2):
        offset = diff - (counter + (counter - 2))
        point[X] -= counter - 1
        point[X] += offset
        point[Y] *= -1
    # target must be on the right side
    else:
        offset = diff - (counter * 2 + (counter - 2))
        point[Y] += (counter - 2) - offset
    # return target point
    return tuple(point)

def get_neighbor_offsets(**kwargs):
    """
    Function to calculate neighbor offsets, and store them
    """
    offset_collection = {}
    offset_collection['cartesian'] = {
        'n': (0, 1),    # Move up
        'ne': (1, 1),   # Move up-right
        'e': (1, 0),    # Move right
        'se': (1, -1),  # Move down-right
        's': (0, -1),   # Move down
        'sw': (-1, -1), # Move down-left
        'w': (-1, 0),   # Move left
        'nw': (-1, 1)   # Move up-left
    }
    offset_collection['matrix'] = {
        'n': (-1, 0),   # Move up
        'ne': (-1, 1),  # Move up-right
        'e': (0, 1),    # Move right
        'se': (1, 1),   # Move down-right
        's': (1, 0),    # Move down
        'sw': (1, -1),  # Move down-left
        'w': (0, -1),   # Move left
        'nw': (-1, -1)  # Move up-left
    }
    offset_collection['screen'] = {
        'n': (0, -1),   # Move up
        'ne': (1, -1),  # Move up-right
        'e': (1, 0),    # Move right
        'se': (1, 1),   # Move down-right
        's': (0, 1),    # Move down
        'sw': (-1, 1),  # Move down-left
        'w': (-1, 0),   # Move left
        'nw': (-1, -1)  # Move up-left
    }

    # Always reset the neighbor offsets for fresh calculation
    neighbor_offsets = {"tuple": [], "complex": []}

    offsets = offset_collection[kwargs.get('coordinate_system', 'screen')]
    directions = kwargs.get('directions', offsets.keys())

    # Calculate offsets:
    for direction in directions:
        point = offsets[direction]
        neighbor_offsets['tuple'].append(point)
        neighbor_offsets['complex'].append(complex(*point))
    return neighbor_offsets

def get_maze_size(self, maze):
    """
    Function to get min(X,Y), max(X,Y) for maze
    """
    X=0
    Y=1
    if isinstance(maze, list):
        # list of list, return 0 to length
        min = tuple([0, 0])
        max = tuple([len(maze), len(maze[0])])
        return min, max
    if not isinstance(maze, dict):
        logger.info("get_maze_size no rule to handle %s", type(maze))
        sys.exit()
    # complex or tuple?
    min = [float('infinity')]*2
    max = [float('infinity')*-1]*2
    is_complex = isinstance(list(maze.keys())[0], complex)
    for key in maze.keys():
        if is_complex:
            if key.real < min[X]:
                min[X] = int(key.real)
            if key.real > max[X]:
                max[X] = int(key.real)
            if key.imag < min[Y]:
                min[Y] = int(key.imag)
            if key.imag > max[Y]:
                max[Y] = int(key.imag)
        else:
            if key[X] < min[X]:
                min[X] = key[X]
            if key[X] > max[X]:
                max[X] = key[X]
            if key[Y] < min[Y]:
                min[Y] = key[Y]
            if key[Y] > max[Y]:
                max[Y] = key[Y]
    return min, max

def get_neighbors(maze, point, **kwargs):
    """
    Function to get neighbors of a point on a map or maze
    This function assumes screen coordinates.  If using another coordinate system,
    please update. Maybe a rule flag to specify?

    Notes: see 2023.21 for infinite complex example

    Args:
        maze: list_x(list_y()) or dict(tuple(x,y) or dict(complex())) 
        point: tuple(x,y) or complex() # should match maze, or things may break
        **kwargs:  using kwargs for rules instead to be more flexible
        rules: dict{} , example:
            rules = {
                "type": "bounded", # or infinite
                "invalid": "#",
                "coordinate_system": "screen" # or matrix, or cartesian, others noted below, 
                    are not yet supported
                "directions": list(('n','s','e','w'))
            }
    Returns:
        neighbors: list(tuple(x,y)) or list(complex())

    Notes:
        tuple to complex:
            complex(my_tuple)
        complex to tuple:
            tuple(my_complex.real, my_complex.imag)
        Coordinate System	X Increases	Y Increases	Common Use
        Screen Coordinates	To the right	Down	Computer graphics, UI, web design
        Matrix Coordinates	To the right (cols)	Down (rows)	Spreadsheets, grid-based systems
        Cartesian Coordinates	To the right	Up	Mathematics, physics, engineering
        Polar Coordinates	N/A (radius and angle)	N/A	Navigation, physics, engineering
        Geographic Coordinates	N/A (longitude)	N/A (latitude)	Geography, GPS
        Isometric Coordinates	120-degree intervals	120-degree intervals	Video games,
            CAD, technical drawing
    """
    X=0
    Y=1
    # define booleans:
    is_dict = isinstance(maze, dict)
    #is_list = isinstance(maze, list)
    is_complex = False
    if is_dict:
        is_complex = isinstance(list(maze.keys())[0], complex)
    # I think I'm getting technical here, but this may matter when we go to apply rules
    # as I typically provide matrix coordinates as (row, col)
    if kwargs.get('coordinate_system', 'screen') ==  'matrix':
        X=1
        Y=0
    # define offsets
    offsets = get_neighbor_offsets(**kwargs)
    logger.info("offsets: %s", offsets)

    # empty list of neighbors
    neighbors = []
    if is_complex:
        for offset in offsets["complex"]:
            neighbors.append(point + offset)
    else:
        for offset in offsets["tuple"]:
            neighbors.append(tuple([point[X] + offset[X], point[Y] + offset[Y]]))
    # process rule type:bounded
    if kwargs.get("type", "bounded") == "bounded":
        min, max = get_maze_size(maze)
        logger.debug("Maze size: min: %s, max: %s", min, max)
        valid_neighbors = []
        for neighbor in neighbors:
            logger.info("bounded, checking %s", neighbor)
            if is_dict:
                if neighbor in maze:
                    valid_neighbors.append(neighbor)
            else:
                if min[X] <= neighbor[X] < max[X] and min[Y] <= neighbor[Y] < max[Y]:
                    valid_neighbors.append(neighbor)
            neighbors = valid_neighbors
    # are there invalid character rules, note, this will probably break in type:infinite
    if "invalid" in kwargs:
        valid_neighbors = []
        for neighbor in neighbors:
            logger.info("invalid: checking %s", neighbor)
            if is_dict:
                logger.info("dict: %s: %s in %s", neighbor, maze[neighbor], kwargs['invalid'])
                if not maze[neighbor] in kwargs['invalid']:
                    valid_neighbors.append(neighbor)
            else:
                # using 0/1 here instead of X/Y to avoid an extra if condition to 
                # look for swapped x/y for matrix coordinates, when we get to a
                # matrix coordinate puzzle, we will need to test thoroughly
                #if not maze[neighbor[0][1]] in kwargs['invalid']:
                logger.info("list: %s: %s in %s", neighbor, maze[neighbor[X]][neighbor[Y]], kwargs['invalid'])
                if not maze[neighbor[X]][neighbor[Y]] in kwargs['invalid']:
                    valid_neighbors.append(neighbor)
        neighbors = valid_neighbors
    return neighbors

def traverse(target):
    """
    Part 2 solultions, builds out grid so we can evaluate neighbors
    """
    # directions to identify position in neighbors
    directions = {"up": 4, "left": 1, "right": 6, "down": 3}
    # init start and mem_map
    start = complex(0, 0)
    mem_map = {start: 1}
    # get neighbors of start
    neighbors = get_neighbors(mem_map, start, type="infinite")
    # init counter
    counter = 1
    # loop indefinitely
    while True:
        # increment counter by 2 (odd numbers)
        counter += 2
        # move current to the right
        current = neighbors[directions["right"]]
        # get neighbors of current
        neighbors = get_neighbors(mem_map, current, type="infinite")
        # initialize entry for current
        mem_map[current] = 0
        # add preexisting neighbor values to current
        for neighbor in neighbors:
            if neighbor in mem_map:
                mem_map[current] += mem_map[neighbor]
        # if current > target, return current value
        if mem_map[current] > target:
            return mem_map[current]
        # make loop up, left, down right
        for direction in ["up", "left", "down", "right"]:
            # start at step 1
            steps = 1
            # unless we are going up, we will have one less step
            if direction == "up":
                steps = 2
            # loop from steps to counter
            for _ in range(steps, counter):
                # get new current
                current = neighbors[directions[direction]]
                # init new current
                mem_map[current] = 0
                # get new neighbors
                neighbors = get_neighbors(mem_map, current, type="infinite")
                # add existing neighbor values
                for neighbor in neighbors:
                    if neighbor in mem_map:
                        mem_map[current] += mem_map[neighbor]
                # if we current > target return value
                if mem_map[current] > target:
                    return mem_map[current]


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        # get target point
        point = get_target_coordinates(int(input_value))
        # return manhattan distance to the center
        return manhattan_distance(point, (0, 0))
    # return mem_map traversal
    return traverse(int(input_value))


year = 2017
day = 3
input_format = {
    1: "text",
    2: "text",
}

funcs = {
    1: solve,
    2: solve,
}

submit = False

if len(sys.argv) > 1 and sys.argv[1].lower() == "submit":
    submit = True

if __name__ == "__main__":
    aoc = AdventOfCode(year=year, day=day, input_formats=input_format, funcs=funcs)
    aoc.run(submit=submit)
