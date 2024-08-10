"""
Advent Of Code 2017 day 11

I may have over designed this one.  I'm pretty sure the object structure is unecessary, and
keeping track of the Hex()s in the HexGrid() is pointless, but I had fun with this one, 
and it runs fast.  So be it.

My first attempt was using axial coordinates, and the calculations were unreliable. Switched
to cube coordinates, and it seems more accurate.

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error


class Hex():
    """
    Class to represent a hex tile
    """
    # define direction offsets
    directions = {
            "n": (0, 1, -1),
            "s": (0, -1, 1),
            "ne": (1, 0, -1),
            "nw": (-1, 1, 0),
            "se": (1, -1, 0),
            "sw": (-1, 0, 1)
        }

    def __init__(self, parent, x_val, y_val, z_val):
        """
        Init a hex tile:
            Args:
                self: Hex() object
                parent: HexGrid() object
                pos: tuple(float(X), float(Y)) coordinates 0.5 increments
        """
        # link back to HexGrid()
        self.parent = parent
        # cube coordinates
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val

    def __str__(self):
        """
        String representation
        """
        return f"Hex Tile ({self.x_val},{self.y_val},{self.z_val})"

    def step(self, direction):
        """
        Function to step in a direction
        """
        # get directional offsets
        dx_val, dy_val, dz_val = self.directions[direction]
        # ask HexGrid for our neighbor, why return, who knows what I was thinking
        return self.parent.get_neighbor(
            self.x_val + dx_val,
            self.y_val + dy_val,
            self.z_val + dz_val
        )

class HexGrid():
    """
    Class to represent a grid of hex tiles
    """
    def __init__(self):
        """
        Init grid
        """
        # store tiles, and create start tile
        self.tiles = {
            (0,0,0): Hex(self, 0,0,0)
        }
        # init start
        self.start = self.tiles[(0,0,0)]
        # init current as start
        self.current = self.tiles[(0,0,0)]

    def get_neighbor(self, x_val ,y_val, z_val):
        """
        Function to get neighbor
        """
        # if cube coordinates are not already in tiles
        if (x_val, y_val, z_val) not in self.tiles:
            # create new tile
            self.tiles[(x_val, y_val, z_val)] = Hex(self, x_val, y_val, z_val)
        # set current to specified tile
        self.current = self.tiles[(x_val, y_val, z_val)]

    def distance(self):
        """
        Function to calculate tile distance
        """
        # calculate distance
        return  0.5 * (
            abs(self.current.x_val - self.start.x_val) +
            abs(self.current.y_val - self.start.y_val) +
            abs(self.current.z_val - self.start.z_val)
        )


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init HexGrid
    grid = HexGrid()
    # init max_distance for part 2
    max_distance = 0
    last_distance = 0
    # for each direction in input
    for direction in input_value.split(','):
        # step in direction
        grid.current.step(direction)
        # update max_distance if we are further away
        last_distance = grid.distance()
        max_distance = max(max_distance, last_distance)
    # part 2?
    if part == 2:
        # return max
        return max_distance
    # part 1, return final distance
    return last_distance

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017,11)
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
