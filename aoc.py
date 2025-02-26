"""
AdventOfCode utility Module
contains utility functions for working AdventOfCode puzzles
"""
import sys
import re
import json
from datetime import datetime
import requests
import os
import time
from getpass import getpass

class AdventOfCode:
    """
    Advent of Code class to handle common functions for solving puzzles"""
    def __init__(self, year=None, day=None):
        today = datetime.today()
        self.year = year if year is not None else today.year
        self.day = day if day is not None else today.day
        # define, but don't calculate yet, we may not need them
        self.neighbor_offsets = {}
        self.start_time = time.time()
        self.parts = {
            1: 1,
            2: 2
        }
        # dict to store answers
        self.answer = {
            1: None,
            2: None
        }
        # correct answers once solved, to validate changes
        self.correct = {
            1: 0,
            2: 0
        }
        # dict to map functions
        self.funcs = {
            1: None,
            2: None
        }
        matches = re.match(r'(.*AdventOfCode).*',os.getcwd())
        if matches:
            base_dir = matches.group(1)
        else:
            base_dir = os.getcwd()

        self.session_file = os.path.join(base_dir,'.aoc.session')
        self.session_id = self.get_session_id()
    def get_session_id(self):
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                self.session_id =  f.read().strip()
                return self.session_id
        return None

    def save_session_id(self):
        with open(self.session_file, 'w') as f:
            f.write(self.session_id)

    def test_session(self):
        response = self.session.get('https://adventofcode.com')
        return 'Advent of Code' in response.text

    def run(self):
        # loop parts
        for my_part in self.parts:
            # log start time
            self.start_time = time.time()
            # get answer
            self.answer[my_part] = self.funcs[my_part](self.input_data, my_part)
            # log end time
            end_time = time.time()
            # print results
            print(f"Part {my_part}: {self.answer[my_part]}, took {end_time-self.start_time} seconds")
            if self.correct[my_part]:
                assert self.correct[my_part] == self.answer[my_part]

    def get_input(self):
        self.init_session()
        url = f'https://adventofcode.com/{self.year}/day/{self.day}/input'
        response = self.session.get(url)
        if response.status_code == 200:
            self.save_input(response.text)
            print(f"Input for day {self.day} of year {self.year} has been saved.")
            return response.text
        else:
            print(f"Failed to retrieve input. Status code: {response.status_code}")
            return None

    def save_input(self, content):
        if not os.path.exists(f'{self.year}'):
            os.makedirs(f'{self.year}')
        with open(f'{self.year}/{self.day}/input.txt', 'w') as f:
            f.write(content)

    def login_to_aoc(self):
        self.session = requests.Session()
        self.session.cookies.set('session', self.session_id)
        return self.session

    def init_session(self):
        self.get_session_id()
        self.session = None

        while True:
            if self.session_id:
                self.session = self.login_to_aoc()
                if self.test_session():
                    break
                else:
                    print("Saved session ID is invalid.")
                    self.session_id = None
            else:
                print("Please enter your Advent of Code session ID.")
                print("You can find this in your browser's cookies for adventofcode.com")
                self.session_id = getpass("Session ID: ")
                self.save_session_id()

    def set_date(self, year, day):
        """
        Function to set the year and day used by functions
        This is likely deprecated by passing the year and day to init
        """
        self.year = year
        self.day = day

    def get_file(self, file_name=None):
        """
        Utility function to open an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - file handle
        """
        if file_name is None:
            file_name = f"{self.year}/{self.day}/input.txt"
        try:
            return open(file_name, 'r', encoding='utf-8')
        except OSError as error_message:
            try:
                self.get_input()
                return open(file_name, 'r', encoding='utf-8')
            except OSError as error_message:
                # file is missing, lets download it
                print(f"Error opening file {file_name}: {error_message}")
                sys.exit()

    def load_lines(self, file_name=None):
        """
        Function to load an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - list of lines from the file
        """
        self.input_data = self.load_text(file_name).rstrip().split('\n')
        return self.input_data
        
    def load_text(self, file_name=None):
        """
        Function to load an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - text content of the file
        """
        with self.get_file(file_name) as file:
            self.input_data = file.read().rstrip()
            return self.input_data

    def load_integers(self, file_name=None):
        """
        Function to load an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - list of ints from file
        """
        self.input_data = [int(x) for x in self.load_lines(file_name)]
        return self.input_data

    def load_grid(self, file_name=None):
        """
        Function to load an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - list of lists from file
        """
        self.input_data =  [list(line) for line in self.load_lines(file_name)]
        return self.input_data
    
    def get_neighbor_offsets(self, **kwargs):
        """
        Function to calculate neighbor offsets, and store them
        """
        print(f"deprecated: get_neighbor_offsets: {kwargs}")
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
        self.neighbor_offsets = {"tuple": [], "complex": []}

        offsets = offset_collection[kwargs.get('coordinate_system', 'screen')]
        directions = kwargs.get('directions', offsets.keys())

        # Calculate offsets:
        for direction in directions:
            point = offsets[direction]
            self.neighbor_offsets['tuple'].append(point)
            self.neighbor_offsets['complex'].append(complex(*point))
        return self.neighbor_offsets


    def get_neighbors(self, maze, point, **kwargs):
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
        offsets = self.get_neighbor_offsets(**kwargs)
        print(f"offsets: {offsets}")
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
            min, max = self.get_maze_size(maze)
            #print(f"Maze size: min: {min}, max: {max}")
            valid_neighbors = []
            for neighbor in neighbors:
                print(f"bounded, checking {neighbor}")
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
                print(f"invalid: checking {neighbor}")
                if is_dict:
                    print(f"dict: {neighbor}: {maze[neighbor]} in {kwargs['invalid']}")
                    if not maze[neighbor] in kwargs['invalid']:
                        valid_neighbors.append(neighbor)
                else:
                    # using 0/1 here instead of X/Y to avoid an extra if condition to 
                    # look for swapped x/y for matrix coordinates, when we get to a
                    # matrix coordinate puzzle, we will need to test thoroughly
                    #if not maze[neighbor[0][1]] in kwargs['invalid']:
                    print(f"list: {neighbor}: {maze[neighbor[X]][neighbor[Y]]} in {kwargs['invalid']}")
                    if not maze[neighbor[X]][neighbor[Y]] in kwargs['invalid']:
                        valid_neighbors.append(neighbor)
            neighbors = valid_neighbors
        return neighbors
    
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
            print(f"get_maze_size no rule to handle {type(maze)}")
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
    
    def manhattan_distance(self,start, goal):
        """
        Function to calculate manhattan distance between two points
        """
        X=0
        Y=1
        if isinstance(start, tuple):
            return abs(start[X] - goal[X]) + abs(start[Y] - goal[Y])
        if isinstance(start, complex):
            return int(abs(start.real - goal.real) + abs(start.imag - goal.imag))

