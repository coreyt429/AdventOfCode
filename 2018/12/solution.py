"""
Advent Of Code 2018 day 12

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def parse_input(input_data):
    """
    Function to parse input
    """
    (init_state, line_text) = input_data.split("\n\n")
    state = {}
    for idx, pot in enumerate(init_state.split(' ')[2]):
        if pot == '#':
            state[idx] = pot
    rules = {}
    for line in line_text.splitlines():
        rule, _, value = line.split(' ')
        rules[rule] = value
    return state, rules

def generation_string(generation, min_key=None, max_key=None):
    """
    Function to present a generation as a string
    """
    if not min_key:
        min_key = min(list(generation.keys()))
    if not max_key:
        max_key = max(list(generation.keys()))
    retval = ''
    for pot in range(min_key - 3, max_key + 3):
        retval += f"{generation.get(pot,'.')}"
    return retval

def print_generations(generations):
    """
    Function to visualize generations
    """
    min_key = 1
    max_key = 1
    for generation in generations:
        for key in generation.keys():
            min_key = min(min_key, key)
            max_key = max(max_key, key)
    for idx, generation in enumerate(generations):
        print(f"{idx:2}: {generation_string(generation, min_key, max_key)}")

def next_generation(generation, rules):
    """
    Funciton to calculate the next generation
    """
    min_key = min(generation.keys())
    max_key = max(generation.keys())
    new_generation = {}
    for idx in range(min_key - 4, max_key + 3):
        selection = ''.join(generation.get(pot, '.' ) for pot in range(idx - 2, idx + 3))
        value = rules.get(selection,'.')
        if value == '#':
            new_generation[idx] = value
    return new_generation

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    init_state, spread_rules = parse_input(input_value)
    generations = []
    generations.append(init_state)
    if part == 1:
        for _ in range(1,21):
            generations.append(next_generation(generations[-1], spread_rules))
        last_generation = generations[-1]
        return sum(last_generation.keys())
    for _ in range(1,100):
        generations.append(next_generation(generations[-1], spread_rules))
    last_generation = generations[-1]
    return sum((50000000000 - (len(generations) - 1)) + key for key in last_generation.keys())

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,12)
    input_text = my_aoc.load_text()
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
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
