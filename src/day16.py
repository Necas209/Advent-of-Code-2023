"""Day 16: The Floor Will Be Lava"""
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


class Position(NamedTuple):
    """Position Tuple"""

    x: int
    y: int


class BeamState(Enum):
    """Beam State Enum"""

    LEFT = "<"
    RIGHT = ">"
    UP = "^"
    DOWN = "v"


HORIZONTAL_STATES = set([BeamState.LEFT, BeamState.RIGHT])
VERTICAL_STATES = set([BeamState.UP, BeamState.DOWN])


@dataclass
class Tile:
    """Grid Tile Class"""

    state: str | BeamState
    energized: bool = False


def move_beam(
    grid: list[list[Tile]], start_pos: Position, start_state: BeamState
) -> None:
    """Move beam across the grid, starting in the given position"""
    size = len(grid[0]), len(grid)

    def is_valid(pos: Position) -> bool:
        """Check if a given position is valid in the grid"""
        return 0 <= pos.x < size[0] and 0 <= pos.y < size[1]

    curr_pos = start_pos
    curr_state = start_state

    while True:
        if not is_valid(curr_pos):
            return
        curr_tile = grid[curr_pos.y][curr_pos.x]
        if curr_tile.state == curr_state:
            return
        curr_tile.energized = True
        match curr_tile.state:
            case "/":
                match curr_state:
                    case BeamState.RIGHT:
                        curr_pos = Position(curr_pos.x, curr_pos.y - 1)
                        curr_state = BeamState.UP
                    case BeamState.LEFT:
                        curr_pos = Position(curr_pos.x, curr_pos.y + 1)
                        curr_state = BeamState.DOWN
                    case BeamState.DOWN:
                        curr_pos = Position(curr_pos.x - 1, curr_pos.y)
                        curr_state = BeamState.LEFT
                    case BeamState.UP:
                        curr_pos = Position(curr_pos.x + 1, curr_pos.y)
                        curr_state = BeamState.RIGHT
            case "\\":
                match curr_state:
                    case BeamState.RIGHT:
                        curr_pos = Position(curr_pos.x, curr_pos.y + 1)
                        curr_state = BeamState.DOWN
                    case BeamState.LEFT:
                        curr_pos = Position(curr_pos.x, curr_pos.y - 1)
                        curr_state = BeamState.UP
                    case BeamState.DOWN:
                        curr_pos = Position(curr_pos.x + 1, curr_pos.y)
                        curr_state = BeamState.RIGHT
                    case BeamState.UP:
                        curr_pos = Position(curr_pos.x - 1, curr_pos.y)
                        curr_state = BeamState.LEFT
            case "|":
                if curr_state in HORIZONTAL_STATES:
                    upper_pos = Position(curr_pos.x, curr_pos.y - 1)
                    bottom_pos = Position(curr_pos.x, curr_pos.y + 1)
                    move_beam(grid, upper_pos, BeamState.UP)
                    move_beam(grid, bottom_pos, BeamState.DOWN)
                    return
                flag = 1 if curr_state == BeamState.DOWN else -1
                curr_pos = Position(curr_pos.x, curr_pos.y + flag)
            case "-":
                if curr_state in VERTICAL_STATES:
                    left_pos = Position(curr_pos.x - 1, curr_pos.y)
                    right_pos = Position(curr_pos.x + 1, curr_pos.y)
                    move_beam(grid, left_pos, BeamState.LEFT)
                    move_beam(grid, right_pos, BeamState.RIGHT)
                    return
                flag = 1 if curr_state == BeamState.RIGHT else -1
                curr_pos = Position(curr_pos.x + flag, curr_pos.y)
            case "." | _:
                match curr_state:
                    case BeamState.RIGHT:
                        curr_pos = Position(curr_pos.x + 1, curr_pos.y)
                    case BeamState.LEFT:
                        curr_pos = Position(curr_pos.x - 1, curr_pos.y)
                    case BeamState.DOWN:
                        curr_pos = Position(curr_pos.x, curr_pos.y + 1)
                    case BeamState.UP:
                        curr_pos = Position(curr_pos.x, curr_pos.y - 1)
                curr_tile.state = curr_state


def compute_total_energized(grid: list[list[Tile]]) -> int:
    """Computes the total number of energized tiles"""
    return sum(tile.energized for row in grid for tile in row)


def main() -> None:
    """Main Function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = list(map(str.strip, lines))

    max_energized = 0
    size = len(lines[0]), len(lines)

    # Left
    for i in range(size[1]):
        grid = [list(map(Tile, line)) for line in lines]
        start = Position(0, i)
        move_beam(grid, start, BeamState.RIGHT)
        total_energized = compute_total_energized(grid)
        max_energized = max(max_energized, total_energized)

    # Right
    for i in range(size[1]):
        grid = [list(map(Tile, line)) for line in lines]
        start = Position(size[0] - 1, i)
        move_beam(grid, start, BeamState.LEFT)
        total_energized = compute_total_energized(grid)
        max_energized = max(max_energized, total_energized)

    # Top
    for i in range(size[0]):
        grid = [list(map(Tile, line)) for line in lines]
        start = Position(i, 0)
        move_beam(grid, start, BeamState.DOWN)
        total_energized = compute_total_energized(grid)
        max_energized = max(max_energized, total_energized)

    # Bottom
    for i in range(size[0]):
        grid = [list(map(Tile, line)) for line in lines]
        start = Position(i, size[1] - 1)
        move_beam(grid, start, BeamState.UP)
        total_energized = compute_total_energized(grid)
        max_energized = max(max_energized, total_energized)

    print("Total energized:", max_energized)


if __name__ == "__main__":
    main()
