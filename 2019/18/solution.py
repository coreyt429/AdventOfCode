"""
Advent Of Code 2019 day 18

Grid() came in handy here.  Part 1 was was a matter of using a BFS
adaptation to explore the map until all the keys were found.

For part 2, I changed the handling of Explorer.pos from assuming a
single tuple, to assuming a list of tuples.  When rerunning for part 1
now, it is just a list with the single tuple.  So the only difference
in part 1 and part2 is the map change from split(map)

"""

# import system modules
import time
import functools
from heapq import heappop, heappush
import string
import networkx

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error


def char_bit_map(input_chars):
    """Function to build bitmaps for string of characters"""
    return {key: 1 << (ord(key) - ord(input_chars[0])) for key in input_chars}


# global key_to_bit map
key_to_bit = char_bit_map(string.ascii_lowercase)
door_to_bit = char_bit_map(string.ascii_uppercase)


class MyGrid(Grid):
    """
    MyGrid is a subclass of Grid to test a networkx driven shortest_path function
    lets work on integrating this into Grid
    """

    def __init__(self, grid_data):
        """init"""
        super().__init__(grid_data, use_overrides=False)
        # init graph
        self.graph = networkx.Graph()
        for point in self:
            tile = self.get_point(point, "#")
            if tile == "#":
                continue
            for direction, neighbor in self.get_neighbors(
                point=point, directions=["n", "e", "s", "w"]
            ).items():
                if direction not in ["n", "e", "s", "w"]:
                    continue
                neighbor_tile = self.get_point(neighbor, "#")
                if neighbor_tile == "#":
                    continue
                self.graph.add_edge(
                    (point[0], point[1]), (neighbor[0], neighbor[1]), weight=1
                )

    def shortest_path(self, start, goal):
        """
        method to calculate shortest path
        """
        try:
            return networkx.dijkstra_path(self.graph, start, goal)
        except networkx.NetworkXNoPath:
            return False

    def dummy(self):
        """dummy method"""
        return True


class Explorer:
    """
    Class to represent our value explorere
    """

    def __init__(self, pos=None, key_value=0, steps=0, key_string=""):
        """
        init: note, I ended up not using parent
        """
        self.key_string = key_string
        # init keys
        self.keys = key_value
        # init pos list(tuple)
        self.pos = pos
        # init step count
        self.steps = steps
        # this took a bit of trial and error, but steps - len(key_string)
        # seems to be the fastest solving sort order
        self.sort_key = steps - len(self.key_string)  # * -1

    def __lt__(self, other):
        """lt for heapq"""
        return self.sort_key < other.sort_key

    def state(self):
        """
        method to provide hashable state for our closed set
        """
        return (*self.pos, self.keys)

    def __str__(self):
        my_string = f"{self.pos}: {self.key_string}"
        return my_string


# init path_cache
path_cache = {}
door_cache = {}


def cache_path(start, goal, path):
    """cache paths"""
    path_cache[(start, goal)] = path
    path_cache[(goal, start)] = list(reversed(path))


def cache_doors(start, goal, door_list):
    """cache doors"""
    door_cache[(start, goal)] = door_list
    door_cache[(goal, start)] = list(reversed(door_list))


# init door and key bitmasks
bitmasks = {"keys": 0, "doors": 0}
bitmasks["keys"] = 0
bitmasks["doors"] = 0
keys = {}
doors = {}


@functools.lru_cache(maxsize=None)
def check_key(key, collected_keys):
    """check to see if key is present"""
    return collected_keys & key_to_bit[key.lower()]


def fetch_doors(start, goal, path):
    """Fetch doors on a path"""
    door_list = []
    for point in doors:
        if point in path:
            door_list.append(point)
    cache_doors(start, goal, door_list)
    return door_list


def key_reachable(grid, start, key, collected_keys):
    """
    Function to determine if a key is reachable
    """
    # we already have this key
    if check_key(key, collected_keys):
        return False
    goal = keys[key]
    path = path_cache.get((start, goal), None)
    # get the path
    if not path:
        path = grid.shortest_path(start, goal)
        cache_path(start, goal, path)
    # no path, return false
    if not path:
        return False
    # we have a path, lets check to see if it is blocked
    door_list = door_cache.get((start, goal), None)
    if door_list is None:
        door_list = fetch_doors(start, goal, path)
    # iterate over doors in path
    for point in door_list:
        # and we don't have the key
        # if not collected_keys & key_to_bit[doors[point].lower()]:
        if not check_key(doors[point].lower(), collected_keys):
            return False
    # all checks passed
    return path


