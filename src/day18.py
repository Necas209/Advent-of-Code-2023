"""Day 18: Lavaduct Lagoon"""
from dataclasses import dataclass
from enum import Enum
from functools import cache
from shapely import Polygon  # type: ignore


class Direction(Enum):
    """Direction Enum"""

    RIGHT = "R"
    DOWN = "D"
    LEFT = "L"
    UP = "U"


@cache
def get_directions() -> list[Direction]:
    """Returns a list of all directions"""
    return list(iter(Direction))


@dataclass
class DigStep:
    """Dig Step Class"""

    direction: Direction
    distance: int


def parse_line_part1(string: str) -> DigStep:
    """Parses a line according to Part 1's instructions"""
    direction, distance, _ = string.split()
    direction = Direction(direction)
    distance = int(distance)
    return DigStep(direction=direction, distance=distance)


def parse_line_part2(string: str) -> DigStep:
    """Parses a line according to Part 2's instructions"""
    _, _, color = string.split()
    color = color[2:-1]
    direction = get_directions()[int(color[-1])]
    distance = int(color[:-1], base=16)
    return DigStep(direction=direction, distance=distance)


def dig(steps: list[DigStep]) -> Polygon:
    """Digs a path in the lava lagoon"""
    path: list[tuple[int, int]] = [(0, 0)]
    for step in steps:
        curr_pos = path[-1]
        match step.direction:
            case Direction.LEFT:
                next_pos = curr_pos[0] - step.distance, curr_pos[1]
            case Direction.RIGHT:
                next_pos = curr_pos[0] + step.distance, curr_pos[1]
            case Direction.UP:
                next_pos = curr_pos[0], curr_pos[1] + step.distance
            case Direction.DOWN:
                next_pos = curr_pos[0], curr_pos[1] - step.distance
        path.append(next_pos)
    return Polygon(path)  # type: ignore


def compute_area(polygon: Polygon) -> int:
    """Computes the area of a polygon"""
    return int(polygon.area + polygon.length // 2 + 1)


def main() -> None:
    """Main Function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()

    steps = list(map(parse_line_part1, lines))
    polygon = dig(steps)
    print(f"Size of the lagoon (Part 1): {compute_area(polygon)}")

    steps = list(map(parse_line_part2, lines))
    polygon = dig(steps)
    print(f"Size of the lagoon (Part 2): {compute_area(polygon)}")


if __name__ == "__main__":
    main()
