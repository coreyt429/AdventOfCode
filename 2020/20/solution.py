"""
Advent Of Code 2020 day 20

"""
# import system modules
import time
import math
import re
from itertools import permutations
from copy import deepcopy

# import my modules
import aoc # pylint: disable=import-error

opposites = {
    "top": "bottom",
    "bottom": "top",
    "left": "right",
    "right": "left"
}

class TilesIterator:
    def __init__(self, parent):
        self.parent = parent
        self.iter_index = -1

    def __iter__(self):
        return self
    
    def __next__(self):
        self.iter_index += 1
        if self.iter_index >= len(self.parent.positions):
            raise StopIteration
        tile_id = self.parent.positions[self.iter_index]
        return self.parent.tile_by_id(tile_id)

class Tiles:
    """Collection class for Tile"""
    def __init__(self, input_data):
        self.tiles = {}
        self.row_size = None
        self.offsets = None
        self.positions = {}
        self.parse(input_data)
    
    def parse(self, input_data):
        for tile_text in input_data.split('\n\n'):
            lines = tile_text.splitlines()
            # print(lines)
            tile_id = int(lines[0].replace('Tile ','').replace(':',''))
            self.add_tile(Tile(tile_id, '\n'.join(lines[1:])))

    def add_tile(self, tile):
        """method to add a tile to the collection"""
        self.tiles[tile.tile_id] = tile
        tile.parent = self
        self.update_row_size()
        if not tile.position:
            last_position = -1
            if self.positions:
                last_position = max(self.positions.keys())
            tile.position = last_position + 1
        self.positions[tile.position] = tile.tile_id

    def update_row_size(self):
        """method to calculate row_size"""
        self.row_size = int(math.sqrt(len(self.tiles)))
        self.offsets = {
            "left": -1,
            "right": 1,
            "top": -1 * self.row_size,
            "bottom": self.row_size,
        }

    def tile_by_id(self, tile_id):
        """method to return a tile by tile_id"""
        return self.tiles.get(tile_id, 'None')
    
    def tile_by_position(self, position):
        """method to return a tile by position"""
        return self.tiles.get(self.positions[position], None)
    
    def swap(self, source_pos, target_pos):
        source = self.tile_by_position(source_pos)
        target = self.tile_by_position(target_pos)
        self.positions[source_pos] = target.tile_id
        self.positions[target_pos] = source.tile_id
        source.position = target_pos
        target.position = source_pos
    
    def refresh(self):
        for tile in self:
            tile.refresh()

    def str_grid(self, **kwargs):
        my_str = ''
        spaces = kwargs.get('spaces', ' ')
        borders = kwargs.get('borders', True)
        grids = []
        for tile in self:
            grid = tile.str_grid().splitlines()
            if not borders:
                grid.pop(0)
                grid.pop(-1)
                for idx, line in enumerate(grid):
                    grid[idx] = line[1:-1]
            grids.append(grid)

        for row in range(self.row_size):
            for idx in range(len(grids[0])):
                for col in range(row * self.row_size, (row * self.row_size) + self.row_size):
                    my_str += grids[col][idx] + spaces
                my_str += '\n'
            if spaces:
                my_str += '\n'
        return my_str

    def __iter__(self):
        """Iterator"""
        return TilesIterator(self)

    def __str__(self):
        """str implemention"""
        my_str = ""
        for tile in self:
            my_str += f"{tile}\n"
        return my_str
    
    def __len__(self):
        return len(self.positions)

