import sys
import re
import math

def find_factors(num):
    factors = set()
    for i in range(1, int(math.sqrt(num)) + 1):
        if num % i == 0:
            factors.add(i)
            factors.add(num // i)
    return factors

def part1():
    return part1_factors()

def part1_factors():
    target = 29000000
    retval = 0
    while True:
        retval += 1
        factors = find_factors(retval)
        presents = sum(factors) * 10
        #print(f'House {retval} got {presents} presents')
        if presents >= target:
            return retval

def part1_sieve():
    target = 29000000
    houses = [0] * (target // 10)
    for elf in range(1, target // 10):
        for house in range(elf, target // 10, elf):
            houses[house] += elf * 10
        if houses[elf] >= target:
            return elf

def part2():
    target = 29000000
    retval = 0
    while True:
        retval += 1
        factors = find_factors(retval)
        presents = sum(factors) * 10
        #print(f'House {retval} got {presents} presents')
        if presents >= target:
            return retval

def parts():
    target = 29000000
    part_one, part_two = None, None
    # guess that we can skip the first (2% of presents) houses
    i = int(.02*target)
    while not part_one or not part_two:
        # optimization cheat, once we determined that both answers are divisible by 40
        i += 40
        factors = find_factors(i)
        if not part_one:
            if sum(factors) * 10 >= target:
                part_one = i
        if not part_two:
            if sum(d for d in factors if i / d <= 50) * 11 >= target:
                part_two = i
    return part_one, part_two

if __name__ == "__main__":
    
    #print("Part 1")
    answer1,answer2 = parts()
    
    #print("Part 2")
    #answer2 = part2()

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    