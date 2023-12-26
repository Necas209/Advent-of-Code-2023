"""Day 24: Never Tell Me The Odds"""
from itertools import combinations
import re

import numpy as np
from z3 import IntVector, ModelRef, Solver  # type: ignore


def part1(hailstones: list[list[int]]) -> int:
    """Part 1"""
    count = 0
    for h1, h2 in combinations(hailstones, 2):
        p1, p2, _, dp1, dp2, _ = h1
        q1, q2, _, dq1, dq2, _ = h2
        sp = dp2 / dp1
        sq = dq2 / dq1
        if sp == sq:
            continue
        sol = np.linalg.solve(
            np.array([[-sp, 1], [-sq, 1]]), [p2 - sp * p1, q2 - sq * q1]
        )
        if (sol[0] - p1) / dp1 < 0 or (sol[0] - q1) / dq1 < 0:
            continue
        if (
            200000000000000 <= sol[0] <= 400000000000000
            and 200000000000000 <= sol[1] <= 400000000000000
        ):
            count += 1
    return count


def part2(hailstones: list[list[int]]) -> int:
    """Part 2"""
    q1, q2, q3, dq1, dq2, dq3 = IntVector("sol", 6)

    def create_model() -> ModelRef:
        ts = IntVector("t", len(hailstones))
        s = Solver()

        for t, (p1, p2, p3, dp1, dp2, dp3) in zip(ts, hailstones):
            s.add(q1 + t * dq1 == p1 + t * dp1)  # type: ignore
            s.add(q2 + t * dq2 == p2 + t * dp2)  # type: ignore
            s.add(q3 + t * dq3 == p3 + t * dp3)  # type: ignore

        s.check()  # type: ignore
        return s.model()

    model = create_model()

    return sum(model[v].as_long() for v in (q1, q2, q3))  # type: ignore


def main() -> None:
    """Main Function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    hailstones = [list(map(int, re.findall(r"-?\d+", line))) for line in lines]

    count = part1(hailstones)
    print("Part 1:", count)

    result = part2(hailstones)
    print("Part 2:", result)


if __name__ == "__main__":
    main()
