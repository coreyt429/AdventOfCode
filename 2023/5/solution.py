"""
Advent Of Code 2023 day 5

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def parse_input(data):
    """
    parse input
    """
    almanac = {}
    data_list = [section.split(':') for section in data.split('\n\n')]
    for section in data_list:
        almanac[section[0].replace(' map', '')] = [
            line.split(' ') for line in section[1].strip().split('\n')
        ]
    # convert to integers
    for key, value in almanac.items():
        almanac[key] = [[int(num) for num in sublist] for sublist in value]
    return almanac

def check_map(seed, conversion_map):
    """
    simple brute force method for part1, takes too long for part2
    """
    for line in conversion_map:
        if line[1] <= seed < (line[1] + line[2]):
            return line[0] + (seed - line[1])
    return seed

def conversion_map_to_range(conversion_map):
    """
    Convert the input conversion map into a nested list where each item is a
    list of start, end, and amount to offset if matched, return sorted nested list
    For instance, [50, 98, 2] becomes [98, 99, -48]
    """
    conversion_list = []
    for line in conversion_map:
        conversion_list.append([line[1], (line[1] + line[2] - 1), (line[0] - line[1])])
    return sorted(conversion_list, key=lambda x: x[0])

def convert_seed_range_list(seed_range, conversion_range):
    """
    For part 2, take the seed_range and convert it to a list of ranges based
    on the conversion_range and return sorted nested list
    """
    seed_range_list = []
    curr_value = seed_range[0]
    for curr_range in conversion_range:
        # If the first entry in conversion_range is higher than lowest seed,
        # add range until that point
        if curr_value < curr_range[0]:
            seed_range_list.append([curr_value, (curr_range[0] - 1)])
            curr_value = curr_range[0]
        # If between the current conversion range, add the range,
        # unless we are at the end of the seed range
        if curr_range[0] <= curr_value <= curr_range[1]:
            # Set max value to seed range end if conversion range is higher than seed range
            max_value = curr_range[1] if not seed_range[1] <= curr_range[1] else seed_range[1]
            seed_range_list.append(
                [(curr_value + curr_range[2]), (max_value + curr_range[2])]
            )
            curr_value = max_value + 1
        if curr_value - 1 == seed_range[1]:  # If we've hit the end of the seed range, break
            break
    # If we did not hit the end of the seed range, add the rest of the range
    if curr_value < seed_range[1]:
        seed_range_list.append([curr_value, seed_range[1]])
    return sorted(seed_range_list, key=lambda x: x[0])

def part1(parsed_data):
    """
    solve part 1
    """
    minimum = None
    for seed in parsed_data['seeds'][0]:
        current_id = seed
        for conversion_map in parsed_data.keys():
            if conversion_map != 'seeds':
                current_id = check_map(current_id, parsed_data[conversion_map])
        #print(f"Seed {seed} has a location number of {current_id}")
        if minimum is None or int(current_id) < minimum:
            minimum = int(current_id)
    return minimum

def part2(parsed_data):
    """
    solve part 2
    """
    # init retval
    minimum = None
    # extract seeds
    seeds = parsed_data['seeds'][0]
    # build seed pairs
    seed_pairs = [[seeds[i], (seeds[i] + seeds[i + 1] - 1)] for i in range(0, len(seeds), 2)]
    # get conversion_map names
    conversion_maps = [
        conversion_map for conversion_map in parsed_data.keys() if conversion_map != 'seeds'
    ]
    conversion_range_dict = {}
    # Convert the conversion maps into a dict of conversion ranges based on the map
    for conversion_map in conversion_maps:
        conversion_range_dict[conversion_map] = conversion_map_to_range(parsed_data[conversion_map])
    for seed_range in seed_pairs:
        # Convert the first seed pair into a nested list so the future loops will function properly
        curr_seed_range = [seed_range.copy()]
        for curr_conv_map in conversion_range_dict.values():
            curr_output_list = []
            for entry in curr_seed_range:
                # Output the new range for each seed range supplied
                output_list = convert_seed_range_list(entry, curr_conv_map)
                curr_output_list.append(output_list)
            # Make sure output is only a single nested list sorted
            curr_output_list = [item for sublist in curr_output_list for item in sublist]
            curr_output_list = sorted(curr_output_list, key=lambda x: x[0])
            # Set the curr seed range to the output list and run through the next conversion map
            curr_seed_range = curr_output_list.copy()
        #print(f"The lowest of seed range {seed_range} is {curr_seed_range[0][0]}")

        if minimum is None or curr_seed_range[0][0] < minimum:
            minimum = curr_seed_range[0][0]

    return minimum

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    data = parse_input(input_value)
    if part == 1:
        return part1(data)
    return part2(data)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2023,5)
    input_text = my_aoc.load_text()
    #print(input_text)
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
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
