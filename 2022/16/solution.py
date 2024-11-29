"""
Advent Of Code 2022 day 16

This one should have been more fun, and it just wasn't.

Part 1 was pretty standard shortest path.  Part 2, was trickier, and
ran well with the test data.  The puzzle data was just a lot of combinations
There is definitely room for improvement here, but my solution gets the right
answer, so moving on.  I'll mark it to revisit later.

It was at least a learning point.  The floyd_warshall distances were faster
than the shortest path solution I had initially used, so that will be good
to keep for future reference.

The scratchpad has a faster solution from u/chris_wojcik that I used to
verify the answer.  There are probably some interesting bits in there that
could speed up my solution.  Oddly, we both get the same answer, with seemingly
different paths.  

"""
# import system modules
import time
import re
from heapq import heappop, heappush
# from collections import deque
from functools import lru_cache
import itertools

# import my modules
import aoc # pylint: disable=import-error

valves = {}

def parse_input(lines):
    """Function to parse input data"""
    regex = r'Valve (\w\w) has flow rate=(\d+); tunnels* leads* to valves* (.*)'
    pattern_input = re.compile(regex)
    for line in lines:
        match = pattern_input.match(line)
        if match:
            valves[match.group(1)] = {
                "flow_rate": int(match.group(2)),
                "tunnels": match.group(3).split(', ')
            }
    set_valve_distances()
    return valves

def set_valve_distances():
    """Function to set valve distances"""
    # get valve names
    valve_names = list(sorted(valves.keys()))
    # init graph
    graph = [[float('infinity') for _ in range(len(valve_names))] for _ in range(len(valve_names))]
    # populate graph with known values
    for idx, valve_id in enumerate(valve_names):
        for idx2, next_valve_id in enumerate(valve_names):
            if valve_id == next_valve_id:
                graph[idx][idx2] = 0
            if next_valve_id in valves[valve_id]['tunnels']:
                graph[idx][idx2] = 1
    # for row in graph:
    #     print(row)
    # floyd warshall the graph
    graph = floyd_warshall(graph)
    # for row in graph:
    #     print(row)
    for idx, valve_id in enumerate(valve_names):
        valve = valves[valve_id]
        valve['distances'] = {}
        for idx2, next_valve_id in enumerate(valve_names):
            valve['distances'][next_valve_id] = graph[idx][idx2]

@lru_cache(maxsize=None)
def pressure_of_valve(valve, minute, time_limit):
    """Function to get pressure relief of a single valve"""
    return (time_limit - minute - 1) * valves[valve]['flow_rate']

@lru_cache(maxsize=None)
def calculate_pressure(history, time_limit):
    """Function to calculate pressure relief from valve history"""
    pressure = 0
    for valve, minute in history:
        # subtract additional minute
        pressure += pressure_of_valve(valve, minute, time_limit)
    return pressure

def floyd_warshall(graph):
    """Function to set floyd warshall distances in a graph"""
    v_size = len(graph)
    while float('infinity') in graph[0]:
        for i in range(v_size):
            for j in range(v_size):
                for k in range(v_size):
                    graph[i][j] = min(graph[i][j], graph[i][k] + graph[k][j])
    return graph

@lru_cache(maxsize=None)
def potential_pressure(minutes, closed_valves, time_limit=30):
    """
    Calculate the potential maximum pressure relief given the current state.
    
    :param minutes: tuple(int), current time used by each worker.
    :param closed_valves: tuple(str), valves that are still closed.
    :param time_limit: int, maximum time limit for the operation.
    :param workers: int, number of workers available to open valves.
    :return: int, the potential maximum pressure relief.
    """
    # Get the flow rates for closed valves and sort them in descending order.
    sorted_valves = sorted(
        (valves[valve_id]["flow_rate"] for valve_id in closed_valves if valve_id != 'DONE'),
        reverse=True
    )
    # Allocate workers to maximize flow rates.
    total_potential_pressure = 0
    available_workers = list(minutes)
    for flow_rate in sorted_valves:
        # Find the worker who will finish first.
        available_workers.sort()
        worker_time = available_workers[0]

        # Check if this worker can turn on this valve before the time limit.
        if worker_time < time_limit:
            # Calculate the remaining time this valve can contribute pressure.
            remaining_time = time_limit - worker_time

            # Add to total potential pressure.
            total_potential_pressure += flow_rate * remaining_time

            # Update the worker's time after opening the valve.
            available_workers[0] += 2  # One minute to open the valve, and one to move to the valve
        else:
            # If no worker can open the valve in time, stop the allocation.
            break
    return total_potential_pressure

