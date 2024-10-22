"""
Advent Of Code 2020 day 5



"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error
from grid import Grid # pylint: disable=import-error

def id_seat(code):
    """
    Function to convert elf binary seat notation to row/col tuple
    """
    row = {
        "min": 0,
        "max": 127
    }
    col = {
        "min": 0,
        "max": 7
    }
    for char in code:
        if char == 'F':
            diff = row['max'] - row['min']
            row['max'] -= diff // 2 + 1
        if char == 'B':
            diff = row['max'] - row['min']
            row['min'] += diff // 2 + 1
        if char == 'L':
            diff = col['max'] - col['min']
            col['max'] -= diff // 2 + 1
        if char == 'R':
            diff = col['max'] - col['min']
            col['min'] += diff // 2 + 1
    # print(row, col)
    # likely unnecessary checks to be sure we found an answer
    if row['min'] != row['max']:
        return None
    if col['min'] != col['max']:
        return None
    return (row['min'], col['min'])

def calc_seat_id(seat):
    """Function to calculate seat ids"""
    row, col = seat
    # Every seat also has a unique seat ID:
    # multiply the row by 8, then add the column.
    return (row * 8) + col

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid('.', use_overrides=False, default_value='.')
    max_seat_id = 0
    for seat_code in input_value:
        seat = id_seat(seat_code)
        grid.set_point(point=seat, value='#')
        seat_id = calc_seat_id(seat)
        max_seat_id = max(max_seat_id, seat_id)
    grid.update()
    # uncomment to visualize
    # print(grid)
    if part == 2:
        for seat in grid:
            if grid.get_point(seat,'.') == '.':
                # Your seat wasn't at the very front or back, though;
                # the seats with IDs +1 and -1 from yours will be in your list.
                # I actually got lucky here, since I visualized my seat with Grid()
                # first, I knew it was not on an end, so I didn't have to check that case
                # so we are just looking for a '.' that has '#' north and south of it
                # this may not work for other inputs
                neighbors = grid.get_neighbors(point=seat, directions='ns')
                if len(neighbors) != 2:
                    continue
                neighbor_seats = ''.join(
                    [grid.get_point(neighbor,'.') for neighbor in neighbors.values()]
                )
                if '.' not in neighbor_seats:
                    # What is the ID of your seat?
                    return calc_seat_id(seat)
    # What is the highest seat ID on a boarding pass?
    return max_seat_id

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020,5)
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
    # correct answers once solved, to validate changes
    correct = {
        1: 915,
        2: 699
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
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
