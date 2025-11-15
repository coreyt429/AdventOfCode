"""
Advent Of Code 2020 day 24

Copied Hex() and HexGrid() from 2017.11

I had to expand the hex grids capabilities for this one.

Fun puzzle though.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


class Hex:
    """
    Class to represent a hex tile
    """

    # define direction offsets
    directions = {
        "e": (1, -1, 0),  # East
        "w": (-1, 1, 0),  # West
        "ne": (0, -1, 1),  # Northeast
        "nw": (-1, 0, 1),  # Northwest
        "se": (1, 0, -1),  # Southeast
        "sw": (0, 1, -1),  # Southwest
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
        self.radius = parent.distance((x_val, y_val, z_val))
        # The tiles are all white on one side and black on the other.
        # They start with the white side facing up.
        self.color = "white"

    def __str__(self):
        """
        String representation
        """
        return f"Hex Tile ({self.x_val},{self.y_val},{self.z_val}): {self.color} {self.radius}"

    def move(self, sequence):
        """
        Method for taking a sequence of steps
        """
        tile = self
        sequence = list(sequence)
        while sequence:
            direction = sequence.pop(0)
            if sequence and direction in ["n", "s"] and sequence[0] in ["e", "w"]:
                direction += sequence.pop(0)
            tile = tile.step(direction)
        return tile

    def step(self, direction):
        """
        Function to step in a direction
        """
        # get directional offsets
        dx_val, dy_val, dz_val = self.directions[direction]
        # ask HexGrid for our neighbor, why return, who knows what I was thinking
        return self.parent.get_neighbor(
            self.x_val + dx_val, self.y_val + dy_val, self.z_val + dz_val
        )

    def flip(self):
        """method to flip a tile"""
        if self.color == "white":
            self.color = "black"
        else:
            self.color = "white"


class HexGrid:
    """
    Class to represent a grid of hex tiles
    """

    # define direction offsets
    directions = {
        "e": (1, -1, 0),  # East
        "w": (-1, 1, 0),  # West
        "ne": (0, -1, 1),  # Northeast
        "nw": (-1, 0, 1),  # Northwest
        "se": (1, 0, -1),  # Southeast
        "sw": (0, 1, -1),  # Southwest
    }

    def __init__(self):
        """
        Init grid
        """
        # store tiles, and create start tile
        self.tiles = {(0, 0, 0): Hex(self, 0, 0, 0)}
        # init start
        self.start = self.tiles[(0, 0, 0)]
        # init current as start
        self.current = self.tiles[(0, 0, 0)]

    def get_neighbor(self, x_val, y_val, z_val):
        """
        Function to get neighbor
        """
        # if cube coordinates are not already in tiles
        if (x_val, y_val, z_val) not in self.tiles:
            # create new tile
            self.tiles[(x_val, y_val, z_val)] = Hex(self, x_val, y_val, z_val)
        # set current to specified tile
        self.current = self.tiles[(x_val, y_val, z_val)]
        return self.current

    def black_tiles(self):
        """Method to count black tiles in the map"""
        counter = 0
        for tile in self.tiles.values():
            if tile.color == "black":
                counter += 1
        return counter

    def distance(self, pos=None):
        """
        Function to calculate tile distance
        """
        if pos is None:
            x_val = self.current.x_val
            y_val = self.current.y_val
            z_val = self.current.z_val
        elif pos == (0, 0, 0):
            return 0
        else:
            x_val, y_val, z_val = pos
        # calculate distance
        return 0.5 * (
            abs(x_val - self.start.x_val)
            + abs(y_val - self.start.y_val)
            + abs(z_val - self.start.z_val)
        )

    def get_neighbors(self, pos):
        """method to get the neighbors of a position"""
        x_val, y_val, z_val = pos
        neighbors = []
        for offset in self.directions.values():
            d_x, d_y, d_z = offset
            new_pos = (x_val + d_x, y_val + d_y, z_val + d_z)
            neighbors.append(self.get_neighbor(*new_pos))
        return neighbors

    def expand(self):
        """Method to expand grid one layer"""
        max_distance = {"white": 0, "black": 0}
        for pos, tile in self.tiles.items():
            max_distance[tile.color] = max(max_distance[tile.color], tile.radius)
        # print(f"max_distance: {max_distance}")
        # 6 is the biggest radius for the first map
        if max_distance["white"] < max_distance["black"] + 6:
            current_pos = list(self.tiles)
            for pos in current_pos:
                self.get_neighbors(pos)

    def update_tiles(self):
        """Method to update tiles"""
        self.expand()
        # get current tile states
        current_state = {}
        for pos, tile in self.tiles.items():
            current_state[pos] = tile.color
        # calculate new tile states
        new_state = {}
        for pos, color in current_state.items():
            # print(f"Current: {self.tiles[pos]}")
            neighbors = self.get_neighbors(pos)

            black_tile_count = 0
            for neighbor in neighbors:
                # print(f"neighbor: {neighbor}")
                if neighbor.color == "black":
                    black_tile_count += 1
            tile = self.tiles[pos]
            # print(f"black tile count: {black_tile_count}")
            if tile.color == "black" and black_tile_count not in [1, 2]:
                # Any black tile with zero or more than 2 black tiles
                # immediately adjacent to it is flipped to white.
                # print(f"flip white")
                new_state[pos] = "white"
            if tile.color == "white" and black_tile_count == 2:
                # Any white tile with exactly 2 black tiles immediately
                # adjacent to it is flipped to black.
                # print(f"flip black")
                new_state[pos] = "black"
        # set tiles
        for pos, color in new_state.items():
            self.tiles[pos].color = color

    def __str__(self):
        """string representation"""
        my_str = ""
        for tile in self.tiles.values():
            my_str += str(tile) + "\n"
        return my_str


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = HexGrid()
    for sequence in input_value:
        tile = grid.start
        tile = tile.move(sequence)
        tile.flip()
    if part == 1:
        return grid.black_tiles()

    for _ in range(1, 100 + 1):
        grid.update_tiles()
        # print(f"Day {day}: {grid.black_tiles()}")
    return grid.black_tiles()


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020, 24)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 307, 2: 3787}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
