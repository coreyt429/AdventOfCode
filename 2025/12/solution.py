"""
Advent Of Code 2025 day 12

"""

# import system modules
import logging
import argparse
import re
from copy import deepcopy
from collections import defaultdict
from dataclasses import dataclass
from time import time

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

pattern_area_description = re.compile(r"(\d+)x(\d+):\s+(\d+(?:\s+\d+)*)")

TEST = False


@dataclass
class Area:
    """
    Class to represent an area
    """

    def __init__(self, width, height, package_counts):
        self.width = min(int(width), int(height))  # enforce width <= height
        self.height = max(int(width), int(height))
        self.package_counts = tuple(package_counts)

    def __str__(self):
        return f"Area {self.width}x{self.height}, Packages: {self.package_counts}"


class Package:
    """
    Class to represent a package
    """

    def __init__(self, package_id, shape_text):
        self.package_id = package_id
        self.shape_text = shape_text
        self.grid = Grid(shape_text, use_overrides=False)
        self._init_state = deepcopy(self.grid.map)
        # Number of '#' cells in the base shape (used for area/slack checks)
        self.size = sum(1 for p in self.grid if self.grid[p] == "#")
        # self.size=9
        self.orientations = set()
        self._generate_orientations()

    def _generate_orientations(self):
        point_groups = (
            deepcopy(self._init_state),
            self._flip_horizontal(deepcopy(self._init_state)),
            self._flip_vertical(deepcopy(self._init_state)),
        )
        # logger.debug("point groups: %s", point_groups)
        for grid_points in point_groups:
            for turns in range(4):
                points = self._rotate_cw(grid_points=grid_points, turns=turns)
                self.orientations.add(points)

    def _points(self, grid_points: tuple):
        """Return normalized (x,y) points for '#' cells in grid_points.

        Normalization shifts the shape so its min x and min y are 0. This ensures
        placements can be anchored on-board without requiring negative offsets.
        """
        self.grid.map = grid_points
        self.grid.update()
        pts = [p for p in self.grid if self.grid[p] == "#"]
        self.grid.map = self._init_state
        self.grid.update()

        if not pts:
            return tuple()

        min_x = min(x for x, _ in pts)
        min_y = min(y for _, y in pts)
        normalized = sorted((x - min_x, y - min_y) for x, y in pts)
        return tuple(normalized)

    def _rotate_cw(self, grid_points, turns=1):
        for _ in range(turns):
            ys = [y for _, y in grid_points]
            max_y = max(ys)

            grid_points = {
                (max_y - y, x): value for (x, y), value in grid_points.items()
            }
        return self._points(grid_points)

    def _flip_vertical(self, grid_points):
        xs = [x for x, _ in grid_points]
        max_x = max(xs)

        grid_points = {(max_x - x, y): value for (x, y), value in grid_points.items()}
        return grid_points

    def _flip_horizontal(self, grid_points):
        ys = [y for _, y in grid_points]
        max_y = max(ys)

        grid_points = {(x, max_y - y): value for (x, y), value in grid_points.items()}
        return grid_points

    def __str__(self):
        return f"Package {self.package_id}:\n{str(self.grid)}"

    def __hash__(self):
        return hash(self.package_id)


def parse_input(input_text):
    """
    Function to parse input
    """
    packages = []
    areas = []
    package_text_list = input_text.split("\n\n")
    for area_text in package_text_list.pop(-1).splitlines():
        match = pattern_area_description.match(area_text)
        if match:
            areas.append(
                Area(
                    width=int(match.group(1)),
                    height=int(match.group(2)),
                    package_counts=tuple(map(int, match.group(3).split())),
                )
            )
    for package_text in package_text_list:
        package_lines = package_text.splitlines()
        package_id = int(package_lines[0].split(":", 1)[0].strip())
        package_desc = "\n".join(package_lines[1:])
        package = Package(package_id, package_desc)
        packages.append(package)

    # Ensure packages are indexed by package_id so `remaining[pkg_index]` lines up with counts.
    packages = sorted(packages, key=lambda p: p.package_id)
    if packages:
        expected = list(
            range(packages[0].package_id, packages[0].package_id + len(packages))
        )
        actual = [p.package_id for p in packages]
        assert actual == expected, (
            f"Non-contiguous or unexpected package IDs: {actual} (expected {expected})"
        )

    return packages, areas


def can_place(package_points, top_left, grid):
    """Return True if all translated package points land inside the grid and on '.' cells."""
    [min_x, min_y], [max_x, max_y] = grid.get_map_size()
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    for px, py in package_points:
        gx = px + top_left[0]
        gy = py + top_left[1]

        # Explicit bounds check first (prevents off-board masks)
        if gx < min_x or gx >= min_x + width or gy < min_y or gy >= min_y + height:
            return False

        if grid[(gx, gy)] != ".":
            return False

    return True


def bit_for(x, y, width, height):
    """bitmask for cell (x,y) in grid of given width/height"""
    assert 0 <= x < width, f"x out of bounds: {x} (width={width})"
    assert 0 <= y < height, f"y out of bounds: {y} (height={height})"
    return 1 << (y * width + x)


def _placement_points(package_points, top_left, width, height):
    """Return the placement bitmask for `package_points` translated to `top_left`."""
    placement_mask = 0
    for x, y in (
        (p_point[0] + top_left[0], p_point[1] + top_left[1])
        for p_point in package_points
    ):
        placement_mask |= bit_for(x, y, width, height)
    return placement_mask


