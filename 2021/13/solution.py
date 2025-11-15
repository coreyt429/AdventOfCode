"""
Advent Of Code 2021 day 13

I think I spent most of the time reading the dots.  I copied
ascii art to text code from a previous solution, and ran into
issues where this grid did not match the assumptions of the
previous code.  So it needed a couple of small fixes.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error


def parse_input(text):
    """Function to parse input returning dots and folds"""
    dots_text, folds_text = text.split("\n\n")
    dots = set()
    for line in dots_text.splitlines():
        x_val, y_val = line.split(",")
        dots.add((int(x_val), int(y_val)))
    folds = []
    for line in folds_text.splitlines():
        fold = line.split(" ")[-1]
        axis, value = fold.split("=")
        folds.append((axis, int(value)))
    return dots, folds


def fold_paper(dots, fold):
    """Function to fold paper and return new dot set"""
    new_dots = set()
    axis, value = fold
    val = {}
    for dot in dots:
        val["x"], val["y"] = dot
        if val[axis] > value:
            val[axis] = value - abs(val[axis] - value)
        new_dots.add((val["x"], val["y"]))
    return new_dots


def read_dots(dots):
    """
    Function to parse dot message
    sourced from 2016.8
    """
    grid = Grid(" ", use_overrides=False)
    for dot in dots:
        grid.set_point(dot, "#")
    grid.update()
    message = str(grid)
    # Split the string into lines
    lines = message.splitlines()
    # pulling the data from grid, did not space pad the end of the last
    # letter. This caused it to not match char_map
    for idx, _ in enumerate(lines):
        lines[idx] += " "

    # Define the width and height of each character
    char_width = 5
    char_height = 6  # Including the space between rows

    # Calculate the number of characters in the message
    # had to update with the +1 2016.8 must have had an even
    # numbe of characters
    num_chars = (len(lines[0]) + 1) // char_width

    # Initialize the result string
    result = ""
    char_map = {
        " ##  #  # #  # #### #  # #  # ": "A",
        "#### #    ###  #    #    #### ": "E",
        " ##  #  # #    # ## #  #  ### ": "G",
        "#  # #  # #### #  # #  # #  # ": "H",
        " ##  #  # #  # #  # #  #  ##  ": "O",
        "###  #  # #  # ###  #    #    ": "P",
        "###  #  # #  # ###  # #  #  # ": "R",
        "#   ##   # # #   #    #    #  ": "Y",
        "#### #    ###  #    #    #    ": "F",
        "  ##    #    #    # #  #  ##  ": "J",
    }
    # Iterate through each character
    for i in range(num_chars):
        # Extract the 5x5 grid for this character
        char_grid = [line[i * char_width : (i + 1) * char_width] for line in lines]
        # Convert the grid to a single string for easier comparison
        char_string = "".join(char_grid)
        # the last O was missing a couple spaces
        while len(char_string) < char_height * char_width:
            char_string += " "
        # match to char_map
        result += char_map.get(char_string, "?")
    return result


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    dots, folds = parse_input(input_value)

    if part == 1:
        folds = folds[:1]
    # How many dots are visible after completing just the
    # first fold instruction on your transparent paper?
    for fold in folds:
        dots = fold_paper(dots, fold)
    if part == 1:
        return len(dots)
    return read_dots(dots)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021, 13)
    input_data = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 785, 2: "FJAHJGAH"}
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
