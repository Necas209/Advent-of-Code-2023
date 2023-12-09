from dataclasses import dataclass
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


@dataclass
class Char:
    value: str
    adjacent: int = 0
    ratio: int = 1

    @property
    def is_gear(self) -> bool:
        return self.adjacent == 2


@dataclass
class Number:
    value: int = -1
    index: Point = Point(-1, -1)
    length: int = 0

    def is_part_number(self, lines: list[list[Char]]) -> bool:
        start_x = max(self.index.x - 1, 0)
        end_x = min(self.index.x + self.length, len(lines[0]) - 1)
        start_y = max(self.index.y - 1, 0)
        end_y = min(self.index.y + 1, len(lines) - 1)
        for line in lines[start_y : end_y + 1]:
            for char in line[start_x : end_x + 1]:
                if char.value != "*":
                    continue

                char.adjacent += 1
                char.ratio *= self.value
                return True
        return False


def main() -> None:
    with open("input.txt") as f:
        chars = f.readlines()
    chars = [[Char(char) for char in line.strip()] for line in chars]

    found_num = False
    numbers: list[Number] = []

    for y, line in enumerate(chars):
        number = Number()
        for x, char in enumerate(line):
            if not char.value.isdigit():
                found_num = False
                if number.value != -1:
                    numbers.append(number)
                number = Number()
                continue
            if not found_num:
                found_num = True
                number.value = int(char.value)
                number.index = Point(x, y)
            else:
                number.value = 10 * number.value + int(char.value)
            number.length += 1
        if number.value != -1:
            numbers.append(number)

    assert all(len(str(num.value)) == num.length for num in numbers)
    assert all(
        str(num.value)[0] == chars[num.index.y][num.index.x].value for num in numbers
    )

    print(*numbers, sep="\n")
    print(len(numbers))

    part_numbers_sum = sum(
        number.value for number in numbers if number.is_part_number(chars)
    )
    print("Sum:", part_numbers_sum)

    print(
        "Gear ratios:",
        sum(char.ratio for line in chars for char in line if char.is_gear),
    )


if __name__ == "__main__":
    main()
