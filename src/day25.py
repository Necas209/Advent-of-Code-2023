"""Day 25: Snowverload"""
from math import prod
import networkx as nx  # type: ignore


def main() -> None:
    """Main function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    nodes: list[str] = []
    edges: list[tuple[str, str]] = []
    for line in lines:
        node, connections = line.split(": ")
        nodes.append(node)
        for connection in connections.split(" "):
            edges.append((node, connection))

    graph = nx.Graph()
    graph.add_nodes_from(nodes)  # type: ignore
    graph.add_edges_from(edges)  # type: ignore

    edges_to_remove = list(nx.minimum_edge_cut(graph))  # type: ignore
    graph.remove_edges_from(edges_to_remove) # type: ignore
    connected_components = list(nx.connected_components(graph))  # type: ignore

    print("Part 1:", prod(len(component) for component in connected_components)) # type: ignore

if __name__ == "__main__":
    main()
