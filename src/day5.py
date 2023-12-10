"""Day 5: If You Give a Seed a Fertilizer"""
from dataclasses import dataclass


@dataclass
class Map:
    """Map class"""
    dest_start: int
    src_start: int
    length: int


def main() -> None:
    """Main function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line != "\n"]

    seed_pairs = list(map(int, lines[0].split(": ")[1].split()))
    ranges = [
        range(start, start + length) for start, length in zip(*[iter(seed_pairs)] * 2)
    ]

    list_of_maps: list[list[Map]] = []
    maps: list[Map] = []
    for line in lines[2:]:
        if line.endswith(":"):
            list_of_maps.append(sorted(maps, key=lambda x: x.src_start))
            maps.clear()
            continue
        dest_start, src_start, length = list(map(int, line.split()))
        new_map = Map(dest_start, src_start, length)
        maps.append(new_map)
    list_of_maps.append(sorted(maps, key=lambda x: x.src_start))
    list_of_maps.reverse()

    min_location = 0
    while True:
        seed = min_location
        for maps in list_of_maps:
            for to_map in maps:
                if to_map.dest_start <= seed < to_map.dest_start + to_map.length:
                    seed = to_map.src_start + seed - to_map.dest_start
                    break
        if any(seed in r for r in ranges):
            break
        min_location += 1

    print("Lowest location:", min_location)


if __name__ == "__main__":
    main()
