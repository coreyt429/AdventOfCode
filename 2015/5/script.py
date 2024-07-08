import sys

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    return lines

def part1(parsed_data):
    retval = {'nice': 0, 'naughty':0};
    """
    It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
"""
    
    forbidden_strings = ['ab', 'cd', 'pq', 'xy']
    vowels=['a','e','i','o','u']
    for line in parsed_data:
        vowel_count=0;
        double=0;
        bad=0
        for i in range(0,len(line)):
            if line[i] in vowels:
                vowel_count+=1
            if i < len(line) - 1:
                if line[i] == line[i+1]:
                    double+=1
                elif line[i:i+2] in forbidden_strings:
                    bad+=1 
        if bad > 0:
            retval['naughty']+=1
        elif vowel_count > 2:
            if double > 0:
                retval['nice']+=1
        else:
            retval['naughty']+=1
    return retval
"""
It contains a pair of any two letters that appears at least twice in the string without overlapping, 
like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.
"""
def part2(parsed_data):
    retval = {'nice': 0, 'naughty':0};
    for line in parsed_data:
        pairs=0
        skips=0
        for i in range(0,len(line)-2):
            if line[i] == line[i+2]:
                skips+=1
            for j in range(i+2,len(line)-1):
                if line[i:i+2] == line[j:j+2]:
                    pairs+=1
        if skips > 0:
            if pairs > 0:
                #print(f'nice: {line}')
                retval['nice']+=1
            else:
                retval['naughty']+=1
                #print(f'naughty: {line}')
        else:
            retval['naughty']+=1
            #print(f'naughty: {line}')
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data1)

    #print("Part 1")
    answer1 = part1(parsed_data)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    