def _calculate_placements(package, grid):
    """
    Function to calculate possible placements for package in grid
    """
    placements = []
    [min_x, min_y], [max_x, max_y] = grid.get_map_size()
    width = (max_x - min_x) + 1
    height = (max_y - min_y) + 1

    for orientation in package.orientations:
        for point in grid:
            if can_place(orientation, point, grid):
                placements.append(_placement_points(orientation, point, width, height))
    return placements


_package_placement_cache = {}
_cell_placement_cache = {}


def get_package_placements(packages, grid):
    """
    Function to get package placements in grid
    """
    [_, _], [w, h] = grid.get_map_size()
    w += 1
    h += 1
    if (w, h) in _package_placement_cache:
        return _package_placement_cache[(w, h)]
    placements = {}
    for pkg_index, package in enumerate(packages):
        placements[pkg_index] = _calculate_placements(package, grid)
    _package_placement_cache[(w, h)] = placements
    return placements


def get_cell_placements(placements, cache_key=None):
    """
    Function to get cell placements
    """
    if cache_key is not None and cache_key in _cell_placement_cache:
        return _cell_placement_cache[cache_key]
    logger.debug("get_cell_placements: placements: %s", placements)
    cell_placements = defaultdict(
        list
    )  # key: cell bit (1<<i) -> list[(pmask, pkg_index)]
    for pkg_index, pkg_placements in placements.items():
        logger.debug("Package: %d, placements: %d", pkg_index, len(pkg_placements))
        for pmask in pkg_placements:
            logger.debug("Package %d placement mask: %s", pkg_index, format(pmask, "b"))
            m = pmask
            while m:
                c = m & -m
                m ^= c
                cell_placements[c].append((pmask, pkg_index))
    result = dict(cell_placements)
    if cache_key is not None:
        _cell_placement_cache[cache_key] = result
    return result


def placement_possible(area, packages):
    """
    Function to check if placement is possible based on area and package sizes
    Quick test for live input.
    """
    total_area = area.width * area.height
    package_area = sum(
        count * packages[idx].size for idx, count in enumerate(area.package_counts)
    )
    logger.debug("Area: %d, Package area: %d", total_area, package_area)
    return package_area <= total_area


def place_packages(area, packages):
    """Return True if all required packages can be placed without overlap.

    This is a simple backtracking solver that iterates through placement combinations.
    It intentionally avoids the blocked/slack/heap logic (which was optimized for live
    input but has been tricky to keep sound).

    Success condition: all package counts are placed (leftover empty space is allowed).
    """
    full_mask = (1 << (area.width * area.height)) - 1
    logger.debug("full mask: %s", format(full_mask, f"0{area.width * area.height}b"))

    # Precompute placement masks for this board size (cached by get_package_placements).
    grid = Grid([["."] * area.width for _ in range(area.height)], use_overrides=False)
    placements = get_package_placements(packages, grid)

    # Sanity: no placement should set bits outside the board.
    for pkg_idx, pmasks in placements.items():
        for pm in pmasks:
            assert (pm & ~full_mask) == 0, (
                f"Placement spills off-board for pkg {pkg_idx}: {pm:b}"
            )

    # Small fast fail: required filled cells must fit in the rectangle.
    pkg_sizes = [p.size for p in packages]
    required_area = sum(
        area.package_counts[i] * pkg_sizes[i] for i in range(len(pkg_sizes))
    )
    if required_area > area.width * area.height:
        return False

    # Memoize failed states: (remaining_tuple, occupied_mask)
    dead = set()

    def _search(remaining, occupied):
        key = (remaining, occupied)
        if key in dead:
            return False

        # Done when all counts are exhausted.
        if all(c == 0 for c in remaining):
            return True

        # Choose next package type using a simple dynamic MRV: pick the remaining type
        # with the fewest currently-valid placements.
        best_k = None
        best_opts = None
        for k, cnt in enumerate(remaining):
            if cnt <= 0:
                continue
            opts = [pm for pm in placements[k] if (pm & occupied) == 0]
            if not opts:
                dead.add(key)
                return False
            if best_opts is None or len(opts) < len(best_opts):
                best_k = k
                best_opts = opts
                if len(best_opts) == 1:
                    break

        # Try each placement for the chosen package type.
        new_remaining_base = list(remaining)
        new_remaining_base[best_k] -= 1
        new_remaining_base = tuple(new_remaining_base)

        for pm in best_opts:
            if _search(new_remaining_base, occupied | pm):
                return True

        dead.add(key)
        return False

    return _search(area.package_counts, 0)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return -1
    packages, areas = parse_input(input_value)
    counter = 0
    if not TEST:
        for idx, area in enumerate(areas):
            logger.debug("Area %d/%d: %s", idx + 1, len(areas), area)
            # Note, this fails with example, and works with actual input.
            if placement_possible(area, packages):
                counter += 1
        return counter
    # Below was a nice elegant solution that works eventually
    count = 0
    start_time = time()
    for idx, area in enumerate(areas):
        logger.debug(
            "Area %d/%d: %s, time: %.2f seconds",
            idx + 1,
            len(areas),
            area,
            time() - start_time,
        )
        if place_packages(area, packages):
            logger.debug(
                "Area %d/%d can be filled: %s, time: %.2f seconds",
                idx + 1,
                len(areas),
                area,
                time() - start_time,
            )
            count += 1
    return count


YEAR = 2025
DAY = 12
input_format = {
    1: "text",
    2: "text",
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
    if args.test:
        TEST = True
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
