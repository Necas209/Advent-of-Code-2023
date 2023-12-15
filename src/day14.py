"""Day 14: Parabolic Reflector Dish"""
from typing import Any
import numpy as np
import numpy.typing as npy


Platform = npy.NDArray[Any]


ROUND_ROCK = ord("O")
CUBE_ROCK = ord("#")
EMPTY_SPACE = ord(".")


def tilt_north(platform: Platform) -> None:
    """Tilt the platform north"""
    for x, col in enumerate(platform.T):
        for y in range(col.shape[0]):
            for j in range(0, col.shape[0] - y - 1):
                if platform[j, x] == EMPTY_SPACE and platform[j + 1, x] == ROUND_ROCK:
                    platform[j, x], platform[j + 1, x] = (
                        platform[j + 1, x],
                        platform[j, x],
                    )


def cycle_platform(platform: Platform) -> None:
    """Cycle the platform"""
    # North
    tilt_north(platform)
    # West
    for y, row in enumerate(platform):
        for x in range(row.shape[0]):
            for j in range(0, row.shape[0] - x - 1):
                if platform[y, j] == EMPTY_SPACE and platform[y, j + 1] == ROUND_ROCK:
                    platform[y, j], platform[y, j + 1] = (
                        platform[y, j + 1],
                        platform[y, j],
                    )
    # South
    for x, col in enumerate(platform.T):
        for y in range(col.shape[0]):
            for j in range(0, col.shape[0] - y - 1):
                if platform[j, x] == ROUND_ROCK and platform[j + 1, x] == EMPTY_SPACE:
                    platform[j, x], platform[j + 1, x] = (
                        platform[j + 1, x],
                        platform[j, x],
                    )
    # East
    for y, row in enumerate(platform):
        for x in range(row.shape[0]):
            for j in range(0, row.shape[0] - x - 1):
                if platform[y, j] == ROUND_ROCK and platform[y, j + 1] == EMPTY_SPACE:
                    platform[y, j], platform[y, j + 1] = (
                        platform[y, j + 1],
                        platform[y, j],
                    )


def compute_total_load(platform: Platform) -> int:
    """Computes total load of platform"""
    return sum(
        (platform.shape[0] - i) * np.count_nonzero(row == ROUND_ROCK)
        for i, row in enumerate(platform)
    )


def main() -> None:
    """Main Function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    platform = np.array([list(line.strip()) for line in lines])
    vectorized_ord = np.vectorize(ord)
    platform: Platform = vectorized_ord(platform)

    cycles: list[bytes] = []
    cycle_start = 0
    i = 0
    while True:
        cycle_platform(platform)
        cycle_str = platform.tobytes()
        if cycle_str in cycles:
            cycle_start = cycles.index(cycle_str)
            break
        cycles.append(cycle_str)
        i += 1

    num_cycles = 1_000_000_000
    cycle_length = i - cycle_start
    idx = cycle_start + (num_cycles - cycle_start) % cycle_length - 1
    cycle = np.frombuffer(cycles[idx], platform.dtype).reshape(platform.shape)

    total_load = compute_total_load(cycle)
    print("Total load:", total_load)


if __name__ == "__main__":
    main()
