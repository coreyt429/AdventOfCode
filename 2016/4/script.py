"""
AdventOfCode 2016 3

Each room consists of an encrypted name (lowercase letters separated by dashes) 
followed by a dash, a sector ID, and a checksum in square brackets.

A room is real (not a decoy) if the checksum is the five most common letters 
in the encrypted name, in order, with ties broken by alphabetization. For example:

aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters are 
                            a (5), b (3), and then a tie between x, y,
                            and z, which are listed alphabetically.
a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are all 
                            tied (1 of each), the first five are listed alphabetically.
not-a-real-room-404[oarel] is a real room.
totally-real-room-200[decoy] is not.
Of the real rooms from the list above, the sum of their sector IDs is 1514.
What is the sum of the sector IDs of the real rooms?
"""
import re
import sys
from heapq import heappush, heappop

INPUT_PATTERN = re.compile(r'(.*)-(\d+)\[(\w*)\]')

def load_data(file_name):
    """
    Loads data from file
    """
    with open(file_name,'r',encoding='utf-8') as file:
        lines = file.read().rstrip().split('\n')
        data = []
        for line in lines:
            matches = INPUT_PATTERN.match(line)
            data.append(
                {
                    'letters': matches.group(1),
                    'sectorId': int(matches.group(2)),
                    'checksum': matches.group(3)
                }
            )
    return data

def build_checksum(letters):
    """
    Function to build checksum
    """
    heap = []
    for letter in set(letters):
        score = -1 * letters.count(letter)
        heappush(heap,(score,letter))
    checksum = ''
    for _ in range(5):
        score,letter = heappop(heap)
        checksum += letter
    return checksum

def check_checksum(letters,checksum):
    """
    Function to compare checksums
    """
    return build_checksum(letters.replace('-','')) == checksum

def decrypt(message,cipher_key):
    """
    Function to decrypt codes
    To decrypt a room name, rotate each letter forward through the alphabet a 
    number of times equal to the room's sector ID. A becomes B, B becomes C, Z 
    becomes A, and so on. Dashes become spaces.
    For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.
    """
    offset = cipher_key % 26
    message.replace('-',' ')
    decrypted_message = ''
    for char in message:
        if char == '-':
            char = ' '
        else:
            char_num = ord(char)
            char_num+=offset
            if char_num > 122:
                char_num -= 26
            char=chr(char_num)
        decrypted_message+=char
    return decrypted_message

if __name__ == "__main__":
    codes = load_data(sys.argv[1])
    total = {
        'p1': 0
    }
    for code in codes:
        if check_checksum(code['letters'],code['checksum']):
            total['p1'] += code['sectorId']
    print(f"Part1: {total['p1']}")

    for code in codes:
        decrypted = decrypt(code['letters'],code['sectorId'])
        if 'north' in decrypted:
            print(decrypted,code['sectorId'])
