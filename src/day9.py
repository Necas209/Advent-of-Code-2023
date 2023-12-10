"""Day 9: Mirage Maintenance"""


def compute_next_element(sequence: list[int]) -> int:
    """Return the next element in the sequence"""
    next_element = 0
    while True:
        if all(el == 0 for el in sequence):
            break
        next_element += sequence[-1]
        sequence = [b - a for a, b in zip(sequence, sequence[1:])]
    return next_element


def main() -> None:
    """Main function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    histories = [list(map(int, line.split())) for line in lines]

    next_element_sum = sum(map(compute_next_element, histories))
    print("Sum (Part 1):", next_element_sum)

    for history in histories:
        history.reverse()

    next_element_sum = sum(map(compute_next_element, histories))
    print("Sum (Part 2 ):", next_element_sum)


if __name__ == "__main__":
    main()
