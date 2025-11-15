"""
Advent Of Code 2018 day 2

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def check_sum(box_ids):
    """
    checksum box_ids
    """
    matches = {2: set(), 3: set()}
    for box_id in box_ids:
        for char in set(list(box_id)):
            count = box_id.count(char)
            if count in matches:
                matches[count].add(box_id)
    # print(matches)
    return len(matches[2]) * len(matches[3])


def is_match(id_1, id_2):
    """
    check box_id for match
    """
    length = len(id_1)
    target = length - 1
    count = 0
    mismatch = None
    for idx, char in enumerate(id_1):
        if id_2[idx] == char:
            count += 1
        else:
            mismatch = idx
    # print(f"{target}: {count}: {id_1} {id_2}")
    if not count == target:
        return False, None
    # note this will fail if the mismatch is at 0, but I don't think it is
    return True, mismatch


def find_matches(box_ids):
    """
    find box_ids that mostly match
    """
    potentials = set()
    for box_id in box_ids:
        for box_id2 in box_ids:
            if box_id == box_id2:
                continue
            match, mismatch = is_match(box_id, box_id2)
            if match:
                potentials.add(tuple([mismatch] + sorted([box_id, box_id2])))
    if len(potentials) == 1:
        mismatch, box_id, _ = potentials.pop()
        box_id = list(box_id)
        box_id.pop(mismatch)
        return "".join(box_id)
    return "somethin bad happened"


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        # part 2
        return find_matches(input_lines)
    # part 1
    return check_sum(input_value)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018, 2)
    # input_text = my_aoc.load_text()
    # print(input_text)
    input_lines = my_aoc.load_lines()
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
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
