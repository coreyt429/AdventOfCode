"""
Advent Of Code 2022 day 7

The Directory() class makes filesystem traversal and size calculation easy.

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

class Directory():
    """Class to represent a directory"""

    def __init__(self, path='/', parent=None):
        """Init method"""
        self.parent = parent
        self.path = path.replace('//','/')
        self.files = {}
        self.children = {}
        self.size = None

    def calculate_size(self, force=False):
        """Method to calculate directory size"""
        if self.size is not None and not force:
            return self.size
        # Start with file sizes
        self.size = sum(self.files.values())
        for child in self.children.values():
            self.size += child.calculate_size(force)
        return self.size

    def add_file(self, file_name, file_size):
        """method to add a file"""
        self.files[file_name] = int(file_size)

    def add_child(self, child_name):
        """method to add a child directory"""
        self.children[child_name] = Directory(path=f"{self.path}/{child_name}", parent=self)

    def __str__(self):
        """string representation"""
        my_str = f"Directory: {self.path}\n"
        my_str += "  Children:\n"
        for child in self.children:
            my_str += f"    {child}\n"
        my_str += "  Files:\n"
        for file_name, file_size in self.files.items():
            my_str += f"    {file_name}: {file_size}\n"
        return my_str

def do_chdir(current_dir, target):
    """function to change directory"""
    if target == '/':
        while current_dir.parent is not None:
            current_dir = current_dir.parent
        return current_dir
    if target == '..':
        return current_dir.parent
    return current_dir.children[target]

def do_ls(current_dir, lines):
    """Function to read ls output"""
    while lines and lines[0][0] != '$':
        line = lines.pop(0)
        tokens = line.split(' ')
        if tokens[0] == 'dir':
            if tokens[1] not in current_dir.children:
                current_dir.add_child(tokens[1])
        else:
            current_dir.add_file(*reversed(tokens))

def scan_filesystem(lines):
    """Function to scan filesystem from input data"""
    root = Directory('/')
    current_dir = root
    while lines:
        line = lines.pop(0)
        # print(line)
        if line[0] == '$':
            tokens = line[2:].split(' ', 1)
            command = tokens[0]
            target = tokens[1] if len(tokens) > 1 else None
            if command == 'cd':
                current_dir = do_chdir(current_dir, target)
                continue
            if command == 'ls':
                do_ls(current_dir, lines)
                continue
    return root


def find_directories(current_dir, size_limit):
    """Function to recurse directory structure"""
    total = 0
    if current_dir.calculate_size() < size_limit:
        total += current_dir.calculate_size()

    for child in current_dir.children.values():
        total += find_directories(child, size_limit)
    return total

def find_delete_directory(current_dir, size_limit, smallest=float('infinity')):
    """Function to recurse directory structure"""
    if current_dir.calculate_size() > size_limit:
        smallest = min(smallest, current_dir.calculate_size())

    for child in current_dir.children.values():
        smallest = find_delete_directory(child, size_limit, smallest)
    return smallest


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    root = scan_filesystem(list(input_value))
    if part == 1:
        return find_directories(root, 100000)
    # part 2
    file_system_size = 70000000
    space_needed = 30000000
    space_available = file_system_size - root.calculate_size()
    target = space_needed - space_available
    return find_delete_directory(root, target)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022,7)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
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
    # correct answers once solved, to validate changes
    correct = {
        1: 1307902,
        2: 7068748
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
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
