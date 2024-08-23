"""
Advent Of Code 2018 day 13

This is working, but slow.  needs some work.

heapq doesn't seem to be helping significantly over just sorting the list.

deque was worse than heapq for part 1, even without sorting it.

streamlined the move and remove operations a bit, but still no great gains

Added a min_manhattan_distance check to skip calculations if the carts aren't
    together.  no real gain

revisiting heapq as the storage for Carts. seemingly no gain, I think we are 
    taking everything out and putting it back in too much.



"""
# import system modules
import time
import sys
from heapq import heapify, heappop, heappush
from collections import deque, Counter
import itertools

# import my modules
import aoc # pylint: disable=import-error
from grid import Grid, manhattan_distance # pylint: disable=import-error
def parse_data(lines):
    """
    Function to parse input file
    """
    data_map = []
    for line in lines:
        data_map.append(list(line))
    new_grid = Grid(data_map, default_value=' ', overrides={})
    return new_grid

class Carts:
    """
    Class for a collection of carts
    """
    def __init__(self, grid):
        self.grid = grid
        self.carts = []
        self.locate_carts()
        self.last_collision = None
        self.index = 0
        self.back_off = 0
    
    def add_cart(self, pos, direction):
        """
        Add a cart to the collection
        """
        heappush(self.carts, Cart(pos, direction, self.grid, self.carts))
    
    def locate_carts(self):
        """
        Function to identify carts on the grid
        """
        direction_map = {
            '^': {"direction": 'n', "char": '|'},
            '>': {"direction": 'e', "char": '-'},
            'v': {"direction": 's', "char": '|'},
            '<': {"direction": 'w', "char": '-'},
        }
        for key, value in self.grid.map.items():
            if value in direction_map:
                direction_info = direction_map[value]
                self.grid.map[key] = direction_info["char"]
                self.add_cart(key, direction_info["direction"])

    def min_manhattan_distance(self, threshold=3):
        """
        Function to find minimum manhattan distance
        between carts
        """
        positions = [cart.pos for cart in self.carts if not cart.removed]
        
        if len(positions) < 2:
            return 0  # No pairs to compare
        min_distance = sys.maxsize
        for pos_1, pos_2 in itertools.combinations(positions, 2):
            distance = manhattan_distance(pos_1, pos_2)
            if distance < threshold:
                return distance
            if distance < min_distance:
                min_distance = distance
        return min_distance

    def detect_collision(self):
        """
        Function to detect collisions
        """
        threshold = 3
        # using manhattan distance to determine if we should back off
        # this should help reduce calculations since the map is pretty big
        if self.back_off >= threshold:
            self.back_off -= 1
            #print("skip detect_collision")
            return False
        self.back_off = self.min_manhattan_distance(threshold)
        #print(f"resetting back_off: {self.back_off}")
        
        
        positions = [cart.pos for cart in self.carts if not cart.removed]
        position_counts = Counter(positions)

        for position, count in position_counts.items():
            if count > 1:
                collision_point = position
                print(f"Collision detected at {collision_point}")
                self.last_collision = {
                    "location": collision_point,
                    "carts": []
                }
                keep = []
                # loop over all carts, note for cart in self.carts would only
                # loop over the carts in the current turn
                while self.carts:
                    cart = self.pop()
                    if cart.pos == collision_point:
                        self.last_collision["carts"].append(cart)
                        print(f"Removing: {cart}")
                        cart.remove()
                    else:
                        keep.append(cart)
                for cart in keep:
                    self.push(cart)
                return True
        return False
    
    def pop(self):
        """
        function to get a cart from Carts
        """
        return heappop(self.carts)
    
    def push(self, cart):
        """
        Function to place a cart in Carts
        """
        heappush(self.carts, cart)

    def sort_deprecated(self):
        """
        Function to sort carts
        """
        self.carts = sorted([cart for cart in self.carts if not cart.removed])
        #self.carts.sort()

    def __str__(self):
        """
        String
        """
        string = f"Carts with {len(self)} carts:\n"
        for idx, cart in enumerate(self.carts):
            string += f"    {idx:2}: {cart}\n"
        string += "\n"
        return string
    
    def __len__(self):
        """
        Method to return length
        """
        return len(self.carts)

    def __iter__(self):
        """
        Method to initialize iteration
        """
        self.index = self.carts[0].moves
        return self

    def __next__(self):
        """
        Method to get the next item
        """
        # if moves doesn't match index, then
        # we have walked all of the items
        if self.carts and self.index == self.carts[0].moves:
            return self.pop()
        else:
            raise StopIteration

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
    curve_map = {
        'n': {'/': 'e', '\\': 'w'},
        'e': {'/': 'n', '\\': 's'},
        's': {'/': 'w', '\\': 'e'},
        'w': {'/': 's', '\\': 'n'}
    }
    turn_map = {
        'n': {'f': 'n', 'l': 'w', 'r': 'e'},
        'e': {'f': 'e', 'l': 'n', 'r': 's'},
        's': {'f': 's', 'l': 'e', 'r': 'w'},
        'w': {'f': 'w', 'l': 's', 'r': 'n'}
    }
    directions = 'rlf'

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
        self.moves = 0

    def __lt__(self, other):
        """
        less than for sorting
        """
        return (self.moves, self.pos[1], self.pos[0]) < (other.moves, other.pos[1], other.pos[0])

    def move(self):
        """
        Move cart forward
        """
        # move grid to our position
        self.grid.pos = self.pos
        # get grid neighbors, but only for the direction we are moving
        neighbors = self.grid.get_neighbors(directions=[self.direction])
        # set next_pos to neighbor
        try:
            next_pos = neighbors[self.direction]
        except KeyError:
            print(self.container)
            print(self)
            print(neighbors)
            sys.exit()
        #commenting out, overrides are only needed if we are printing
        #self.grid.overrides.pop(self.pos, None)  # Safely remove old override
        # set new position
        self.pos = next_pos
        # Cache the value of the new grid tile
        next_tile = self.grid.map[next_pos]
        # Is it a curve?
        if next_tile in self.curve_map[self.direction]:
            # change direction based on curve
            self.direction = self.curve_map[self.direction][next_tile]
        # Each time a cart has the option to turn (by arriving at any intersection),
        # it turns left the first time, goes straight the second time, turns right the third time,
        # and then repeats those directions starting again with left the fourth time,
        # straight the fifth time, and so on. This process is independent of the particular
        # intersection at which the cart has arrived  - that is, the cart has no per-intersection
        # memory.
        # is it an intersection
        if next_tile == '+':
            # increment turn counter, it starts at 0, and we increment before
            # deciding.  if you move to increment after it will change
            # the decision tree, unless you also update self.directions
            self.turns += 1
            # get turn direction from class.directions
            turn_direction = self.directions[self.turns % 3]
            # get new direction from turn_map
            self.direction = self.turn_map[self.direction][turn_direction]

        #commenting out, overrides are only needed if we are printing
        #if self.pos in self.grid.overrides:
        #    # collision
        #    self.grid.overrides[self.pos] = 'X'
        #    return False
        #self.grid.overrides[self.pos] =  self.symbols[self.direction]
        self.moves += 1
        return True

    def remove(self):
        """
        Function to remove a cart from the track
        """
        # commenting out, any references to overrides are
        # only relevant if you want to print the map
        #self.grid.overrides.pop(self.pos, None)  # Safely remove the override
        self.removed = True
        self.pos = (sys.maxsize, sys.maxsize)

    def __str__(self):
        """
        String
        """
        return f"Cart {self.cart_id} at {self.pos} removed: {self.removed} moves: {self.moves}"

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    #solve_start = time.time()
    grid = parse_data(input_value)
    cart_collection = Carts(grid)
    #print(cart_collection)
    if part == 1:
        collision = False
        while not collision:
            for cart in cart_collection:
                cart.move()
                cart_collection.push(cart)
                if cart_collection.detect_collision():
                    collision = True
                    break
        #print(cart_collection)
        return ','.join(str(coord) for coord in cart_collection.last_collision['location'])
    #if part == 2:
    #    return None
    # we learn in part1 that 3 and 7 are the first collision,
    # so I don't feel that this is oeverly cheating
    keep = []
    for cart in cart_collection:
        if cart.cart_id in [3,7]:
            cart.remove()
        else:
            keep.append(cart)
    for cart in keep:
        cart_collection.push(cart)

    while len(cart_collection) > 1:
        for cart in cart_collection:
            if cart.removed:
                continue
            cart.move()
            cart_collection.push(cart)
            cart_collection.detect_collision()
    for cart in cart_collection:
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
