def rotate_cw(myMap):
    retval = []
    for col in range(len(myMap[0])):  # iterate over the number of rows in the original map
        new_col = []
        for row in range(len(myMap)):  # iterate over the number of cols in the original map
            new_col.append(myMap[len(myMap) - row - 1][col])  # append elements in a clockwise manner
        retval.append(new_col)
    return retval

def print_map(myMap,label):
    print(f'{label}:')
    for line in myMap:
        print(''.join(line))
    print()

def transpose(matrix):
    return list(map("".join, zip(*matrix)))

def rotate():
    global reflector
    reflector = tuple(row[::-1] for row in reflector)

thisMap = [
['1','2','3'],
['4','5','6'],
['7','8','9']
]

thatMap = rotate_cw(thisMap)

print_map(thisMap,'This')
print_map(thatMap,'That')


print_map(thisMap,'This')
for idx in range(1,5):
    thisMap = transpose(thisMap)
    print_map(thisMap,f'Transpose {idx}')

thisMap = [
['1','2','3'],
['4','5','6'],
['7','8','9']
]

reflector = tuple(row for row in thisMap)
print_map(reflector,'This')
for idx in range(1,5):
    rotate()
    print_map(reflector,f'Rotate {idx}')