def load_map_data(grid, start_points):
    """
    Function to read the map
    """
    bitmasks["keys"] = 0
    bitmasks["doors"] = 0
    for my_dict in [keys, doors, path_cache, door_cache]:
        key_list = list(my_dict.keys())
        for key in key_list:
            my_dict.pop(key)
    # iterate over grid
    for point in grid:
        # get point value
        tile = grid.get_point(point, "#")
        # @ represents a start point, so append to starting points
        if tile == "@":
            start_points.append(point)
            continue
        if tile in string.ascii_lowercase:
            # add key
            keys[tile] = point
            bitmasks["keys"] += key_to_bit[tile]
        if tile in string.ascii_uppercase:
            # add key
            doors[tile] = point
            doors[point] = tile
            bitmasks["doors"] += door_to_bit[tile]


def starting_paths(grid, start_points, path_tiles, reachable_keys):
    """
    Function to calculate paths from start_points to keys
    """
    while reachable_keys:
        reachable_keys.pop()
    # iterate over start_points
    for idx, start in enumerate(start_points):  #  + list(keys.values()): commented out
        reachable_keys.append(set())
        # iterate over key locations
        for key, goal in keys.items():
            if start == goal:
                continue
            # calculate shortest paths, and iterate
            # print(f"grid.shortest_paths({start}, {goal})")
            path = grid.shortest_path(start, goal)
            if path:
                path_tiles.update(path)
                cache_path(start, goal, path)
                reachable_keys[idx].add(key)


def explore_map(map_text):
    """
    Breadth First Search to explore map.
    utilized bitmask for keys and doors, shaved part 1 from 16 seconds to 13 seconds
    """
    # init grid with map_text
    grid = MyGrid(map_text)
    # init start_points
    start_points = []

    # find starting coordinates and keys
    load_map_data(grid, start_points)
    # calculate paths to all keys, this shaved part 1 from 15 seconds to 7 seconds
    # note, may cause issues for part 2, testing. Okay, this was minimal for part 2
    # init path_tiles as empty set
    # added paths between the keys as well, this may cost more time upfront, just
    # concerned it may miss the shortest path.  may take this out if it takes
    # too long.  yeah, that took part 1 to 109 seconds
    path_tiles = set()
    reachable_keys = []
    starting_paths(grid, start_points, path_tiles, reachable_keys)
    # init heap
    heap = []
    # add explorer to heap at start point holding no keys
    # heappush(heap, (0, Explorer(pos=start_points)))
    heappush(heap, Explorer(pos=start_points))

    # init closed set seen
    seen = {}
    # init min_steps
    min_steps = float("infinity")
    # process heap
    while heap:
        # pull explorer from heap
        explorer = heappop(heap)
        if explorer.steps >= min_steps:
            continue
        # if we have seen this state, move on
        if explorer.state() in seen and explorer.steps >= seen[explorer.state()]:
            continue
        seen[explorer.state()] = explorer.steps

        # if we have found all the keys, set min_steps and break
        if explorer.keys == bitmasks["keys"]:
            min_steps = min(min_steps, explorer.steps)

        for idx, pos in enumerate(explorer.pos):
            # get reachable keys
            for test_key in reachable_keys[idx]:
                path = key_reachable(grid, pos, test_key, explorer.keys)
                if path:
                    cache_path(pos, keys[test_key], path)
                if not path:
                    continue
                new_explorer = Explorer(
                    pos=list(explorer.pos),
                    steps=explorer.steps + len(path) - 1,
                    key_value=int(explorer.keys),
                    key_string=explorer.key_string + test_key,
                )
                new_explorer.pos[idx] = path[-1]
                new_explorer.keys |= key_to_bit[test_key]
                new_explorer.sort_key = new_explorer.steps - len(
                    new_explorer.key_string
                )
                heappush(heap, new_explorer)
    # return shortest distance
    return min_steps


def split_map(map_text):
    """
    Function to split map for part 2
    """
    # init grid
    grid = Grid(map_text, use_overrides=False)
    # iterate over grid
    for point in grid:
        # find start point
        if grid.get_point(point, "#") == "@":
            # pull all neighbors
            neighbors = grid.get_neighbors(point=point)
            # change start point to wall
            grid.set_point(point, "#")
            # iterate over neighbors
            for direction, neighbor in neighbors.items():
                # ne, nw, se, sw:
                if len(direction) == 2:
                    # make new start point
                    grid.set_point(neighbor, "@")
                else:
                    # make wall
                    grid.set_point(neighbor, "#")
            # stop processing
            break
    # return new text map
    return str(grid)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init map_text
    map_text = input_value
    if part == 2:
        # split map for part 2
        map_text = split_map(input_value)
        # return -1
    # return result of explore_map
    return explore_map(map_text)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019, 18)
    input_text = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 3512, 2: 1514}
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
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
