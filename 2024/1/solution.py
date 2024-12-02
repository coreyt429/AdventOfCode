"""
Advent Of Code 2024 day 1

List/tuple manipulation and number comparison.  For part 1, I made myself use zip(),
I usually don't naturally go there decades of nested for loops are hard to unwind :)



"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def parse_data(lines):
    """Function to parse input data"""
    list_1 = []
    list_2 = []
    for line in lines:
        # both test and input data seem evenly spaced, so just splitting
        # if this turned out not to be the case, we could use a regex to extract
        # the numbers
        num_1, num_2 = (int(num) for num in line.split('   '))
        list_1.append(num_1)
        list_2.append(num_2)
    # probably could have stuck with lists, here.  I'm trying to stay in the practice of
    # passing tuples between functions to use lru_cache() for repetitive calls
    return tuple(list_1), tuple(list_2)

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    loc_lists = parse_data(input_value)
    if part == 2:
        # part 2:
        # What is their similarity score?
        similarity = 0
        for num in loc_lists[0]:
            # The first number in the left list is 3. It appears in the right list three times,
            count = loc_lists[1].count(num)
            # so the similarity score increases by 3 * 3 = 9
            similarity += num*count
        return similarity
    # part 1:
    # What is the total distance between your lists?
    distance = 0
    # To find out, pair up the numbers and measure how far apart they are.
    for num_a, num_b in zip(*(sorted(loc_list) for loc_list in loc_lists)):
        distance += abs(num_a - num_b)
    return distance

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024,1)
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
        1: 936063,
        2: 23150395
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