def mark_done(locations, minutes, time_limit):
    """Function to mark workers as done"""
    new_locations = list(locations)
    for idx, _ in enumerate(new_locations):
        if minutes[idx] >= time_limit:
            new_locations[idx] = 'DONE'
    return tuple(new_locations)

def max_pressure_relief(working_valves, time_limit=30, workers=1):
    """Function to calculate maximum pressure relief"""
    heap = []
    # We are starting in AA which doesn't have a useable valve (flow rate=0)
    # so let's not put AA on the heap, but rather all of the working valves we can get to in
    # one minute from AA
    # since AA has a flow rate of 0, lets just pretend it is already open
    heappush(
        heap,
        (
            0,
            tuple(0 for _ in range(workers)),
            tuple('AA' for _ in range(workers)),
            ('AA',),
            tuple((key for key in working_valves.keys() if key not in ('AA',))),
            ()
        )
    )
    stats = {
        "pressure": 0,
        "history": tuple(),
        "seen": set()
    }
    while heap:
        current = heappop(heap)
        if current[1:4] in stats['seen']:
            continue
        stats['seen'].add(current[1:4])
        current = {
            "minutes": current[1],
            "locations": current[2],
            "open_valves": current[3],
            "closed_valves": current[4],
            "history": current[5]
        }
        # timeout at time_limit minutes, and point to DONE
        if any(minute >= time_limit for minute in current['minutes']):
            current['locations'] = mark_done(current['locations'], current['minutes'], time_limit)
        pressure = calculate_pressure(current['history'], time_limit)
        if pressure > stats['pressure']:
            stats['pressure'] = pressure
            stats['history'] = current['history']
        elif (
            pressure + potential_pressure(current['minutes'], current['closed_valves'], time_limit)
            ) < stats['pressure']:
            continue

        # if all are done, stop processing this branch
        if all(
            location == 'DONE' for location in current['locations']
        ) or current['closed_valves'] == ('DONE',):
            continue

        # open valve if not already
        if any(location in current['closed_valves'] for location in current['locations']):
            new_data = {
                "open_valves": list(current['open_valves']),
                "closed_valves": list(current['closed_valves']),
                "history": list(current['history']),
                "minutes": list(current['minutes'])
            }
            for idx, location in enumerate(current['locations']):
                # don't open any more valves after we've reached time_limit
                if current['minutes'][idx] > time_limit or location == 'DONE':
                    continue
                if location in current['closed_valves']:
                    new_data['history'].append((location, current['minutes'][idx]))
                    new_data['minutes'][idx] += 1
                    new_data['open_valves'].append(location)
                    new_data['closed_valves'].remove(location)
            heappush(
                heap,
                (
                    (2 * time_limit) - sum(new_data['minutes']),
                    tuple(new_data['minutes']),
                    current['locations'],
                    tuple(new_data['open_valves']),
                    tuple(new_data['closed_valves']),
                    tuple(new_data['history'])
                )
            )
            # I don't think we will gain anything by entertaining the scenario where we
            # choose not to turn the valve on, so continue here
            continue
        # move to other tunnels
        next_hops = trim_next_hops(
            (working_valves[location]['next_hops'] for location in current['locations']),
            current['locations'], current['open_valves']
            )
        for next_locations in itertools.product(*next_hops):
            if len(next_locations) > 1 and next_locations[0] == next_locations[1]:
                # same location? skip
                continue
            new_data = {
                "minutes": add_travel_minutes(
                    current['minutes'],
                    current['locations'],
                    next_locations
                )
            }
            heappush(
                heap,
                (
                    (2 * time_limit) - sum(new_data['minutes']),
                    new_data['minutes'],
                    next_locations,
                    current['open_valves'],
                    current['closed_valves'],
                    current['history']
                )
            )
        # print(f"end of heap loop")
    return stats['pressure'], stats['history']

