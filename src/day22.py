"""Day 22: Sand Slabs"""
from dataclasses import dataclass, field
from typing import NamedTuple, Self


class Range(NamedTuple):
    """Range Tuple"""

    start: int
    stop: int


@dataclass(unsafe_hash=True)
class Brick:
    """Brick Class"""

    x: Range
    y: Range
    z: Range
    below: set[Self] = field(default_factory=set, hash=False)
    above: set[Self] = field(default_factory=set, hash=False)

    def is_below(self, other: Self) -> bool:
        """
        Checks for overlap in the x-y plane with self positioned below other along the z-axis.
        """
        return (
            (self.x.start <= other.x.stop and other.x.start <= self.x.stop)
            and (self.y.start <= other.y.stop and other.y.start <= self.y.stop)
            and (self.z.stop <= other.z.start)
        )

    def drop(self, new_z: int) -> None:
        """
        Drops the brick down to the specified lower z-value (new_z).
        """
        self.z = Range(new_z, new_z + (self.z.stop - self.z.start))

    def collapse(self) -> set[Self]:
        """
        Checks if the current brick is supported by a subset of <removed>.
        If true, mark it as removed and check if all bricks above it would fall (recursively).
        """
        removed = {self}
        for other in self.above:
            other.collapse_removed(removed)
        removed.remove(self)
        return removed

    def collapse_removed(self, removed: set[Self]) -> None:
        """Recursive method called in 'collapse'"""
        if not self.below.issubset(removed):
            return
        removed.add(self)
        for other in self.above:
            other.collapse_removed(removed)


def parse_bricks(lines: list[str]) -> list[Brick]:
    """Parses a list of strings and returns a list of Bricks"""

    def parse_brick(line: str) -> Brick:
        start, end = line.split("~")
        start = tuple(map(int, start.split(",")))
        end = tuple(map(int, end.split(",")))
        return Brick(
            x=Range(start[0], end[0]),
            y=Range(start[1], end[1]),
            z=Range(start[2], end[2]),
        )

    bricks = list(map(parse_brick, lines))
    bricks.sort(key=lambda brick: brick.z.start)

    by_zval: list[list[Brick]] = [[] for _ in range(bricks[-1].z.start)]

    # Adding the floor for bricks to land on; needed below to find the z-val
    base = parse_brick("0,0,0~1000,1000,0")
    settled = [base]
    for brick in bricks:
        top_z = max((other.z.stop for other in settled if other.is_below(brick)))
        brick.drop(top_z + 1)
        settled.append(brick)
        by_zval[top_z + 1].append(brick)

    # For each brick, find the bricks that it supports
    for brick in bricks:
        for other in by_zval[brick.z.stop + 1]:
            if brick.is_below(other):
                other.below.add(brick)
                brick.above.add(other)

    return bricks


def main() -> None:
    """Main Function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    bricks = parse_bricks(lines)

    remove_count = 0
    chain_count = 0
    for brick in bricks:
        if len(brick.above) == 0 or all(len(other.below) > 1 for other in brick.above):
            remove_count += 1
            continue

        supported = brick.collapse()
        chain_count += len(supported)

    print(f"Part 1: {remove_count}")
    print(f"Part 2: {chain_count}")


if __name__ == "__main__":
    main()
