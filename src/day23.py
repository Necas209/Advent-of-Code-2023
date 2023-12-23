"""Day 23: A Long Walk"""
from collections import defaultdict
from dataclasses import dataclass, field
from typing import ClassVar, NamedTuple


class Position(NamedTuple):
    """Position Tuple"""

    x: int = 0
    y: int = 0


@dataclass
class MountainMap:
    """Mountain Map Class"""

    _map: list[list[str]]
    start: Position = field(default_factory=Position)
    end: Position = field(default_factory=Position)

    _directions: ClassVar[list[tuple[int, int]]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __post_init__(self) -> None:
        self.start = Position(1, 0)
        self.end = Position(self.width - 2, self.height - 1)

    @property
    def height(self) -> int:
        """Height of the map"""
        return len(self._map)

    @property
    def width(self) -> int:
        """Width of the map"""
        return len(self._map[0])

    def cell(self, pos: Position) -> str:
        """Returns the map cell for the given position"""
        return self._map[pos.y][pos.x]

    def possible_next_steps(
        self, pos: Position, visited: set[Position]
    ) -> list[Position]:
        """Returns a set with the next possible steps, given the current position"""
        return [
            new_pos
            for m_y, m_x in MountainMap._directions
            if 0 <= (n_y := pos.y + m_y) < self.height
            and 0 <= (n_x := pos.x + m_x) < self.width
            and (new_pos := Position(n_x, n_y)) not in visited
            and self.cell(new_pos) != "#"
        ]


def hike_part1(
    mountain_map: MountainMap,
    start: Position,
    visited: set[Position] | None = None,
) -> int:
    """Take a hike (Part 1)"""
    if visited is None:
        visited = set()

    curr_pos = start
    count = 0
    while curr_pos != mountain_map.end:
        visited.add(curr_pos)
        match mountain_map.cell(curr_pos):
            case ".":
                new_positions = mountain_map.possible_next_steps(curr_pos, visited)
                match len(new_positions):
                    case 0:
                        return 0
                    case 1:
                        curr_pos = new_positions[0]
                    case _:
                        count += max(
                            hike_part1(mountain_map, pos, visited.copy())
                            for pos in new_positions
                        )
                        return count

            case "^":
                curr_pos = Position(curr_pos.x, curr_pos.y - 1)
            case ">":
                curr_pos = Position(curr_pos.x + 1, curr_pos.y)
            case "v":
                curr_pos = Position(curr_pos.x, curr_pos.y + 1)
            case "<":
                curr_pos = Position(curr_pos.x - 1, curr_pos.y)
            case _:
                pass
        count += 1
    return count


def hike_part2(grid: list[list[str]], start: Position) -> int:
    """Take a hike (Part 2)"""
    target = len(grid) - 1, len(grid[0]) - 2

    def create_graph() -> tuple[Position, int]:
        queue = [(start, start, {start, (0, 1)})]
        final_node = Position()
        final_steps = 0
        while queue:
            curr_xy, prev_node, visited = queue.pop()
            if curr_xy == target:
                final_node = prev_node
                final_steps = len(visited) - 1
                continue

            (x, y) = curr_xy
            neighbors: list[Position] = []
            for i, j in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (i, j) in visited or grid[i][j] == "#":
                    continue
                neighbors.append(Position(i, j))

            if len(neighbors) == 1:
                nxt_xy = neighbors.pop()
                queue.append((nxt_xy, prev_node, visited | {nxt_xy}))

            elif len(neighbors) > 1:
                steps = len(visited) - 1
                if (curr_xy, steps) in graph[prev_node]:
                    continue
                graph[prev_node].append((curr_xy, steps))
                graph[curr_xy].append((prev_node, steps))
                while neighbors:
                    nxt_xy = neighbors.pop()
                    queue.append((nxt_xy, curr_xy, {curr_xy, nxt_xy}))
        return final_node, final_steps

    # create graph where the nodes are the intersections of the grid
    graph: defaultdict[Position, list[tuple[Position, int]]] = defaultdict(list)
    final_node, final_steps = create_graph()

    # traverse graph
    max_steps = 0
    new_queue = [(start, int(0), {start})]
    while new_queue:
        curr, steps, visited = new_queue.pop()
        if curr == final_node:
            max_steps = max(steps, max_steps)
            continue
        for nxt, distance in graph[curr]:
            if nxt in visited:
                continue
            new_queue.append((nxt, steps + distance, visited | {nxt}))

    return max_steps + final_steps


def main() -> None:
    """Main Functions"""
    with open("input.txt", "r", encoding="utf-8") as f:
        content = f.read()

    grid = list(map(list, content.splitlines()))
    mountain_map = MountainMap(grid)

    print("Part 1:", hike_part1(mountain_map, mountain_map.start))

    print("Part 2:", hike_part2(grid, start=Position(1, 1)))


if __name__ == "__main__":
    main()
