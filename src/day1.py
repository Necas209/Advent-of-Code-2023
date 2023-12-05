import regex as re


def main() -> None:
    with open("input.txt", "r") as f:
        lines = f.readlines()

    digit_names = ["one", "two", "three",
                   "four", "five", "six",
                   "seven", "eight", "nine"]

    digits = [re.findall(rf"(\d|{"|".join(digit_names)})", line, overlapped=True)
               for line in lines]

    def convert_to_digit(s: str) -> int:
        if len(s) == 1:
            return int(s)
        else:
            return digit_names.index(s) + 1

    calibration_values = [10 * convert_to_digit(digit[0]) + convert_to_digit(digit[-1])
                           for digit in digits]

    print(*enumerate(zip(digits, calibration_values), 1), sep='\n')

    print(sum(calibration_values))


if __name__ == "__main__":
    main()