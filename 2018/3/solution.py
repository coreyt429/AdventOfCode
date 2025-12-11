"""
Advent Of Code 2018 day 3

"""

# import system modules
from __future__ import annotations
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


# input regex match
pattern_input = re.compile(r"#(\d+)\s+@\s+(\d+),(\d+): (\d+)x(\d+)")


def parse_input(lines):
    """
    Parse input
    """
    # init squares
    squares = []
    # walk lines
    for line in lines:
        # regex match
        match = pattern_input.match(line)
        if match:
            # add square
            squares.append(
                {
                    "id": int(match.group(1)),
                    "col": int(match.group(2)),
                    "row": int(match.group(3)),
                    "width": int(match.group(4)),
                    "height": int(match.group(5)),
                }
            )
    return squares


def find_overlaps(squares):
    """
    Function find overlaps
    """
    # init occupied
    occupied = {}
    # walk squares
    for square in squares:
        # walk rows
        for row in range(square["row"], square["row"] + square["height"]):
            # walk cols
            for col in range(square["col"], square["col"] + square["width"]):
                # init position
                position = tuple([row, col])
                # init occupied if needed
                if position not in occupied:
                    occupied[position] = 0
                occupied[position] += 1
    # init duplicates
    duplicates = set()
    # walk squares
    for square, count in occupied.items():
        # if occupied by more than one, add to duplicates
        if count > 1:
            duplicates.add(square)
    # return duplicate square count
    return len(duplicates)


def squares_overlap_failed(sq_1, sq_2):
    """
    First attempt to find overlaps by corners.

    This doesn't take into account rectangles that overlap
    in the middle
         11
         11
    22222XX22222
    22222XX22222
         11
         11
    """
    # sq_2: [(13, 146), (13, 170), (37, 170), (37, 146)]
    min_row = min((point[0] for point in sq_2))
    max_row = max((point[0] for point in sq_2))
    min_col = min((point[1] for point in sq_2))
    max_col = max((point[1] for point in sq_2))
    sq_overlap = False
    for point in sq_1:
        row, col = point
        if min_row <= row <= max_row and min_col <= col <= max_col:
            sq_overlap = True
    return sq_overlap


def squares_overlap(sq_1, sq_2):
    """
    full overlap check
    """
    # init row and cols
    rows = {}
    cols = {}
    # Unpack the rectangle coordinates
    rows["sq_1"] = [point[0] for point in sq_1]
    cols["sq_1"] = [point[1] for point in sq_1]
    rows["sq_2"] = [point[0] for point in sq_2]
    cols["sq_2"] = [point[1] for point in sq_2]

    # init min_row, max_row and min_col max_col
    min_row = {}
    max_row = {}
    min_col = {}
    max_col = {}

    # Determine the boundaries of both squares
    min_row["sq_1"], max_row["sq_1"] = min(rows["sq_1"]), max(rows["sq_1"])
    min_col["sq_1"], max_col["sq_1"] = min(cols["sq_1"]), max(cols["sq_1"])
    min_row["sq_2"], max_row["sq_2"] = min(rows["sq_2"]), max(rows["sq_2"])
    min_col["sq_2"], max_col["sq_2"] = min(cols["sq_2"]), max(cols["sq_2"])

    # Check for overlap
    overlap = {}
    overlap["row"] = (
        min_row["sq_1"] <= max_row["sq_2"] and max_row["sq_1"] >= min_row["sq_2"]
    )
    overlap["col"] = (
        min_col["sq_1"] <= max_col["sq_2"] and max_col["sq_1"] >= min_col["sq_2"]
    )

    return overlap["row"] and overlap["col"]


def find_non_overlap(squares):
    """
    This is a more streamlined effort to find the non overlapping rectangle.
    Identify the 4 corners of each, then look for them to be overlapping
    """
    # init new_squares
    new_squares = {}
    # walk squares
    for square in squares:
        # get corners
        upper_left = tuple([square["row"], square["col"]])
        upper_right = tuple([square["row"], square["col"] + square["width"] - 1])
        lower_left = tuple([square["row"] + square["height"] - 1, square["col"]])
        lower_right = tuple(
            [square["row"] + square["height"] - 1, square["col"] + square["width"] - 1]
        )
        # store corners by id in new_squares
        new_squares[square["id"]] = [upper_left, upper_right, lower_right, lower_left]
    # init overlaps
    overlaps = set()
    # for each square in new_squares
    for sq_1_id, sq_1 in new_squares.items():
        # init overlap
        overlap = False
        # if we have already seen this square overlap, then we konw it isn't the one
        if sq_1_id in overlaps:
            continue
        # walk squares again
        for sq_2_id, sq_2 in new_squares.items():
            # don't compare to yourself
            if sq_1_id == sq_2_id:
                continue
            # do teh squares overlap?
            if squares_overlap(sq_1, sq_2):
                # yes, add to overlaps so we skip them in teh outer loop
                overlaps.add(sq_1_id)
                overlaps.add(sq_2_id)
                # set overlap
                overlap = True
        # if sq_1 didn't overlap with anything, then it is our winner
        if not overlap:
            # return sq_1_id
            return sq_1_id
    # we shouldn't get here
    return "not possible"


def find_non_overlap_failed(squares):
    """
    With this function, I wqs able to narrow it down to 58 rectangles
    Then by printing them, I was able to visibly identify the rectangle
    and it was one of three that were 21x10
    #22 @ 488,347: 21x10
    #415 @ 517,356: 21x10   <--- this was it
    #1012 @ 895,306: 21x10
    but that just won't do, so back to the drawing board
    """
    occupied = {}
    for square in squares:
        # print(f"{square['width']}x{square['height']}")
        for row in range(square["row"], square["row"] + square["height"]):
            for col in range(square["col"], square["col"] + square["width"]):
                # print("#",end="")
                position = tuple([row, col])
                if position not in occupied:
                    occupied[position] = 0
                occupied[position] += 1
            # print()
        # print()
    min_row = float("infinity")
    max_row = 0
    min_col = float("infinity")
    max_col = 0
    for position, _ in occupied.items():
        row, col = position
        min_row = min(row, min_row)
        max_row = max(row, max_row)
        min_col = min(col, min_col)
        max_col = max(col, max_col)
    # visualization
    # for row in range(min_row, max_row + 1):
    #    for col in range(min_col, max_col + 1):
    #        print(f"{occupied.get((row, col), 0)} ", end="")
    #    print()
    potential = []
    for square in squares:
        corners = [
            tuple([square["row"], square["col"]]),
            tuple([square["row"], square["col"] + square["width"] - 1]),
            tuple([square["row"] + square["height"] - 1, square["col"]]),
            tuple(
                [
                    square["row"] + square["height"] - 1,
                    square["col"] + square["width"] - 1,
                ]
            ),
        ]
        for corner in corners:
            if occupied[corner] > 1:
                continue
        for col in range(square["col"], square["col"] + square["width"]):
            for row in range(square["row"], square["row"] + square["height"]):
                position = tuple([row, col])
                if occupied[position] > 1:
                    continue
        potential.append(square)
    print(f"{len(potential)} of {len(squares)} might be the one")
    return len(potential)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    squares = parse_input(input_value)
    if part == 2:
        non_overlap = find_non_overlap(squares)
        return non_overlap
    overlap = find_overlaps(squares)
    return overlap


YEAR = 2018
DAY = 3
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
