def no_ways_to_win_race(race: tuple[int, int]) -> int:
    no_ways = 0
    race_time = race[0]
    record_distance = race[1]
    for acc_time in range(1, race_time + 1):
        curr_speed = acc_time
        curr_distance = (race_time - acc_time) * curr_speed
        if curr_distance > record_distance:
            no_ways += 1
    return no_ways


def main() -> None:
    with open("input.txt") as f:
        lines = f.readlines()

    times_str = lines[0].split()[1:]
    times = map(int, times_str)
    distances_str = lines[1].split()[1:]
    distances = map(int, distances_str)

    races = list(zip(times, distances))

    total = 1
    for race in races:
        no_ways = no_ways_to_win_race(race)
        total *= no_ways

    print("Answer (1):", total)

    the_race = int(''.join(times_str)), int(''.join(distances_str))
    print("Answer (2):", no_ways_to_win_race(the_race))


if __name__ == "__main__":
    main()