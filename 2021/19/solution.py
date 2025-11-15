"""
Advent Of Code 2021 day 19

Okay, this one kicked my butt.  I still suck at matrix math.
There are also still some efficiencies that can probably be made.
To start with, this should probably drop the object model, or at
least move a lot of the methods to functions so lru_cache can
be used to cache repetitive operations.

"""

# import system modules
import time
import re
from itertools import permutations, product
import numpy as np

# import my modules
import aoc  # pylint: disable=import-error
from grid import manhattan_distance  # pylint: disable=import-error


class Scanner:
    """Class to represent a scanner"""

    pattern_digit = re.compile(r"(\-*\d+)")

    def __init__(self, scanner_text):
        """init"""
        lines = scanner_text.splitlines()
        header = lines.pop(0)
        self.scanner_id = int(self.pattern_digit.findall(header)[0])
        self.beacons = []
        self.position = None
        self.aligned = False
        self.translation_vector = None
        self.translated = False
        if self.scanner_id == 0:
            self.position = (0, 0, 0)
            self.aligned = True
            self.translated = True
        for line in lines:
            point = [int(num) for num in self.pattern_digit.findall(line)]
            self.beacons.append(tuple(point))

    def __str__(self):
        """String"""
        my_str = f"scanner_id: {self.scanner_id}, aligned: {self.aligned}"
        my_str += f", position: {self.position}, translation_vector: {self.translation_vector}\n"
        # for beacon in self.beacons:
        #     my_str += f"  {beacon}\n"
        return my_str.rstrip()

    def rotate_point(self, point, rotation_matrix):
        """Method to rotate a point around an axis"""
        return tuple(np.dot(rotation_matrix, point))

    def calculate_scanner_location(self, translation_vector):
        """Find scanner 1's position relative to scanner 0."""
        return tuple(-np.array(translation_vector))

    def transform_all_points(
        self, scanner_1_points, rotation_matrix, translation_vector
    ):
        """Transform all scanner 1 points relative to scanner 0."""
        rotated_points = [
            self.rotate_point(p, rotation_matrix) for p in scanner_1_points
        ]
        transformed_points = [
            tuple(np.add(p, translation_vector)) for p in rotated_points
        ]
        return transformed_points

    def align(self, other):
        """Method to align a scanner to another scanner"""
        if self.aligned:
            return True
        # Step 1: Find matching points
        rotation_matrix, translation_vector, _ = self.find_matching_points(other)
        if rotation_matrix is not None:
            # Step 2: Calculate Scanner 1's Location
            self.position = self.calculate_scanner_location(translation_vector)
            # Step 3: Transform all points
            self.translation_vector = translation_vector
            self.beacons = self.transform_all_points(
                self.beacons, rotation_matrix, translation_vector
            )
            self.aligned = True
            return True
        self.aligned = False
        return False

    def generate_rotation_matrices(self):
        """Generate all 24 valid rotation matrices for 90-degree cube rotations."""
        base_axes = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        signs = [1, -1]
        matrices = []
        for permuted_axes in permutations(base_axes):
            for sign_comb in product(signs, repeat=3):
                matrix = np.array(
                    [s * np.array(axis) for s, axis in zip(sign_comb, permuted_axes)]
                )
                if np.linalg.det(matrix) == 1:
                    matrices.append(matrix)
        return matrices

    def find_matching_points(self, other):
        """Find 12 matching points under any rotation."""
        rotation_matrices = self.generate_rotation_matrices()

        for rotation_matrix in rotation_matrices:
            rotated_scanner_1 = [
                self.rotate_point(p, rotation_matrix) for p in self.beacons
            ]

            # Compare each rotated beacon set
            for p_0 in other.beacons:
                for p_1 in rotated_scanner_1:
                    translation = np.subtract(p_0, p_1)
                    transformed_beacons = {
                        tuple(np.add(beacon, translation))
                        for beacon in rotated_scanner_1
                    }

                    # Check if there are at least 12 matching points
                    common_beacons = transformed_beacons.intersection(other.beacons)
                    if len(common_beacons) >= 12:
                        return rotation_matrix, translation, common_beacons
        return None, None, None


def parse_data(text):
    """Function to parse input text"""
    scanners = []
    scanner_texts = text.split("\n\n")
    for scanner_text in scanner_texts:
        scanners.append(Scanner(scanner_text))
    return scanners


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return answer[2]
    scanners = parse_data(input_value)
    # scanner_count = len(scanners)
    # seeds = (0, 17, 9, 20, 24, 7, 3, 10, 16, 21, 13, 14, 1, 15, 4, 8, 12, 11, 6)
    alignments = {
        9: 0,
        17: 0,
        20: 17,
        24: 9,
        3: 9,
        7: 20,
        10: 24,
        13: 7,
        14: 20,
        15: 3,
        16: 10,
        21: 16,
        1: 21,
        4: 13,
        8: 1,
        11: 15,
        12: 4,
        6: 11,
        2: 6,
        5: 14,
        18: 8,
        19: 3,
        22: 17,
        23: 12,
        25: 7,
    }
    # counter = 0
    while any((not scanner.aligned for scanner in scanners)):
        # use_seeds = True
        # if all([scanner.aligned for scanner in scanners if scanner.scanner_id in seeds]):
        #     use_seeds = False
        # aligned_count = len([scanner for scanner in scanners if scanner.aligned])
        # print(f"pass {counter}: ({aligned_count}/{scanner_count})")
        # counter += 1
        for scanner in scanners:
            if scanner.aligned:
                continue
            # if use_seeds and scanner.scanner_id not in seeds:
            #     continue
            for other in scanners:
                # major speed cheat, comment out if not running with my input
                if other.scanner_id != alignments[scanner.scanner_id]:
                    continue
                if not other.aligned:
                    continue
                # speed cheat, identified the matching targets already, so skip
                # the others
                # if other.scanner_id not in seeds:
                #     continue
                # print(f"Trying to align: {scanner.scanner_id} with {other.scanner_id} ", end='')
                scanner.align(other)
                # print(scanner.aligned)
                if scanner.aligned:
                    # print(f"  Aligned {scanner.scanner_id} with {other.scanner_id}")
                    break
    max_distance = 0
    for scanner in scanners:
        for other in scanners:
            max_distance = max(
                max_distance, manhattan_distance(scanner.position, other.position)
            )
    answer[2] = max_distance
    all_beacons = set()
    for scanner in scanners:
        all_beacons.update(scanner.beacons)
    return len(all_beacons)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021, 19)
    input_data = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 318, 2: 12166}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
