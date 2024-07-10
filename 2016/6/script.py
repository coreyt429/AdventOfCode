"""
AdventOfCode 2016 day 6
"""
from heapq import heappush, heappop
import sys

def load_data(file_name):
    """
    Load data file
    """
    with open(file_name,'r',encoding='utf=8') as file:
        return list(file.read().rstrip().split('\n'))

if __name__ == '__main__':
    lines = load_data(sys.argv[1])
    messages = {
	    'p1': '',
	    'p2': ''
    }
    for pos in range(len(lines[0])):
        tmp_str = '' # pylint: disable=invalid-name
        for line in lines:
            tmp_str += line[pos]
        letters = set(tmp_str)
        heap = []
        for letter in letters:
            heappush(heap,(-1*tmp_str.count(letter),letter))
        count,letter = heappop(heap)
        messages['p1'] += letter
        while heap:
            count,letter = heappop(heap)
        messages['p2'] += letter

    print(f"Part 1: {messages['p1']}")
    print(f"Part 2: {messages['p2']}")
