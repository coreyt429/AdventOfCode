"""
Classes and Functions for workign grid problems.

This was originally ambitious and wanted to handle multiple
data stores and grid types.

I'll keep grid types, but my testing indicates that the overhead
of complex() coordinates is not worth the hassle, and I just like
working with dict() of tuple(x,y) better than list_x(list_y())

So stripping this down to just work with dict() keyed on tuple(x/y)
"""
import sys
from copy import deepcopy
from queue import PriorityQueue
import functools
import numpy as np


neighbor_cache = {
    "screen": {},
    "cartesian": {},
    "matrix": {}
}
class Node:
    """
    Node class A* shortest path solution
    """
    def __init__(self, position, goal, parent=None, **kwargs):
        """
        Init node
        """
        self.parent = parent
        self.position = position
        self.goal = goal
        self.grid = kwargs.get('grid', None)
        if not kwargs.get('skip_scoring', False):
            self.g_score = self.calc_g_score()
            self.h_score = self.calc_h_score()
            self.f_score = self.calc_f_score()
    
    def calc_h_score(self):
        return manhattan_distance(self.position, self.goal)
    
    def calc_g_score(self):
        if not self.parent:
            return 0
        return self.parent.g_score + 1
    
    def calc_f_score(self):
        return self.g_score + self.h_score

    def get_children(self, child_pos):
        return  [self.__class__(
                    child_pos,
                    self.goal,
                    self,
                    grid=self.grid
                )]
    
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
    
    def __eq__(self, other):
        """
        Node equal
        """
        try:
            return self.position == other.position
        except AttributeError:
            return self.position == other
    
    def __hash__(self):
        """
        Node Hash
        """
        return hash(self.position)

def deprecated(message):
    print(f"deprecated: {message} no longer supported!")
    print("import from grid_too_complex instead")
    sys.exit()

class GridIterator:
    def __init__(self, grid, cfg):
        self.grid = grid
        self.cfg = cfg
        self.iter_index = -1
        if self.cfg['coordinate_system'] == 'screen':
            # upper left hand corner -1x
            #self.iter_pos = [-1, 0]
            self.iter_pos = [self.cfg['min'][0] -1, self.cfg['min'][1]]
        elif self.cfg['coordinate_system'] == 'matrix':
            # upper left hand corner -1col
            self.iter_pos = [self.cfg['min'][0], self.cfg['min'][1] -1]
            #self.iter_pos = [0, -1]
        elif self.cfg['coordinate_system'] == 'cartesian':
            # upper left hand corner -1x
            self.iter_pos = [self.cfg['min'][0] -1, self.cfg['max'][1]]
        
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.cfg['coordinate_system'] == 'screen':
            self.iter_pos[0] += 1
            if self.iter_pos[0] > self.cfg['max'][0]:
                self.iter_pos[0] = self.cfg['min'][0]
                self.iter_pos[1] += 1
            if self.iter_pos[1] > self.cfg['max'][1]:
                raise StopIteration
        elif self.cfg['coordinate_system'] == 'matrix':
            # advance column
            self.iter_pos[1] += 1
            if self.iter_pos[1] > self.cfg['max'][1]:
                self.iter_pos[1] = self.cfg['min'][1]
                # advance row
                self.iter_pos[0] += 1
            if self.iter_pos[0] > self.cfg['max'][0]:
                raise StopIteration
        elif self.cfg['coordinate_system'] == 'cartesian':
            # advance x
            self.iter_pos[0] += 1
            if self.iter_pos[0] > self.cfg['max'][0]:
                self.iter_pos[0] = self.cfg['min'][0]
                # decrement y
                self.iter_pos[1] -= 1
            if self.iter_pos[1] < self.cfg['min'][1]:
                raise StopIteration
        return tuple(self.iter_pos)

