import numpy as np
from typing import TYPE_CHECKING, Dict, Any

from src.strategies.base_strategy import BaseStrategy
if TYPE_CHECKING:
    from src.game.cards import Card


class DescendingOrderStrategy(BaseStrategy):
    """
    Always chooses the highest card available, but takes the lowest point pile when replacing.
    When multiple piles have the same lowest points, chooses the pile with the lowest last
    card.
    """
    def choose_card_to_play(self, game_state: Dict[str, Any]) -> Card:
        player_hand = self.player.hand.values()
        # Select the highest numbered card from the player's hand
        card_to_play = max(player_hand, key=lambda card: card.card_number)
        return card_to_play

    def choose_pile_to_replace(self, game_state: Dict[str, Any]) -> int:
        points_per_pile = game_state["points_per_pile"]
        min_points = min(points_per_pile)
        candidate_pile_indices = [i for i, points in enumerate(points_per_pile)
                                  if points == min_points]
        if len(candidate_pile_indices) == 1:
            return candidate_pile_indices[0]
        last_cards_per_pile = game_state["last_cards_per_pile"]
        index_of_lowest_card_pile = np.argmin(
            [last_cards_per_pile[i] for i in candidate_pile_indices]
        )
        return candidate_pile_indices[index_of_lowest_card_pile]
