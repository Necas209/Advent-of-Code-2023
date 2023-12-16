"""Day 15: Lens Library"""


def compute_hash(string: str) -> int:
    """Holiday ASCII String Helper algorithm (HASH algorithm)"""
    curr = 0
    for char in string:
        curr += ord(char)
        curr *= 17
        curr %= 256
    return curr


def main() -> None:
    """Main Function"""
    assert compute_hash("HASH") == 52

    with open("input.txt", "r", encoding="utf-8") as f:
        init_seq = f.read()

    steps = init_seq.split(",")

    results_sum = sum(map(compute_hash, steps))
    print("Sum:", results_sum)

    boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]

    for step in steps:
        last_char = step[-1]
        if last_char == "-":
            label = step[:-1]
            box_idx = compute_hash(label)
            boxes[box_idx] = [box for box in boxes[box_idx] if box[0] != label]
            continue

        label = step[:-2]
        focal_length = int(step[-1])
        box_idx = compute_hash(label)
        box = boxes[box_idx]
        # Check if label already exists
        label_idx = -1
        for i, lens in enumerate(boxes[box_idx]):
            if lens[0] == label:
                label_idx = i
                break
        if label_idx == -1:
            box.append((label, focal_length))
        else:
            box[label_idx] = (label, focal_length)

    focusing_power = sum(
        i * j * lens[1]
        for i, box in enumerate(boxes, 1)
        for j, lens in enumerate(box, 1)
    )

    print("Focusing power:", focusing_power)


if __name__ == "__main__":
    main()
