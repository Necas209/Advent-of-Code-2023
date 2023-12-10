from dataclasses import dataclass
from functools import reduce
import operator


@dataclass
class Race:
    """Race class"""
    time: int
    distance: int

    def ways_to_win(self) -> int:
        num_ways = 0
        for acc_time in range(1, self.time + 1):
            curr_speed = acc_time
            curr_distance = (self.time - acc_time) * curr_speed
            if curr_distance > self.distance:
                num_ways += 1
        return num_ways


def main() -> None:
    """Main function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    times_str = lines[0].split()[1:]
    times = map(int, times_str)
    distances_str = lines[1].split()[1:]
    distances = map(int, distances_str)

    races = list(map(Race, times, distances))
    total = reduce(operator.mul, map(Race.ways_to_win, races))
    print("Answer (Part 1):", total)

    the_race = Race(int("".join(times_str)), int("".join(distances_str)))
    print("Answer (Part 2):", the_race.ways_to_win())


if __name__ == "__main__":
    main()
