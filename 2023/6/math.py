import re
import sys
from math import prod, ceil, floor
from scipy.optimize import fsolve

def simulate(time: int, distance: int, hold: int):
    return (time - hold) * hold > distance

def main():
    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    
    times = [int(num) for num in re.findall(r'\d+', lines[0])]
    distances = [int(num) for num in re.findall(r'\d+', lines[1])]

    # part 1
    ways_to_win = [len([i for i in range(time) if simulate(time, distance, i)]) for time, distance in zip(times, distances)]    
    print(prod(ways_to_win))

    new_time = [int(num) for num in re.findall(r'\d+', lines[0].replace(' ', ''))][0]
    new_distance = [int(num) for num in re.findall(r'\d+', lines[1].replace(' ', ''))][0]
    print(f'new_time {new_time}')
    print(f'new_distance {new_distance}')

    # part 2 brute force
    # print(len(list(i for i in range(new_time) if simulate(new_time, new_distance, i))))

    # part 2 math
    roots = fsolve(lambda x: x * new_time - x ** 2 - new_distance, x0=[0, new_distance])
    print(f'roots: {roots}')
    print(f'{floor(roots[1])} - {ceil(roots[0])} + 1')
    print(floor(roots[1]) - ceil(roots[0]) + 1)
    return

main()