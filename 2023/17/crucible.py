"""
Advent of Code 2023 Day 17

This script implements a modified Dijkstra's algorithm with minimum and maximum 
forward paths.
"""

import sys
from heapq import heappop, heappush

def next_position(my_map, current_position, new_direction):
    """
    Function to get next position in a direction.

    parameters: 
        my_map: dict heatmap of city blocks
        current_position: tuple (r,c) coordinates
        new_direction: str 'N', 'S', 'E', 'W'

    returns:
        next_pos: tuple (r,c) coordinates
    """
    next_pos = None
    # up
    if new_direction == 'N':
        if current_position[0] != 0:
            next_pos = (current_position[0] - 1, current_position[1])
    # down
    elif new_direction == 'S':
        if current_position[0] < len(my_map) - 1:
            next_pos = (current_position[0] + 1, current_position[1])
    # left
    elif new_direction == 'W':
        if current_position[1] != 0:
            next_pos = (current_position[0], current_position[1] - 1)
    # right
    elif new_direction == 'E':
        if current_position[1] < len(my_map[0]) - 1:
            next_pos = (current_position[0], current_position[1] + 1)
    return next_pos

# DIRECTION_MAP dict of possible directions based on ingress direction
DIRECTION_MAP = {
    'N': {'L': 'W', 'R': 'E', 'F': 'N'},
    'S': {'L': 'E', 'R': 'W', 'F': 'S'},
    'E': {'L': 'N', 'R': 'S', 'F': 'E'},
    'W': {'L': 'S', 'R': 'N', 'F': 'W'}
}

def dijkstra(start_pos, min_forward, max_forward):
    """
    modified dijkstra algorithm

    parameters:
        start_pos: tuple (r,c) coordinagtes
        min_forward: int minimum forward movements allowed per line
        max_forward: int maximum forward movements allowed per line

    returns:
        heat_loss: dict heat_loss scores
        previous_blocks: dict mapping of blocks to their predecessor in this path
    """
    #print(f"dijkstra(CITY_MAP, {start_pos}, {min_forward}, {max_forward})")
    heap = [
        (0, start_pos, 0, 'S'),
        (0, start_pos, 0, 'E')
    ]  # (cost, position, forward movements, ingress direction)

    previous_nodes = {}
    heat_loss = {}
    heat_loss[(start_pos, 0, 'S')] = 0
    heat_loss[(start_pos, 0, 'E')] = 0

    while heap:
        fields = ['heat_loss', 'position', 'forward_movements', 'direction']
        current = dict(zip(fields, heappop(heap)))
        current_position_key = (
            current['position'],
            current['forward_movements'],
            current['direction']
        )

        if current_position_key not in previous_nodes:
            previous_nodes[current_position_key] = None

        # Early termination if we've reached the bottom-right corner
        if current['position'] == (len(CITY_MAP) - 1, len(CITY_MAP[0]) - 1):
            break

        for movement in 'LRF':
            new = {}
            new['direction'] = DIRECTION_MAP[current['direction']][movement]
            new['position'] = next_position(CITY_MAP, current['position'], new['direction'])
            new['forward_movements'] = current['forward_movements'] + 1 if movement == 'F' else 1

            if new['position']:
                row, col = new['position']
                new['heat_loss'] = current['heat_loss'] + CITY_MAP[row][col]

                # Check if this movement results in a lower heat loss
                if new['heat_loss'] < heat_loss.get(
                        (new['position'], new['forward_movements'], new['direction']),
                        float('infinity')
                    ):
                    # Skip forward movement if it exceeds max_forward
                    if movement == 'F' and new['forward_movements'] > max_forward:
                        continue
                    # Skip non-forward movement if not enough forward moves
                    if movement != 'F' and current['forward_movements'] < min_forward:
                        continue

                    heat_loss[(
                        new['position'],
                        new['forward_movements'],
                        new['direction']
                        )] = new['heat_loss']
                    new_position_key = (new['position'], new['forward_movements'], new['direction'])
                    previous_nodes[new_position_key] = current_position_key
                    heappush(
                        heap,
                        (
                            new['heat_loss'],
                            new['position'],
                            new['forward_movements'],
                            new['direction']
                        )
                    )

    return heat_loss, previous_nodes

def reconstruct_path(previous_nodes, min_heat_loss_key):
    """
    function to build the path from pervious_nodes data
    
    parameters:
        previous_nodes: dict mapping of previous nodes
        min_heat_loss_key: key of the record we want to backtrack from

    returns:
        path: list of nodes in order
    """
    path = []
    current_node = min_heat_loss_key
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes.get(current_node)
        #print(f"current_node: {current_node}")

    path.reverse()  # Reverse the path to get it from start to end
    return path

def print_map(grid,path):
    """
    function to visualize map and path

    parameters:
        grid: list of list heatmap of blocks
        path: list of nodes in path
    """
    rows = len(grid)
    cols = len(grid[0])
    grid_with_path = [[' ' for _ in range(cols)] for _ in range(rows)]
    symbol = {
        'N': '^',
        'S': 'v',
        'E': '>',
        'W': '<'

    }
    for row in range(rows):
        for col in range(cols):
            grid_with_path[row][col] = str(grid[row][col])

    for (row, col), _, direction in path:
        grid_with_path[row][col] = symbol[direction]

    for row in grid_with_path:
        print(''.join(row))

if __name__ == "__main__":
    # Load map as list of lists
    with open(sys.argv[1], 'r', encoding='utf-8') as file:
        CITY_MAP = [[int(char) for char in line] for line in file.read().splitlines()]
    # Start at top left
    start = (0, 0)
    # End at bottom right
    end = (len(CITY_MAP) - 1, len(CITY_MAP[0]) - 1)

    parts = {
        'part1': (0,3),
        'part2': (4,10)

    }

    for part, (min_moves, max_moves) in parts.items():
        print(f"{part}: {min_moves}, {max_moves}")
        heat_loss_results, previous_blocks = dijkstra(start, min_moves, max_moves)
        MIN_HEAT_LOSS_KEY = None
        for key, path_heat_loss in heat_loss_results.items():
            (position, forward_movement_count, ingress_direction) = key
            # ((12, 11), 0, 'S'): 131

            if position == end:
                if not MIN_HEAT_LOSS_KEY:
                    MIN_HEAT_LOSS_KEY = key
                elif path_heat_loss < heat_loss_results[MIN_HEAT_LOSS_KEY]:
                    MIN_HEAT_LOSS_KEY = key

        if MIN_HEAT_LOSS_KEY:
            print(f"Heat loss to {end}: {heat_loss_results[MIN_HEAT_LOSS_KEY]}")
        else:
            print(f"No path found to {end}")

        #my_path = reconstruct_path(previous_blocks, MIN_HEAT_LOSS_KEY)
        #print(f"Path: {my_path}")
        #print_map(CITY_MAP,my_path)
