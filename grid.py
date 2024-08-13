from copy import deepcopy

#FIXME, dont' take complex  coordinates into account

class Grid():
    def __init__(self, grid_map, **kwargs):
        self.cfg = {}
        self.cfg['coordinate_system'] = kwargs.get('coordinate_system', 'screen')
        self.cfg['datastore'] = kwargs.get('datastore', 'dict')
        self.map = self.load_map(grid_map)
        self.pos = kwargs.get('start_pos', (0,0))
        if self.cfg['datastore'] == 'dict':
            self.cfg['pos_type'] = kwargs.get('pos_type', 'tuple')
            if self.cfg['pos_type'] == 'complex':
                self.convert_map()
                if isinstance(self.pos, tuple):
                    self.pos = complex(*self.pos)
        self.cfg['min'], self.cfg['max'] =  self.get_map_size()

    def convert_map(self):
        keys = self.map.keys()
        for key in list(keys):
            if isinstance(key, tuple):
                self.map[complex(*key)] = self.map.pop(key)
        
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
            if self.cfg['datastore'] == 'dict':
                return tmp_dict
            # Rebuild screen list from the dict
            tmp_list = [['' for _ in range(3)] for _ in range(3)]  # Initialize an empty grid
            for (x, y), value in tmp_dict.items():
                tmp_list[x][y] = value
            return tmp_list
        if self.cfg['coordinate_system'] == 'matrix':
            # Matrix Coordinates
            tmp_list = [list(line) for line in grid_map]
            if self.cfg['datastore'] == 'list':
                return tmp_list
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
            if self.cfg['datastore'] == 'list':
                return tmp_list
            tmp_dict = {}
            for row, line in enumerate(tmp_list):
                for col, char in enumerate(line):
                    tmp_dict[(row, col)] = char
            return tmp_dict
            
    
    def __str__(self):
        X=0
        Y=1
        do_complex = False
        if self.cfg['datastore'] == 'dict':
            if self.cfg['pos_type'] == 'complex':
                do_complex = True
        my_string = ""
        if self.cfg['coordinate_system'] == 'matrix':
            if self.cfg['datastore'] == 'list':
                for y, row  in enumerate(self.map):
                    for x, char in enumerate(row):
                        if (y, x) == self.pos:
                            my_string += '*'
                        else:
                            my_string += char
                    my_string += '\n'
            elif self.cfg['datastore'] == 'dict':
                # Determine the size of the grid
                max_x = self.cfg["max"][X] + 1
                max_y = self.cfg["max"][Y] + 1
                for x in range(max_x):
                    for y in range(max_y):
                        if do_complex:
                            if complex(x, y) == self.pos:
                                my_string += '*'
                            else:
                                my_string += self.map.get(complex(x, y), ' ')
                        else:
                            if (x, y) == self.pos:
                                my_string += '*'
                            else:
                                my_string += self.map.get((x, y), ' ')
                    my_string += '\n'
        elif self.cfg['coordinate_system'] == 'screen':
            if self.cfg['datastore'] == 'list':
                for y in range(len(self.map)):
                    for x in range(len(self.map[0])):
                        if (x, y) == self.pos:
                            my_string += '*'
                        else:
                            my_string += self.map[x][y]
                    my_string += '\n'
            elif self.cfg['datastore'] == 'dict':
                # Determine the size of the grid
                max_x = self.cfg["max"][X] + 1
                max_y = self.cfg["max"][Y] + 1
                for y in range(max_y):
                    for x in range(max_x):
                        if do_complex:
                            if complex(x, y) == self.pos:
                                my_string += '*'
                            else:
                                my_string += self.map.get(complex(x, y), ' ')
                        else:
                            if (x, y) == self.pos:
                                my_string += '*'
                            else:
                                my_string += self.map.get((x, y), ' ')
                    my_string += '\n'
        elif self.cfg['coordinate_system'] == 'cartesian':
            if self.cfg['datastore'] == 'list':
                max_x = len(self.map)
                max_y = len(self.map[0])
                for y in range(max_y - 1, -1, -1):
                    for x in range(max_x):
                        if (x, y) == self.pos:
                            my_string += '*'
                        else:
                            my_string += self.map[x][y]
                    my_string += '\n'   
            elif self.cfg['datastore'] == 'dict':
                # Determine the size of the grid
                max_x = self.cfg["max"][X] + 1
                max_y = self.cfg["max"][Y] + 1
                for y in range(max_y - 1, -1, -1):
                    for x in range(max_x):
                        if do_complex:
                            if complex(x, y) == self.pos:
                                my_string += '*'
                            else:
                                my_string += self.map.get(complex(x, y), ' ')
                        else:
                            if (x, y) == self.pos:
                                my_string += '*'
                            else:
                                my_string += self.map.get((x, y), ' ')
                    my_string += '\n'
        else:
            my_string = f"Unhandled coordinate_system: {self.cfg['coordinate_system']}"
        return my_string.strip('\n')
    
    def get_map_size(self):
        """
        Function to get min(X,Y), max(X,Y) for map
        """
        X=0
        Y=1
        if isinstance(self.map, list):
            # list of list, return 0 to length
            min = tuple([0, 0])
            max = tuple([len(self.map), len(self.map[0])])
            return min, max
        if not isinstance(self.map, dict):
            print(f"get_map_size no rule to handle {type(self.map)}")
            sys.exit()
        # complex or tuple?
        min = [float('infinity')]*2
        max = [float('infinity')*-1]*2
        is_complex = isinstance(list(self.map.keys())[0], complex)
        for key in self.map.keys():
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
        self.neighbor_offsets = {"tuple": {}, "complex": {}}

        offsets = offset_collection[self.cfg.get('coordinate_system', 'screen')]
        directions = kwargs.get('directions', offsets.keys())

        # Calculate offsets:
        for direction in directions:
            point = offsets[direction]
            self.neighbor_offsets['tuple'][direction] = point
            self.neighbor_offsets['complex'][direction] = complex(*point)
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
            #point: tuple(x,y) or complex() # should match maze, or things may break
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
        is_dict = isinstance(self.map, dict)
        #is_list = isinstance(self.map, list)
        is_complex = False
        if is_dict:
            is_complex = isinstance(list(self.map.keys())[0], complex)
        # I think I'm getting technical here, but this may matter when we go to apply rules
        # as I typically provide matrix coordinates as (row, col)
        if kwargs.get('coordinate_system', 'screen') ==  'matrix':
            X=1
            Y=0
        # define offsets
        offsets = self.get_neighbor_offsets(**kwargs)
        #print(f"offsets: {offsets}")
        # empty list of neighbors
        neighbors = {}
        if is_complex:
            for direction, offset in offsets["complex"].items():
                neighbors[direction] = self.pos + offset
        else:
            for direction, offset in offsets["tuple"].items():
                neighbors[direction] = tuple([self.pos[X] + offset[X], self.pos[Y] + offset[Y]])
        # process rule type:bounded
        if kwargs.get("type", "bounded") == "bounded":
            min, max = self.get_map_size()
            #print(f"Maze size: min: {min}, max: {max}")
            valid_neighbors = {}
            for direction, neighbor in neighbors.items():
                #print(f"bounded, checking {neighbor}")
                if is_dict:
                    if neighbor in self.map:
                        valid_neighbors[direction] = neighbor
                else:
                    if min[X] <= neighbor[X] < max[X] and min[Y] <= neighbor[Y] < max[Y]:
                        valid_neighbors[direction] = neighbor
                neighbors = valid_neighbors
        # are there invalid character rules, note, this will probably break in type:infinite
        if "invalid" in kwargs:
            valid_neighbors = {}
            for direction, neighbor in neighbors.items():
                #print(f"invalid: checking {neighbor}")
                if is_dict:
                    #print(f"dict: {neighbor}: {self.map[neighbor]} in {kwargs['invalid']}")
                    if not self.map[neighbor] in kwargs['invalid']:
                        valid_neighbors[direction] = neighbor
                else:
                    # using 0/1 here instead of X/Y to avoid an extra if condition to 
                    # look for swapped x/y for matrix coordinates, when we get to a
                    # matrix coordinate puzzle, we will need to test thoroughly
                    #if not self.map[neighbor[0][1]] in kwargs['invalid']:
                    print(f"list: {neighbor}: {self.map[neighbor[X]][neighbor[Y]]} in {kwargs['invalid']}")
                    if not self.map[neighbor[X]][neighbor[Y]] in kwargs['invalid']:
                        valid_neighbors[direction] = neighbor
            neighbors = valid_neighbors
        return neighbors
    
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
        # normalize to lowercase
        direction = direction.lower()
        # normalize to n, s, e, w
        if direction in translation_table:
            direction = translation_table[direction]
        neighbors = self.get_neighbors(directions=[direction], **kwargs)
        if direction in neighbors:
            self.pos = neighbors[direction]
            return True
        return False

def manhattan_distance(start, goal):
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
            return abs(start[X] - goal[X]) + abs(start[Y] - goal[Y]) + abs(start[Z] - goal[Z])
    if isinstance(start, complex):  # Still handle complex numbers as 2D
        return int(abs(start.real - goal.real) + abs(start.imag - goal.imag))