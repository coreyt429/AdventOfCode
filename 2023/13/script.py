import sys
from copy import deepcopy
from typing import List

def parse_input(data):
    patterns =  []
    # Split the data into lines
    blocks = data.strip().split('\n\n')
    for block in blocks:
        patterns.append(block.split('\n'))
    return patterns

# Returns the number of lines above the horizontal reflection line,
# or zero if there is no horizontal reflection line. Where the reflection line
# is chosen such that there are exactly smudge_target "smudges"
def find_reflection(block: List[str], smudge_target: int = 0) -> int:
    retval = 0
    for split in range(len(block) - 1):
        smudges = 0
        for i in range(split + 1):
            if split + i + 1 >= len(block):
                continue

            row_above = block[split - i]
            row_below = block[split + i + 1]
            for a, b in zip(row_above, row_below):
                if a != b:
                    smudges += 1
        if smudges == smudge_target:
            retval = split + 1
            break
    return retval

def print_block(block):
    for row in block:
        print(row)

def transpose_block(block):
    transpose = []
    for i in range(len(block[0])):
        transpose.append("".join([row[i] for row in block]))
    return transpose

def part1(parsed_data):
    retval = 0
    h_total = 0
    v_total = 0
    for block in parsed_data:
        transpose = transpose_block(block)
        h_total += find_reflection(block)
        v_total+= find_reflection(transpose)
    retval = v_total + 100 * h_total
    return retval

def part2(parsed_data):
    retval = 0
    h_total = 0
    v_total = 0
    for block in parsed_data:
        transpose = transpose_block(block)
        h_total += find_reflection(block,1)
        v_total+= find_reflection(transpose,1)
    retval = v_total + 100 * h_total
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data)

    #print("Part 1")
    answer1 = part1(parsed_data)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
