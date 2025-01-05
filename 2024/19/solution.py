"""
Advent Of Code 2024 day 19

Part 1, I started with a heap based solution.  This worked for part 1,
and was too slow for part 2.

Part 2, I switched to a recursive solution, which was using too much
memory when I was storing the possible solutions. I realized I didn't need
to know the actual solutions, just the count of possible solutions.
So I modified the recursive solutions to return the count of possible solutions
instead.
I then moved that function into solve() as a sub function, and added lru_cache.
This let me just pass the remaining design string to the function, and it would
pickup the towel list from solve().  This was much faster and used less memory.

"""
# import system modules
from functools import lru_cache
# import my modules
from heapq import heappush, heappop
from aoc import AdventOfCode # pylint: disable=import-error

def parse_input(input_text):
    """Function to parse input"""
    towels, designs = input_text.split('\n\n')
    towels = towels.split(', ')
    designs = designs.split('\n')
    return towels, designs

def find_towel_heap(towels, design, part):
    """
    Function to find a towel combination
    not used in final solution, preserved for reference
    """
    possible_towels = []
    for towel in towels:
        if towel in design:
            possible_towels.append(towel)
    heap = []
    heappush(heap, (0, ()))
    seen = set()
    selection = set()
    while heap:
        _, selected = heappop(heap)
        selected_string = ''.join(selected)
        if selected in seen:
            continue
        seen.add(selected)
        if not design.startswith(selected_string):
            continue
        if selected_string == design:
            if part == 1:
                return selected
            selection.add(selected)
        for possible_towel in possible_towels:
            new_selected = selected + (possible_towel,)
            new_selected_string = ''.join(new_selected)
            if new_selected_string in seen:
                continue
            if design.startswith(new_selected_string):
                heappush(heap, (len(design) - len(new_selected_string), new_selected))

    return selection

def find_towel_recursive(towels, design, current=None):
    """
    Function to find towel combinations recursively
    not used in final solution, preserved for reference
    """
    solutions = []
    if current is None:
        current = []
    print(f"find_towel: {current}")
    current_string = ''.join(current)
    if current_string == design:
        return solutions + [current]
    for towel in towels:
        if design.startswith(current_string + towel):
            solutions.extend(find_towel_recursive(towels, design, current + [towel]))
    return solutions

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    towels, designs = parse_input(input_value)
    count = 0
    @lru_cache(maxsize=None)
    def find_towel_optimized(design):
        solutions = 0
        if design == '':
            return 1
        for towel in towels:
            if design.startswith(towel):
                solutions += find_towel_optimized(design[len(towel):])
        return solutions
    if part == 1:
        for design in designs:
            if find_towel_optimized(design) > 0:
                count += 1
    else:
        for design in designs:
            design_count = find_towel_optimized(design)
            count += design_count
    return count

if __name__ == "__main__":
    aoc = AdventOfCode(2024,19)
    aoc.load_text()
    # my_aoc.load_list()
    # correct answers once solved, to validate changes
    aoc.correct[1] = 220
    aoc.correct[2] = 565600047715343
    aoc.funcs[1] = solve
    aoc.funcs[2] = solve
    aoc.run()
