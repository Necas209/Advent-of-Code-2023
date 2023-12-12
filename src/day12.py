"""Day 12: Hot Springs"""
from collections import defaultdict
from itertools import product


def get_arrangement_count(row: str, groups: list[int]):
    """Computes the number of possible arrangements"""
    group_count = len(groups)
    arrangements: dict[tuple[int, int], int] = {}
    arrangements[0, 0] = 1

    def is_valid(group_index: int, current_group_size: int, strict: bool = True):
        if group_index >= len(groups):
            return False
        if strict:
            return current_group_size == groups[group_index]
        return current_group_size <= groups[group_index]

    for char in row:
        new_arrangements: defaultdict[tuple[int, int], int] = defaultdict(int)
        for (group_index, current_group_size), count in arrangements.items():
            valid = True
            if char == "#":
                current_group_size += 1
                valid = is_valid(group_index, current_group_size, False)
            elif char == "?":
                if current_group_size <= 0:
                    new_arrangements[group_index, current_group_size] += count
                elif is_valid(group_index, current_group_size):
                    new_arrangements[group_index + 1, 0] += count
                valid2 = is_valid(group_index, current_group_size + 1, False)
                new_arrangements[group_index, current_group_size + 1] += count * valid2
                continue
            elif current_group_size > 0:
                valid = is_valid(group_index, current_group_size)
                current_group_size = 0
                group_index += 1
            new_arrangements[group_index, current_group_size] += count * valid
        arrangements = new_arrangements

    total_count = 0
    for (group_index, current_group_size), count in arrangements.items():
        if group_index < len(groups) and current_group_size == groups[group_index]:
            group_index += 1
        elif current_group_size > 0:
            continue
        total_count += count * (group_index == group_count)
    return total_count


def get_arrangement_count_naive(springs: str, groups: list[int]) -> int:
    """Computes the number of possible arrangements"""
    count = 0
    groups_tuple = tuple(groups)
    for replacement in product(["#", "."], repeat=springs.count("?")):
        i = 0
        new_string = ""
        for char in springs:
            if char == "?":
                new_string += replacement[i]
                i += 1
            else:
                new_string += char
        spring_counts = tuple(map(len, new_string.replace(".", " ").split()))
        count += spring_counts == groups_tuple
    return count


def main() -> None:
    """Main function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    sum_arrangements = 0
    for line in lines:
        springs, groups = line.split()
        groups = list(map(int, groups.split(",")))

        springs = "?".join(5 * [springs])
        groups = 5 * groups

        sum_arrangements += get_arrangement_count(springs, groups)

    print("Sum:", sum_arrangements)


if __name__ == "__main__":
    main()
