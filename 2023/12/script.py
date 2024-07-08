import sys
import re
import functools

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    records = []
    for line in lines:
        record,counts = line.split(' ')
        records.append({'record': record, 'counts': [int(count) for count in counts.split(',')]})
    return records

@functools.cache
def n_arrangements(s, groups_left, group_sz):
    # FIXME:  study this logic until you understand it.
    #print(f'n_arrangements({s}, {groups_left}, {group_sz})')
    """
    s = what is left of input line
    groups_left = groups left (tuple)
    group_sz = current size of group in consumed line (s)
    """
    # base case for recursion
    if len(s) == 0:
        if len(groups_left) == 0 and group_sz == 0:
            # No groups left, it's a match
            return 1
        elif len(groups_left) == 1 and group_sz == groups_left[0]:
            # 1 group left the same size as current group, match
            return 1
        else:
            # No match
            return 0

    # consumed groups larger than groups left
    if len(groups_left) > 0 and group_sz > groups_left[0]:
        return 0
    # don't expect any more groups but I am in a group
    # I need group therapy
    elif len(groups_left) == 0 and group_sz > 0:
        return 0

    # all good so far
    n = 0

    spring = s[0]

    # If ? is # or if spring is # is the same case
    if spring == '#' or spring == '?':
        n += n_arrangements(s[1:], groups_left, group_sz + 1)

    # If ? is . or if spring is . is the same case
    if spring == '.' or spring == '?':
        if len(groups_left) > 0 and group_sz == groups_left[0]:
            n += n_arrangements(s[1:], groups_left[1:], 0)
        elif group_sz == 0:
            n += n_arrangements(s[1:], groups_left, 0)

    # so above ? will recurse 2 times while . or # will recurse
    # 1 time, each case consuming one input line (s) character
    return n



def part1(parsed_data):
    retval = 0;
    for record in parsed_data:
        template = record['record']
        counts = []
        for count in record['counts']:
            counts.append(count)
        counts = tuple(counts)
        n = n_arrangements(template, counts, 0)
        #print(template,counts, n)
        retval += n
    return retval


def part2(parsed_data):
    retval = 0;
    for record in parsed_data:
        arrangements = []
        template = '?'.join([record['record'],record['record'],record['record'],record['record'],record['record']])
        counts = []
        for i in range(5):
            for count in record['counts']:
                counts.append(count)
        counts = tuple(counts)
        n = n_arrangements(template, counts, 0)
        #print(template,counts, n)
        retval += n
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