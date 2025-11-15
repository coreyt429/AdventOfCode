"""
Advent Of Code 2015 day 19

Fudge!!!!!!

Okay, so I failed at this one in my original attempt, but I know more now, I can do this. Right?

So, my original implementation was a bfs (likely borrowed, from who I don't recall). But it
didn't work.

So I tried improving it, and decided the search space was just too big, so....

Lets try Dijkstra.  Pruning will help right.  no.

A* sounds good, what's a good heuristic,  memory error.

Read through other solutions, and found CYK.  Discussed CYK with chatGPT for hours.
Worked through examples manually, and programatically, great.  lets try it with the
example data HOHOHO.  yeah, no go my implementation didn't work with this grammar.

utter frustration.

lets try this over complex parsing and grouping routine and DFS it.  nope, ran into impossible
combinations.

ugh.  lets just play with the data in the scratchpad.  what happens if I just replace all the
substrings.  hey, that was shorter.  what if I do it again.  shorter.  3 times, shorter.

4 times.  e  wtf?  that simple?  really.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def parse_input(data):
    """
    Function to parse data
    """
    grammar_rules = {}
    # split between chart of grammar rules, and start string
    chart, start = data.strip().split("\n\n")
    # for each line in split
    for line in chart.split("\n"):
        # get source and destination
        src, dst = line.split(" => ")
        # add to grammar_rules
        grammar_rules.setdefault(src, []).append(dst)
    return start, grammar_rules


def calibrate(str_current, replacements, depth):
    """
    Function to calibrate (part 1)
    """
    # init compounds
    compounds = set()
    # decrement depth
    depth -= 1
    # for idx and char in string
    for idx, char in enumerate(str_current):
        # if cahr is a key in replacement
        if char in replacements:
            # for rule in replacement
            for mod in replacements[char]:
                # modify and add to compounts
                str_new = str_current[:idx] + mod + str_current[idx + 1 :]
                # print(str_new)
                compounds.add(str_new)
                # recurse until depth is 0
                if depth > 0:
                    calibrate(str_new, replacements, depth)
        # if first two chars are in replacements
        elif str_current[idx : idx + 2] in replacements:
            # for rule in replacement
            for mod in replacements[str_current[idx : idx + 2]]:
                # modify and add
                str_new = str_current[:idx] + mod + str_current[idx + 2 :]
                compounds.add(str_new)
                # recurse
                if depth > 0:
                    calibrate(str_new, replacements, depth)
    return compounds


def reverse_rules(replacements):
    """
    Function to reverse grammar rules
    """
    # init rules
    rules = {}
    # walk replacements
    for key, values in replacements.items():
        for value in values:
            # swap positions
            rules[value] = key
    return rules


def part1(start, replacements, target):
    """
    Function to solve part 2
    """
    # calibrate and return length
    return len(calibrate(start, replacements, target))


def part2(start, replacements):
    """
    Function to solve part 1
    """
    # reverse the rule set
    reversed_rules = reverse_rules(replacements)
    # init target and changes
    target = start
    changes = 0
    # while target is longer than 'e'
    while len(target) > 1:
        # walk reversed rules
        for key, value in reversed_rules.items():
            # if key is in remainin string
            if key in target:
                # increment changes by the count of key in string
                changes += target.count(key)
                # replace key with value
                target = target.replace(key, value)
    return changes


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # parse input file
    start, replacements = parse_input(input_value)
    # part 1
    if part == 1:
        return part1(start, replacements, 1)
    # part 2
    return part2(start, replacements)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015, 19)
    input_text = my_aoc.load_text()
    # print(input_text)
    # input_lines = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
