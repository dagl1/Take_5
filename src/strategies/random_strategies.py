import random
from typing import Any, Dict, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from src.game.cards import Card
from src.strategies.base_strategy import BaseStrategy


class FullRandomStrategy(BaseStrategy):
    """
    Randomly chooses a card, and randomly takes a pile when replacing.
    """

    def choose_card_to_play(self, game_state: Dict[str, Any]) -> Card:
        hand = self.player.hand
        card_to_play = random.choice(list(hand.values()))
        return card_to_play

    def choose_pile_to_replace(self, game_state: Dict[str, Any]) -> int:
        piles = game_state["piles"]
        pile_index_to_replace = random.randint(0, len(piles) - 1)
        return pile_index_to_replace


class RandomCardStrategy(BaseStrategy):
    """
    Randomly chooses a card, but always takes the lowest point pile when replacing.
    When multiple piles have the same lowest points, chooses the pile with the lowest last
    card.
    """

    def choose_card_to_play(self, game_state: Dict[str, Any]) -> Card:
        hand = self.player.hand
        card_to_play = random.choice(list(hand.values()))
        return card_to_play

    def choose_pile_to_replace(self, game_state: Dict[str, Any]) -> int:
        points_per_pile = game_state["points_per_pile"]
        min_points = min(points_per_pile)
        candidate_pile_indices = [
            i for i, points in enumerate(points_per_pile) if points == min_points
        ]
        if len(candidate_pile_indices) == 1:
            return candidate_pile_indices[0]
        last_cards_per_pile = game_state["last_cards_per_pile"]
        index_of_lowest_card_pile = np.argmin(
            [last_cards_per_pile[i].card_points for i in candidate_pile_indices]
        )
        return candidate_pile_indices[index_of_lowest_card_pile]
