import time


def main() -> None:
    with open("input.txt") as f:
        lines = f.readlines()
    
    lines = [line.split(": ")[1] for line in lines]

    points = 0
    scratchcards: list[int] = len(lines) * [1]

    start = time.perf_counter()
    for i, line in enumerate(lines, 1):
        nums = line.split(" | ")
        winning_nums = set(map(int, nums[0].split()))
        have_nums = set(map(int, nums[1].split()))
        matches = winning_nums & have_nums
        no_matches = len(matches)
        if no_matches > 0:
            points += 2 ** (no_matches - 1)
        for _ in range(scratchcards[i - 1]):
            for j in range(i, i + no_matches):
                scratchcards[j] += 1
    end = time.perf_counter()

    print("Points:", points)
    print("Scratchcards:", sum(scratchcards))
    print(f"Algorithm took {end - start:.3f}s")


if __name__ == "__main__":
    main()