@lru_cache(maxsize=None)
def trim_next_hops(next_hops, locations, open_valves):
    """Function to trim invalid entries from next_hops"""
    # print(f"trim_next_hops({next_hops}, {locations}, {open_valves})")
    new_hops = []
    for hop_list in next_hops:
        new_hop_list = []
        for hop in hop_list:
            if hop not in locations and hop not in open_valves:
                if valves[hop]['flow_rate'] > 0:
                    new_hop_list.append(hop)
        new_hops.append(tuple(new_hop_list))
    return tuple(new_hops)

@lru_cache(maxsize=None)
def add_travel_minutes(minutes, locations, next_locations):
    """Function to add travel_minutes to minutes"""
    travel_minutes = calc_travel_minutes(locations, next_locations)
    return tuple((a or 0) + (b or 0) for a, b in zip(minutes, travel_minutes))

@lru_cache(maxsize=None)
def calc_travel_minutes(locations, next_locations):
    """Function to calculate travel_minutes based on location and next_location"""
    return tuple(
        shortest_path(
            location,
            next_location) for location, next_location in zip(locations, next_locations)
        )

@lru_cache(maxsize=None)
def shortest_path(start, goal):
    """Function to calculate shortest path between valves"""
    return valves[start]['distances'][goal]

@lru_cache(maxsize=None)
def get_ordered_next_hops(valve_id):
    """
    Get the next hops for a given valve, ordered by the corresponding distance.

    :param valve_id: The ID of the valve to query.
    :return: List of next hops ordered by distance.
    """
    # Check if the valve_id exists in the valves dictionary
    if valve_id not in valves:
        raise ValueError(f"Valve ID '{valve_id}' does not exist.")

    # Get the next_hops and distances for the specified valve
    valve = valves[valve_id]
    next_hops = valve.get('distances', {}).keys()
    distances = valve.get('distances', {})

    # Sort next_hops based on their distances
    ordered_next_hops = sorted(next_hops, key=lambda hop: distances.get(hop, float('inf')))
    ordered_next_hops = [hop for hop in ordered_next_hops if valves[hop]['flow_rate'] > 0]
    if valve_id in ordered_next_hops:
        ordered_next_hops.pop(ordered_next_hops.index(valve_id))
    return ordered_next_hops

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    time_limit=30
    workers=1
    if part == 2:
        time_limit=26
        workers=2
    for valve_id, valve in parse_input(input_value).items():
        valves[valve_id] =  valve
    working_valves = {}
    # get working valves
    for valve_id, valve in valves.items():
        if valve["flow_rate"] > 0 or valve_id == 'AA':
            working_valves[valve_id] = valve
            valve["next_hops"] = get_ordered_next_hops(valve_id)

    working_valves['DONE'] = {
        'next_hops': ['DONE']
    }
    # part 2
    # 2084 too low
    # 2122 too low
    # 2123 too low
    # 2167 not right
    # 2206 not right, but I keep getting this, must me some edge case I'm missing
    pressure, _ = max_pressure_relief(working_valves,time_limit=time_limit, workers=workers)
    return pressure

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022,16)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {
        1: 1,
        2: 2
    }
    # dict to store answers
    answer = {
        1: None,
        2: None
    }
    # correct answers once solved, to validate changes
    correct = {
        1: 1580,
        2: 2213
    }
    # dict to map functions
    funcs = {
        1: solve,
        2: solve
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
