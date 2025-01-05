"""
Advent Of Code YEAR day DAY

"""
# import system modules

# import my modules
from aoc import AdventOfCode # pylint: disable=import-error

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    return part

if __name__ == "__main__":
    aoc = AdventOfCode(YEAR,DAY)
    aoc.load_text()
    # aoc.load_list()
    # correct answers once solved, to validate changes
    aoc.correct[1] = None
    aoc.correct[2] = None
    aoc.funcs[1] = solve
    aoc.funcs[2] = solve
    aoc.run()
