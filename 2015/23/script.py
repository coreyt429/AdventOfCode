import sys
import re

REGISTERS = {
	'a': 0,
	'b': 0
}

INSTRUCTIONS = [
	'hlf',
	'tpl',
	'inc',
	'jmp',
	'jie',
	'jio'
]

PATTERN_INSTRUCTION = re.compile(r'(jmp|jio|inc|tpl|jie|hlf) *([ab])?(?:, )?([\+-]?\d+)?')
PATTERN_JUMP_VALUE = re.compile(r'([+-])(\d+)')

def read_program_from_file(file_name):
	program = []
	with open(file_name,'r',encoding='utf-8') as file:
		lines = file.read().split('\n')
	
	for line in lines:
		matches = PATTERN_INSTRUCTION.match(line)
		if matches:
			instruction = matches.group(1)
			if instruction in ['hlf','tpl', 'inc']:
				register = matches.group(2)
				program.append({
					'instruction': instruction,
					'register': register
				})
			elif instruction in ['jio', 'jie']:
				register = matches.group(2)
				value = matches.group(3)
				matches2 = PATTERN_JUMP_VALUE.match(value)
				program.append({
					'instruction': instruction,
					'register': register,
					'direction': matches2.group(1),
					'value': int(matches2.group(2))
				})
			elif instruction in ['jmp']:
				print(line)
				print(matches)
				print(matches.groups())
				value = matches.group(3)
				matches2 = PATTERN_JUMP_VALUE.match(value)
				program.append({
					'instruction': instruction,
					'direction': matches2.group(1),
					'value': int(matches2.group(2))
				})
			else:
				print(f"unkown instruction in: {line}")
		else:
			print(f"unkown instruction in: {line}")
			
	print(program)
	return program

def run_progam():
	pointer = 0
	sentinel = 0
	threshold = 100000
	while 0 <= pointer < len(PROGRAM):
		sentinel+=1
		if sentinel > threshold:
			print("runaway?")
			break
		current_line = PROGRAM[pointer]
		if current_line['instruction'] == 'inc':
			REGISTERS[current_line['register']]+=1
			pointer+=1
		elif current_line['instruction'] == 'tpl':
			REGISTERS[current_line['register']]*=3
			pointer+=1
		elif current_line['instruction'] == 'hlf':
			REGISTERS[current_line['register']] =int(REGISTERS[current_line['register']]/2)
			pointer+=1
		elif current_line['instruction'] == 'jmp':
			if current_line['direction'] == '+':
				pointer+=current_line['value']
			else:
				pointer-=current_line['value']
		elif current_line['instruction'] == 'jie':
			if REGISTERS[current_line['register']] % 2 == 0:
				if current_line['direction'] == '+':
					pointer+=current_line['value']
				else:
					pointer-=current_line['value']
			else:
				pointer += 1
		elif current_line['instruction'] == 'jio':
			if REGISTERS[current_line['register']] % 2 != 0:
				if current_line['direction'] == '+':
					pointer+=current_line['value']
				else:
					pointer-=current_line['value']
			else:
				pointer += 1
		print(f"After: ({current_line}): pointer: {pointer}, REGISTERS: {REGISTERS}")



		

if __name__ == '__main__':
	print(REGISTERS)
	print(INSTRUCTIONS)
	PROGRAM = read_program_from_file(sys.argv[1])
	run_progam()
	print(REGISTERS)