class Tile:
    opposites = {
        "top": "bottom",
        "bottom": "top",
        "left": "right",
        "right": "left"
    }

    def __init__(self, tile_id, input_data):
        self.parent = None
        self.tile_id = tile_id
        self.grid = []
        self.sides = {}
        self.mates = {}
        self.position = None
        self.parse(input_data)
        self.get_sides()
        self.variety = '?'
        
    
    def parse(self, input_data):
        for line in input_data.splitlines():
            self.grid.append(list(line))
            self.row_size = len(line)
    
    def refresh(self):
        self.get_sides()
        self.find_matches()     
    
    def get_sides(self):
        self.sides = {
            "top": ''.join(self.grid[0]),
            "bottom": ''.join(self.grid[self.row_size - 1]),
            "left": ''.join([self.grid[row][0] for row in range(len(self.grid))]),
            "right": ''.join(self.grid[row][self.row_size - 1] for row in range(len(self.grid))),
        }

    def swap(self, position):
        self.parent.swap(self.position, position)
    
    def find_matches(self):
        self.mates = {}
        for other in self.parent:
            if other.tile_id == self.tile_id:
                continue
            for side, border in self.sides.items():
                for other_side, other_border in other.sides.items():
                    if other_border == border or other_border == border[::-1]:
                        self.mates[other.tile_id] = {'this': side, 'other': other_side }
        if len(self.mates) == 2:
            self.variety = 'corner'
        elif len(self.mates) == 3:
            self.variety = 'edge'
        else:
            self.variety = 'inner'  

    def rotate(self):
        # print(f"rotate({self})")
        self.grid = [list(row) for row in zip(*self.grid[::-1])]

    def flip_horizontal(self):
        self.grid = [row[::-1] for row in self.grid]

    def flip_vertical(self):
        self.grid = self.grid[::-1]
    
    def is_left_edge(self, position=None):
        if position is None:
            position = self.position
        return position % self.parent.row_size == 0

    def is_right_edge(self, position=None):
        if position is None:
            position = self.position
        return (position + 1) % self.parent.row_size == 0

    def is_top_edge(self, position=None):
        if position is None:
            position = self.position
        return position < self.parent.row_size

    def is_bottom_edge(self, position=None):
        if position is None:
            position = self.position
        return position > self.parent.row_size * (self.parent.row_size -1)

    def orient_self(self):
        self.refresh()
        neighbor_positions = []
        valid_directions = []
        for direction, offset in self.parent.offsets.items():
            if self.is_right_edge() and offset == 1:
                continue
            if self.is_left_edge() and offset == -1:
                continue
            if 0 <= self.position + offset < self.parent.row_size**2:
                neighbor_positions.append(self.position + offset)
                valid_directions.append(direction)
        directions = [mate['this'] for mate in self.mates.values()]
        sentinel = 0
        while not all(direction in valid_directions for direction in directions):
            sentinel += 1
            if sentinel > 4:
                return False
            self.rotate()
            self.refresh()
            directions = [mate['this'] for mate in self.mates.values()]
        if self.position > 0:
            for mate_id in self.mates:
                mate = self.parent.tile_by_id(mate_id)
                # not next to us, don't align
                if mate.position not in neighbor_positions:
                    continue
                # print(f"is mate closer to origin? {mate} < {self}")
                if mate.position < self.position:
                    # print(f"wrong direction?  {self.mates[mate_id]['this']} == {self.mates[mate_id]['other']}")
                    while self.mates[mate_id]['this'] != self.opposites[self.mates[mate_id]['other']]:
                        self.rotate()
                        self.parent.refresh()
                    edge = self.mates[mate_id]['this']
                    if self.sides[edge] == mate.sides[self.opposites[edge]][::-1]:
                        self.flip_edge(edge)
                        self.parent.refresh()
    
    def flip_edge(self, edge):
        # print(f"flip_edge({self}, {edge})")
        if edge in ['left', 'right']:
            self.flip_vertical()
        else:
            self.flip_horizontal()
        
    def orient_mates(self):
        """
        Method to place and orient a tiles mates
        """
        # print(f"orient_mates({self.tile_id})")
        self.parent.refresh()
        # print(f"{self} Mates:")
        # for mate_id in self.mates:
        #     print(f"  {self.parent.tile_by_id(mate_id)}")


        neighbor_positions = {}
        for direction, offset in self.parent.offsets.items():
            # print(f"direction: {direction}")
            # print(f"offset: {offset}")
            # print(f"position: self.position + offset")
            # print(f"0 <= {self.position + offset} < {self.parent.row_size**2}")
            if 0 <= self.position + offset < self.parent.row_size**2:
                neighbor_positions[direction] = self.position + offset
        for mate_id in self.mates:
            mate = self.parent.tile_by_id(mate_id)
            if mate.position < self.position:
                continue
            # print(f"self.mates[{mate_id}]: {self.mates[mate_id]}")
            # print(f"neighbor_positions[{self.mates[mate_id]['this']}]: {neighbor_positions[self.mates[mate_id]['this']]}")
            target = neighbor_positions.get(self.mates[mate_id]['this'], None)
            if target is None:
                # print(f"Target is None, refreshing")
                mate.refresh()
                self.refresh()
                target = neighbor_positions.get(self.mates[mate_id]['this'], None)
                if target is None:
                    # print("target is still none, skipping")
                    continue
            # 7 < 6
            # self.mates[1171]: {'this': 'bottom', 'other': 'right'}
            # neighbor_positions[bottom]: 10
            # target: 10
            # don't swap over a neighbor that is set
            if target < self.position:
                continue
            if mate.position != target:
                # print(f"swapping {mate.position} <> {target}")
                mate.swap(target)
                mate.refresh()
                self.refresh()
                mate.orient_self()

    def str_grid(self):
        my_str = ""
        for row in self.grid:
            my_str += ''.join(row)
            my_str += "\n"
        return my_str

    def __str__(self):
        """str implemention"""
        my_str = f"{self.position}:{self.tile_id}"
        # my_str += self.str_grid()
        # my_str += "\n"
        return my_str

