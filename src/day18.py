"""Day 18: Lavaduct Lagoon"""
from dataclasses import dataclass
from enum import Enum
from typing import Callable


class Direction(Enum):
    """Direction Enum"""

    RIGHT = "R"
    DOWN = "D"
    LEFT = "L"
    UP = "U"


@dataclass
class DigStep:
    """Dig Step Class"""

    direction: Direction
    distance: int
    color: int


def parse_line_part1(string: str) -> DigStep:
    """Parses a line according to Part 1's instructions"""
    parts = string.split()
    return DigStep(
        direction=Direction(parts[0]),
        distance=int(parts[1]),
        color=int(parts[2][2:-1], base=16),
    )


DIRECTIONS = list(iter(Direction))


def parse_line_part2(string: str) -> DigStep:
    """Parses a line according to Part 2's instructions"""
    parts = string.split()
    color = parts[2][2:-1]
    return DigStep(
        direction=DIRECTIONS[int(color[-1])],
        distance=int(color[:-1], base=16),
        color=0,
    )


ParseFunc = Callable[[str], DigStep]


def get_area(lines: list[str], parse_func: ParseFunc) -> int:
    """Computes the area of the lava lagoon"""
    inside_sum = 0
    length = 0
    y = 0
    for line in lines:
        step = parse_func(line)
        length += step.distance
        match step.direction:
            case Direction.LEFT:
                inside_sum += y * step.distance
            case Direction.RIGHT:
                inside_sum -= y * step.distance
            case Direction.UP:
                y -= step.distance
            case Direction.DOWN:
                y += step.distance

    area = abs(inside_sum) + length // 2 + 1
    return area


def main() -> None:
    """Main Function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    parts: list[ParseFunc] = [parse_line_part1, parse_line_part2]

    for i, parse_func in enumerate(parts, 1):
        print(f"Size of the lagoon (Part {i}): {get_area(lines, parse_func)}")


if __name__ == "__main__":
    main()
