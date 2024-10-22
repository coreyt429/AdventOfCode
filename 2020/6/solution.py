"""
Advent Of Code 2020 day 6

python sets make this one pretty easy.

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def parse_groups(input_string):
    """Function to parse groups"""
    groups = []
    # Each group's answers are separated by a blank line
    input_groups = input_string.split('\n\n')
    for group in input_groups:
        # within each group, each person's answers are on a single line.
        groups.append(group.splitlines())
    return groups

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    groups = parse_groups(input_value)
    total = 0
    total_2 = 0
    for group in groups:
        all_answers = set()
        first = True
        # part 2:
        # You don't need to identify the questions to which anyone answered "yes";
        # you need to identify the questions to which everyone answered "yes"!
        # so for the people in the group, we will use set intersection to
        # identify the questions answered by all in the group
        for person in group:
            # print(f"all_answers: {all_answers}, person: {person}")
            if first:
                all_answers = set(person)
                first = False
            else:
                all_answers.intersection_update(set(person))
        group_answers = set(''.join(group))

        # print(f"Final all_answers: {all_answers} ")
        total_2 += len(all_answers)
        # For each group, count the number of questions to which anyone answered "yes".
        # What is the sum of those counts?
        total += len(group_answers)
    if part == 2:
        # print(all_answers)
        return total_2
    return total

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020,6)
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
    # correct answers once solved, to validate changes
    correct = {
        1: 6161,
        2: 2971
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
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
