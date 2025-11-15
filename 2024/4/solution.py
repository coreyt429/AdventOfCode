"""
Advent Of Code 2024 day 4

Grid() made this one fairly easy. I extended it to at an items() method that I ended
up not using.  I think that will come in handy in the future though, as I usually
end up doing something like this:
for point in grid:
    char = grid.get_point(point)
    # do something with char

Now I can just do this:
for point, char in grid.items():
    # do something with char

The only trip ups on this one were typo's ([all_directions]  !- all_directions),
and bad assumptions

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid, all_directions, diagonal_directions  # pylint: disable=import-error


def count_words(grid, word, point, index=0, directions=all_directions):
    """Function to count the instances of word for a point"""
    if grid.get_point(point) != word[index]:
        return 0
    # are we on the last letter?
    if index == len(word) - 1:
        return 1
    total = 0
    for direction, neighbor in grid.get_neighbors(
        point=point, directions=directions
    ).items():
        total += count_words(grid, word, neighbor, index + 1, [direction])
    return total


def check_x_mas(grid, point):
    """
    Function to find X-MAS in the grid

    This one is a bit more hard coded to find MAS,
    unlike count_words, which should work with any word
    """
    if grid.get_point(point) != "A":
        return False
    # making an assumption here that this line means that a + is also an X:
    # "One way to achieve that is like this"
    # this assumption was wrong:  2031 - too high
    neighbors = grid.get_neighbors(point=point, directions=diagonal_directions)
    opposite_pairs = (("ne", "sw"), ("nw", "se"))
    valid = set()
    # check direction pairs to see if they match up to MS or SM
    for pair in opposite_pairs:
        chars = ""
        for direction in pair:
            if direction in neighbors:
                chars += grid.get_point(neighbors[direction])
        if chars in ["MS", "SM"]:
            valid.add(pair)
    # are there at least two pairs
    if len(valid) < 2:
        return False
    return True


def find_words(grid, word, part=1):
    """Function to find a word in the grid"""
    words = 0
    for point in grid:
        if part == 1:
            words += count_words(grid, word, point)
        else:
            if check_x_mas(grid, point):
                words += 1
    return words


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    return find_words(grid, "XMAS", part)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024, 4)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 2618, 2: 2011}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
