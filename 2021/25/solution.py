"""
Advent Of Code 2021 day 25

nice simple puzzle to end.  Nice win after the brutality of the 24th.


"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def move_sea_cucumbers(in_map):
    """Function to move sea cucumbers one step"""
    # Every step, the sea cucumbers in the east-facing herd attempt to move forward one location,
    # then the sea cucumbers in the south-facing herd attempt to move forward one location. When
    # a herd moves forward, every sea cucumber in the herd first simultaneously considers whether
    # there is a sea cucumber in the adjacent location it's facing (even another sea cucumber
    # facing the same direction), and then every sea cucumber facing an empty location
    # simultaneously moves into that location.
    out_map = [["."] * len(line) for line in in_map]
    row_count = len(in_map)
    col_count = len(in_map[0])
    move_count = 0
    # move east
    for row, line in enumerate(in_map):
        for col, char in enumerate(line):
            if char == ">":
                if line[(col + 1) % col_count] == ".":
                    out_map[row][(col + 1) % col_count] = ">"
                    out_map[row][col] = "."
                    move_count += 1
                else:
                    out_map[row][col] = ">"
    # move south
    for row, line in enumerate(in_map):
        for col, char in enumerate(line):
            if char == "v":
                # if slot is open in the current map, and not already occupied in the new map
                if all(
                    [
                        in_map[(row + 1) % row_count][col] != "v",
                        out_map[(row + 1) % row_count][col] == ".",
                    ]
                ):
                    out_map[(row + 1) % row_count][col] = "v"
                    out_map[row][col] = "."
                    move_count += 1
                else:
                    out_map[row][col] = "v"
    return move_count, out_map


def print_map(in_map, title):
    """Function to print map for debug"""
    print(f"{title}:")
    for line in in_map:
        print("".join(line))
    print()


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return "Remote Start Sleigh"
    current_map = [list(line) for line in input_value]
    # print_map(current_map, "Initial state")
    idx = 0
    while True:
        idx += 1
        moves, current_map = move_sea_cucumbers(current_map)
        if moves == 0:
            return idx
            # print(f"No movement at {idx}")
            # break
        # ess = 's'
        # if idx == 1:
        #     ess = ''
        # print_map(current_map, f"After {idx} step{ess}")


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021, 25)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 471, 2: "Remote Start Sleigh"}
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
