import dataclasses

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

@dataclasses.dataclass
class Game:
    id: int = 0
    red: int = 0
    green: int = 0
    blue: int = 0

    @staticmethod
    def parse_str(s: str):
        s = s.strip()
        game = Game()
        colon = s.split(": ")
        game.id = int(colon[0].split()[1])
        game_sets = [game_round.split(', ')
                     for game_round in colon[1].split('; ')]
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
        return self.red * self.green * self.blue

    @property
    def is_possible(self) -> bool:
        return (self.red <= MAX_RED
                and self.green <= MAX_GREEN
                and self.blue <= MAX_BLUE)


def main() -> None:
    with open("sinput.txt") as f:
        lines = f.readlines()

    games = [Game.parse_str(line)
             for line in lines]
    
    print(*games, sep='\n')

    print("Sum IDs:", sum(game.id for game in games if game.is_possible))
    print("Sum Powers:", sum(game.cubes_power for game in games))


if __name__ == "__main__":
    main()