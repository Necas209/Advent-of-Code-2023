"""Day 21: Step Counter"""
from dataclasses import dataclass


Position = tuple[int, int]


@dataclass
class Garden:
    """Garden Class"""

    rocks: set[Position]
    start: Position
    extents: Position


def walk_garden(garden: Garden, steps: int) -> int:
    """Returns the number of garden plots reached after a given number of steps"""
    height, width = garden.extents

    curr_positions: set[Position] = {garden.start}
    for _ in range(steps):
        new_positions: set[Position] = set()
        for c_y, c_x in curr_positions:
            new_positions |= {
                new_pos
                for m_y, m_x in [(1, 0), (0, 1), (-1, 0), (0, -1)]
                if 0 <= (n_y := c_y + m_y) < height
                and 0 <= (n_x := c_x + m_x) < width
                and (new_pos := (n_y, n_x)) not in garden.rocks
            }
        curr_positions = new_positions

    return len(curr_positions)


def compute_part2(garden: Garden) -> int:
    """Computes the solution for Part 2"""
    b0 = walk_garden(garden, 65)
    b1 = walk_garden(garden, 65 + 131)
    b2 = walk_garden(garden, 65 + 2 * 131)
    n = 202300

    # Cramer's Rule to solve for x0, x1, x2
    det_a = -2
    det_a0 = -b0 + 2 * b1 - b2
    det_a1 = 3 * b0 - 4 * b1 + b2
    det_a2 = -2 * b0

    # Calculate x0, x1, x2
    x0 = det_a0 // det_a
    x1 = det_a1 // det_a
    x2 = det_a2 // det_a

    # Calculate the result using the obtained values
    result = x0 * n * n + x1 * n + x2
    return result


def build_garden(lines: list[str], expand: int = 1) -> Garden:
    """Builds garden from content"""
    num_rows, num_cols = len(lines), len(lines[0])
    start = num_rows * expand // 2, num_cols * expand // 2
    extents = num_rows * expand, num_cols * expand

    rocks: set[Position] = set()
    for row, line in enumerate(lines):
        for col, ch in enumerate(line):
            if ch == "#":
                rocks.add((row, col))

    if expand <= 1:
        return Garden(rocks, start, extents)

    expanded_rocks: set[Position] = set()
    for rock in rocks:
        for row_mul in range(expand):
            for col_mul in range(expand):
                expanded_rocks.add(
                    (rock[0] + num_rows * row_mul, rock[1] + num_cols * col_mul)
                )

    return Garden(expanded_rocks, start, extents)


def main() -> None:
    """Main Function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    garden = build_garden(lines)
    print("Part 1:", walk_garden(garden, steps=64))

    garden = build_garden(lines, expand=5)
    print("Part 2:", compute_part2(garden))


if __name__ == "__main__":
    main()