def rotate_clockwise(matrix):
    return [list(row) for row in zip(*matrix[::-1])]

def rotate_counterclockwise(matrix):
    return [list(row) for row in zip(*matrix)][::-1]

def flip_horizontal(matrix):
    return [row[::-1] for row in matrix]

def flip_vertical(matrix):
    return matrix[::-1]

def parse_input(text):
    """Function to parse input"""
    squares = {}
    # squares are divided by two new lines
    for square in text.split("\n\n"):
        lines = square.splitlines()
        # line 1 of the square is the title with its id, extract it
        square_id = int(lines[0].replace('Tile ','').replace(':',''))
        # the rest of the square is a 10x10 grid
        squares[square_id] = {}
        squares[square_id]['square'] = []
        for line in lines[1:]:
            squares[square_id]['square'].append(list(line))
        squares[square_id]['sides'] = sides(squares[square_id]['square'])
    return squares

def print_square(square):
    """
    Utility funciton to print a square
    """
    for y_val, row in enumerate(square):
        print(f"{y_val}: ", end='')
        for col in row:
            print(f"{col}", end='')
        print()

def sides(square):
    """
    Function to calculate the border sides of a square starting at the top left
    corner and going clockqise around the square
    """
    return {
        "top": ''.join(square[0]),
        "bottom": ''.join(reversed(square[9])),
        "left": ''.join(reversed([square[row][0] for row in range(len(square))])),
        "right": ''.join(square[row][9] for row in range(len(square))),
    }
    
def find_matches(current_id, squares):
    """
    Function to find squares with matching borders
    """
    current = squares[current_id]
    current['mates'] = {}
    for other_id, other in squares.items():
        if other_id == current_id:
            continue
        for side, border in current['sides'].items():
            for other_side, other_border in other['sides'].items():
                if other_border == border or other_border == border[::-1]:
                    current['mates'][other_id] =  {'this': side, 'other': other_side }

def is_left_edge(position, row_size):
    return position % row_size == 0

def is_right_edge(position, row_size):
    return (position + 1) % row_size == 0

def is_top_edge(position, row_size):
    return position < row_size

