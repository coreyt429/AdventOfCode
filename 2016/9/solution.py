"""
AdventOfCode 2016 day 9

This seemed really familiar, not sure if it was a similar puzzle from another year
or if I tried this one long ago.

Regardless, I made the same mistake.  I originally worked to actually decompress
the string (def decompress_string), which works great for part 1.  Not so much 
for part 2

I was solving this one at the end of the work day, and didn't have it in me. So I
borrowed an algorithm from a reddit solution (Thanks u/blockingthesky).

That worked, but I don't learn anything from just copying code.  So I commented the
decompress (now def decompress_borrowed) function to be sure I understood it.  Then
stripped away the code and worked form my comments to rebuild it in my style (def
decompress)
"""

import re
import aoc #pylint: disable=import-error

pattern_marker = re.compile(r'\((\d+)x(\d+)\)')

def decompress_string(input_string):
    """
    Function to decompress a string
    This was my attempt to actually build the string.
    This worked great for part1, and was impossible for part 2

    see decompress instead
    """
    # convert to a list so we can work with it
    input_list = list(input_string)
    # initialize new list for decompressed data
    new_list = []
    # idx will be a pointer to our location in the string, start at 0
    idx = 0
    # walk the string. note: we may increment idx within the loop, so not using enumerate
    while idx < len(input_list):
        # check to see if we might be at the start of a marker
        if input_list[idx] == '(':
            marker = '('
            idx+=1
            # add to marker until we reach ')'
            while input_list[idx] != ')':
                marker += input_list[idx]
                idx+=1
            marker += ')'
            # regex to see if we have really found a marker or just a '('
            # note, there could be something really evil in the data like:
            #  (4x5othertext)
            # hopefully not really, really evil like:
            #  (4x5othertext(4x5), if so we will miss a marker, wait I think I can fix that
            match = pattern_marker.search(marker)
            if match:
                # fix for (4x5othertext(4x5) case
                if match.span()[0] != 0:
                    # add non-matching portion of marker back to new_list
                    new_list = new_list + list(f'{marker[0:match.span()[0]]}')
                char_count = int(match.group(1))
                multiplier = int(match.group(2))
                tmp_string = ''
                # get next char_count characters
                for _ in range(char_count):
                    idx+=1
                    tmp_string += input_list[idx]
                # add to newlist multiplier times
                new_list = new_list + list(tmp_string)*multiplier
                idx+=1
            else: # not a marker lets just stick it on the string
                new_list = new_list + list(f'({marker})')
        else:
            new_list.append(input_list[idx])
            idx += 1
    return ''.join(new_list)

# borrowed algorithm. documenting for my understanding
def decompress_borrowed_to_study(s): # pylint: disable=invalid-name
    """
    recursive decompress function
    credit: u/blockingthesky

    paramaters:
      - s: string to decompress
    
    returns:
      - ret: integer length of decompressed data
    """
    # simple case input string does not have any markers, return its length
    if '(' not in s:
        return len(s)
    # initialize ret
    ret = 0
    while '(' in s:
        # add characters up to next marker
        ret += s.find('(')
        # extract marker
        s = s[s.find('('):]
        marker = s[1:s.find(')')].split('x')
        s = s[s.find(')') + 1:]
        # for part 2, lets get recursive
        if part2: # pylint: disable=undefined-variable
            # decompress next marker[0] characters multiplied by marker[1]
            ret += decompress(s[:int(marker[0])]) * int(marker[1])
        else:
            # add length of marker[0] characters multiplied by marker[1]
            ret += len(s[:int(marker[0])]) * int(marker[1])
        # remove processed string portion
        s = s[int(marker[0]):]
    # add length of remaining string
    ret += len(s)
    return ret

# borrowed algorithm. rewritten from my notes
def decompress(input_string,version_two=False):
    """
    recursive decompress function
    original algorithm credit: u/blockingthesky

    for this version I stripped out the code leaving my comments for guidance 
    and rewrote the function

    Note, this does fail my super evil case: '(4x5othertext(4x5)ABCD', 
    fortunately that doesn't seem
    to exist in the puzzle input.
    
    parameters:
      - input_string: string to decompress
      - version_two: bool flag to use version_two recursion default False
    
    returns:
      - decompressed_length: integer length of decompressed data
    """
    # simple case input string does not have any markers, return its length
    if '(' not in input_string:
        return len(input_string)
    # initialize decompressed_length
    decompressed_length = 0
    match = pattern_marker.search(input_string)
    while match:
        #<re.Match object; span=(1, 6), match='(1x5)'>
        # add characters up to next marker
        decompressed_length += int(match.span()[0])
        # extract marker
        span=int(match.group(1))
        multiplier=int(match.group(2))
        next_span = input_string[int(match.span()[1]):match.span()[1]+span]
        # for part 2, lets get recursive
        if version_two:
            # decompress next span characters multiplied by multiplier
            decompressed_length += decompress(next_span,version_two)*multiplier
        else:
            # add length of span characters multiplied by multiplier
            decompressed_length += len(next_span)*multiplier
        # remove processed string portion
        input_string = input_string[match.span()[1]+span:]
        # reprocess match (leave commented for now to avoid infinite loop)
        match = pattern_marker.search(input_string)
    # add length of remaining string
    decompressed_length += len(input_string)

    return decompressed_length

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016,9)
    input_text = my_aoc.load_text()
    print(f"Part 1: {len(decompress_string(input_text))}")
    print(f"Part 1: {decompress(input_text)}")
    print(f"Part 2: {decompress(input_text,True)}")
