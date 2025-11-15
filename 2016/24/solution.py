"""
Advent Of Code 2016 day 24

This one was a learning experience.

BFS, DFS, and Dijkstra usually get me through the path finding puzzles, but I was
struggling with the size of this search space.

So I had to learn A* and piece together a hybrid solution.

I use A* to map the shortest path from each node to all other nodes

Then fed that graph data into Dijkstra to get the shortest path to hit
all nodes.

This approach worked for part 2 as well, though I did need to add loop detection
in part 2.


"""

# import system modules
import time
import re
from heapq import heappush, heappop
from queue import PriorityQueue
from colorama import init, Fore, Style

# import my modules
import aoc  # pylint: disable=import-error

# static X/Y variables for coordinate tuples
X = 0
Y = 1


class Node:
    """
    Node class for scoring positions
    """

    def __init__(self, position, g_score, h_score, parent=None):
        """
        Init node
        """
        self.position = position
        self.g_score = g_score
        self.h_score = h_score
        self.f_score = g_score + h_score
        self.parent = parent

    def __gt__(self, other):
        """
        Node greater than
        """
        return self.f_score > other.f_score

    def __lt__(self, other):
        """
        Node less than
        """
        return self.f_score < other.f_score


def get_neighbors(position, maze):
    """
    function to find neighbors.

    """
    row, col = position
    neighbors = []
    for delta_row, delta_col in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_row, new_col = row + delta_row, col + delta_col
        if (
            0 <= new_row < len(maze)
            and 0 <= new_col < len(maze[0])
            and maze[new_row][new_col] != "#"
        ):
            neighbors.append((new_row, new_col))
    return neighbors


def a_star(start, goal, maze, heuristics):
    """
    Function to execute A* algorithm to detect shortest path between each pair
    """
    # set start_node  (position, g_score, h_score)
    start_node = Node(heuristics[start]["pos"], 0, heuristics[start]["distances"][goal])
    # initialize PriorityQueue
    open_set = PriorityQueue()
    # add start_node to priority_queue (f_score, node)
    open_set.put((start_node.f_score, start_node))
    # initialize closed set
    closed_set = set()

    # process open set
    while not open_set.empty():
        # get current node
        current_node = open_set.get()[1]

        # are we at the goal?
        if current_node.position == heuristics[goal]["pos"]:
            path = []
            # start at current node
            while current_node:
                # add position to path
                path.append(current_node.position)
                # move to parent
                current_node = current_node.parent
            # return reverse path
            return path[::-1]

        # add to closed set
        closed_set.add(current_node.position)
        # get neighbors
        for neighbor_pos in get_neighbors(current_node.position, maze):
            # skip if already closed
            if neighbor_pos in closed_set:
                continue
            # Set neighbor node
            neighbor_node = Node(
                neighbor_pos,
                current_node.g_score + 1,
                manhattan_distance(neighbor_pos, heuristics[goal]["pos"]),
                current_node,
            )
            # if not already in open_set, add it
            if (neighbor_node.f_score, neighbor_node) not in open_set.queue:
                open_set.put((neighbor_node.f_score, neighbor_node))

    return None  # No path found


def manhattan_distance(start, goal):
    """
    Function to calculate manhattan distance between two points
    """
    return abs(start[X] - goal[X]) + abs(start[Y] - goal[Y])


init()  # Initialize colorama


def print_map(maze, total_path):
    """
    Function to print our map
    """
    # colors for paths
    colors = [
        Fore.RED,
        Fore.GREEN,
        Fore.YELLOW,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.RED,
        Fore.GREEN,
        Fore.YELLOW,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.CYAN,
    ]
    # walk rows
    for row, line in enumerate(maze):
        print_line = ""
        # walk line
        for col, char in enumerate(line):
            # if this position is in a path, colorize it
            for idx, path in enumerate(total_path):
                if (row, col) in path and not char.isdigit():
                    char = colors[idx] + "*" + Style.RESET_ALL
                    break
            # replace '.'  with ' ' for clarity
            if char == ".":
                char = " "
            print_line += char
        # print map line
        print(print_line)


