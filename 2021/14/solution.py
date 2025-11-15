"""
Advent Of Code 2021 day 14

Brute force worked for part 1.  Part 2, I'm kicking myself, because after
seeing the solution from u/ThreadsOfCode, I realized I've been down this
road before.  The solution makes sense, and I was able to adapt it to
my solution.  Now will I remember this next time I see one of these?

"""

# import system modules
import time
from collections import Counter, defaultdict

# import my modules
import aoc  # pylint: disable=import-error


def parse_input(text):
    """Function to parse input text and return template and rules"""
    template, rules_text = text.split("\n\n")
    rules = {}
    for rule in rules_text.splitlines():
        pair, insertion = rule.split(" -> ")
        rules[pair] = (pair[0] + insertion, insertion + pair[1])
    return template, rules


def process(template, rules):
    "Function to process template by rules, returning new_template"
    new_template = ""
    for idx, char in enumerate(template):
        if idx == len(template) - 1:
            new_template += char
            continue
        pair = char + template[idx + 1]
        if pair in rules:
            new_template += rules[pair][0]
            continue
        new_template += char
    return new_template


def process_2(template, rules, steps):
    """
    Function to process template rules.

    Improved version maintains pair counter instead of trying
    to build the template.
    """
    pairs = ["".join(pair) for pair in zip(template, template[1:])]
    counter = Counter(pairs)
    for _ in range(steps):
        new_counter = {key: 0 for key in rules.keys()}
        for key, value in counter.items():
            new_counter[rules[key][0]] += value
            new_counter[rules[key][1]] += value
        counter = new_counter
    letters = defaultdict(int)
    for key, value in counter.items():
        letters[key[0]] += value
    letters[template[-1]] += 1
    most_common_letters = Counter(letters).most_common()
    return most_common_letters[0][1] - most_common_letters[-1][1]


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    template, rules = parse_input(input_value)
    passes = 10
    if part == 2:
        passes = 40
    return process_2(template, rules, passes)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021, 14)
    input_data = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 3118, 2: 4332887448171}
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
