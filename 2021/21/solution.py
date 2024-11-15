"""
Advent Of Code 2021 day 21

Part 1 was pretty easy.  Part 2, I tripped on myself.  Scrapped a recursive model.
Built a monstrocity. Gave up. Found a solution that worked, that was a simpler version
of my first idea (thanks u/joshbduncan/).

"""
# import system modules
import time
import re
import itertools
from functools import lru_cache

# import my modules
import aoc # pylint: disable=import-error

digit_pattern = re.compile(r'(\d+)')
def deterministic_die(sides=100):
    """dice roll generator for part 1"""
    value = 1
    while True:
        yield value
        value += 1
        if value > sides:
            value = 1

def parse_data(lines):
    """Function to parse input data"""
    player_data = []
    for line in lines:
        player_num, position = digit_pattern.findall(line)
        player_data.append({
            "position": int(position),
            "name": f"Player {player_num}",
            "score": 0
        })
    return player_data

@lru_cache(maxsize=None)
def next_position(pos, rolls):
    """Function to calculate the next position"""
    new_pos =  (pos + sum(rolls)) % 10
    if new_pos == 0:
        return 10
    return new_pos

dirac_rolls = tuple(itertools.product((1, 2, 3), (1, 2, 3), (1, 2, 3)))
@lru_cache(maxsize=None)
def play_turn(pos_1, score_1, pos_2, score_2):
    """Function to play turns recursively until we get a win"""
    wins_1 = wins_2 = 0

    for rolls in dirac_rolls:
        new_pos_1 = next_position(pos_1, rolls)
        new_score_1 = score_1 + new_pos_1
        if new_score_1 >= 21:
            wins_1 += 1
        else:
            results =  play_turn(pos_2, score_2, new_pos_1, new_score_1)
            wins_1 += results[1]
            wins_2 += results[0]
    return wins_1, wins_2

def part_2(input_value):
    """Function to solve part 2"""
    players = parse_data(input_value)
    wins = play_turn(
        players[0]['position'],
        players[0]['score'],
        players[1]['position'],
        players[1]['score']
    )
    return max(wins)

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return part_2(input_value)
    die = deterministic_die()
    players = parse_data(input_value)
    roll_count = 0
    while not any((player['score'] >=1000 for player in players)):
        for player in players:
            rolls = (next(die), next(die), next(die))
            roll_count += 3
            player['position'] = (player['position'] + sum(rolls)) % 10
            if player['position'] == 0:
                player['score'] += 10
            else:
                player['score'] += player['position']
            # break here in case player 1 finishes first, so player 2 doesn't move again
            if player['score'] >= 1000:
                break
    losing_score = min((player['score'] for player in players))
    return losing_score * roll_count

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021,21)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
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
        1: 605070,
        2: 218433063958910
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
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
