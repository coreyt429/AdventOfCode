"""
AdventOfCode utility Module
contains utility functions for working AdventOfCode puzzles
"""
YEAR=2015
DAY=1

def set_date(year,day):
  global YEAR
  global DAY
  YEAR = year
  DAY = day
  
def load_lines(file_name=None):
    """
    Function to load an input file

    parameters:
      - file_name - string name of file to load, default input.txt

    returns:
      - list of lines from the file
    """
    global YEAR
    global DAY
    if file_name is None:
      file_name = f"{YEAR}/{DAY}/input.txt"
    with open(file_name,'r',encoding='utf-8') as file:
        return list(file.read().rstrip().split('\n'))

