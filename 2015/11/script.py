import sys
import re

def next_char(char):
    intChar = ord(char)
    intChar+=1
    if intChar > 122:
        intChar = 97
    if intChar in [105,108,111]: # banned letters i, l, and o
        intChar+=1
    char = chr(intChar)
    return char
    

def next_password(password):
    #print(f'next_password({password})')
    for idx in range(len(password)-1,0,-1):
        char = password[idx]
        newchar = next_char(char) 
        #print(f'Before Insert: {password} {newchar}')
        password = password[:idx]+newchar+password[idx+1:]
        #print(f'After Insert: {password}')
        if newchar != 'a':
            break
    return password

def is_valid(password):
    #print(f'is_valid({password})')
    valid = True;
    conditions = [False, True, False]
    # 3 consecutive letters
    letters = list(password)
    ints = [ord(char) for char in letters]
    for idx in range(len(ints)-2):
        if ints[idx+1]- ints[idx] == 1:
            if ints[idx+2]- ints[idx+1] == 1:
                conditions[0]=True
                break
    # banned letters i, o, l
    if any(char in password for char in ['i','o','l']):
        conditions[1] = False
    # two matched pairs
    count = 0;
    last = [];
    for idx in range(len(ints)-1):
        if ints[idx+1] == ints[idx]:
            if not idx in last:
                count+=1
                last = [idx,idx+1]
    if count >=2:
        conditions[2] = True
    #print(conditions)
    any_false = any(not condition for condition in conditions)
    if any_false:
        valid = False
    return valid

def part1():
    retval = 0;
    password = 'cqjxjnds'
    password = next_password(password)
    while not is_valid(password):
        password = next_password(password)
    
    return password

def part2():
    retval = 0;
    password = 'cqjxxyzz'
    password = next_password(password)
    while not is_valid(password):
        password = next_password(password)
    
    return password

if __name__ == "__main__":
    
    #print("Part 1")
    answer1 = part1()
    
    #print("Part 2")
    answer2 = part2()

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    