
# last 3 queue test

queue = [0,0,0]

for idx in range(10):
	for idx2 in range(3):
		queue.pop(0)
		queue.append(idx)
		print(queue)

		if all(x == queue[0] for x in queue):
			print('All Match')


def parse_input(data):
    rows = []
    lines = data.strip().split('\n')
    for line in lines:
        rows.append(tuple(map(int, list(line))))
    return tuple(rows)

def find_least_cost_path(grid):
    n = len(grid)
    # Initialize cost matrix
    cost = [[0 for _ in range(n)] for _ in range(n)]

    # Populate cost matrix
    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                cost[i][j] = grid[i][j]
            elif i == 0:
                cost[i][j] = cost[i][j - 1] + grid[i][j]
            elif j == 0:
                cost[i][j] = cost[i - 1][j] + grid[i][j]
            else:
                cost[i][j] = min(cost[i - 1][j], cost[i][j - 1]) + grid[i][j]

    # Backtrack to find the path (optional)
    path = []
    i, j = n - 1, n - 1
    while i > 0 or j > 0:
        path.append((i, j))
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        else:
            if cost[i - 1][j] < cost[i][j - 1]:
                i -= 1
            else:
                j -= 1
    path.append((0, 0))
    path.reverse()

    return cost[-1][-1], path  # Returns the total cost and the path

# Example usage
data = "2413432311323\n3215453535623\n3255245654254\n3446585845452\n4546657867536\n1438598798454\n4457876987766\n3637877979653\n4654967986887\n4564679986453\n1224686865563\n2546548887735\n4322674655533"
grid = parse_input(data)
least_cost, path = find_least_cost_path(grid)
print("Least cost:", least_cost)
print("Path:", path)