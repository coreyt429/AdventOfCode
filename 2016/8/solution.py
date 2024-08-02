"""
Advent Of Code 2016 day 8

This just felt like a good object oriented exercise, so I created the Display class

This one worked well, and refactored pretty easy, but I was never quite happy that 
part 2 didn't have a real answer, so fixing that this time.

"""
# import system modules
import time
import re

# import my modules
import aoc # pylint: disable=import-error

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

    def message(self):
        """
        Function to parse display message
        """
        # Split the string into lines
        lines = str(self).strip().split('\n')

        # Define the width and height of each character
        char_width = 5
        char_height = 6  # Including the space between rows

        # Calculate the number of characters in the message
        num_chars = len(lines[0]) // char_width

        # Initialize the result string
        result = ""
        char_map = {
            " ##  #  # #  # #### #  # #  # ": 'A',
            "#### #    ###  #    #    #### ": 'E',
            " ##  #  # #    # ## #  #  ### ": 'G',
            "#  # #  # #### #  # #  # #  # ": 'H',
            " ##  #  # #  # #  # #  #  ##  ": 'O',
            "###  #  # #  # ###  #    #    ": 'P',
            "###  #  # #  # ###  # #  #  # ": 'R',
            "#   ##   # # #   #    #    #  ": 'Y'
        }
        # Iterate through each character
        for i in range(num_chars):
            # Extract the 5x5 grid for this character
            char_grid = [line[i * char_width:(i + 1) * char_width] for line in lines]
            # Convert the grid to a single string for easier comparison
            char_string = ''.join(char_grid)
            # the last O was missing a couple spaces
            while len(char_string) < char_height*char_width:
                char_string += ' '
            # match to char_map
            result += char_map.get(char_string, '?')
        return result

def solve(instructions, part):
    """
    Function to solve puzzle
    """
    display = Display()
    for instruction in instructions:
        display.run_command(instruction)
    if part == 1:
        return display.lit_pixels()
    return display.message()

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016,8)
    input_lines = my_aoc.load_lines()
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
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
