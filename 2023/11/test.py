import copy

test1 = []
test2 = ['bob', 'fred']
test1.append(test2)
test1.append(test2)
test1.append(test2)

# Create a deep copy of test1
test1copy = copy.deepcopy(test1)

print(f'Test1: {test1}')
print(f'Test2: {test2}')

# Modify an element in the copied list
test1copy[0][0] = 'wilma'
print(f'Test1: {test1}')
print(f'Test1copy: {test1copy}')
print(f'Test2: {test2}')
