from dataclasses import dataclass
import math


@dataclass
class Node:
    """Node class"""
    left: int
    right: int
    is_z: bool = False


def get_ascii_value(s: str) -> int:
    """Return ascii value of string"""
    res = 0
    for char in s:
        res = res * 26 + ord(char) - ord("A")
    return res


def no_steps_to_z(node: Node, network: list[Node], instructions: list[int]):
    """Return number of steps to Z"""
    steps = 0
    while True:
        for instruction in instructions:
            if node.is_z:
                return steps
            if instruction == 0:  # "L"
                data = node.left
            else:  # "R"
                data = node.right
            node = network[data]
            steps += 1


def main() -> None:
    """Main function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = list(map(str.strip, f.readlines()))

    instructions = [0 if char == "L" else 1 for char in lines[0]]

    network: list[Node] = 26**3 * [None]  # type: ignore
    nodes_end_with_a: list[Node] = []

    first_node = None
    for line in lines[2:]:
        data, jump = line.split(" = ")
        left, right = jump[1:-1].split(", ")
        idx = get_ascii_value(data)
        network[idx] = Node(get_ascii_value(left), get_ascii_value(right))
        if first_node is None:
            first_node = network[idx]
        if data.endswith("A"):
            nodes_end_with_a.append(network[idx])
        if data.endswith("Z"):
            network[idx].is_z = True

    steps = [no_steps_to_z(node, network, instructions) for node in nodes_end_with_a]
    min_steps = math.lcm(*steps)
    print("Number of steps:", min_steps)


if __name__ == "__main__":
    main()
