"""
AdventOfCode 2016 day 5
"""
import hashlib

def md5_checksum(input_string):
    """
    returns md5sum of input_string
    """
    md5_obj = hashlib.md5()
    md5_obj.update(input_string.encode('utf-8'))
    return md5_obj.hexdigest()


if __name__ == "__main__":
    DOOR_ID = 'abbhdwsy'
    counter = 0 # pylint: disable=invalid-name
    password = '' # pylint: disable=invalid-name
    password_list = ['-']*8
    while '-' in password_list:
        if counter != 0:
            counter +=1
        md5_hash = md5_checksum(DOOR_ID + str(counter)) # pylint: disable=invalid-name
        while not md5_hash.startswith('00000'):
            counter += 1
            md5_hash = md5_checksum(DOOR_ID + str(counter)) # pylint: disable=invalid-name
        if(len(password)) < 8:
            password += md5_hash[5]
        if md5_hash[5] in '01234567':
            if password_list[int(md5_hash[5])] == '-':
                password_list[int(md5_hash[5])] = md5_hash[6]

    print(f"Part 1: {password}")
    print(f"Part 2: {''.join(password_list)}")
