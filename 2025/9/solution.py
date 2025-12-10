"""
Advent Of Code 2025 day 9



"""

# import system modules
import logging
import argparse
import numpy as np

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def get_axis_aligned_rectangles(points: np.ndarray):
    """Get all axis-aligned rectangles defined by pairs of points."""
    dx = np.abs(points[:, None, 0] - points[None, :, 0]) + 1
    dy = np.abs(points[:, None, 1] - points[None, :, 1]) + 1
    areas = dx * dy

    n = len(points)
    i, j = np.triu_indices(n, k=1)

    return {
        "i": i,
        "j": j,
        "area": areas[i, j],
    }


def segments_intersect(a1, a2, b1, b2):
    """Return True if line segments a1a2 and b1b2 intersect (excluding endpoints)."""

    def orient(p, q, r):
        return np.sign((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]))

    o1 = orient(a1, a2, b1)
    o2 = orient(a1, a2, b2)
    o3 = orient(b1, b2, a1)
    o4 = orient(b1, b2, a2)

    return (o1 * o2 < 0) and (o3 * o4 < 0)


def _point_on_segment(p, a, b) -> bool:
    """Return True if point p lies on segment ab (inclusive)."""
    (px, py), (ax, ay), (bx, by) = p, a, b

    # Colinearity check via cross product == 0
    cross = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
    if cross != 0:
        return False

    # Within bounding box
    return min(ax, bx) <= px <= max(ax, bx) and min(ay, by) <= py <= max(ay, by)


def _point_in_polygon_single(p, poly: np.ndarray) -> bool:
    """
    Boundary-inclusive point-in-polygon for a single point p.
    Returns True if p is inside or on the boundary of poly.
    """
    px, py = p
    x0 = poly[:, 0]
    y0 = poly[:, 1]
    x1 = np.roll(x0, -1)
    y1 = np.roll(y0, -1)

    # 1) Boundary check: on any edge -> inside
    for ax, ay, bx, by in zip(x0, y0, x1, y1):
        if _point_on_segment((px, py), (ax, ay), (bx, by)):
            return True

    # 2) Standard ray-cast for strict interior
    inside = False
    for ax, ay, bx, by in zip(x0, y0, x1, y1):
        # Check if edge straddles the horizontal ray
        if (ay > py) != (by > py):
            xints = ax + (bx - ax) * (py - ay) / (by - ay)
            if px < xints:
                inside = not inside

    return inside


def points_in_polygon(pts: np.ndarray, poly: np.ndarray) -> np.ndarray:
    """
    Boundary-inclusive: True if point is inside OR on the polygon boundary.
    """
    return np.array([_point_in_polygon_single(p, poly) for p in pts], dtype=bool)


def rect_fully_inside_polygon(p1, p2, polygon):
    """
    Check if axis-aligned rectangle defined by p1 and p2 is fully inside polygon
    """
    x_min = min(p1[0], p2[0])
    x_max = max(p1[0], p2[0])
    y_min = min(p1[1], p2[1])
    y_max = max(p1[1], p2[1])

    rect = np.array(
        [
            [x_min, y_min],
            [x_min, y_max],
            [x_max, y_max],
            [x_max, y_min],
        ]
    )

    # 1) all corners inside
    if not points_in_polygon(rect, polygon).all():
        return False

    # 2) no edge intersections
    rect_edges = list(zip(rect, np.roll(rect, -1, axis=0)))
    poly_edges = list(zip(polygon, np.roll(polygon, -1, axis=0)))

    for ra, rb in rect_edges:
        for pa, pb in poly_edges:
            if segments_intersect(ra, rb, pa, pb):
                return False

    return True


def parse_input(input_lines):
    """
    Parse input into numpy array of points
    """
    points = []
    for line in input_lines:
        x_str, y_str = line.split(",")
        x = int(x_str.strip())
        y = int(y_str.strip())
        points.append((x, y))
    return np.array(points)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    points = parse_input(input_value)
    upper = get_axis_aligned_rectangles(points)
    if upper["area"].size == 0:
        return 0, (None, None)  # fewer than 2 points
    if part == 1:
        max_pos = np.argmax(upper["area"])
        logger.debug("max_pos: %s", max_pos)
        max_area = upper["area"][max_pos]
        i_max = upper["i"][max_pos]
        j_max = upper["j"][max_pos]
        logger.debug("i_max: %s, j_max: %s", i_max, j_max)
        logger.debug("Point 1: %s", points[i_max])
        logger.debug("Point 2: %s", points[j_max])
        return max_area
    # Part 2: search rectangles in descending area, stop at first valid
    polygon = np.asarray(points)
    max_area = 0

    for idx in np.argsort(upper["area"])[::-1]:
        area = upper["area"][idx]
        if area <= max_area:
            break  # everything else is smaller

        i = upper["i"][idx]
        j = upper["j"][idx]
        p1 = points[i]
        p2 = points[j]
        logger.debug("Checking points %s and %s with area %s", p1, p2, area)

        if rect_fully_inside_polygon(p1, p2, polygon):
            return area
    return None


YEAR = 2025
DAY = 9
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
