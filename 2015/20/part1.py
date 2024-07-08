def part1_sieve(target):
    houses = [0] * (target // 10)
    for elf in range(1, target // 10):
        for house in range(elf, target // 10, elf):
            houses[house] += elf * 10
        if houses[elf] >= target:
            return elf

# Test the optimized function
target = 29000000
print(part1_sieve(target))