def is_bottom_edge(position, row_size):
    return position > row_size * (row_size -1)

def get_combinations(squares, corners):
    """
    Function to iterate over all possible combinations
    This search space is too big, it examines way too many invalid
    combinations
    """
    row_size = int(math.sqrt(len(squares)))
    corner_positions = [
            0, 
            row_size -1, 
            row_size * (row_size -1),
            row_size * row_size -1
        ]
    combos = []
    for combo in permutations(squares.keys()):
        print(combo)
        valid = True
        for corner_position in corner_positions:
            if combo[corner_position] not in corners:
                valid = False
                break
        if not valid:
            continue
        for idx in range(len(squares)):
            mate_count = len(squares[combo[idx]]['mates'])
            if idx in corner_positions:
                if mate_count != 2:
                    valid = False
            elif is_top_edge(idx, row_size):
                if mate_count != 3:
                    valid = False
            elif is_bottom_edge(idx, row_size):
                if mate_count != 3:
                    valid = False
            elif is_right_edge(idx, row_size):
                if mate_count != 3:
                    valid = False
            elif is_left_edge(idx, row_size):
                if mate_count != 3:
                    valid = False
            else:
                if mate_count != 4:
                    valid = False
        if not valid:
            continue
        combos.append(combo)
    return combos

def orient_square(current_id, squares, first=False, neighbor=None):
    current = squares[current_id]
    mates = list(current['mates'].keys())
    oriented = False
    sentinel = 0
    while not oriented:
        sentinel += 1
        if sentinel > 4:
            # print(f"orient_square({current_id}): sentinel break")
            return False
        oriented = first
        if first:
            for mate in mates:
                if current['mates'][mate]['this'] not in ["bottom", "right"]:
                    oriented = False
                    break
        if neighbor:
            other = squares[neighbor]
            # print(f"current: {current['mates'][mate]['this']} <> other: {other['mates'][current_id]['this']}")
            current_side = current['mates'][neighbor]['this']
            other_side = other['mates'][current_id]['this']
            if current_side == opposites[other_side]:
                # print(f"current: {mate} {current['mates'][mate]['this']} <> other: {current_id} {other['mates'][current_id]['this']}")
                # check to see if we need to flip
                if current['sides'][current_side] == other['sides'][other_side][::-1]:
                    if current_side in ['top', 'bottom']:
                        current['square'] = flip_vertical(current['square'])
                    else:
                        current['square'] = flip_horizontal(current['square'])
                    current['sides'] = sides(current['square'])
                    find_matches(current_id, squares)
                oriented = True
            
        if not oriented:
            # print(f"rotating {current_id}")
            current['square'] = rotate_clockwise(current['square'])
            current['sides'] = sides(current['square'])
            find_matches(current_id, squares)
            for mate in mates:
                find_matches(mate, squares)
    # print(f"orient_square({current_id}): returning {oriented}")
    return oriented

def check_configuration(squares):
    row_size = int(math.sqrt(len(squares)))
    for current_id, current in squares.items():
        # print(f"current: {current_id}: {current['position']} {current['mates']}")
        for mate_id in current['mates']:
            mate = squares[mate_id]
            # print(f"mate: {mate_id} {mate['position']}")
            if abs(current['position'] - mate['position']) not in [1, row_size]:
                return False
    return True

def get_square_by_position(position, squares):
    for current_id, current in squares.items():
        if current['position'] == position:
            return current_id, current

def refresh_squares(squares, *args):
    for square_id in args:
        square = squares[square_id]
        square['sides'] = sides(square['square'])
        find_matches(square_id, squares)

