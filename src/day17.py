"""Day 17: Clumsy Crucible"""
from heapq import heappop, heappush
from typing import NamedTuple

Position = tuple[int, int]
Grid = dict[complex, int]


class QueueItem(NamedTuple):
    """Queue Item tuple"""
    cost: int
    position: Position
    direction: Position

    def to_complex(self) -> tuple[complex, complex]:
        """Convert integer coordinates to complex ones"""
        return complex(*self.position), complex(*self.direction)


def dijkstra(grid: Grid, dest: complex, min_moves: int = 0, max_moves: int = 3) -> int:
    """Dijkstra's algorithm, adapted"""

    def c2t(c: complex) -> Position:
        return int(c.real), int(c.imag)

    pq: list[QueueItem] = []
    visited: dict[tuple[complex, complex], int] = {}

    for startd in [1, 1j, -1, -1j]:
        heappush(pq, QueueItem(0, c2t(0), c2t(startd)))

    while pq:
        item = heappop(pq)
        curr_block = item.to_complex()

        if curr_block in visited and visited[curr_block] <= item.cost:
            continue
        if curr_block[0] == dest:
            return item.cost

        visited[curr_block] = item.cost
        for turn in (1j, -1j):
            newd = curr_block[1] * turn
            newp = curr_block[0]
            new_cost = item.cost
            for i in range(1, max_moves + 1):
                newp += newd
                if newp not in grid:
                    break
                new_cost += grid[newp]
                if i > min_moves:
                    heappush(pq, QueueItem(new_cost, c2t(newp), c2t(newd)))
    raise ValueError("No solution found")


def main() -> None:
    """Main Function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    grid: Grid = {}
    p = complex()
    for r, line in enumerate(map(str.strip, lines)):
        for c, char in enumerate(line):
            p = c - r * 1j
            grid[p] = int(char)

    print("Heat loss (Part 1):", dijkstra(grid, dest=p))
    print("Heat loss (Part 2):", dijkstra(grid, dest=p, min_moves=3, max_moves=10))


if __name__ == "__main__":
    main()
