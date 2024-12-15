"""
Advent Of Code 2024 day 13

Tried BFS/DFS, and was taking too long, using too much memory, etc.

Sat down with pencil and paper to figure out the math, and came up short.

Discussed what I understood of the problem mathematically with ChatGPT, and
came up with a sound math strategy.  Ran that through sympy and solved,
sample data and part 1 with no problem.

Bring on part 2.  oh that's it, just add to prize x/y values.  same solution
same solve time. 


"""
# import system modules
import time
import re
from sympy import symbols, solve

# import my modules
import aoc # pylint: disable=import-error

digit_pattern = re.compile(r'(\d+)')

def parse_input(text, part):
    """Function to parse input"""
    machines = []
    machine_texts = text.split("\n\n")
    add = 0
    if part == 2:
        add = 10000000000000
    for machine_text in machine_texts:
        machine_list = machine_text.splitlines()
        button_a = digit_pattern.findall(machine_list[0])
        button_b = digit_pattern.findall(machine_list[1])
        prize = digit_pattern.findall(machine_list[2])
        machines.append({
            'button_a': tuple(int(num) for num in button_a),
            'button_b': tuple(int(num) for num in button_b),
            'prize': tuple(int(num) + add for num in prize),
        })
    return machines



def solve_two_diophantine(eq1, eq2):
    """
    Solve two simultaneous linear Diophantine equations:
    eq1: c_1 = a_coef1 * a + b_coef1 * b
    eq2: c_2 = a_coef2 * a + b_coef2 * b
    Returns values of (a, b) that satisfy both equations.
    """
    # Unpack coefficients and constants
    a_coef1, b_coef1, c_1 = eq1
    a_coef2, b_coef2, c_2 = eq2

    # Define variables
    sym_a, sym_b = symbols('a b', integer=True)

    # Solve the system of equations
    solutions = solve(
        [a_coef1 * sym_a + b_coef1 * sym_b - c_1, a_coef2 * sym_a + b_coef2 * sym_b - c_2],
        (sym_a, sym_b),
        dict=True
    )

    if solutions:
        return solutions
    return "No integer solutions exist."

def solution(input_value, part):
    """
    Function to solve puzzle
    """
    machines = parse_input(input_value, part)

    total = 0
    for machine in machines:
        equations = [None, None]
        for dim in (0, 1):
            equations[dim] = (
                machine['button_a'][dim],
                machine['button_b'][dim],
                machine['prize'][dim]
            )
        equation1 = (machine['button_a'][0], machine['button_b'][0], machine['prize'][0])
        equation2 = (machine['button_a'][1], machine['button_b'][1], machine['prize'][1])
        result = solve_two_diophantine(equation1, equation2)
        if isinstance(result, list):
            cost = float('infinity')
            for press_data in result:
                presses = tuple(press_data.values())
                cost = min(cost, (presses[0] * 3) + (presses[1] * 1))
            total += cost
    return total

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024,13)
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
        1: 31623,
        2: 93209116744825
    }
    # dict to map functions
    funcs = {
        1: solution,
        2: solution
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
