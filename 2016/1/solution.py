"""
Advent Of Code 2016 day 1

This was another newer solution, so it is already pretty efficient.
Just repackaged into my current format.
"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

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

def follow_direction(direction, block_count, fd_x,fd_y, heading):
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

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return answer[2]
    my_directions = [
        (direction[0], int(direction[1:])) for direction in input_value.rstrip().split(', ')
    ]
    my_x = 0
    my_y = 0
    my_heading = 'N'
    path = [(my_x,my_y)]
    visited = set()
    visited.add((my_x,my_y))
    found = False
    part2_coord = ()
    for my_direction, blocks in my_directions:
        my_x, my_y, my_heading, visits = follow_direction(
            my_direction,
            blocks,
            my_x,
            my_y,
            my_heading
        )
        path.append((my_x,my_y))
        for coord in visits:
            if coord in visited:
                #print(f"already visited: {coord} - {abs(coord[0]) + abs(coord[1])}")
                if not found:
                    part2_coord = coord
                    found = True
            visited.add(coord)
    answer[2] = abs(part2_coord[0]) + abs(part2_coord[1])
    return abs(my_x) + abs(my_y)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016,1)
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
