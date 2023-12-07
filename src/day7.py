from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import cmp_to_key


class HandType(Enum):
    NONE = 0
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

    @staticmethod
    def from_cards(cards: str):
        counter = Counter(cards)

        # Special case: J is a Joker, a wilcard that acts like
        # whatever card would make the hand the strongest type possible
        if counter['J'] != 0 and counter['J'] != 5:
            most_common_cards = counter.most_common(2)
            if most_common_cards[0][0] == 'J':
                most_common_card = most_common_cards[1][0]
            else:
                most_common_card = most_common_cards[0][0]
            cards = cards.replace('J', most_common_card)
            counter = Counter(cards)
        
        card_set = set(cards)
        match len(card_set):
            case 1:
                return HandType.FIVE_OF_A_KIND
            case 2:
                if any(counter[card] == 4 for card in card_set):
                    return HandType.FOUR_OF_A_KIND
                else:
                    return HandType.FULL_HOUSE
            case 3:
                if any(counter[card] == 3 for card in card_set):
                    return HandType.THREE_OF_A_KIND
                else:
                    return HandType.TWO_PAIR
            case 4:
                return HandType.ONE_PAIR
            case 5:
                return HandType.HIGH_CARD
            case _:
                return HandType.NONE
        

@dataclass
class Hand:
    cards: str
    bid: int
    hand_type: HandType = HandType.NONE

    def __post_init__(self) -> None:
        self.hand_type = HandType.from_cards(self.cards)


def compare_to(val1: int, val2: int) -> int:
    if val1 > val2:
        return 1
    elif val1 < val2:
        return -1
    else:
        return 0

CARDS_BY_STRENGTH = "AKQT98765432J"

def compare_hands(hand1: Hand, hand2: Hand) -> int:
    if hand1.hand_type != hand2.hand_type:
        return compare_to(hand1.hand_type.value, hand2.hand_type.value)
    
    for card1, card2 in zip(hand1.cards, hand2.cards):
        if card1 == card2:
            continue

        card1_stregth = CARDS_BY_STRENGTH.index(card1)
        card2_strength = CARDS_BY_STRENGTH.index(card2)
        return compare_to(card2_strength, card1_stregth)

    return 0

def main() -> None:
    with open("input.txt") as f:
        lines = f.readlines()

    hands = [line.strip().split() for line in lines]
    hands = [Hand(hand[0], int(hand[1])) for hand in hands]

    hands = sorted(hands, key=cmp_to_key(compare_hands))

    total_winnings = sum(i * hand.bid for i, hand in enumerate(hands, 1))
    print("Total winnings:", total_winnings)


if __name__ == "__main__":
    main()