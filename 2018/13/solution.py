"""
Advent Of Code 2018 day 13


This is working, but slow.  needs some work.

"""
# import system modules
import time
import sys
from heapq import heapify, heappop, heappush

# import my modules
import aoc # pylint: disable=import-error
from grid import Grid # pylint: disable=import-error
def parse_data(lines):
    """
    Function to parse input file
    """
    data_map = []
    for line in lines:
        data_map.append(list(line))
    new_grid = Grid(data_map, default_value=' ', overrides={})
    return new_grid

class Cart:
    """
    Class to represent cart
    """
    symbols = {
        'n': '^',
        'e': '>',
        's': 'v',
        'w': '<'
    }

    def __init__(self, pos, direction, grid, container):
        """
        Init new cart
        """
        self.cart_id = len(container)
        self.pos = pos
        self.direction = direction
        self.grid = grid
        self.grid.overrides[self.pos] = self.symbols[self.direction]
        self.turns = 0
        self.removed = False
        self.container = container

    def __lt__(self, other):
        """
        less than for sorting
        """
        if self.pos[1] < other.pos[1]:
            return True
        if self.pos[1] > other.pos[1]:
            return False
        if self.pos[0] < other.pos[0]:
            return True
        if self.pos[0] > other.pos[0]:
            return False
        return False

    def move(self):
        """
        Move cart forward
        """
        self.grid.pos = self.pos
        neighbors = self.grid.get_neighbors(directions=[self.direction])
        next_pos = neighbors[self.direction]
        if self.pos in self.grid.overrides:
            self.grid.overrides.pop(self.pos)
        self.pos = next_pos
        curves = {
            'n': {'/': 'e', '\\': 'w'},
            'e': {'/': 'n', '\\': 's'},
            's': {'/': 'w', '\\': 'e'},
            'w': {'/': 's', '\\': 'n'}
        }
        if self.grid.map[next_pos] in '/\\':
            self.direction = curves[self.direction][self.grid.map[next_pos]]
        # Each time a cart has the option to turn (by arriving at any intersection),
        # it turns left the first time, goes straight the second time, turns right the third time,
        # and then repeats those directions starting again with left the fourth time,
        # straight the fifth time, and so on. This process is independent of the particular
        # intersection at which the cart has arrived  - that is, the cart has no per-intersection
        # memory.
        directions = 'rlf'
        turns = {
            'n' : {'f': 'n', 'l': 'w', 'r': 'e'},
            'e' : {'f': 'e', 'l': 'n', 'r': 's'},
            's' : {'f': 's', 'l': 'e', 'r': 'w'},
            'w' : {'f': 'w', 'l': 's', 'r': 'n'}
        }
        if self.grid.map[next_pos] in '+':
            self.turns += 1
            turn_direction = directions[self.turns % 3]
            self.direction = turns[self.direction][turn_direction]

        if self.pos in self.grid.overrides:
            # collision
            self.grid.overrides[self.pos] = 'X'
            return False
        self.grid.overrides[self.pos] =  self.symbols[self.direction]
        return True

def identify_carts(grid):
    """
    function to identify carts on the grid
    """
    carts = []
    for point in grid.map.keys():
        if grid.map[point] == '^':
            grid.map[point] = '|'
            carts.append(Cart(point, 'n', grid, carts))
        if grid.map[point] == 'v':
            grid.map[point] = '|'
            carts.append(Cart(point, 's', grid, carts))
        if grid.map[point] == '>':
            grid.map[point] = '-'
            carts.append(Cart(point, 'e', grid, carts))
        if grid.map[point] == '<':
            grid.map[point] = '-'
            carts.append(Cart(point, 'w', grid, carts))
    return carts

def cull_collision_carts(cart, carts):
    """
    Function to remove collision pairs
    """
    for other_cart in carts:
        if cart.cart_id == other_cart.cart_id:
            continue
        if other_cart.pos == cart.pos:
            cart.removed = True
            other_cart.removed = True
            cart.pos = (sys.maxsize, sys.maxsize)
            other_cart.pos = (sys.maxsize, sys.maxsize)
            print(f"removing: {cart.cart_id} and {other_cart.cart_id} at {cart.pos}")
            if cart.pos in cart.grid.overrides:
                cart.grid.overrides.pop(cart.pos)
            break

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = parse_data(input_value)
    carts = identify_carts(grid)
    if part == 1:
        collision = False
        collision_point = None
        while not collision:
            for cart in carts:
                collision = not cart.move()
                if collision:
                    collision_point = cart.pos
                    break
        return ','.join(str(coord) for coord in collision_point)
    cart_count = len(carts)
    counter = 0
    while cart_count > 1:
        counter += 1
        carts.sort()
        collision = False
        any_collision = False
        for cart in carts:
            if cart.removed:
                continue
            collision = not cart.move()
            if collision:
                any_collision = True
                collision_point = cart.pos
                print(f"collision at {collision_point}")
                cull_collision_carts(cart, carts)
        #print(f"{counter}: {[(cart.cart_id,cart.removed) for cart in carts]}")
        cart_count = 0
        for cart in carts:
            if cart.removed:
                continue
            cart_count += 1
        #if any_collision:
        #    print(f"carts: {cart_count}")
        #    for cart in carts:
        #        print(f"{cart.cart_id}, {cart.removed}")
    for cart in carts:
        if not cart.removed:
            break
    return ','.join(str(coord) for coord in cart.pos)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,13)
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
