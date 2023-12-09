def next_element(history: list[int]) -> int:
    diffs_lst = [history]
    while True:
        last_diffs = diffs_lst[-1]
        diffs = [b - a for a, b in zip(last_diffs, last_diffs[1:])]
        if all(diff == 0 for diff in diffs):
            break
        diffs_lst.append(diffs)

    return sum(diffs[-1] for diffs in diffs_lst)


def main() -> None:
    with open("input.txt") as f:
        lines = f.readlines()

    histories = [list(map(int, line.split())) for line in lines]

    sum_extrapolated = sum(next_element(history) for history in histories)
    print("Sum (Part 1):", sum_extrapolated)

    for history in histories:
        history.reverse()

    sum_extrapolated = sum(next_element(history) for history in histories)
    print("Sum (Part 2 ):", sum_extrapolated)


if __name__ == "__main__":
    main()
