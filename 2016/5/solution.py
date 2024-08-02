"""
Advent Of Code 2016 day 5

Simple refactor, already ran ok,  it takes 39 seconds to answer both parts though.
Could we make it faster?
"""
# import system modules
import time
import hashlib

# import my modules
import aoc # pylint: disable=import-error

def md5_checksum(input_string):
    """
    returns md5sum of input_string
    """
    md5_obj = hashlib.md5()
    md5_obj.update(input_string.encode('utf-8'))
    return md5_obj.hexdigest()

def solve(door_id, part):
    """
    Function to solve puzzle
    """
    # part 2 gets answered on the first pass, so just return the answer
    if part == 2:
        return answer[2]
    counter = 0
    password = ''
    password_list = ['-']*8
    while '-' in password_list:
        if counter != 0:
            counter +=1
        md5_hash = md5_checksum(door_id + str(counter))
        while not md5_hash.startswith('00000'):
            counter += 1
            md5_hash = md5_checksum(door_id + str(counter))
        if(len(password)) < 8:
            password += md5_hash[5]
        if md5_hash[5] in '01234567':
            if password_list[int(md5_hash[5])] == '-':
                password_list[int(md5_hash[5])] = md5_hash[6]
    # store answer for part 2
    answer[2] = ''.join(password_list)
    return password

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016,5)
    input_text = my_aoc.load_text()
    print(input_text)
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
        1: solve,
        2: solve
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
