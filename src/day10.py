"""Day 10: Pipe Maze"""

from typing import Protocol
from shapely import Polygon, Point  # type: ignore


Position = tuple[int, int]


def find_first_adjacent_pipe(x: int, y: int, lines: list[str]) -> Position:
    "Find coordinates of the first adjacent pipe"
    if (x - 1) >= 0 and lines[y][x - 1] in "-LF":
        return x - 1, y
    if (x + 1) < len(lines[0]) and lines[y][x + 1] in "-J7":
        return x + 1, y
    if (y - 1) >= 0 and lines[y - 1][x] in "|7F":
        return x, y - 1
    if (y + 1) < len(lines) and lines[y + 1][x] in "|LJ":
        return x, y + 1
    return x, y


class PolygonProtocol(Protocol):
    def contains(self, other: Point) -> bool:
        ...


def calculate_path(
    x: int, y: int, lines: list[str]
) -> tuple[list[Position], PolygonProtocol]:
    """Calculates the path and its respective bounding polygon"""
    prev_x, prev_y = x, y
    curr_x, curr_y = find_first_adjacent_pipe(x, y, lines)
    path: list[Position] = []
    while True:
        temp = curr_x, curr_y
        path.append(temp)
        match lines[curr_y][curr_x]:
            case "S":
                break
            case "|":
                curr_y += 1 if curr_y > prev_y else -1
            case "-":
                curr_x += 1 if curr_x > prev_x else -1
            case char:
                if curr_y == prev_y:
                    if char in "LJ":
                        curr_y -= 1
                    else:
                        curr_y += 1
                else:
                    if char in "J7":
                        curr_x -= 1
                    else:
                        curr_x += 1
        prev_x, prev_y = temp
    return path, Polygon(path)


def find_start(lines: list[str]) -> Position:
    x, y = 0, 0
    for y, line in enumerate(lines):
        if (x := line.find("S")) != -1:
            break
    return x, y


def main() -> None:
    "Main function"
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    x, y = find_start(lines)
    print(f"Start = ({x}, {y})")

    path, polygon = calculate_path(x, y, lines)
    print("Loop length:", len(path))
    print("Farthest:", len(path) // 2)

    count = sum(
        polygon.contains(Point(x, y))
        for y, line in enumerate(lines)
        for x, _ in enumerate(line)
        if (x, y) not in path
    )

    print("Count:", count)


if __name__ == "__main__":
    main()
