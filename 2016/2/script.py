import sys

KEYPAD = {
	(0,0): '1',
	(0,1): '2',
	(0,2): '3',
	(1,0): '4',
	(1,1): '5',
	(1,2): '6',
	(2,0): '7',
	(2,1): '8',
	(2,2): '9'
}

"""
 01234 
0  1
1 234
256789
3 ABC
4  D
"""

KEYPAD2 = {
	(0,2): '1',
	(1,1): '2',
	(1,2): '3',
	(1,3): '4',
	(2,0): '5',
	(2,1): '6',
	(2,2): '7',
	(2,3): '8',
	(2,4): '9',
	(3,1): 'A',
	(3,2): 'B',
	(3,3): 'C',
	(4,2): 'D'
}

MOVEMENTS = {
	'U': (-1,0),
	'D': (1,0),
	'L': (0,-1),
	'R': (0,1)
}
def load_instructions(file_name):
	with open(file_name,'r',encoding='utf-8') as file:
		return [line for line in file.read().rstrip().split("\n")]

def next_key(keypad, current_key_loc, new_move_direction):
	new_key_loc = list(current_key_loc)
	for coord in (0,1):
		new_key_loc[coord] += MOVEMENTS[new_move_direction][coord]
	if tuple(new_key_loc) in keypad:
		return new_key_loc
	else:
		return current_key

if __name__ == '__main__':
	current_key = [1,1]
	code_instructions = load_instructions(sys.argv[1])
	bathroom_code = '';
	for current_instruction in code_instructions:
		for current_movement in current_instruction:
			current_key = next_key(KEYPAD,current_key,current_movement)
		bathroom_code += KEYPAD[tuple(current_key)]
	print(f"Part 1: {bathroom_code}")
	"""
	Part 2 isn't going to reuse much from above :(
	"""
	current_key = [2,0]
	bathroom_code = '';
	for current_instruction in code_instructions:
		for current_movement in current_instruction:
			current_key = next_key(KEYPAD2,current_key,current_movement)
		bathroom_code += KEYPAD2[tuple(current_key)]
	print(f"Part 2: {bathroom_code}")

