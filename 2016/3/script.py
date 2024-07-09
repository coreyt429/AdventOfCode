import sys
import re
def load_file(file_name):
	with open(file_name,'r',encoding='utf-8') as file:
		lines = [line.lstrip() for line in file.read().rstrip().split('\n')]
		num_list = []
		num_list_2 = []
		num_list_3 = []
		number_pattern = re.compile(r'\d+') 
		for line in lines:
			num_list_2.append([int(num) for num in number_pattern.findall(line)])
			num_list.append(sorted([int(num) for num in number_pattern.findall(line)]))
		for row in range(0,len(num_list_2),3):
			for col in range(3):
				num_list_3.append(
					sorted([
						num_list_2[row][col],
						num_list_2[row+1][col],
						num_list_2[row+2][col]
					])
				)
	return num_list, num_list_3



if __name__ == '__main__':
	data = {}
	data['p1'], data['p2'] = load_file(sys.argv[1])
	counter = {
		'p1': 0,
		'p2': 0
	}
	for part in data:
		for side_a, side_b, side_c in data[part]:
			if side_a + side_b > side_c:
				counter[part]+=1
	print(f"Part 1: {counter['p1']}")
	print(f"Part 2: {counter['p2']}")
	