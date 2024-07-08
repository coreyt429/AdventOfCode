import json

def day12():
    def sum_numbers(obj):
        if type(obj) == type(dict()):
            if "red" in obj.values():
                return 0
            return sum(map(sum_numbers, obj.values()))

        if type(obj) == type(list()):
            return sum(map(sum_numbers, obj))

        if type(obj) == type(0):
            return obj

        return 0

    data = json.loads(open('input.txt', 'r').read())
    return sum_numbers(data)

print(day12())

from json import loads

def n(j):
    print(f'n({j})')
    if type(j) == int:
        return j
    if type(j) == list:
        return sum([n(j) for j in j])
    if type(j) != dict:
        return 0
    if 'red' in j.values():
        return 0
    return n(list(j.values()))

print(n(loads(open('input.txt', 'r').read())))