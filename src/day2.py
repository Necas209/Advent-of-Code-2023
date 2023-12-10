"""Day 2: Cube Conundrum"""
from dataclasses import dataclass
from typing import Self

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14


@dataclass
class Game:
    """Game class"""
    id: int = 0
    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def parse_str(cls, s: str) -> Self:
        """Parse string to Game object"""
        s = s.strip()
        game = cls()
        colon = s.split(": ")
        game.id = int(colon[0].split()[1])
        game_sets = [game_round.split(", ") for game_round in colon[1].split("; ")]
        game_sets = [item for sublist in game_sets for item in sublist]
        for game_set in game_sets:
            no_cubes = int(game_set.split()[0])
            if game_set.endswith("red"):
                game.red = max(game.red, no_cubes)
            elif game_set.endswith("green"):
                game.green = max(game.green, no_cubes)
            else:
                game.blue = max(game.blue, no_cubes)
        return game

    @property
    def cubes_power(self) -> int:
        """Return cubes power"""
        return self.red * self.green * self.blue

    @property
    def is_possible(self) -> bool:
        """Return True if game is possible"""
        return self.red <= MAX_RED and self.green <= MAX_GREEN and self.blue <= MAX_BLUE


def main() -> None:
    """Main function"""
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    games = [Game.parse_str(line) for line in lines]

    print(*games, sep="\n")

    print("Sum IDs:", sum(game.id for game in games if game.is_possible))
    print("Sum Powers:", sum(game.cubes_power for game in games))


if __name__ == "__main__":
    main()
