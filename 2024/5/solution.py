"""
Advent Of Code 2024 day 5

Part 1 was easy. Part 2, I took a couple wrong approaches first.
Then sorted it out.

"""
# import system modules
import time
from itertools import permutations
from functools import lru_cache

# import my modules
import aoc # pylint: disable=import-error


@lru_cache(maxsize=None)
def rules_for_num(num, rules):
    """
    Function to break rules for a number down to
    two lists numbers that come before it and after
    """
    less_than = []
    greater_than = []
    for rule in rules:
        if num == rule[0]:
            less_than.append(rule[1])
        if num == rule[1]:
            greater_than.append(rule[0])
    return tuple(greater_than), tuple(less_than)

def check_pages(page_list, rules):
    """function to check a page_list for rule compliance"""
    for rule in rules:
        if not is_valid(page_list, rule):
            return False
    return True

def sort_pages(page_list, rules):
    """Function to sort pages"""
    nums = list(sorted(page_list))
    sorted_list = list(page_list)
    while not check_pages(sorted_list, rules):
        for num in nums:
            before, after = rules_for_num(num, rules)
            for other in after:
                if other not in nums:
                    continue
                if sorted_list.index(other) < sorted_list.index(num):
                    sorted_list.remove(other)
                    index = sorted_list.index(num)
                    sorted_list.insert(index + 1, other)
            for other in before:
                if other not in nums:
                    continue
                if sorted_list.index(other) > sorted_list.index(num):
                    sorted_list.remove(other)
                    index = sorted_list.index(num)
                    sorted_list.insert(index, other)
    return tuple(sorted_list)

# itertools.permutations is going to be faster,
def corrected(page_list, rules):
    """
    Function to correct pages using permutations
    This worked for the test data, not for the puzzle input (too slow)
    """
    for new_list in permutations(page_list):
        if check_pages(new_list, rules):
            return new_list
    # page list couldn't be fixed, giving up
    return page_list

def parse_data(text):
    """Funtion to parse input"""
    rules_text, pages_text = text.split('\n\n')
    rules = []
    for line in rules_text.splitlines():
        rules.append(tuple((int(num) for num in line.split('|'))))
    pages = []
    for line in pages_text.splitlines():
        pages.append(tuple((int(num) for num in line.split(','))))
    return tuple(rules), tuple(pages)

def is_valid(page_list, rule):
    """Function to test a page_list against a rule"""
    for num in rule:
        if num not in page_list:
            return True
    return page_list.index(rule[0]) < page_list.index(rule[1])

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    rules, pages = parse_data(input_value)
    total = 0
    for page_list in pages:
        if part == 1 and check_pages(page_list, rules):
            total += page_list[len(page_list) // 2]
        elif part == 2 and not check_pages(page_list, rules):
            new_page_list = sort_pages(page_list, rules)
            total += new_page_list[len(page_list) // 2]
    return total

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024,5)
    input_data = my_aoc.load_text()
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
        1: 4957,
        2: 6938
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
