"""
Advent Of Code 2021 day 20
Grid worked like a charm for this one.  There was some odd behavior in my puzzle input
with the outside edges.  It took me a few attempts to sort those out.
"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


class Image(Grid):
    """Class to represent an image as a Grid"""

    def __init__(self, image_data, enhancement_filter):
        """init method"""
        super().__init__(
            image_data,
            use_overrides=False,
            coordinate_system="cartesian",
            type="infinite",
            ob_default_value="%",
            default_value="?",
        )
        self.enhancement_filter = enhancement_filter

    def get_pixel_value(self, point):
        """Method to calculate pixel value"""
        neighbors = self.get_neighbors(point=point)
        value_string = ""
        neighbors["c"] = point
        upper_left = tuple(self.cfg["min"])
        for direction in ["nw", "n", "ne", "w", "c", "e", "sw", "s", "se"]:
            new_value = self.get_point(neighbors.get(direction, (-1, -1)), ".")
            if new_value == "%":
                new_value = self.get_point(upper_left)
            value_string += new_value
        binary_string = value_string.replace(".", "0").replace("#", "1")
        value = int(binary_string, 2)
        return value

    def set_pixel(self, point, value):
        """Method to set a pixel based on integer value"""
        self.set_point(point, self.enhancement_filter[value])

    def enhance(self):
        """Method to enhance an image and return the new image"""
        new_image = Image(["."], self.enhancement_filter)
        pad = 2
        for x_val in range(self.cfg["min"][0] - pad, self.cfg["max"][0] + 1 + pad):
            for y_val in range(self.cfg["min"][1] - pad, self.cfg["max"][1] + 1 + pad):
                point = (x_val, y_val)
                new_image.set_pixel(point, self.get_pixel_value(point))
        new_image.update()
        return new_image


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    enhancement_filter = input_value[0]
    image_data = []
    for line in input_value[2:]:
        # image_data.append('.....'+line+'.....')
        image_data.append(line)
    input_image = Image(image_data, enhancement_filter)
    enhanced_image = input_image.enhance()
    count = 2
    if part == 2:
        count = 50
    for _ in range(count - 1):
        enhanced_image = enhanced_image.enhance()
    # part 1:
    # 5053 too high
    # 5151 trimmed left and right edges, not even trying it, that higher
    # 5041 trimmed bottom edge, too low, so trimmed too much, let me see
    # 5044 programatically trimmed edges, Bingo!
    # part 2:
    # 10385 too low (maybe not trim here?)
    # 10749 still too low, maybe not padding enough
    # 14788 still too low, more padding?
    # 15611 not right, add trimming back
    # 15128 not right
    # Changed handling of get_pixel_value for pixels not in the source image
    # if they are missing, use the value of the upper left hand corner of the
    # source instead of always .
    # 18074 Bingo!
    return str(enhanced_image).count("#")


YEAR = 2021
DAY = 20
input_format = {
    1: "lines",
    2: "lines",
}

funcs = {
    1: solve,
    2: solve,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