class Grid():
    def __init__(self, grid_map, **kwargs):
        self.cfg = {}
        self.cfg['coordinate_system'] = kwargs.get('coordinate_system', 'screen')
        self.cfg['datastore'] = kwargs.get('datastore', 'dict')
        if self.cfg['datastore'] != 'dict':
            deprecated(f"datastore {self.cfg['datastore']} no longer supported")
        self.cfg['type'] = kwargs.get('type', 'bounded')
        self.cfg['default_value'] = kwargs.get('default_value', ' ')
        self.map = self.load_map(grid_map)
        self.overrides = kwargs.get('overrides', {})
        self.tmp_overrides = {}
        self.pos = kwargs.get('start_pos', (0,0))
        self.iter_pos = (0, 0)
        self.cfg['pos_type'] = kwargs.get('pos_type', 'tuple')
        if self.cfg['pos_type'] == 'complex':
            deprecated(f"pos_type {self.cfg['pos_type']} not supported")
        self.cfg['use_overrides'] = kwargs.get('use_overrides', True)
        self.update()
        
    def update(self):
        self.cfg['min'], self.cfg['max'] =  self.get_map_size()

    def load_map(self, grid_map):
        X=0
        Y=1
        if isinstance(grid_map, str):
            grid_map = grid_map.strip('\n').split('\n')
        if self.cfg['coordinate_system'] == 'screen':
            # Screen Coordinates (x as horizontal, y as vertical)
            tmp_list = [list(line) for line in grid_map]
            tmp_dict = {}
            for row, line in enumerate(tmp_list):
                for col, char in enumerate(line):
                    tmp_dict[(col, row)] = char
            return tmp_dict
        if self.cfg['coordinate_system'] == 'matrix':
            # Matrix Coordinates
            tmp_list = [list(line) for line in grid_map]
            tmp_dict = {}
            for row, line in enumerate(tmp_list):
                for col, char in enumerate(line):
                    tmp_dict[(row, col)] = char
            return tmp_dict
        if self.cfg['coordinate_system'] == 'cartesian':
            def rotate_90_degrees(matrix):
                return [list(row) for row in zip(*matrix[::-1])]
            # Cartesian Coordinates (bottom-left origin, y increases upwards)
            tmp_list = rotate_90_degrees(grid_map)
            tmp_dict = {}
            for row, line in enumerate(tmp_list):
                for col, char in enumerate(line):
                    tmp_dict[(row, col)] = char
            return tmp_dict
    
    def __iter__(self):
        #self.update()
        return GridIterator(self.map, self.cfg)

    def __str__(self):
        X=0
        Y=1
        # leaving this for backards compatibility
        if not self.overrides:
            self.overrides = {self.pos: '*'}
        # if self.tmp_overrides:
        #     for key, value in self.tmp_overrides.items():
        #         overrides[key] = value
        my_string = ""
        if self.cfg['coordinate_system'] == 'matrix':
            last_x = 0
            for point in self:
                # new row, new line
                if point[0] != last_x:
                    last_x = point[0]
                    my_string += "\n"
                # if point in overrides:
                #     my_string += overrides[point]
                # else:
                my_string += self.get_point(point, self.cfg["default_value"])
            my_string += '\n'
        elif self.cfg['coordinate_system'] == 'screen':
            last_y = 0
            for point in self:
                # new row, new line
                if point[1] != last_y:
                    last_y = point[1]
                    my_string += "\n"
                # if point in overrides:
                #     my_string += overrides[point]
                # else:
                my_string += self.get_point(point, self.cfg["default_value"])
            my_string += '\n'
        elif self.cfg['coordinate_system'] == 'cartesian':
            last_y = 0
            for point in self:
                # new row, new line
                if point[1] != last_y:
                    last_y = point[1]
                    my_string += "\n"
                # if point in overrides:
                #     my_string += overrides[point]
                # else:
                my_string += self.get_point(point, self.cfg["default_value"])
            my_string += '\n'
        else:
            my_string = f"Unhandled coordinate_system: {self.cfg['coordinate_system']}"
        return my_string.strip('\n')
    
    def get_map_size(self):
        """
        Function to get min(X,Y), max(X,Y) for map
        """
        X, Y = 0, 1
        keys = self.map.keys()
        
        # Initialize min and max using the first key in the map
        try:
            first_key = next(iter(keys))
        except StopIteration:
            return (0,0), (0,0)
        minimum = [first_key[X], first_key[Y]]
        maximum = [first_key[X], first_key[Y]]
        
        # Check map, overrides, and tmp_overrides
        for check_dict in [self.map, self.overrides, self.tmp_overrides]:
            keys = check_dict.keys()
            # Iterate through the keys starting from the second one
            for key in keys:
                minimum[X] = min(minimum[X], key[X])
                maximum[X] = max(maximum[X], key[X])
                minimum[Y] = min(minimum[Y], key[Y])
                maximum[Y] = max(maximum[Y], key[Y])
        return minimum, maximum

    def get_neighbor_offsets(self, **kwargs):
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
        self.neighbor_offsets = {"tuple": {}}

        offsets = offset_collection[self.cfg.get('coordinate_system', 'screen')]
        # directions = kwargs.get('directions', offsets.keys())
        # lets always return all offsets, to improve cache hits
        directions = offsets.keys()
        # print(f"get_neighbor_offsets(directions={directions})")

        # Calculate offsets:
        for direction in directions:
            point = offsets[direction]
            self.neighbor_offsets['tuple'][direction] = point
        return self.neighbor_offsets
    
    
    def get_neighbors(self, **kwargs):
        """
        Function to get neighbors of a point on a map or maze
        This function assumes screen coordinates.  If using another coordinate system,
        please update. Maybe a rule flag to specify?

        Args:
            # inherited from class now
            **kwargs:  using kwargs for rules instead to be more flexible
            point: tuple(x,y) # should match maze, or things may break
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
            neighbors: list(tuple(x,y))

        Notes:
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
        # init point, default to self.pos
        point = kwargs.get("point", self.pos)
        # define booleans:
        # I think I'm getting technical here, but this may matter when we go to apply rules
        # as I typically provide matrix coordinates as (row, col)
        if kwargs.get('coordinate_system', 'screen') ==  'matrix':
            X=1
            Y=0
        neighbors = []
        if point in neighbor_cache[self.cfg["coordinate_system"]]:
            neighbors =  neighbor_cache[self.cfg["coordinate_system"]][point]
        if not neighbors:
            # define offsets
            offsets = self.get_neighbor_offsets(**kwargs)
            # empty list of neighbors
            neighbors = {}
            for direction, offset in offsets["tuple"].items():
                neighbors[direction] = tuple([point[X] + offset[X], point[Y] + offset[Y]])
            # process rule type:bounded
            if self.cfg["type"] == "bounded":
                # minimum, maximum = self.get_map_size()
                valid_neighbors = {}
                for direction, neighbor in neighbors.items():
                    if neighbor in self.map:
                        valid_neighbors[direction] = neighbor
                neighbors = valid_neighbors
            neighbor_cache[self.cfg["coordinate_system"]][point] = neighbors
        # are there invalid character rules, note, this will probably break in type:infinite
        if "invalid" in kwargs:
            valid_neighbors = {}
            for direction, neighbor in neighbors.items():
                if not self.get_point(neighbor) in kwargs['invalid']:
                    valid_neighbors[direction] = neighbor
            neighbors = valid_neighbors
        
        if "directions" in kwargs:
            neighbors = {key:value for key, value in neighbors.items() if key in kwargs['directions']}
        return neighbors
    
    def get_point(self, point, default='.', ob_default='%'):
        """
        Function to retrieve the value of a point
        """
        #self.update()
        if self.cfg['use_overrides']:
            if point in self.overrides:
                return self.overrides.get(point, default)
            if point in self.tmp_overrides:
                return self.overrides.get(point, default)
        if not self.in_bounds(point):
            return ob_default
        return self.map.get(point, default)
    
    def in_bounds(self, point):
        if not (self.cfg["min"][0] <= point[0] <= self.cfg["max"][0]):
            return False
        if not (self.cfg["min"][1] <= point[1] <= self.cfg["max"][1]):
            return False
        return True
    
    def set_point(self, point, value=None):
        """
        Function to set the value of a point
        """
        if not value:
            value = self.cfg["default_value"]
        self.map[point] = value
        # if self.cfg["type"] == "infinite":
        #     self.cfg['min'], self.cfg['max'] =  self.get_map_size()
        return True

    def move(self, direction, **kwargs):
        translation_table = {
            "up":    "n",
            "u":     "n",
            "down":  "s",
            "d":     "s",
            "left":  "w",
            "l":     "w",
            "right": "e",
            "r":     "e"
            
        }
        self.overrides.pop(self.pos, None)
        # normalize to lowercase
        direction = direction.lower()
        # normalize to n, s, e, w
        if direction in translation_table:
            direction = translation_table[direction]
        neighbors = self.get_neighbors(directions=[direction], **kwargs)
        if direction in neighbors:
            if self.cfg["type"] == "infinite":
                value = self.get_point(neighbors[direction], self.cfg["default_value"])
                self.set_point(neighbors[direction], value)
                # self.cfg['min'], self.cfg['max'] =  self.get_map_size()
            self.pos = neighbors[direction]
            self.overrides[self.pos] = '*'
            return True
        return False

    def shortest_paths(self, start, goal, invalid=['#'], directions=['n','s','e','w'], max_paths=1, limit=None, **kwargs):
        debug = kwargs.get('debug', False)
        node_class = kwargs.get('node_class', Node)
        use_closed_set = kwargs.get('use_closed_set', True)
        #if debug: print(f"shortest_paths({start}, {goal}, {invalid}, {directions}, {max_paths}, {limit})")
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
        # init shortest_paths and shortest_length
        shortest_paths = []
        shortest_nodes = []
        shortest_length = float('infinity')
        # set start_node  (position, g_score, h_score)
        start_node = node_class(start, goal, grid=self)
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
            # print(f"queue: {open_set.qsize()}, current: {current_node.g_score} {current_node.position}")
            if use_closed_set and (current_node.parent, current_node) in closed_set:
                #if debug: print(f"current_position already closed: {current_node.position}")
                continue
            
            if limit and current_node.g_score > limit:
                if current_node.parent:
                    closed_set.add((current_node.parent, current_node))
                #if debug: print(f"limit reached: {limit} < {current_node.g_score}")
                continue

            # ignore paths that are longer than the shortest seen
            if current_node.g_score > shortest_length:
                if current_node.position == goal:
                    path = current_node.path()
                    #if debug: print(f"failed path of length({len(path)}): {path}")
                continue
            if current_node.has_loop():
                #if debug: print(f"Loop detected: {current_node.path()}")
                continue

            # are we at the goal?
            if current_node.position == goal:
                path = current_node.path()
                #if debug: print(f"Found path of length({len(path)}): {path}")
                #if debug: print(f"{current_node.g_score} == {shortest_length}: {current_node.g_score == shortest_length}")
                if current_node.g_score == shortest_length:
                    # add  path to shortest paths
                    shortest_paths.append(path)
                    shortest_nodes.append(current_node)
                elif current_node.g_score < shortest_length:
                    # set shortest paths to reverse path
                    shortest_paths = [path]
                    shortest_nodes = [current_node]
                    shortest_length = current_node.g_score
                    if len(shortest_paths) == max_paths:
                        #if debug: print(f"max_paths {max_paths} reached {len(shortest_paths)}")
                        # return shortest_paths
                        # break while loop instead
                        break
                continue

            # add to closed set movement from parent to current
            if current_node.parent:
                closed_set.add((current_node.parent.position, current_node.position))
            # get neighbors
            neighbors = self.get_neighbors(point=current_node.position, invalid=invalid, directions=directions)
            #if debug: print(f"neighbors of {current_node.position} are {neighbors}")
            for direction in directions:
                #if debug: print(f"Trying neighbor: {direction} {neighbors.get(direction, None)}")
                neighbor_pos = neighbors.get(direction, None)
                if not neighbor_pos:
                    continue
                # Set neighbor node
                neighbor_nodes = current_node.get_children(neighbor_pos)
                if not neighbor_nodes:
                    continue
                for neighbor_node in neighbor_nodes:
                    # print(f"neighbor_node: {neighbor_node}")
                    # skip if already closed
                    if use_closed_set and (current_node, neighbor_node) in closed_set:
                        #if debug: print(f"neighbor: {neighbor_pos} already closed")
                        continue
                    # if not already in open_set, add it
                    if (neighbor_node.f_score, neighbor_node) not in open_set.queue:
                        open_set.put((neighbor_node.f_score, neighbor_node))
                    #else:
                        #if debug: print(f"neighbor: {neighbor_node.position} f_score: {neighbor_node.f_score} already in open set")
        if kwargs.get('retval', 'path') == 'length':
            return shortest_length
        if kwargs.get('retval', 'path') == 'both':
            return shortest_length, shortest_paths
        if kwargs.get('retval', 'path') == 'nodes':
            return shortest_nodes
        return shortest_paths

@functools.lru_cache(maxsize=None)
def manhattan_distance_old(start, goal):
    """
    Function to calculate manhattan distance between two points
    in 2D (x,y) or 3D (x,y,z)
    """
    # handle 2d or 3d tuples
    return sum(abs(s - g) for s, g in zip(start, goal))

@functools.lru_cache(maxsize=None)
def manhattan_distance(p1, p2):
    return np.sum(np.abs(np.array(p1) - np.array(p2)))

if __name__ == "__main__":
    test_grid = "123\n456\n789"
    print(f"Test pattern:\n{test_grid}\n")
    print("Test 1 Grid generation, iteration, and printing")
    for coordinate_system in ["screen", "matrix", "cartesian"]:
        print(f"coordinate_system: {coordinate_system}, bounded")
        grid = Grid(test_grid, coordinate_system=coordinate_system)
        grid.move('u')
        grid.move('u')
        print(grid)
        print()

    print("Test 2 Neighbors")
    for coordinate_system in ["screen", "matrix", "cartesian"]:
        print(f"coordinate_system: {coordinate_system}, bounded")
        grid = Grid(test_grid, coordinate_system=coordinate_system)
        print(f"Neighbors of {grid.pos}: {grid.get_neighbors()}")
    
    print("Test 3 movement")
    for coordinate_system in ["screen", "matrix", "cartesian"]:
        print(f"coordinate_system: {coordinate_system}, bounded")
        grid = Grid(test_grid, coordinate_system=coordinate_system)
        for direction in 'drul':
            print(f"direction: {direction}")
            grid.move(direction)
            grid.move(direction)
            print(grid)
            print()
    
    print("Test 4 infinite cartesian")
    coordinate_system = 'cartesian'
    grid = Grid(test_grid, coordinate_system=coordinate_system, )

