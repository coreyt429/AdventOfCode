"""
Advent Of Code 2018 day 10

"""
# import system modules
import time
import re

# import my modules
import aoc # pylint: disable=import-error

X=0
Y=1
pattern_nums = re.compile(r'(-*\d+)')

def parse_data(lines):
    points = []
    for line in lines:
        data = [int(datum) for datum in pattern_nums.findall(line)]
        point = {
            "position": ((data[0]), data[1]),
            "velocity": (data[2], data[3])            
        }
        points.append(point)
    return points

def advance_points(points, reverse=False):
    for point in points:
        position = list(point['position'])
        velocity = point['velocity']
        for axis in [X,Y]:
            if reverse:
                position[axis] -= velocity[axis]
            else:
                position[axis] += velocity[axis]
        point['position'] = tuple(position)
    return points

def string_lights(points, message="lights"):
    retval = f"{message:}\n"
    x_values = [point['position'][X] for point in points]
    y_values = [point['position'][Y] for point in points]
    max_x = max(x_values)
    max_y = max(y_values)
    min_x = min(x_values)
    min_y = min(y_values)
    lights = [point['position'] for point in points]
    for pos_y in range(min_y, max_y + 1):
        for pos_x in range(min_x, max_x + 1):
            if (pos_x, pos_y) in lights:
                retval += '#'
            else:
                retval += '.'
        retval += '\n'
    retval += '\n'
    return retval

def print_lights(points, message="lights"):
    print(f"{message:}")
    x_values = [point['position'][X] for point in points]
    y_values = [point['position'][Y] for point in points]
    max_x = max(x_values)
    max_y = max(y_values)
    min_x = min(x_values)
    min_y = min(y_values)
    lights = [point['position'] for point in points]
    for pos_y in range(min_y, max_y + 1):
        for pos_x in range(min_x, max_x + 1):
            if (pos_x, pos_y) in lights:
                print('#', end="")
            else:
                print(".", end="")
        print()
    print()

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return answer[2]
    points = parse_data(input_value)
    last_seconds = 0
    last_diff_y = float('infinity')
    seconds = 0
    while True:
        #x_values = [point['position'][X] for point in points]
        y_values = [point['position'][Y] for point in points]
        #max_x = max(x_values)
        max_y = max(y_values)
        #min_x = min(x_values)
        min_y = min(y_values)
        #diff_x = max_x - min_x
        diff_y = max_y - min_y
        # points are moving back apart
        if diff_y > last_diff_y:
            break
        #print(f"seconds: {seconds}, max_x: {max_x}, min_x: {min_x}, diff: {max_x - min_x}")
        #print(f"seconds: {seconds}, max_y: {max_y}, min_y: {min_y}, diff: {max_y - min_y}")
        #print(f"second: {seconds}, max_y_count: {max([y_values.count(y_value) for y_value in y_values])}")
        #print(f"second: {seconds}, max_x_count: {max([x_values.count(x_value) for x_value in x_values])}")
        #print_lights(points, f"{seconds} seconds")
        points = advance_points(points)
        last_diff_y = diff_y
        last_seconds = seconds
        seconds += 1
    points = advance_points(points, reverse=True)
    lights = string_lights(points, f"{last_seconds} seconds)")
    print(lights)
    answer[2] = last_seconds
    return 'FNRGPBHR'

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,10)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_lines = my_aoc.load_lines()
    #print(input_lines)
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
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
