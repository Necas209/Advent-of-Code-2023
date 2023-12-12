"""Day 11: Cosmic Expansion"""
from dataclasses import dataclass
from itertools import combinations
import numpy as np


@dataclass
class Space:
    "Empty Space class"
    empty_rows: list[int]
    empty_cols: list[int]
    expansion_rate: int = 2


Position = tuple[int, int]


def calculate_path_length(galaxy1: Position, galaxy2: Position, space: Space) -> int:
    """Calculates the length of the path between two galaxies, given the space they reside in"""
    x_min, x_max = min(galaxy1[0], galaxy2[0]), max(galaxy1[0], galaxy2[0])
    y_min, y_max = min(galaxy1[1], galaxy2[1]), max(galaxy1[1], galaxy2[1])

    no_rows_between = sum(x_min < row < x_max for row in space.empty_rows)
    no_cols_between = sum(y_min < col < y_max for col in space.empty_cols)

    x_max += no_rows_between * (space.expansion_rate - 1)
    y_max += no_cols_between * (space.expansion_rate - 1)

    diff_x = x_max - x_min
    diff_y = y_max - y_min

    if x_min == x_max:
        return diff_y
    if y_min == y_max:
        return diff_x
    return diff_x + diff_y


def main() -> None:
    """Main function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [list(line.strip()) for line in lines]
    space = np.array(lines)

    galaxies = list(zip(*np.where(space == "#")))
    pairs_of_galaxies = combinations(galaxies, 2)

    empty_rows = [i for i, row in enumerate(space) if np.all(row == ".")]
    empty_cols = [i for i, col in enumerate(space.T) if np.all(col == ".")]
    space = Space(empty_rows, empty_cols, expansion_rate=1_000_000)

    path_length_sum = sum(
        calculate_path_length(*pair_of_galaxies, space)
        for pair_of_galaxies in pairs_of_galaxies
    )
    print("Sum:", path_length_sum)


if __name__ == "__main__":
    main()