"""
Below here are functions to support the __main__:

This is code to build the aoc structure for the puzzle you are working on

"""

import os
import sys
import shutil
from datetime import datetime
import subprocess

def get_year_day():
    current_year = datetime.now().year
    current_day = datetime.now().day

    if len(sys.argv) == 3:
        return str(int(sys.argv[1])), str(int(sys.argv[2]))
    else:
        year = input(f"Enter year (default: {current_year}): ") or str(current_year)
        day = input(f"Enter day (default: {current_day}): ") or f"{current_day}"
        while not day.isdigit() and year.isdigit:
            print(f"Non Numeric input: {year} {day}")
            year = input(f"Enter year (default: {current_year}): ") or str(current_year)
            day = input(f"Enter day (default: {current_day}): ") or f"{current_day}"
        return str(int(year)), str(int(day))

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def create_init_file(path):
    init_file = os.path.join(path, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            pass  # Create an empty file
        print(f"Created empty __init__.py in: {path}")
        subprocess.run(['git', 'add', init_file], check=True)

def copy_and_modify_template(year, day, src, dst):
    if os.path.exists(dst):
        print(f"File already exists: {dst}")
        return

    with open(src, 'r') as f:
        content = f.read()
    
    content = content.replace('YEAR', year)
    content = content.replace('DAY', day)
    
    with open(dst, 'w') as f:
        f.write(content)
    print(f"Created and modified: {dst}")
    subprocess.run(['git', 'add', dst], check=True)

def create_jupyter_notebook(path, year, day):
    if os.path.exists(path):
        print(f"File already exists: {path}")
        return

    notebook_content = {
     "cells": [
        {
            "cell_type": "code",
            "execution_count": 1,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import sys\n",
                "sys.path.append(os.path.realpath('../..'))\n",
                "import aoc\n",
                f"aoc.set_date({year},{day})"
            ]
        }
     ],
     "metadata": {},
     "nbformat": 4,
     "nbformat_minor": 4
    }
    
    with open(path, 'w') as f:
        import json
        json.dump(notebook_content, f)
    print(f"Created Jupyter notebook: {path}")
    subprocess.run(['git', 'add', path], check=True)

