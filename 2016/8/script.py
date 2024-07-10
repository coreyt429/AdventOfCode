"""
AdventOfCode 2016 day 8

This just felt like a good object oriented exercise, so I created the Display class
"""
import sys
import re

class Display:
    """
    Class to handle display manipulation
    """

    def __init__(self, rows=6, cols=50):
        """
        Initialize the display, default to 6x50
        """
        self.rect_pattern = re.compile(r'rect (\d+)x(\d+)')
        self.rotate_pattern = re.compile(r'rotate (row|column) [xy]=(\d+) by (\d+)')
        self.display = []
        for row in range(rows):
            self.display.append([])
            for _ in range(cols):
                self.display[row].append('.')

    def __str__(self):
        """
        String representation of display
        """
        retval = ''
        for row in self.display:
            retval += ''.join(row) + '\n'
        retval += '\n'
        return retval.replace('.',' ')

    def rect(self,cols,rows):
        """
        Lights up rectangle in upper left hand corner 
        """
        for row in range(rows):
            for col in range(cols):
                self.display[row][col] = '#'

    def rotate_col(self,col,pixels):
        """
        rotates a column down
        """
        tmp_list = []
        for idx, row in enumerate(self.display):
            tmp_list.append(row[col])
        for _ in range(pixels):
            tmp_var = tmp_list.pop()
            tmp_list.insert(0,tmp_var)
        for idx, row in enumerate(self.display):
            row[col] = tmp_list[idx]

    def rotate_row(self,row,pixels):
        """
        rotates a row right
        """
        for _ in range(pixels):
            tmp_var = self.display[row].pop()
            self.display[row].insert(0,tmp_var)

    def run_command(self,command):
        """
        Parses and executes command string
        """
        matches = self.rect_pattern.match(command)
        if matches:
            self.rect(int(matches.group(1)), int(matches.group(2)))
        else:
            matches = self.rotate_pattern.match(command)
            if matches:
                if matches.group(1) == 'row':
                    self.rotate_row(int(matches.group(2)),int(matches.group(3)))
                else:
                    self.rotate_col(int(matches.group(2)),int(matches.group(3)))
            else:
                print(f"How did we get here? {command}")

    def lit_pixels(self):
        """
        returns number of lit pixels
        """
        return f'{self}'.count('#')

def load_data(file_name):
    """
    load instructions from file
    """
    with open(file_name,'r',encoding='utf-8') as file:
        return list(file.read().rstrip().split('\n'))

if __name__ == "__main__":
    display = Display()
    instructions = load_data(sys.argv[1])
    for instruction in instructions:
        display.run_command(instruction)

    print(f'Part 1: {display.lit_pixels()}')
    print(f'Part 2:\n{display}')
