"""
Advent Of Code 2022 day 2

Easy enough.  I only tripped on one small bug in part 2.  For some reason, I was
expecting 3 % 3 to be 3 instead of 0. Which is especially bad since I explicitly
tested that and still did it wrong.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def play_round(elf, player, part):
    """Function to play round of rock paper scissors"""
    moves = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
    # convert move to score
    elf = moves[elf]
    if part == 1:
        player = moves[player]
    else:
        # Anyway, the second column says how the round needs to end:
        # X means you need to lose,
        if player == "X":
            player = (elf - 1) % 3
        # Y means you need to end the round in a draw, and
        elif player == "Y":
            player = elf
        # Z means you need to win. Good luck!
        elif player == "Z":
            player = (elf + 1) % 3
        # fix scissors
        if player == 0:
            player = 3
    # get diff
    diff = abs(elf - player)

    if diff == 0:  # draw
        return elf + 3, player + 3
    if diff == 1:  # 1,2 or 2, 3 higher score wins
        if elf > player:
            return elf + 6, player
        return elf, player + 6
    if player == 1:  # 1, 3 - 1 wins
        return elf, player + 6
    return elf + 6, player
    # part 2:
    # 13662 too low


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    elf_total = 0
    player_total = 0
    for line in input_value:
        elf_score, player_score = play_round(*line.split(" "), part)
        elf_total += elf_score
        player_total += player_score
    return player_total


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022, 2)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 10718, 2: 14652}
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
