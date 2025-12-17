"""
Advent Of Code 2023 day 23

"""

# import system modules
import logging
import argparse
from collections import defaultdict, deque
from functools import cache

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(lines: list[str]) -> tuple[tuple[str, ...], ...]:
    """parse input data into grid"""
    # Split the data into lines
    grid = []
    for line in lines:
        grid.append(tuple(list(line)))
    return tuple(grid)


def neighbors(
    grid: tuple[tuple[str, ...], ...], r: int, c: int, ignore_slopes: bool
):
    """get neighbor coordinates from (r,c)"""
    logger.debug("neighbors r=%d c=%d", r, c)
    cell = grid[r][c]
    logger.debug("cell=%s", cell)

    if ignore_slopes or cell == ".":
        for r, c in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            logger.debug("checking neighbor r=%d c=%d", r, c)
            logger.debug("len(grid)=%d", len(grid))
            logger.debug("len(grid[r])=%d", len(grid[r]) if 0 <= r < len(grid) else -1)
            if r >= len(grid):
                continue
            if grid[r][c] != "#":
                yield r, c
    elif cell == "v":
        yield (r + 1, c)
    elif cell == "^":
        yield (r - 1, c)
    elif cell == ">":
        yield (r, c + 1)
    elif cell == "<":
        yield (r, c - 1)


def num_neighbors(
    grid: tuple[tuple[str, ...], ...], r: int, c: int, ignore_slopes: bool
) -> int:
    """count number of neighbors from (r,c)"""
    if ignore_slopes or grid[r][c] == ".":
        return sum(
            grid[r][c] != "#"
            for r, c in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
        )
    return 1


def is_node(
    grid: tuple[tuple[str, ...], ...],
    rc: tuple[int, int],
    src: tuple[int, int],
    dst: tuple[int, int],
    ignore_slopes: bool,
) -> bool:
    """determine if rc is a node"""
    return rc == src or rc == dst or num_neighbors(grid, *rc, ignore_slopes) > 2


def adjacent_nodes(
    grid: tuple[tuple[str, ...], ...],
    rc: tuple[int, int],
    src: tuple[int, int],
    dst: tuple[int, int],
    ignore_slopes: bool = False,
) -> tuple[tuple[tuple[int, int], int], ...]:
    """find adjacent nodes from rc"""
    q = deque([(rc, 0)])
    seen = set()

    while q:
        rc, dist = q.popleft()
        seen.add(rc)

        for n in neighbors(grid, *rc, ignore_slopes):
            if n in seen:
                continue

            if is_node(grid, n, src, dst, ignore_slopes):
                yield (n, dist + 1)
                continue

            q.append((n, dist + 1))


def graph_from_grid(
    grid: tuple[tuple[str, ...], ...],
    src: tuple[int, int],
    dst: tuple[int, int],
    ignore_slopes: bool = False,
) -> dict[tuple[int, int], list[tuple[tuple[int, int], int]]]:
    """Generate graph from grid"""
    g = defaultdict(list)
    q = deque([src])
    seen = set()

    while q:
        rc = q.popleft()
        if rc in seen:
            continue

        seen.add(rc)

        for n, weight in adjacent_nodes(grid, rc, src, dst, ignore_slopes):
            g[rc].append((n, weight))
            q.append(n)

    return g


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = parse_input(input_value)
    start = (0, grid[0].index("."))
    end = (len(grid) - 1, grid[-1].index("."))
    graph = graph_from_grid(grid, start, end)
    return len(graph)


YEAR = 2023
DAY = 23
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
