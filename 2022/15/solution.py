"""
Advent Of Code 2022 day 15

I thought I had this one, I thought, I could math the heck out of it.

I did.  wrongly!  I spent a while trying to treat my scan_range as
the radius of a circle, when the instructions made it clear we were
using manhattan_distance, and the resulting area was diamond shaped.



"""

# import system modules
import time
import re

# import my modules
import aoc  # pylint: disable=import-error
from grid import manhattan_distance  # pylint: disable=import-error


class Sensor:
    """Class to represent a sensor"""

    def __init__(self, position, beacon):
        self.position = position
        self.beacon = beacon
        self.scan_range = self.distance(beacon)
        self.min = (
            self.position[0] - self.scan_range,
            self.position[1] - self.scan_range,
        )
        self.max = (
            self.position[0] + self.scan_range,
            self.position[1] + self.scan_range,
        )

    def distance(self, point):
        """method to calculate distance between a sensor and a point"""
        return manhattan_distance(self.position, point)

    def coverage(self, y_val):
        """Calculate the horizontal coverage of the sensor at a specific y-value."""
        # Vertical distance between the sensor and y_val
        delta_y = abs(self.position[1] - y_val)

        # Check if the sensor covers y_val
        if delta_y > self.scan_range:
            return None  # Sensor does not cover y_val

        # Horizontal coverage
        delta_x = self.scan_range - delta_y
        x_min = self.position[0] - delta_x
        x_max = self.position[0] + delta_x
        return (x_min, x_max)

    def outside_perimeter(self):
        """Method to generate outside perimeter points"""
        x_s, y_s = self.position
        r_s = self.scan_range
        for d_x in range(-r_s - 1, r_s + 2):
            d_y = (r_s + 1) - abs(d_x)
            x_candidates = [x_s + d_x]
            y_candidates = [y_s + d_y, y_s - d_y]
            for x_c in x_candidates:
                for y_c in y_candidates:
                    yield ((x_c, y_c))

    def __str__(self):
        """String Method"""
        return (
            f"Sensor: {self.position}, range: {self.scan_range}, beacon: {self.beacon}"
        )


def find_uncovered_point(sensors, max_x, max_y):
    """Function to find the point that is not covered by a sensor"""
    # I tried several orders to make something logical, but for my input
    # reversed was the fastest.  The key here is to have sensor that is close
    # to the signal early, but I didn't find a logic based sorting method that helped
    for sensor in reversed(sensors):
        for point in sensor.outside_perimeter():
            # Check if the candidate is within bounds
            if 0 <= point[0] <= max_x and 0 <= point[1] <= max_y:
                # Check if the point is not covered by any sensor
                # my manhattan_distance function was significantly slower than just
                # calculating it.  possibly due to the overhead of converting to np.array
                # if all(manhattan_distance(point, s.position) > s.scan_range for s in sensors):
                #     return point
                if all(
                    abs(point[0] - s.position[0]) + abs(point[1] - s.position[1])
                    > s.scan_range
                    for s in sensors
                ):
                    # Found the uncovered point
                    return point
    return None  # If no point is found


def parse_input(lines):
    """Function to read sensor data from input lines"""
    pattern_input = re.compile(
        r"S.* x=(\-?\d+), y=(\-?\d+): c.*t x=(\-?\d+), y=(\-?\d+)"
    )
    sensors = []
    for line in lines:
        values = [int(num) for num in pattern_input.findall(line)[0]]
        sensors.append(Sensor(tuple(values[:2]), tuple(values[2:])))
    return sensors


def solve(input_value, part, y_val=None):
    """
    Function to solve puzzle
    """
    sensors = parse_input(input_value)
    if part == 2:
        if y_val is None:
            y_val = 4000000
        point = find_uncovered_point(sensors, y_val, y_val)
        return point[0] * 4000000 + point[1]
    if y_val is None:
        y_val = 2000000
    # part 1
    min_x = float("infinity")
    max_x = 0
    beacons = set()
    no_beacons = set()
    for sensor in sensors:
        beacons.add(sensor.beacon)
        x_vals = sensor.coverage(y_val)
        # if sensor.min[1] <= y_val <= sensor.max[1]:
        if x_vals is not None:
            min_x = min(sensor.min[0], min_x)
            max_x = max(sensor.max[1], max_x)
            start_x = min(x_vals)
            end_x = max(x_vals)
            for x_val in range(start_x, end_x + 1):
                no_beacons.add((x_val, y_val))
    no_beacons.difference_update(beacons)
    # part 1
    # 30076 - too low
    # 30079 - round instead of ceil and floor, still too low
    # 105958 - extended search to max_range, still too low
    return len(no_beacons)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022, 15)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 4876693, 2: 11645454855041}
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
