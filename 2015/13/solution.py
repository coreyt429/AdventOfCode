"""
Advent Of Code 2015 day 13

"""
# import system modules
import time
import itertools
import re

# import my modules
import aoc # pylint: disable=import-error

# Regex pattern for input
# Alice would gain 2 happiness units by sitting next to Bob.
pattern_input = re.compile(r'(\w+) would (gain|lose) (\d+) .* to (\w+).')

def parse_input(lines):
    """
    Function to parse input
    """
    # happiness score structure
    scores = {}
    # loop through lines
    for line in lines:
        # match pattern
        match = pattern_input.match(line)
        if match:
            # get values
            (peep, gain_lose, happiness, neighbor) = match.groups()
            # initialize peep if not already
            if not peep in scores:
                scores[peep] = {}
            # get integer value for happiness
            happiness = int(happiness)
            # if lose, negate hapiness
            if gain_lose == 'lose':
                happiness *= -1
            # store score
            scores[peep][neighbor] = happiness
    return scores

def score(my_map, my_peeps):
    """
    function to score seating arrangement
    """
    happiness = {}
    #print(my_map)
    for idx, current_peep in enumerate(my_peeps):
        if not current_peep in happiness:
            # initialize score
            happiness[current_peep] = 0
        #if first
        # get next peep
        next_peep = my_peeps[(idx + 1) % len(my_peeps)]
        # get previous peep
        prev_peep = my_peeps[(idx - 1) % len(my_peeps)]

        # add next_peep happiness
        happiness[current_peep] += my_map[current_peep][next_peep]
        # add prev_peep happiness
        happiness[current_peep] += my_map[current_peep][prev_peep]
    # return sum of hapiness
    return sum(happiness.values())


def solve(parsed_data, part):
    """
    Function to solve puzzle
    """
    # part 2
    if part == 2:
        # add Me
        parsed_data['Me'] = {}
        # for add peep relations to me
        for peep in parsed_data.keys():
            if not peep == 'Me':
                parsed_data['Me'][peep] = 0
                parsed_data[peep]['Me'] = 0
    # initialize max_happiness
    max_happiness = 0
    # get people
    peeps = set(parsed_data.keys())
    # use itertools to get permutations of people
    options = list(itertools.permutations(peeps))
    # test all options
    for option in options:
        # get score
        my_score = score(parsed_data, option)
        # if greater happiness
        if my_score > max_happiness:
            # update max_happiness
            max_happiness = my_score
    # return results
    return max_happiness

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,13)
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
        answer[my_part] = funcs[my_part](parse_input(input_lines), my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