def dijkstra(graph, start_node, part):
    """
    Functon to implement dijkstra to find the shortest path through our points
    """
    # initialize heap with start node
    heap = []
    # steps, node, path
    heappush(heap, (0, start_node, ("0")))
    # save nodes for easy access
    nodes = graph.keys()
    # init min_steps and min_path
    min_steps = float("infinity")
    min_path = None
    # process heap
    while heap:
        # get next node
        steps, current_node, visited = heappop(heap)
        # too long?  drop it
        if steps > min_steps:
            continue
        # part 1, just look for all nodes
        if part == 1:
            if sorted(visited) == sorted(nodes):
                # set min_steps and min_path if this path is shorter than previous
                if steps < min_steps:
                    min_steps = steps
                    min_path = visited
                continue
        else:
            # loop detection
            # if we visited any node more than twice, then the return path is going
            # to be longer than just backtracking the original shortest path
            # through all nodes
            if any(visited.count(node) > 2 for node in set(visited)):
                continue
            # starts and ends at '0''
            if visited[0] == "0" and visited[-1] == "0":
                if set(nodes).issubset(set(visited)):
                    if steps < min_steps:
                        min_steps = steps
                        min_path = visited
                    continue
        # add the path to each node from current node
        for next_node in graph[current_node]:
            heappush(
                heap,
                (
                    steps + graph[current_node][next_node],
                    next_node,
                    tuple(list(visited) + [next_node]),
                ),
            )
        # return minimums
    return min_steps, min_path


def solve(maze, part):
    """
    Function to solve puzzle
    """
    # get numbers from input
    numbers = re.findall(r"\d", "\n".join(maze))
    # heuristics data structure
    heuristics = {}
    # get number positions
    for number in numbers:
        heuristics[number] = {"pos": (0, 0), "distances": {}, "paths": {}}
        for idx, line in enumerate(maze):
            num_loc = line.find(number)
            if num_loc >= 0:
                heuristics[number]["pos"] = (idx, num_loc)
    # get manhattan distance to other numbers
    for number in numbers:
        for target in numbers:
            heuristics[number]["distances"][target] = manhattan_distance(
                heuristics[number]["pos"], heuristics[target]["pos"]
            )
    numbers = sorted(heuristics.keys())
    total_path = []
    # use A* to get the graph data for dijkstra
    graph = {}
    # walk numbers
    for number in numbers:
        graph[number] = {}
        # walk numbers again
        for target in numbers:
            # if not self
            if number != target:
                # save A* distance
                heuristics[number]["paths"][target] = a_star(
                    number, target, maze, heuristics
                )
                # add to graph
                graph[number][target] = len(heuristics[number]["paths"][target])
    # get shortest path through graph
    steps, path = dijkstra(graph, "0", part)
    total_path = []
    # build map path from graph path
    for idx, node_a in enumerate(path):
        if idx + 1 < len(path):
            node_b = path[idx + 1]
            total_path.append(heuristics[node_a]["paths"][node_b])
    # print map, its pretty :)
    # print_map(maze, total_path)

    # init steps to get actual path step length
    steps = []
    # walk paths in total_path
    for path in total_path:
        # add path to steps, skip the first node in each path
        # it is either the start node, or the last node in the
        # previous path
        steps = steps + path[1:]
    # return answer
    return len(steps)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016, 24)
    # input_text = my_aoc.load_text()
    # print(input_text)
    my_input_lines = my_aoc.load_lines()
    # print(input_lines)
    SAMPLE_TEXT = """###########
#0.1.....2#
#.#######.#
#4.......3#
###########"""
    # my_input_lines = SAMPLE_TEXT.split('\n')

    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](my_input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
