def parse(filename):
    grid, start = {}, None
    for y, line in enumerate(open(filename).read().split("\n")):
        for x, c in enumerate(line):
            if c == "S":
                start = x + 1j * y
            grid[x + 1j * y] = c
    maxX, maxY = int(max(p.real for p in grid)), int(max(p.imag for p in grid))            
    return grid, start, maxX, maxY

def infinite_grid(grid, p, maxX, maxY):
    x = p.real % (maxX + 1)
    y = p.imag % (maxY + 1)
    return grid[x + y * 1j]

def generate_history(grid, start, maxX, maxY, steps):
    odds, evens, queue = set(), {start}, {start}
    n4 = lambda p: [p - 1j, p - 1, p + 1, p + 1j]
    odd_history, even_history = [0], [1]
    for i in range(1,steps+1):
        new_points = set()
        for p in queue:
            for n in [n for n in n4(p) if n not in evens and n not in odds]:
                if infinite_grid(grid, n, maxX, maxY) in ".S":
                    new_points.add(n)
        if i % 2:
            odds |= new_points
        else:
            evens |= new_points
        odd_history.append(len(odds))
        even_history.append(len(evens))
        queue = new_points
    return odd_history, even_history

def part1(grid, start, maxX, maxY):
    _, even_history = generate_history(grid, start, maxX, maxY, 64)
    print(even_history[-1])

def part2(grid, start, maxX, maxY):
    history, _ = generate_history(grid, start, maxX, maxY, 3*262+65)
    steps = 101150 # (26501365 - 65) // 262 
    a = history[2*262+65]
    b = history[2*262+65] - history[262+65]
    c = history[3*262+65] - 2*history[2*262+65] + history[262+65]
    print(a + b*(steps-2) + c*((steps-2)*(steps-1)//2))

grid, start, maxX, maxY = parse("input.txt")
print(grid)
print(start, maxX, maxY)
part1(grid, start, maxX, maxY)
part2(grid, start, maxX, maxY)
