"""
AdventOfCode 2016 7
"""
import re
import sys

supernet_pattern = re.compile(r'(\[\w+\])')

def load_data(file_name):
    """
    load data from file_name
    """
    with open(file_name,'r',encoding='utf-8') as file:
        return list(file.read().rstrip().split('\n'))

def contains_abba(my_string):
    """
    Checks for abba pattern in string
    """
    for idx in range(len(my_string)-3):
        if my_string[idx] == my_string[idx+3] and my_string[idx+1] == my_string[idx+2] and my_string[idx] != my_string[idx+1]:
            return True
    return False

def contains_aba(my_string):
    """
    checks for aba patterns
    """
    abas = []
    retval = False
    for idx in range(len(my_string)-2):
        if my_string[idx] == my_string[idx+2] and  my_string[idx] != my_string[idx+1]:
            retval = True
            abas.append(my_string[idx:idx+3])
    return retval, abas

def contains_bab(my_string, aba):
    """
    contains reverse of aba
    """
    bab = aba[1]+aba[0]+aba[1]
    return bab in my_string

def supports_ssl(my_string):
    """
    check for ssl suport ABA outside [] and BAB inside []
    """
    supernets = supernet_pattern.findall(my_string)
    for supernet in supernets:
        my_string = my_string.replace(supernet,'-')

    has_aba, my_abas = contains_aba(my_string)
    if has_aba:
        for aba in my_abas:
            for supernet in supernets:
                if contains_bab(supernet,aba):
                    return True
    return False

def supports_tls(my_string):
    """
    check for tls support (abba outside of square brackets, but not inside)
    """
    for my_str in supernet_pattern.findall(my_string):
        if contains_abba(my_str):
            return False
    if contains_abba(my_string):
        return True
    return False

if __name__ == "__main__":
    lines = load_data(sys.argv[1])
    counter = {
        'p1': 0,
        'p2': 0
    }
    for line in lines:
        if supports_tls(line):
            counter['p1']+=1
        if supports_ssl(line):
            counter['p2']+=1
    print(f"Part 1: {counter['p1']}")
    print(f"Part 2: {counter['p2']}")
