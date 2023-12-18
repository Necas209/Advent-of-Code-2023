"""Day 10: Pipe Maze"""
from shapely import Polygon, Point  # type: ignore


Position = tuple[int, int]


def find_first_adjacent_pipe(position: Position, lines: list[str]) -> Position:
    """Find coordinates of the first adjacent pipe"""
    x, y = position
    if (x - 1) >= 0 and lines[y][x - 1] in "-LF":
        return x - 1, y
    if (x + 1) < len(lines[0]) and lines[y][x + 1] in "-J7":
        return x + 1, y
    if (y - 1) >= 0 and lines[y - 1][x] in "|7F":
        return x, y - 1
    if (y + 1) < len(lines) and lines[y + 1][x] in "|LJ":
        return x, y + 1
    return x, y


def calculate_path(start: Position, lines: list[str]) -> list[Position]:
    """Calculates the loop path"""
    prev_x, prev_y = start
    curr_x, curr_y = find_first_adjacent_pipe(start, lines)
    path: list[Position] = []
    while True:
        temp = curr_x, curr_y
        path.append(temp)
        match lines[curr_y][curr_x]:
            case "S":
                break
            case "|":
                curr_y += 1 if curr_y > prev_y else -1
            case "-":
                curr_x += 1 if curr_x > prev_x else -1
            case char:
                if curr_y == prev_y:
                    if char in "LJ":
                        curr_y -= 1
                    else:
                        curr_y += 1
                else:
                    if char in "J7":
                        curr_x -= 1
                    else:
                        curr_x += 1
        prev_x, prev_y = temp
    return path


def find_start(lines: list[str]) -> Position:
    """Find start position"""
    x, y = 0, 0
    for y, line in enumerate(lines):
        if (x := line.find("S")) != -1:
            break
    return x, y


def main() -> None:
    "Main function"
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    start = find_start(lines)
    print(f"Start = {start}")

    path = calculate_path(start, lines)
    print("Loop length:", len(path))
    print("Farthest:", len(path) // 2)

    polygon = Polygon(path) # type: ignore
    count = sum(
        polygon.contains(Point(x, y))  # type: ignore
        for y, line in enumerate(lines)
        for x, _ in enumerate(line)
        if (x, y) not in path
    )

    print("Count:", count)


if __name__ == "__main__":
    main()
