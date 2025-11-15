"""
Advent Of Code 2016 day 7

already fast, refactored, simplifying main logic and moving to current format

"""

# import system modules
import time
import re

# import my modules
import aoc  # pylint: disable=import-error

supernet_pattern = re.compile(r"(\[\w+\])")


def contains_abba(my_string):
    """
    Checks for abba pattern in string
    """
    for idx in range(len(my_string) - 3):
        if (
            my_string[idx] == my_string[idx + 3]
            and my_string[idx + 1] == my_string[idx + 2]
            and my_string[idx] != my_string[idx + 1]
        ):
            return True
    return False


def contains_aba(my_string):
    """
    checks for aba patterns
    """
    abas = []
    retval = False
    for idx in range(len(my_string) - 2):
        if (
            my_string[idx] == my_string[idx + 2]
            and my_string[idx] != my_string[idx + 1]
        ):
            retval = True
            abas.append(my_string[idx : idx + 3])
    return retval, abas


def contains_bab(my_string, aba):
    """
    contains reverse of aba
    """
    bab = aba[1] + aba[0] + aba[1]
    return bab in my_string


def supports_ssl(my_string):
    """
    check for ssl suport ABA outside [] and BAB inside []
    """
    supernets = supernet_pattern.findall(my_string)
    for supernet in supernets:
        my_string = my_string.replace(supernet, "-")

    has_aba, my_abas = contains_aba(my_string)
    if has_aba:
        for aba in my_abas:
            for supernet in supernets:
                if contains_bab(supernet, aba):
                    return True
    return False


def supports_tls(my_string):
    """
    check for tls support (abba outside of square brackets, but not inside)
    """
    for my_str in supernet_pattern.findall(my_string):
        if contains_abba(my_str):
            return False
    if contains_abba(my_string):
        return True
    return False


def solve(lines, part):
    """
    Function to solve puzzle
    """
    counter = 0
    func_map = {1: supports_tls, 2: supports_ssl}
    for line in lines:
        if func_map[part](line):
            counter += 1
    return counter


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016, 7)
    input_lines = my_aoc.load_lines()
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
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
