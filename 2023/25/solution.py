"""
Advent Of Code 2023 day 25

"""

# import system modules
import logging
import argparse
import networkx as nx


# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(lines: list[str]) -> set[tuple[str, str]]:
    """parse input data into edges set"""
    edges = set();

    for line in lines:
        # jqt: rhn xhk nvd
        a, b = line.split(': ')
        b = b.split(' ')

        for c in b:
            edges.add((a,c))
            edges.add((c,a))
    return edges

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return None
    edges = parse_input(input_value)
    graph = nx.from_edgelist(edges)
    edge_betweenness = nx.edge_betweenness_centrality(graph)
    most_crucial_edges = sorted(edge_betweenness, key=edge_betweenness.get)[-3:]
    graph.remove_edges_from(most_crucial_edges)
    size1, size2 = [len(c) for c in nx.connected_components(graph)]
    return  size1 * size2


YEAR = 2023
DAY = 25
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
