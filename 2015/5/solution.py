"""
Advent Of Code 2015 day 5

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def part1(lines):
    """
    Function to solve part 1
    It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or
      aabbccdd (aa, bb, cc, or dd).
    It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the
      other requirements.
    """
    retval = {'nice': 0, 'naughty': 0}

    forbidden_strings = ['ab', 'cd', 'pq', 'xy']
    vowels = ['a', 'e', 'i', 'o', 'u']
    for line in lines:
        vowel_count = 0
        double = 0
        bad = 0
        for idx, char in enumerate(line):
            if char in vowels:
                vowel_count += 1
            if idx < len(line) - 1:
                if char == line[idx + 1]:
                    double += 1
                elif line[idx:idx + 2] in forbidden_strings:
                    bad += 1
        if bad > 0:
            retval['naughty'] += 1
        elif vowel_count > 2:
            if double > 0:
                retval['nice'] += 1
        else:
            retval['naughty'] += 1
    return retval

def part2(lines):
    """
    Function to solve part 2
    It contains a pair of any two letters that appears at least twice in the string without
      overlapping, 
    like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    It contains at least one letter which repeats with exactly one letter between them, like
      xyx, abcdefeghi (efe), or even aaa.
    """
    retval = {'nice': 0, 'naughty': 0}
    for line in lines:
        pairs=0
        skips=0
        for idx in range(0, len(line) - 2):
            if line[idx] == line[idx + 2]:
                skips += 1
            for idx2 in range(idx + 2, len(line) - 1):
                if line[idx:idx + 2] == line[idx2:idx2 + 2]:
                    pairs += 1
        if skips > 0:
            if pairs > 0:
                #print(f'nice: {line}')
                retval['nice'] += 1
            else:
                retval['naughty'] += 1
                #print(f'naughty: {line}')
        else:
            retval['naughty'] += 1
            #print(f'naughty: {line}')
    return retval


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,5)
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
        1: part1,
        2: part2
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
