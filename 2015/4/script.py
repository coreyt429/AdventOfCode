import sys
import hashlib
import re

def part1(myKey):
    myNum = 0;
    # Create an MD5 hash object
    hash_object = hashlib.md5()
    hex_md5=''
    while not re.match("^00000", hex_md5):
        myNum += 1
        # Create a new MD5 hash object for each iteration
        hash_object = hashlib.md5()
        hash_object.update(f'{myKey}{myNum}'.encode())
        hex_md5 = hash_object.hexdigest()
    return myNum

def part2(myKey):
    myNum = 0;
    # Create an MD5 hash object
    hash_object = hashlib.md5()
    hex_md5=''
    while not re.match("^000000", hex_md5):
        myNum += 1
        # Create a new MD5 hash object for each iteration
        hash_object = hashlib.md5()
        hash_object.update(f'{myKey}{myNum}'.encode())
        hex_md5 = hash_object.hexdigest()
    return myNum

if __name__ == "__main__":
    answer1 = part1('bgvyzdsv')
    answer2 = part2('bgvyzdsv')

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    