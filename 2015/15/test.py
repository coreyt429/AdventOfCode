def find_recipe(a, b=()):
    print(f'find_recipe({a}, {b})')
    if len(b) < len(a):
        q = sum(b)
        for i in range(100 - q, 0, -1):
            tmpList = list(b)
            tmpList.append(i)
            find_recipe(a, tuple(tmpList))
    elif sum(b) == 100:
        print(f"Combination that sums to 100: {b}")

a = tuple([1, 2, 3])
find_recipe(a)
