import sys
import networkx as nx


def parse_input(data):
    edges = set();

    for line in data.splitlines():
        # jqt: rhn xhk nvd
        a, b = line.split(': ')
        b = b.split(' ')

        for c in b:
            edges.add((a,c))
            edges.add((c,a))
    return edges



def part1(parsed_data):
    retval = 0;
    graph = nx.from_edgelist(parsed_data)
    edge_betweenness = nx.edge_betweenness_centrality(graph)
    most_crucial_edges = sorted(edge_betweenness, key=edge_betweenness.get)[-3:]
    graph.remove_edges_from(most_crucial_edges)
    size1, size2 = [len(c) for c in nx.connected_components(graph)]
    retval =  size1 * size2
    return retval

def part2(parsed_data):
    retval = 0;
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data)

    #print("Part 1")
    answer1 = part1(parsed_data)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    