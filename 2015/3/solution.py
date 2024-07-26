"""
Advent Of Code 2015 day 3

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def part1(data):
    """
    Function to solve part 1
    """
    lattitude = 0
    longitude = 0
    houses = {f'{lattitude}-{longitude}': 1}
    for char in data:
        if char == '>':
            longitude += 1
        elif char == '<':
            longitude -= 1
        elif char == 'v':
            lattitude -= 1
        elif char == '^':
            lattitude += 1
        house_name = f'{lattitude}-{longitude}'
        if house_name in houses:
            houses[house_name] += 1
        else:
            houses[house_name] = 1
    return len(houses)

def part2(data):
    """
    Function to solve part 2
    """
    vehicles = ['Santa','RoboSanta']
    lattitude = {'Santa': 0,'RoboSanta': 0}
    longitude = {'Santa': 0,'RoboSanta': 0}
    houses = {f'{lattitude["Santa"]}-{longitude["Santa"]}': 2}
    for idx, char in enumerate(list(data)):
        v_idx = idx % 2
        vehicle=vehicles[v_idx]
        if char == '>':
            longitude[vehicle] += 1
        elif char == '<':
            longitude[vehicle] -= 1
        elif char == 'v':
            lattitude[vehicle] -= 1
        elif char == '^':
            lattitude[vehicle] += 1
        house_name = f'{lattitude[vehicle]}-{longitude[vehicle]}'
        if house_name in houses:
            houses[house_name] += 1
        else:
            houses[house_name] = 1
    return len(houses)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,3)
    input_text = my_aoc.load_text()
    #print(input_text)
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
        1: part1,
        2: part2
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
