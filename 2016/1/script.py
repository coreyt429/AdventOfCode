"""
AdventOfCode 2016 1

This works, but should probably be refactored.  

In part 2, I at first I wasn't accounting for the blocks follow_direction
was skipping over.  I worked around this by having it return a set of 
visite_blocks.

"""
import sys

def read_directions_file(file_name):
    """
    Read data from file
    """
    with open(file_name,'r',encoding='utf-8') as file:
        return [(direction[0],int(direction[1:])) for direction in file.read().rstrip().split(', ')]

HEADING_DIRECTIONS = {
    'N': {'L': 'W', 'R': 'E'},
    'S': {'L': 'E', 'R': 'W'},
    'E': {'L': 'N', 'R': 'S'},
    'W': {'L': 'S', 'R': 'N'},
}

DIRECTIONAL_MOVEMENTS = {
    'N': { 'x': 0, 'y': 1},
    'S': { 'x': 0, 'y': -1},
    'E': { 'x': 1, 'y': 0},
    'W': { 'x': -1, 'y': 0},
}

def follow_direction(direction,block_count,fd_x,fd_y,heading):
    """
    follow direction
    """
    heading = HEADING_DIRECTIONS[heading][direction]
    visited_blocks = set()
    for _ in range(block_count):
        fd_x += DIRECTIONAL_MOVEMENTS[heading]['x']
        fd_y += DIRECTIONAL_MOVEMENTS[heading]['y']
        visited_blocks.add((fd_x, fd_y))
    return fd_x, fd_y, heading, visited_blocks

if __name__ == "__main__":
    my_directions = read_directions_file(sys.argv[1])
    my_x = 0 # pylint: disable=invalid-name
    my_y = 0 # pylint: disable=invalid-name
    my_heading = 'N' # pylint: disable=invalid-name
    path = [(my_x,my_y)]
    visited = set()
    visited.add((my_x,my_y))
    FOUND = False
    part2_coord = ()
    for my_direction, blocks in my_directions:
        my_x, my_y, my_heading, visits = follow_direction(my_direction,blocks,my_x,my_y,my_heading)
        path.append((my_x,my_y))
        for coord in visits:
            if coord in visited:
                #print(f"already visited: {coord} - {abs(coord[0]) + abs(coord[1])}")
                if not FOUND:
                    part2_coord = coord
                    FOUND = True
            visited.add(coord)


    print(f"Part1: {abs(my_x) + abs(my_y)}")
    print(f"Part1: {abs(part2_coord[0]) + abs(part2_coord[1])}")
    