def align_mate_borders(current_id, previous_id, squares):
    # FIXME:  moving on for now, but I suspect there may be a square than needs horizontal and vertical flips that may require more logic
    current = squares[current_id]
    previous = squares[previous_id]
    direction = previous['mates'][current_id]['this']
    sentinel = 0
    if direction == 'right':
        while current['mates'][previous_id]['this'] != 'left':
            sentinel += 1
            if sentinel > 20:
                print("breaking loop right")
                break
            current['square'] = rotate_clockwise(current['square'])
            refresh_squares(squares, current_id, previous_id)
        if current['sides']['left'] != previous['sides']['right']:
            current['square'] = flip_vertical(current['square'])
            refresh_squares(squares, current_id, previous_id)
    elif direction == 'left':
        while current['mates'][previous_id]['this'] != 'right':
            sentinel += 1
            if sentinel > 20:
                print("breaking loop left")
                break
            current['square'] = rotate_clockwise(current['square'])
            refresh_squares(squares, current_id, previous_id)
        if current['sides']['right'] != previous['sides']['left']:
            current['square'] = flip_vertical(current['square'])
            refresh_squares(squares, current_id, previous_id)
    elif direction == 'top':
        while current['mates'][previous_id]['this'] != 'bottom':
            sentinel += 1
            if sentinel > 20:
                print("breaking loop top")
                break
            current['square'] = rotate_clockwise(current['square'])
            refresh_squares(squares, current_id, previous_id)
        if current['sides']['bottom'] != previous['sides']['top']:
            current['square'] = flip_horizontal(current['square'])
            refresh_squares(squares, current_id, previous_id)
    elif direction == 'bottom':
        while current['mates'][previous_id]['this'] != 'top':
            sentinel += 1
            if sentinel > 20:
                print("breaking loop bottom")
                break
            current['square'] = rotate_clockwise(current['square'])
            refresh_squares(squares, current_id, previous_id)
        if current['sides']['top'] != previous['sides']['bottom']:
            current['square'] = flip_horizontal(current['square'])
            refresh_squares(squares, current_id, previous_id)

    for mate_id in current['mates']:
        mate = squares[mate_id]
        refresh_squares(squares, current_id, mate_id)
        if current['mates'][mate_id]['this'] in ['bottom', 'right']:
            align_mate_borders(mate_id, current_id, squares)
    


def align_borders(squares):
    # start at zero
    row_size = int(math.sqrt(len(squares)))
    current_id, current = get_square_by_position(0, squares)
    right_id, right = get_square_by_position(1, squares)
    bottom_id, bottom = get_square_by_position(row_size, squares)
    sentinel = 0
    while current['mates'][right_id]['this'] != 'right':
        sentinel += 1
        if sentinel > 20:
            print("right loop")
            break
        current['square'] = rotate_clockwise(current['square'])
        refresh_squares(squares, current_id, right_id, bottom_id)
    sentinel = 0
    while current['mates'][bottom_id]['this'] != 'bottom':
        sentinel += 1
        if sentinel > 20:
            print("bottom loop")
            break
        current['square'] = flip_vertical(current['square'])
        refresh_squares(squares, current_id, right_id, bottom_id)
    for mate_id in current['mates']:
        align_mate_borders(mate_id, current_id, squares)

def strip_borders(squares):
    new_squares = deepcopy(squares)
    for square in new_squares.values():
        # remove first row
        square['square'].pop(0)
        # remove last row
        square['square'].pop(-1)
        for line in square['square']:
            # remove first char
            line.pop(0)
            # remove last_char
            line.pop(-1)
    return new_squares

def calculate_water_roughness(data, corners):
    combos = get_combinations(data, corners)
    found = False
    for combo in combos:
        for position, square_id in enumerate(combo):
            data[square_id]['position'] = position
        for current_id, current in data.items():
            orient_square(current_id, data)
            current['sides'] = sides(current['square'])
            find_matches(current_id, data)
        if check_configuration(data):
            found = True
            # print(f"Winning combo: {combo}")
            break

    align_borders(squares=data)
    borderless = strip_borders(data)
    return None

