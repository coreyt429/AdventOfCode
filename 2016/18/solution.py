"""
Advent Of Code 2016 day 18

"""
import time
import aoc # pylint: disable=import-error

def next_row(last_row):
    """
    Function to determine next row based on:
    Its left and center tiles are traps, but its right tile is not.
    Its center and right tiles are traps, but its left tile is not.
    Only its left tile is a trap.
    Only its right tile is a trap.
    """
    new_row = ''
    for col in range(len(last_row)):
        # left wall safe, doesn't matter what center is: _.^, _^^, _^., _..
        if col == 0:
            new_row += last_row[1] # safe or trap
        # right wall safe, doesn't matter what center is:  .^_, ^^_, ^._, .._
        elif col == len(last_row)-1:
            new_row += last_row[-2] #safe or trap
        # all traps, this tile must be safe ^^^
        elif '.' not in last_row[col-1:col+2]:
            new_row += '.' # safe
        # all safe, this tile must be safe ...
        elif '^' not in last_row[col-1:col+2]:
            new_row += '.' # safe
        # both left and right, or neither left nor right: '^.^','.^.'
        elif last_row[col-1:col+2] in ['^.^','.^.']:
            new_row += '.' # safe
        # Remaining trap scenarios: .^^, ..^, , ^^.
        else:
            new_row += '^'
    return new_row

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016,18)
    first_row = my_aoc.load_text()
    # part 1
    start_time = time.time()
    parts = {
        1: 40,
        2: 400000
    }
    for part, num_rows in parts.items():
        rows = [first_row]
        while len(rows) < num_rows:
            rows.append(next_row(rows[-1]))
        end_time = time.time()
        COUNT = '\n'.join(rows).count('.')
        print(f"Part {part}: {COUNT}, took {end_time - start_time} seconds")
