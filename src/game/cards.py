from typing import Optional, Dict
from dataclasses import dataclass, field
import random


@dataclass
class Card:
    # ends on 5 = 2, same digits = 5, except if ends on 5 such as 55 then 7
    # ends on 0 = 3

    # 15, 25, 35 = 2
    # 10, 20, 50, 100 = 3
    # 22, 33, 44 = 5
    # 55 = 7
    # all others = 1
    card_number: int
    card_points: int = field(init=False)

    def points(self) -> int:
        if self.card_number % 10 == 5 and (self.card_number // 10) % 10 == 5:
            return 7
        elif self.card_number % 5 == 0:
            return 2
        elif self.card_number % 10 == 0:
            return 3
        elif len(str(self.card_number)) >1 and len(set(str(self.card_number))) == 1:
            return 5
        else:
            return 1

    def __post_init__(self):
        self.card_points = self.points()

    def __repr__(self) -> str:
        if self.card_points == 1:
            return f"Card {self.card_number} with {self.card_points} point"
        return f"Card {self.card_number} with {self.card_points} points"

class Deck:
    def __init__(
        self,
        start_card: Optional[int] = 1,
        end_card: Optional[int] = 103,
        min_points: Optional[int] = 1,
        max_points: Optional[int] = 7,
    ):
        self.cards: Dict[int, Card] = {}
        for card_num in range(start_card, end_card + 1):
            card = Card(card_number=card_num)
            self.cards[card_num] = card
        self.min_points = min_points
        self.max_points = max_points
        self.shuffle()
        self.error_checks()

    def error_checks(self) -> None:
        error_messages = {}
        if not self.cards:
            raise ValueError("Deck is empty.")
        for card_num, card in self.cards.items():
            if card.card_number != card_num:
                error_messages[card_num] = (
                    f"Card number mismatch: expected {card_num}, got {card.card_number}"
                )
            if not (self.min_points <= card.card_points <= self.max_points):
                error_messages[card_num] = (
                    f"Card points {card.card_points} out of bounds ({self.min_points}, {self.max_points})"
                )
        if error_messages:
            raise ValueError(f"Deck validation errors: {error_messages}")

    def shuffle(self) -> None:
        card_items = list(self.cards.items())
        random.shuffle(card_items)
        self.cards = dict(card_items)

    def draw_card(self, card_number: Optional[int] = None) -> Card:
        if card_number is None:
            card_number = next(iter(self.cards))
            card = self.cards.pop(card_number)
            return card
        if card_number in self.cards:
            return self.cards.pop(card_number)
        else:
            raise ValueError(f"Card number {card_number} not found in deck.")

