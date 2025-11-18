from copy import deepcopy
from queue import PriorityQueue

# FIXME, dont' take complex  coordinates into account
neighbors_cache = {}


class Node:
    """
    Node class A* shortest path solution
    """

    def __init__(self, position, g_score, h_score, parent=None):
        """
        Init node
        """
        self.position = position
        self.g_score = g_score
        self.h_score = h_score
        self.f_score = g_score + h_score
        self.parent = parent

    def has_loop(self):
        path = list(self.path())
        for pos in path:
            if path.count(pos) > 1:
                return True
        return False

    def path(self):
        trace_node = self
        # start at current node
        path = []
        while trace_node:
            # add position to path
            path.append(trace_node.position)
            # move to parent
            trace_node = trace_node.parent
        return tuple(path[::-1])

    def __gt__(self, other):
        """
        Node greater than
        """
        return self.f_score > other.f_score

    def __lt__(self, other):
        """
        Node less than
        """
        return self.f_score < other.f_score


class Grid:
    def __init__(self, grid_map, **kwargs):
        self.cfg = {}
        self.cfg["coordinate_system"] = kwargs.get("coordinate_system", "screen")
        self.cfg["datastore"] = kwargs.get("datastore", "dict")
        self.cfg["type"] = kwargs.get("type", "bounded")
        self.cfg["default_value"] = kwargs.get("default_value", " ")
        self.map = self.load_map(grid_map)
        self.overrides = kwargs.get("overrides", {})
        self.tmp_overrides = {}
        self.pos = kwargs.get("start_pos", (0, 0))
        self.iter_pos = (0, 0)
        if self.cfg["datastore"] == "dict":
            self.cfg["pos_type"] = kwargs.get("pos_type", "tuple")
            if self.cfg["pos_type"] == "complex":
                self.convert_map()
                if isinstance(self.pos, tuple):
                    self.pos = complex(*self.pos)
        self.cfg["min"], self.cfg["max"] = self.get_map_size()

    def convert_map(self):
        keys = self.map.keys()
        for key in list(keys):
            if isinstance(key, tuple):
                self.map[complex(*key)] = self.map.pop(key)

    def load_map(self, grid_map):
        X = 0
        Y = 1
        if isinstance(grid_map, str):
            grid_map = grid_map.strip("\n").split("\n")
        if self.cfg["coordinate_system"] == "screen":
            # Screen Coordinates (x as horizontal, y as vertical)
            tmp_list = [list(line) for line in grid_map]
            tmp_dict = {}
            for row, line in enumerate(tmp_list):
                for col, char in enumerate(line):
                    tmp_dict[(col, row)] = char
            if self.cfg["datastore"] == "dict":
                return tmp_dict
            # Rebuild screen list from the dict
            tmp_list = [
                ["" for _ in range(3)] for _ in range(3)
            ]  # Initialize an empty grid
            for (x, y), value in tmp_dict.items():
                tmp_list[x][y] = value
            return tmp_list
        if self.cfg["coordinate_system"] == "matrix":
            # Matrix Coordinates
            tmp_list = [list(line) for line in grid_map]
            if self.cfg["datastore"] == "list":
                return tmp_list
            tmp_dict = {}
            for row, line in enumerate(tmp_list):
                for col, char in enumerate(line):
                    tmp_dict[(row, col)] = char
            return tmp_dict
        if self.cfg["coordinate_system"] == "cartesian":

            def rotate_90_degrees(matrix):
                return [list(row) for row in zip(*matrix[::-1])]

            # Cartesian Coordinates (bottom-left origin, y increases upwards)
            tmp_list = rotate_90_degrees(grid_map)
            if self.cfg["datastore"] == "list":
                return tmp_list
            tmp_dict = {}
            for row, line in enumerate(tmp_list):
                for col, char in enumerate(line):
                    tmp_dict[(row, col)] = char
            return tmp_dict

    def __iter__(self):
        # FIXME: currently only handling screen coordinates
        self.iter_pos = [-1, 0]
        return self

    def __next__(self):
        # FIXME: currently only handling screen coordinates
        self.iter_pos[0] += 1
        if self.iter_pos[0] > self.cfg["max"][0]:
            self.iter_pos[0] = 0
            self.iter_pos[1] += 1
        if self.iter_pos[1] > self.cfg["max"][1]:
            raise StopIteration
        return tuple(self.iter_pos)

    def __str__(self):
        X = 0
        Y = 1
        overrides = self.overrides
        if not overrides:
            overrides = {self.pos: "*"}
        if self.tmp_overrides:
            for key, value in self.tmp_overrides.items():
                overrides[key] = value
        do_complex = False
        if self.cfg["datastore"] == "dict":
            if self.cfg["pos_type"] == "complex":
                do_complex = True
        my_string = ""
        if self.cfg["coordinate_system"] == "matrix":
            if self.cfg["datastore"] == "list":
                for y, row in enumerate(self.map):
                    for x, char in enumerate(row):
                        if (y, x) in overrides:
                            my_string += overrides[(x, y)]
                        else:
                            my_string += char
                    my_string += "\n"
            elif self.cfg["datastore"] == "dict":
                # Determine the size of the grid
                max_x = self.cfg["max"][X] + 1
                max_y = self.cfg["max"][Y] + 1
                for x in range(max_x):
                    for y in range(max_y):
                        if do_complex:
                            if complex(x, y) in overrides:
                                my_string += overrides[complex(x, y)]
                            else:
                                my_string += self.map.get(
                                    complex(x, y), self.cfg["default_value"]
                                )
                        else:
                            if (x, y) in overrides:
                                my_string += overrides[(x, y)]
                            else:
                                my_string += self.map.get(
                                    (x, y), self.cfg["default_value"]
                                )
                    my_string += "\n"
        elif self.cfg["coordinate_system"] == "screen":
            if self.cfg["datastore"] == "list":
                for y in range(len(self.map)):
                    for x in range(len(self.map[0])):
                        if (x, y) in overrides:
                            my_string += overrides[(x, y)]
                        else:
                            my_string += self.map[x][y]
                    my_string += "\n"
            elif self.cfg["datastore"] == "dict":
                # FIXME: this uses self.__iter__ to generate the map
                # that currently only works for screen coordinate dicts
                # update other sections as that improves
                last_y = 0
                for point in self:
                    # new row, new line
                    if point[1] != last_y:
                        last_y = point[1]
                        my_string += "\n"
                    if do_complex:
                        if complex(point) in overrides:
                            my_string += overrides[point]
                        else:
                            my_string += self.map.get(
                                complex(point), self.cfg["default_value"]
                            )
                    else:
                        if point in overrides:
                            my_string += overrides[point]
                        else:
                            my_string += self.map.get(point, self.cfg["default_value"])
                my_string += "\n"
        elif self.cfg["coordinate_system"] == "cartesian":
            if self.cfg["datastore"] == "list":
                max_x = len(self.map)
                max_y = len(self.map[0])
                for y in range(max_y - 1, -1, -1):
                    for x in range(max_x):
                        if (x, y) in overrides:
                            my_string += overrides[(x, y)]
                        else:
                            my_string += self.map[x][y]
                    my_string += "\n"
            elif self.cfg["datastore"] == "dict":
                # Determine the size of the grid
                max_x = self.cfg["max"][X] + 1
                max_y = self.cfg["max"][Y] + 1
                min_x = self.cfg["min"][X]
                min_y = self.cfg["min"][Y] - 1
                # FIXME:  this is handling correctly, other functions of cartesian need
                #         to be checked to be sure they are taking minimum into account
                for y in range(max_y - 1, min_y, -1):
                    for x in range(min_x, max_x):
                        if do_complex:
                            if complex(x, y) in overrides:
                                my_string += overrides[complex(x, y)]
                            else:
                                my_string += self.map.get(
                                    complex(x, y), self.cfg["default_value"]
                                )
                        else:
                            if (x, y) in overrides:
                                my_string += overrides[(x, y)]
                            else:
                                my_string += self.map.get(
                                    (x, y), self.cfg["default_value"]
                                )
                    my_string += "\n"
        else:
            my_string = f"Unhandled coordinate_system: {self.cfg['coordinate_system']}"
        return my_string.strip("\n")

    def get_map_size(self):
        """
        Function to get min(X,Y), max(X,Y) for map
        """
        X = 0
        Y = 1
        if isinstance(self.map, list):
            # list of list, return 0 to length
            minimum = tuple([0, 0])
            maximum = tuple([len(self.map), len(self.map[0])])
            return minimum, maximum
        if not isinstance(self.map, dict):
            print(f"get_map_size no rule to handle {type(self.map)}")
            sys.exit()
        # complex or tuple?
        minimum = [float("infinity")] * 2
        maximum = [float("infinity") * -1] * 2
        is_complex = isinstance(list(self.map.keys())[0], complex)
        for key in self.map.keys():
            if is_complex:
                if key.real < minimum[X]:
                    minimum[X] = int(key.real)
                if key.real > maximum[X]:
                    maximum[X] = int(key.real)
                if key.imag < minimum[Y]:
                    minimum[Y] = int(key.imag)
                if key.imag > maximum[Y]:
                    maximum[Y] = int(key.imag)
            else:
                if key[X] < minimum[X]:
                    minimum[X] = key[X]
                if key[X] > maximum[X]:
                    maximum[X] = key[X]
                if key[Y] < minimum[Y]:
                    minimum[Y] = key[Y]
                if key[Y] > maximum[Y]:
                    maximum[Y] = key[Y]
        return minimum, maximum

    def get_neighbor_offsets(self, **kwargs):
        """
        Function to calculate neighbor offsets, and store them
        """
        offset_collection = {}
        offset_collection["cartesian"] = {
            "n": (0, 1),  # Move up
            "ne": (1, 1),  # Move up-right
            "e": (1, 0),  # Move right
            "se": (1, -1),  # Move down-right
            "s": (0, -1),  # Move down
            "sw": (-1, -1),  # Move down-left
            "w": (-1, 0),  # Move left
            "nw": (-1, 1),  # Move up-left
        }
        offset_collection["matrix"] = {
            "n": (-1, 0),  # Move up
            "ne": (-1, 1),  # Move up-right
            "e": (0, 1),  # Move right
            "se": (1, 1),  # Move down-right
            "s": (1, 0),  # Move down
            "sw": (1, -1),  # Move down-left
            "w": (0, -1),  # Move left
            "nw": (-1, -1),  # Move up-left
        }
        offset_collection["screen"] = {
            "n": (0, -1),  # Move up
            "ne": (1, -1),  # Move up-right
            "e": (1, 0),  # Move right
            "se": (1, 1),  # Move down-right
            "s": (0, 1),  # Move down
            "sw": (-1, 1),  # Move down-left
            "w": (-1, 0),  # Move left
            "nw": (-1, -1),  # Move up-left
        }

        # Always reset the neighbor offsets for fresh calculation
        self.neighbor_offsets = {"tuple": {}, "complex": {}}

        offsets = offset_collection[self.cfg.get("coordinate_system", "screen")]
        directions = kwargs.get("directions", offsets.keys())

        # Calculate offsets:
        for direction in directions:
            point = offsets[direction]
            self.neighbor_offsets["tuple"][direction] = point
            # self.neighbor_offsets['complex'][direction] = complex(*point)
        return self.neighbor_offsets

    def get_neighbors(self, **kwargs):
        """
        Function to get neighbors of a point on a map or maze
        This function assumes screen coordinates.  If using another coordinate system,
        please update. Maybe a rule flag to specify?

        Notes: see 2023.21 for infinite complex example

        Args:
            # inherited from class now
            #maze: list_x(list_y()) or dict(tuple(x,y) or dict(complex()))
            **kwargs:  using kwargs for rules instead to be more flexible
            point: tuple(x,y) or complex() # should match maze, or things may break
                    defaults to self.pos
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
        X = 0
        Y = 1
        # init point, default to self.pos
        point = kwargs.get("point", self.pos)
        # define booleans:
        is_dict = isinstance(self.map, dict)
        # is_list = isinstance(self.map, list)
        is_complex = False
        if is_dict:
            is_complex = isinstance(list(self.map.keys())[0], complex)
        # I think I'm getting technical here, but this may matter when we go to apply rules
        # as I typically provide matrix coordinates as (row, col)
        if kwargs.get("coordinate_system", "screen") == "matrix":
            X = 1
            Y = 0
        neighbors = neighbors_cache.get(point)
        if not neighbors:
            # define offsets
            offsets = self.get_neighbor_offsets(**kwargs)
            # print(f"offsets: {offsets}")
            # empty list of neighbors
            neighbors = {}
            if is_complex:
                for direction, offset in offsets["complex"].items():
                    neighbors[direction] = point + offset
            else:
                for direction, offset in offsets["tuple"].items():
                    neighbors[direction] = tuple(
                        [point[X] + offset[X], point[Y] + offset[Y]]
                    )
            # process rule type:bounded
            if self.cfg["type"] == "bounded":
                minimum, maximum = self.get_map_size()
                valid_neighbors = {}
                for direction, neighbor in neighbors.items():
                    # print(f"bounded, checking {neighbor}")
                    if is_dict:
                        if neighbor in self.map:
                            valid_neighbors[direction] = neighbor
                    else:
                        if (
                            minimum[X] <= neighbor[X] < maximum[X]
                            and minimum[Y] <= neighbor[Y] < maximum[Y]
                        ):
                            valid_neighbors[direction] = neighbor
                    neighbors = valid_neighbors
            neighbors_cache[point] = neighbors
        # are there invalid character rules, note, this will probably break in type:infinite
        if "invalid" in kwargs:
            valid_neighbors = {}
            for direction, neighbor in neighbors.items():
                # print(f"invalid: checking {neighbor}")
                if is_dict:
                    # print(f"dict: {neighbor}: {self.map[neighbor]} in {kwargs['invalid']}")
                    if not self.get_point(neighbor) in kwargs["invalid"]:
                        valid_neighbors[direction] = neighbor
                else:
                    # using 0/1 here instead of X/Y to avoid an extra if condition to
                    # look for swapped x/y for matrix coordinates, when we get to a
                    # matrix coordinate puzzle, we will need to test thoroughly
                    # if not self.map[neighbor[0][1]] in kwargs['invalid']:
                    print(
                        f"list: {neighbor}: {self.map[neighbor[X]][neighbor[Y]]} in {kwargs['invalid']}"
                    )
                    if not self.map[neighbor[X]][neighbor[Y]] in kwargs["invalid"]:
                        valid_neighbors[direction] = neighbor
            neighbors = valid_neighbors
        return neighbors

    def get_point(self, point, default="."):
        """
        Function to retrieve the value of a point
        """
        if point in self.overrides:
            return self.overrides.get(point, default)
        if point in self.tmp_overrides:
            return self.overrides.get(point, default)
        return self.map.get(point, default)

    def set_point(self, point, value):
        """
        Function to set the value of a point
        """
        self.map[point] = value
        return True

    def move(self, direction, **kwargs):
        translation_table = {
            "up": "n",
            "u": "n",
            "down": "s",
            "d": "s",
            "left": "w",
            "l": "w",
            "right": "e",
            "r": "e",
        }
        # normalize to lowercase
        direction = direction.lower()
        # normalize to n, s, e, w
        if direction in translation_table:
            direction = translation_table[direction]
        neighbors = self.get_neighbors(directions=[direction], **kwargs)
        if direction in neighbors:
            if self.cfg["type"] == "infinite":
                if isinstance(self.map, dict) and neighbors[direction] not in self.map:
                    self.map[neighbors[direction]] = self.cfg["default_value"]
                    self.cfg["min"], self.cfg["max"] = self.get_map_size()
                elif isinstance(self.map, list):
                    print("Infinite currently only supported for dict")
            self.pos = neighbors[direction]
            return True
        return False

    def shortest_paths(
        self,
        start,
        goal,
        invalid=["#"],
        directions=["n", "s", "e", "w"],
        max_paths=1,
        limit=None,
    ):
        # print(f"shortest_paths({start}, {goal}, {invalid}, {directions}, {max_paths})")
        """
        Function to execute A* algorithm to detect shortest path between each pair
        Note, for now this only supports screen coordinate tuple dicts

        Args:
            self: Grid() object
            start: tuple() x/y coordinate
            goal: tuple() x/y coordinate
            invalid: list(str()) characters to exlude from path
            directions: list(str) directions to include in lookups
            max_paths: int() max number of paths to return, default 1
            limit: int() max number of steps

        Returns:
            path: list(tuple()) x/y coordinates of path

        A* Node parameters:
            position: tuple() x/y coordinates
            g_score: int() steps taken
            h_score: int() heuristic manhattan_distance(position, goal)

        """
        shortest_paths = []
        if shortest_paths:
            return shortest_paths

        shortest_length = float("infinity")
        # set start_node  (position, g_score, h_score)
        start_node = Node(start, 0, manhattan_distance(start, goal))
        # initialize PriorityQueue
        open_set = PriorityQueue()
        # add start_node to priority_queue (f_score, node)
        open_set.put((start_node.f_score, start_node))
        # initialize closed set
        closed_set = set()

        # process open set
        while not open_set.empty():
            # get current node
            current_node = open_set.get()[1]
            if current_node.position in closed_set:
                continue

            if limit and current_node.g_score > limit:
                closed_set.add(current_node.position)
                # print(f"limit reached: {limit} < {current_node.g_score}")
                continue

            # ignore paths that are longer than the shortest seen
            if current_node.g_score > shortest_length:
                if current_node.position == goal:
                    path = current_node.path()
                    # print(f"failed path of length({len(path)}): {path}")
                continue
            if current_node.has_loop():
                # print(f"Loop detected: {current_node.path()}")
                continue

            # are we at the goal?
            if current_node.position == goal:
                path = current_node.path()
                # print(f"Found path of length({len(path)}): {path}")
                # print(f"{current_node.g_score} == {shortest_length}: {current_node.g_score == shortest_length}")
                if current_node.g_score == shortest_length:
                    # add  path to shortest paths
                    shortest_paths.append(path)
                elif current_node.g_score < shortest_length:
                    # set shortest paths to reverse path
                    shortest_paths = [path]
                    shortest_length = current_node.g_score
                    if len(shortest_paths) == max_paths:
                        # print(f"max_paths {max_paths} reached {len(shortest_paths)}")
                        return shortest_paths

            # add to closed set
            closed_set.add(current_node.position)
            # get neighbors
            neighbors = self.get_neighbors(
                point=current_node.position, invalid=invalid, directions=directions
            )
            for direction in ["n", "w", "e", "s"]:
                neighbor_pos = neighbors.get(direction, None)
                if not neighbor_pos:
                    continue
                # skip if already closed
                if neighbor_pos in closed_set:
                    continue
                # Set neighbor node
                neighbor_node = Node(
                    neighbor_pos,
                    current_node.g_score + 1,
                    manhattan_distance(neighbor_pos, goal),
                    current_node,
                )
                # if not already in open_set, add it
                if (neighbor_node.f_score, neighbor_node) not in open_set.queue:
                    open_set.put((neighbor_node.f_score, neighbor_node))
        return shortest_paths


def manhattan_distance_old(start, goal):
    """
    Function to calculate manhattan distance between two points
    in 2D (x,y) or 3D (x,y,z)
    """
    X = 0
    Y = 1
    Z = 2

    if isinstance(start, tuple):
        if len(start) == 2:  # 2D coordinates
            return abs(start[X] - goal[X]) + abs(start[Y] - goal[Y])
        elif len(start) == 3:  # 3D coordinates
            return (
                abs(start[X] - goal[X])
                + abs(start[Y] - goal[Y])
                + abs(start[Z] - goal[Z])
            )
    if isinstance(start, complex):  # Still handle complex numbers as 2D
        return int(abs(start.real - goal.real) + abs(start.imag - goal.imag))


manhattan_distance_cache = {}


def manhattan_distance(start, goal):
    """
    Function to calculate manhattan distance between two points
    in 2D (x,y) or 3D (x,y,z)
    """
    cached_value = manhattan_distance_cache.get(start, {}).get(goal, None)
    if cached_value:
        return cached_value
    # handle 2d or 3d tuples
    if isinstance(start, tuple):
        if start not in manhattan_distance_cache:
            manhattan_distance_cache[start] = {}
        manhattan_distance_cache[start][goal] = sum(
            abs(s - g) for s, g in zip(start, goal)
        )
        return manhattan_distance_cache[start][goal]

    # Handle complex numbers as 2D
    if isinstance(start, complex):
        return int(abs(start.real - goal.real) + abs(start.imag - goal.imag))

    raise TypeError("Unsupported coordinate type. Must be tuple or complex.")
