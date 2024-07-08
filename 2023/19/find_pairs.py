def find_pairs(filename, target_sum):
    # Try opening with UTF-8, fallback to UTF-16 on failure
    try:
        file = open(filename, 'r', encoding='utf-8-sig')
    except UnicodeDecodeError:
        file = open(filename, 'r', encoding='utf-16')

    with file:
        # Skip the header
        next(file)
        next(file)

        # Extract numbers from the file, handling potential formatting issues
        numbers = []
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 3 and parts[2].isdigit():
                numbers.append(int(parts[2]))

    # Use a set to store numbers and check for pairs
    seen = set()
    pairs = []
    for number in numbers:
        complement = target_sum - number
        if complement in seen:
            pairs.append((complement, number))
        seen.add(number)

    print(seen)
    return pairs

# Path to the data file
filename = 'data.txt'

# The target sum to find
target_sum = 126721490376

# Find pairs
pairs = find_pairs(filename, target_sum)

# Print the pairs
for pair in pairs:
    print(pair)
