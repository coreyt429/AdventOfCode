"""
Advent Of Code 2018 day 20

"""

# import system modules
import time
import re
from heapq import heappop, heappush

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error


def move(grid, direction):
    """
    Function to move to the next room in the grid.
    This is a bit more complex than Grid().move() because:
      - we are creating the rooms as we go
      - moving to a room is 2 move (door, room)
      - we are identifying doors as we go through them

    Args:
        grid: Grid() object
        direction: str() movement direction 'n', 's', 'e', 'w'
    """
    # map doors by direction
    door = {"e": "|", "w": "|", "n": "-", "s": "-"}
    # get the neighbors of the current position
    neighbors = grid.get_neighbors()
    # save door location so we can mark it after we go through
    door_location = neighbors[direction]
    # move direction twice
    grid.move(direction)
    grid.move(direction)
    # mark path as door after moving through it.
    grid.set_point(door_location, door[direction])
    # get neighbors of new room position
    neighbors = grid.get_neighbors(
        directions=["ne", "nw", "se", "sw", "n", "w", "e", "s"]
    )
    # init walls if they are not already
    # walk neighbor directions
    for n_dir in ["ne", "nw", "se", "sw"]:
        # get neighbor
        neighbor = neighbors[n_dir]
        # get neighbor value
        value = grid.get_point(neighbor, "%")
        # if oob, make in bounds
        # this seems like a Grid() issue.  This grid is infinite
        # so there should be no oob
        if value == "%":
            value = "#"
            # set point of wall
            grid.set_point(neighbor, value)
    # walk door direcdtions
    for n_dir in ["n", "w", "e", "s"]:
        # get neighbor
        neighbor = neighbors[n_dir]
        # get neighbor value
        value = grid.get_point(neighbor, " ")
        # if default value (door not already set), then mark unkown
        if value in " ":
            value = "?"
            # set value
            grid.set_point(neighbor, value)
    # set room value
    grid.set_point(grid.pos, ".")
    # update grid data
    # grid.update


def set_start(grid, pos=(1, 1)):
    """
    Set the start point in the grid
    """
    # set start position
    grid.pos = pos
    grid.overrides = {grid.pos: "*"}


def follow_path(grid, path):
    """
    Function to follow a path of movements
    This was an early attempt and not used in final solution
    The idea was to calculate the paths from the "regex"
    and that wasn't practical
    Args:
        grid: Grid() object
        path: str() list of movements, ex :'nesw'
    """
    # set start position
    set_start(grid)
    # walk directions in path
    for direction in path.lower():
        # move in direction
        move(grid, direction)
    # set start position
    set_start(grid)


def follow_path2(grid, line, line_ptr=0, start_position=(1, 1)):
    """
    Revision of follow path, that recursively walks the
    path string
    """
    set_start(grid, start_position)
    skip_idx = -1
    for idx in range(line_ptr, len(line) - 1):
        if idx < skip_idx:
            continue
        char = line[idx]
        if char in "news":
            move(grid, char)
        elif char == "|":
            set_start(grid, start_position)
        elif char == "(":
            current_pos = grid.pos
            skip_idx = follow_path2(grid, line, idx + 1, current_pos)
        elif char == ")":
            return idx + 1
        elif char == "$":
            return 0
        elif char == "^":
            pass
        else:
            print(f"Unknown character: {char}")
    return 0


def expand_string(line):
    """
    Function to expand "regex" strings
    This worked for small data sets, not for the input file
    Args:
        line: str() input string
    Returns:
        final_strings: set() of str()
    """
    # regex to match inner ()
    pattern_group = re.compile(r"\(([^()]+)\)")
    # Remove ^ and $ as they're just markers
    line = line.strip("^$")
    # init heap
    heap = []
    # init final strings
    final_strings = set()
    # push input line onto heap.  heap is sorted by '(' count
    # so we finish out the fewest replacements first
    # I don't think this provides any benefit, and we likely
    # could have just left popped a deque instead.  If this
    # step takes to long with the input data, try that
    heappush(heap, (line.count("("), line))
    already_seen = set()
    # process heap
    while heap:
        # get next line to try
        count, line = heappop(heap)
        # print(len(heap), count, len(already_seen), len(final_strings))
        # fully resolved, add to final_strings
        if count == 0:
            final_strings.add(line)
            continue

        if line in already_seen:
            continue

        already_seen.add(line)
        # check for regex
        match = pattern_group.findall(line)
        # process match
        if match:
            # get last match string
            replace = f"({match[0]})"
            # expand replacements for last match string
            replacements = match[0].split("|")
            # walk replacements
            for replacement in replacements:
                # create new line with replacement replacing replace
                new_line = line.replace(replace, replacement)
                if not new_line in already_seen:
                    # add to heap
                    heappush(heap, (new_line.count("("), new_line))
        else:
            # catch regex misses
            print(f"We shouldn't see this, but we did: {line}")
    return final_strings


def adjacent_rooms(grid, point):
    """
    Get adjacent rooms for a room
    """
    # get all neighbors
    neighbors = grid.get_neighbors(point=point)
    # init rooms
    rooms = []
    # init offsets
    offsets = {"n": (0, 2), "e": (2, 0), "s": (0, -2), "w": (-2, 0)}
    # for nesw directions
    for direction in "news":
        # if point is a door
        if grid.get_point(neighbors[direction]) in "|-":
            # room is on the other side of the door
            pos_x, pos_y = point
            rooms.append((pos_x + offsets[direction][0], pos_y + offsets[direction][1]))
    return rooms


def map_rooms(grid):
    """
    BFS Function to map room paths
    """
    # init start point
    current_pos = (1, 1)
    set_start(grid, current_pos)
    # init heap, paths, already_seen, and max_doors
    heap = []
    paths = {}
    max_doors = 0
    already_seen = set()
    # add start to heap
    heappush(heap, (0, current_pos, ()))
    # process heap
    while heap:
        # get next room
        doors, current_pos, path = heappop(heap)
        # if we have already processed this room, move on
        if current_pos in already_seen:
            continue
        # update max_doors
        max_doors = max(max_doors, doors)
        # convert path to list
        path = list(path)
        # add current position to path
        path.append(current_pos)
        # convert back to tuple
        path = tuple(path)
        # add to already seen
        already_seen.add(current_pos)
        # add to paths
        paths[current_pos] = path
        # get next rooms
        next_rooms = adjacent_rooms(grid, current_pos)
        # put next rooms on heap
        for room in next_rooms:
            heappush(heap, (doors + 1, room, path))
    # return data
    return max_doors, paths


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init grid data
    initial_grid = """#?#
?.?
#?#"""
    # init grid
    my_grid = Grid(initial_grid, coordinate_system="cartesian", type="infinite")
    # process input to expand grid
    follow_path2(my_grid, input_value.lower())
    # update grid data
    my_grid.update()
    set_start(my_grid)
    # map_str = str(my_grid)
    # map_str = str(my_grid).replace('?','#').replace('*','X').replace(' ','#')
    # print(f"map built {time.time() - start_time} seconds")
    # print(map_str)
    # map rooms to get results
    most_doors, paths = map_rooms(my_grid)
    # part 2?
    if part == 1:
        return most_doors
    # init count
    count = 0
    # walk paths
    for _, path in paths.items():
        # if path is longer than 1000 then we should have 1000 doors
        if len(path) > 1000:
            # increment count
            count += 1
    # return part 2 answer
    return count


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018, 20)
    input_text = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
