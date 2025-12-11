"""
Advent Of Code 2018 day 8

"""

# import system modules
from __future__ import annotations
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_nodes(in_data, nodes=None, node_id="0"):
    """
    Function to parse data
    Args:
        in_data: list(int()) puzzle input
        nodes: current node dict(), default: None
        node_id: current node_id str(), default: '0'

    Returns:
        data: list(int()) copy of in_data minus items used
        nodes: dict() updated node data
    """
    # init default
    if not nodes:
        nodes = {}
    # copy in_data to data
    data = list(in_data)
    # get header children=int(), metadata=int()
    children = data.pop(0)
    metadata = data.pop(0)
    # init new node
    nodes[node_id] = {"children": [], "metadata": []}
    # for idx in 1 to children
    for idx in range(1, children + 1):
        # new child_id
        child_id = f"{node_id}.{idx}"
        # add child_id to children
        nodes[node_id]["children"].append(child_id)
        # parse child recursively
        data, nodes = parse_nodes(data, nodes, child_id)
    # after we have all the children, lets get the metadata
    for _ in range(metadata):
        # pop(0) to for each metadata item
        nodes[node_id]["metadata"].append(data.pop(0))
    # return data, and nodes
    return data, nodes


def sum_metadata(nodes, node_id="0"):
    """
    Function to tally metadata count
    Args:
        nodes: dict{} node data
        node_id: str() current node, default:'0'
    """
    # get node for node_id
    node = nodes[node_id]
    # sum metadata
    metadata = sum(node["metadata"])
    # walk children
    for child_id in node["children"]:
        # add child metadata
        metadata += sum_metadata(nodes, child_id)
    # return
    return metadata


def score(nodes, node_id="0"):
    """
    Function to score node
    Args:
        nodes: dict() noda data
        node_id: str() current node id, default: '0'
    Returns:
        value: int() value of node

    If a node has no child nodes, its value is the sum of its metadata entries.
    So, the value of node B is 10+11+12=33, and the value of node D is 99.

    However, if a node does have child nodes, the metadata entries become indexes
    which refer to those child nodes. A metadata entry of 1 refers to the first child
    node, 2 to the second, 3 to the third, and so on. The value of this node is the sum
    of the values of the child nodes referenced by the metadata entries. If a referenced
    child node does not exist, that reference is skipped. A child node can be referenced
    multiple time and counts each time it is referenced. A metadata entry of 0 does not
    refer to any child node.
    """
    node = nodes[node_id]
    if len(node["children"]) == 0:
        # return sum of metadata
        return sum(node["metadata"])

    # walk metadata
    value = 0
    for child_ref in node["metadata"]:
        # skip invalid children
        if 0 < child_ref <= len(node["children"]):
            # child_ref 1, is first child node['children'][0]
            child_id = node["children"][child_ref - 1]
            value += score(nodes, child_id)
    return value


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # convert into dat to list of ints
    my_data = [int(num) for num in input_value.strip().split(" ")]
    # parse input data into node data
    my_data, my_nodes = parse_nodes(my_data)
    # Part 1: What is the sum of all metadata entries?
    result = sum_metadata(my_nodes)
    if part == 1:
        return result
    # Part 2: What is the value of the root node?
    return score(my_nodes)


YEAR = 2018
DAY = 8
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
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