def main():
    # load config
    file_path = '.aoc.cfg.json'
    with open(file_path, 'r') as file:
        cfg = json.load(file)
    year, day = get_year_day()
    original_dir = os.getcwd()
    year_dir = year
    day_dir = os.path.join(year_dir, day)
    
    create_directory(year_dir)
    create_directory(day_dir)
    
    # Create __init__.py files
    create_init_file(year_dir)
    create_init_file(day_dir)
    
    template_path = 'solution_template.py'
    solution_path = os.path.join(day_dir, 'solution.py')
    copy_and_modify_template(year, day, template_path, solution_path)
    
    print("Opening solution.py ...")
    #subprocess.run([cfg['editor'], solution_path], shell=False)
    subprocess.Popen([cfg['editor'], solution_path], start_new_session=True)

    old_solution_path = os.path.join(day_dir, 'script.py')
    if os.path.exists(old_solution_path):
        subprocess.Popen([cfg['editor'], old_solution_path], start_new_session=True)

    # Note, terminal currently only supports windows terminal
    # we could replace the command line parameters with a template from cfg
    print("Opening Shell")
    #  powershell -NoExit -Command "function global:run { python -m 2016.21.solution};function global:check { pylint 2016/21/solution.py }"
    #func_run = f"function global:run {{ python -m {year}.{day}.solution }}"
    #func_check = f"function global:check {{ pylint {year}/{day}/solution.py }}"

    command = f"aoc.ps1 {year} {day}"

    print(' '.join([
        cfg['terminal'], '-w', '0', 'sp', '-H', '-s', '0.7', '-d', '.',
        '--title', 'AdventOfCode', 'powershell.exe', '-NoExit',
        '-Command', f'"{command}"'
    ]))

    subprocess.run(
        [
            cfg['terminal'], '-w', '0', 'sp', '-H', '-s', '0.7', '-d', '.',
            '--title', 'AdventOfCode', 'powershell.exe', '-NoExit',
            '-Command', f'"{command}"'
        ], shell=True)
        
    notebook_path = os.path.join(day_dir, 'scratch_pad.ipynb')
    notebook_template_path = 'scratch_pad_template.ipynb'
    #create_jupyter_notebook(notebook_path, year, day)
    copy_and_modify_template(year, day, notebook_template_path, notebook_path)
    print("Opening Puzzle")
    os.startfile(f'https://adventofcode.com/{year}/day/{day}')
    #os.startfile(f'https://adventofcode.com/{year}/day/{day}/input')
    #Insert code to pull input file here (or not, input should be pulled with
    # an aoc method from the solution)

    print("Launching Jupyter notebook...")
    os.chdir(original_dir)  # Change back to the original directory
    #subprocess.run(['jupyter', 'notebook', notebook_path])
    # update, we can run this from vs code now
    subprocess.Popen([cfg['editor'], notebook_path], start_new_session=True)


