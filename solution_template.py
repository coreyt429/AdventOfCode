"""
Advent Of Code YEAR day DAY

"""
import time
import aoc # pylint: disable=import-error

def solve(input_value, part):
    return part

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(YEAR,DAY)
    lines = my_aoc.load_lines()
    print(lines)
    # parts structure to loop
    parts = {
        1: 1,
        2: 2
    }
    answer = {
        1: None,
        2: None
    }
    # loop parts
    for part in parts:
        start = time.time()
        answer[part] = solve(my_input, part)
        end = time.time()
        print(f"Part {part}: {answer[part]}, took {end-start} seconds")