def find_monster(grid_text, watch_point=None):
    grid = []
    for line in grid_text.splitlines():
        grid.append(list(line))
    monster_index = [[18], [0, 5, 6, 11, 12, 17, 18, 19], [1, 4, 7, 10, 13, 16]]
    monster_points = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            found = True
            possible_points = []
            for row_offset, row_data in enumerate(monster_index):
                for col_offset in row_data:
                    try:
                        if watch_point and watch_point == (row, col):
                            print(f"{(row, col)} + {(row_offset, col_offset)} = {(row + row_offset, col + col_offset)}, {grid[row + row_offset][col + col_offset]}")
                        if grid[row + row_offset][col + col_offset] != '#':
                            if watch_point and watch_point == (row, col):
                                print(f"{[row + row_offset][col + col_offset]} is not '#")
                            found = False
                        else:
                            possible_points.append((row + row_offset, col + col_offset))
                    except IndexError:
                        found = False
            if watch_point and watch_point == (row, col):
                print(f"found? {found}: {possible_points}")
            if found:
                monster_points.extend(possible_points)
            if watch_point and watch_point == (row, col):
                print(f"monster_points: {monster_points}")
    if monster_points:
        new_grid = []
        for row in range(len(grid)):
            new_row = []
            for col in range(len(grid[row])):
                if (row, col) in monster_points:
                    new_row.append('O')
                else:
                    new_row.append(grid[row][col])
            new_grid.append(new_row)
        return True, new_grid
    return False, []

def text_to_grid(grid_text):
    grid = []
    for line in grid_text.splitlines():
        grid.append(list(line))
    return grid

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        # load data
        tile_collection = Tiles(input_text)
        tile_collection.refresh()
        corners = []
        for tile in tile_collection:
            # print(f"{tile.position}: {tile.tile_id}, {tile.variety}, {len(tile.mates)} {tile.mates}")
            if tile.variety == 'corner':
                corners.append(tile.tile_id)
        # print(f"corners: {corners}")
        tile_collection.tile_by_id(corners[0]).swap(0)

        for position in range(len(tile_collection)):
            tile_collection.refresh()
            # print(f"placing position {position} of {len(tile_collection)}")
            tile = tile_collection.tile_by_position(position)
            # print(f"{tile.position}: {tile.tile_id}, {tile.variety}")
            # print(f"mates: {tile.mates}")
            tile.orient_self()
            tile.orient_mates()

        combined_grid = text_to_grid(tile_collection.str_grid(spaces='', borders=False))
        flips = []
        flips.append(combined_grid)
        flips.append(flip_horizontal(combined_grid))
        flips.append(flip_vertical(combined_grid))
        flips.append(flip_horizontal(flip_vertical(combined_grid)))
        potentials = set()
        middle_row_regex = r'.*(\#....\#\#....\#\#....\#\#\#).*'
        middle_row_pattern = re.compile(middle_row_regex)
        bottom_row_regex = r'.*(.\#..\#..\#..\#..\#..\#...).*'
        bottom_row_pattern = re.compile(bottom_row_regex)
        for idx, combined_grid in enumerate(flips):
            for turn in range(1,5):
                combined_grid = rotate_clockwise(combined_grid)
                grid_text=''
                for row in combined_grid:
                    grid_text += ''.join(row) + '\n'
                match = middle_row_pattern.search(grid_text)
                if match:
                    match = bottom_row_pattern.search(grid_text)
                    if match:
                        potentials.add(grid_text)

        for idx, grid in enumerate(potentials):
            watch = None
            found, monster_grid = find_monster(grid)
            count = 0
            if found:
                for row in monster_grid:
                    print(''.join(row))
                    count += ''.join(row).count('#')
                print()
                return count
        return -1
    data = parse_input(input_value)
    corners = []
    for sq_id in data:
        find_matches(sq_id, data)
        if len(data[sq_id]['mates']) == 2:
            corners.append(sq_id)
    
    return math.prod(corners)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020,20)
    input_text = my_aoc.load_text()
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
        1: 14986175499719,
        2: 2161
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
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
