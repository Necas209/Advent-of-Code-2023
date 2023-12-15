"""Day 13: Point of Incidence"""
from itertools import groupby
from typing import Any
import numpy as np
import numpy.typing as npy


def find_reflection_line(pattern: npy.NDArray[Any], dims: int) -> int:
    """Finds reflection line and returns the number of rows above it"""
    max_smudges = 1
    # Check for identical rows
    midpoint = dims // 2
    left_side = midpoint
    right_side = midpoint

    def check_side(curr_idx: int, diff: int) -> int:
        if diff > max_smudges:
            return 0
        smudge_found = diff == max_smudges
        j = 1
        left = curr_idx - 1
        right = curr_idx + 2
        while left >= 0 and right < dims:
            diff = np.count_nonzero(pattern[left] != pattern[right])
            if smudge_found:
                if diff != 0:
                    smudge_found = False
                    break
            else:
                if diff > max_smudges:
                    break
                if diff == max_smudges:
                    smudge_found = True
            j += 1
            left = curr_idx - j
            right = curr_idx + j + 1
        else:
            if smudge_found:
                return curr_idx + 1
        return 0

    while left_side >= 0 or right_side < dims:
        count = 0
        if left_side >= 0:
            diff = np.count_nonzero(pattern[left_side] != pattern[left_side + 1])
            count = check_side(left_side, diff)
        if count == 0 and right_side < dims - 1:
            diff = np.count_nonzero(pattern[right_side] != pattern[right_side + 1])
            count = check_side(right_side, diff)
        if count != 0:
            return count
        left_side -= 1
        right_side += 1
    return 0


def main() -> None:
    """Main Function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    patterns = [list(line.strip()) for line in lines]
    patterns = [
        np.array(list(group))
        for key, group in groupby(patterns, lambda x: not x)
        if not key
    ]

    summary = 0
    for pattern in patterns:
        n_rows, n_cols = pattern.shape
        # Check for identical rows
        count = find_reflection_line(pattern, n_rows)
        summary += 100 * count
        if count != 0:
            continue
        # Check for identical columns
        count = find_reflection_line(pattern.T, n_cols)
        summary += count

    print("Summary:", summary)


if __name__ == "__main__":
    main()