####
# Test Functions
####


def test_get_neighbor_offsets():
    # Instantiate the object
    my_aoc = aoc.AdventOfCode(2017, 19)
    
    # Test for 'screen' coordinate system
    screen_result = my_aoc.get_neighbor_offsets(directions=['n', 's', 'e', 'w'], coordinate_system="screen")
    expected_screen = {
        'tuple': [(0, -1), (0, 1), (1, 0), (-1, 0)],
        'complex': [complex(0, -1), complex(0, 1), complex(1, 0), complex(-1, 0)]
    }
    assert screen_result['tuple'] == expected_screen['tuple'], f"Screen coordinates failed: {screen_result['tuple']}"
    assert screen_result['complex'] == expected_screen['complex'], f"Screen coordinates failed: {screen_result['complex']}"

    # Test for 'matrix' coordinate system
    matrix_result = my_aoc.get_neighbor_offsets(directions=['n', 's', 'e', 'w'], coordinate_system="matrix")
    expected_matrix = {
        'tuple': [(-1, 0), (1, 0), (0, 1), (0, -1)],
        'complex': [complex(-1, 0), complex(1, 0), complex(0, 1), complex(0, -1)]
    }
    assert matrix_result['tuple'] == expected_matrix['tuple'], f"Matrix coordinates failed: {matrix_result['tuple']}"
    assert matrix_result['complex'] == expected_matrix['complex'], f"Matrix coordinates failed: {matrix_result['complex']}"
    
    # Test for 'cartesian' coordinate system (assuming 'screen' is the cartesian system)
    cartesian_result = my_aoc.get_neighbor_offsets(directions=['n', 's', 'e', 'w'])
    expected_cartesian = {
        'tuple': [(0, -1), (0, 1), (1, 0), (-1, 0)],
        'complex': [complex(0, -1), complex(0, 1), complex(1, 0), complex(-1, 0)]
    }
    assert cartesian_result['tuple'] == expected_cartesian['tuple'], f"Cartesian coordinates failed: {cartesian_result['tuple']}"
    assert cartesian_result['complex'] == expected_cartesian['complex'], f"Cartesian coordinates failed: {cartesian_result['complex']}"

    print("All tests passed!")

