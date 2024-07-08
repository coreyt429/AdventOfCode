import sys

def parse_input(data):
    almanac = {}
    data_list = [section.split(':') for section in data.split('\n\n')]
    for section in data_list:
        almanac[section[0].replace(' map', '')] = [line.split(' ') for line in section[1].strip().split('\n')]
    # convert to integers
    for key in almanac.keys():
        almanac[key] = [[int(num) for num in sublist] for sublist in almanac[key]]
    return almanac

def check_map(seed,cm): # simple brute force method for part1, takes too long for part2
    for line in cm:
        if seed >= line[1] and seed < (line[1] + line[2]):
            return (line[0] + (seed - line[1]))
    return seed

def conversion_map_to_range(conversion_map):
    # Convert the input conversion map into a nested list where each item is a list of start, end, and amount to offset if matched, return sorted nested list
    # For instance, [50, 98, 2] becomes [98, 99, -48]
    conversion_list = []
    for line in conversion_map:
        conversion_list.append([line[1], (line[1] + line[2] - 1), (line[0] - line[1])])
    return sorted(conversion_list, key=lambda x: x[0])

def convert_seed_range_list(seed_range, conversion_range):
    #print(f'convert_seed_range_list({seed_range}, {conversion_range})')
    # For part 2, take the seed_range and convert it to a list of ranges based on the conversion_range and return sorted nested list
    seed_range_list = []
    curr_value = seed_range[0]
    for i in range(len(conversion_range)):
        if curr_value < conversion_range[i][0]:  # If the first entry in conversion_range is higher than lowest seed, add range until that point
            seed_range_list.append([curr_value, (conversion_range[i][0] - 1)])
            curr_value = conversion_range[i][0]
        if curr_value >= conversion_range[i][0] and curr_value <= conversion_range[i][1]:  # If between the current conversion range, add the range, unless we are at the end of the seed range
            max_value = conversion_range[i][1] if not seed_range[1] <= conversion_range[i][1] else seed_range[1]  # Set max value to seed range end if conversion range is higher than seed range
            seed_range_list.append([(curr_value + conversion_range[i][2]), (max_value + conversion_range[i][2])])
            curr_value = max_value + 1
        if curr_value - 1 == seed_range[1]:  # If we've hit the end of the seed range, break
            break
    if curr_value < seed_range[1]:  # If we did not hit the end of the seed range, add the rest of the range
        seed_range_list.append([curr_value, seed_range[1]])
    return sorted(seed_range_list, key=lambda x: x[0])

def part1(parsed_data):
    minimum = None
    for seed in parsed_data['seeds'][0]:
        currentId = seed
        for cm in parsed_data.keys():
            if cm != 'seeds':
                currentId = check_map(currentId, parsed_data[cm])
        print(f"Seed {seed} has a location number of {currentId}")
        if minimum is None or int(currentId) < minimum:
            minimum = int(currentId)
    return minimum

def part2(parsed_data):
    # init retval
    minimum = None
    # extract seeds
    seeds = parsed_data['seeds'][0]
    # build seed pairs
    seed_pairs = [[seeds[i], (seeds[i] + seeds[i + 1] - 1)] for i in range(0, len(seeds), 2)]
    # get conversion_map names
    conversion_maps = [cm for cm in parsed_data.keys() if cm != 'seeds']
    conversion_range_dict = {}
    for cm in conversion_maps:  # Convert the conversion maps into a dict of conversion ranges based on the map
        conversion_range_dict[cm] = conversion_map_to_range(parsed_data[cm])
    for seed_range in seed_pairs:
        curr_seed_range = [seed_range.copy()]  # Convert the first seed pair into a nested list so the future loops will function properly
        for curr_conv_map in conversion_range_dict.keys():
            curr_output_list = []
            for entry in curr_seed_range:
                output_list = convert_seed_range_list(entry, conversion_range_dict[curr_conv_map])  # Output the new range for each seed range supplied
                curr_output_list.append(output_list)
            curr_output_list = [item for sublist in curr_output_list for item in sublist]  # Make sure output is only a single nested list sorted
            curr_output_list = sorted(curr_output_list, key=lambda x: x[0])
            curr_seed_range = curr_output_list.copy()  # Set the curr seed range to the output list and run through the next conversion map
        print(f"The lowest of seed range {seed_range} is {curr_seed_range[0][0]}")

        if minimum is None or curr_seed_range[0][0] < minimum:
            minimum = curr_seed_range[0][0]

    return minimum

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())

    print('Part 1:')
    answer1 = part1(parsed_data)
    print('Part 2:')
    answer2 = part2(parsed_data)

    print(f"Part 1: {answer1}")
    print(f"Part 2: {answer2}")
    