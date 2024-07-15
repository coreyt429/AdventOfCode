"""
Advent Of Code YEAR day DAY

"""
import aoc # pylint: disable=import-error


if __name__ == "__main__":
	my_aoc = aoc.AdventOfCode(YEAR,DAY)
	lines = my_aoc.load_lines()
	print(lines)