def test_get_neighbors():
    # Instantiate the object
    my_aoc = aoc.AdventOfCode(2017, 19)

    # Define a simple maze as a dictionary
    maze_dict = {
        (0, 0): '.', (0, 1): '.', (0, 2): '#',
        (1, 0): '.', (1, 1): '.', (1, 2): '.',
        (2, 0): '#', (2, 1): '#', (2, 2): '.'
    }

    # Define a simple maze as a list of lists
    maze_list = [
        ['.', '.', '#'],
        ['.', '.', '.'],
        ['#', '#', '.']
    ]
    
    # Test case 1: Screen coordinates, bounded grid, no invalid characters (dict)
    point = (1, 1)
    rules = {
        "type": "bounded",
        "coordinate_system": "screen",
        "directions": ['n', 's', 'e', 'w']
    }
    expected_neighbors = [(1, 0), (1, 2), (2, 1), (0, 1)]
    result = my_aoc.get_neighbors(maze_dict, point, **rules)
    assert sorted(result) == sorted(expected_neighbors), f"Test 1 (dict) failed: {result}"
    
    # Test case 2: Matrix coordinates, bounded grid, no invalid characters (dict)
    rules = {
        "type": "bounded",
        "coordinate_system": "matrix",
        "directions": ['n', 's', 'e', 'w']
    }
    expected_neighbors = [(0, 1), (2, 1), (1, 2), (1, 0)]
    result = my_aoc.get_neighbors(maze_dict, point, **rules)
    assert sorted(result) == sorted(expected_neighbors), f"Test 2 (dict) failed: {result}"

    # Test case 3: Cartesian coordinates, bounded grid, no invalid characters (dict)
    rules = {
        "type": "bounded",
        "coordinate_system": "cartesian",
        "directions": ['n', 's', 'e', 'w']
    }
    expected_neighbors = [(1, 0), (1, 2), (2, 1), (0, 1)]
    result = my_aoc.get_neighbors(maze_dict, point, **rules)
    assert sorted(result) == sorted(expected_neighbors), f"Test 3 (dict) failed: {result}"

    # Test case 4: Screen coordinates, bounded grid, with invalid characters (dict)
    rules = {
        "type": "bounded",
        "coordinate_system": "screen",
        "directions": ['n', 's', 'e', 'w'],
        "invalid": "#"
    }
    expected_neighbors = [(1, 0), (1, 2), (0, 1)]
    result = my_aoc.get_neighbors(maze_dict, point, **rules)
    assert sorted(result) == sorted(expected_neighbors), f"Test 4 (dict) failed: {result}"
    
    # Test case 5: Screen coordinates, unbounded grid, with invalid characters (dict)
    rules = {
        "type": "infinite",
        "coordinate_system": "screen",
        "directions": ['n', 's', 'e', 'w'],
        "invalid": "#"
    }
    expected_neighbors = [(1, 0), (1, 2), (0, 1)]
    result = my_aoc.get_neighbors(maze_dict, point, **rules)
    assert sorted(result) == sorted(expected_neighbors), f"Test 5 (dict) failed: {result}"

    # Test case 6: Screen coordinates, bounded grid, no invalid characters (list)
    expected_neighbors = [(1, 0), (1, 2), (0, 1)]
    result = my_aoc.get_neighbors(maze_list, point, **rules)
    assert sorted(result) == sorted(expected_neighbors), f"Test 6 (list) failed: {result}"
    
    # Test case 7: Matrix coordinates, bounded grid, no invalid characters (list)
    rules = {
        "type": "bounded",
        "coordinate_system": "matrix",
        "directions": ['n', 's', 'e', 'w']
    }
    expected_neighbors = [(0, 1), (2, 1), (1, 2), (1, 0)]
    result = my_aoc.get_neighbors(maze_list, point, **rules)
    assert sorted(result) == sorted(expected_neighbors), f"Test 7 (list) failed: {result}"

    # Test case 8: Cartesian coordinates, bounded grid, no invalid characters (list)
    rules = {
        "type": "bounded",
        "coordinate_system": "cartesian",
        "directions": ['n', 's', 'e', 'w']
    }
    expected_neighbors = [(1, 0), (1, 2), (2, 1), (0, 1)]
    result = my_aoc.get_neighbors(maze_list, point, **rules)
    assert sorted(result) == sorted(expected_neighbors), f"Test 8 (list) failed: {result}"

    # Test case 9: Screen coordinates, bounded grid, with invalid characters (list)
    rules = {
        "type": "bounded",
        "coordinate_system": "screen",
        "directions": ['n', 's', 'e', 'w'],
        "invalid": "#"
    }
    expected_neighbors = [(1, 0), (1, 2), (0, 1)]
    result = my_aoc.get_neighbors(maze_list, point, **rules)
    assert sorted(result) == sorted(expected_neighbors), f"Test 9 (list) failed: {result}"
    
    # Test case 10: Screen coordinates, unbounded grid, with invalid characters (list)
    rules = {
        "type": "infinite",
        "coordinate_system": "screen",
        "directions": ['n', 's', 'e', 'w'],
        "invalid": "#"
    }
    expected_neighbors = [(1, 0), (1, 2), (0, 1)]
    result = my_aoc.get_neighbors(maze_list, point, **rules)
    assert sorted(result) == sorted(expected_neighbors), f"Test 10 (list) failed: {result}"

    print("All tests passed!")

if __name__ == "__main__":
    main()
