START_CODE=20151125
MULTIPLIER=252533
DIVISOR=33554393

TARGET_ROW = 2981
TARGET_COL = 3075.


current_code = START_CODE
row = 1
col = 1
next_row = 2
#print(current_code,row,col)
previous_code = current_code
while True:
	row -= 1
	col += 1
	if row < 1:
		row = next_row
		next_row += 1
		col = 1
	current_code = (previous_code * MULTIPLIER) % DIVISOR
	if row == TARGET_ROW and col == TARGET_COL:
		print(current_code,row,col)
		break
	previous_code = current_code
