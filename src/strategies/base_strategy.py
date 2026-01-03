
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Any, Optional

if TYPE_CHECKING:
    from src.game.player import Player
    from src.game.cards import Card

class BaseStrategy(ABC):
    player: Optional[Player] = None

    def _set_player(self, player: Player) -> None:
        self.player = player

    @abstractmethod
    def choose_card_to_play(self, game_state: Dict[str, Any]) -> Card:
        pass

    @abstractmethod
    def choose_pile_to_replace(self, game_state: Dict[str, Any]) -> int:
        pass

    def show_per_pile_cards(self, game_state: Dict[str, Any]) -> None:
        for i, pile in enumerate(game_state["piles"]):
            print(f"Pile {i + 1}: {pile} (Points: {game_state['points_per_pile'][i]})")

    def show_player_hand(self) -> None:
        print(f"Hand with {len(self.player.hand)} cards:")
        for card_number, card in self.player.hand.items():
            print(f"Card: {card_number}, points: {card.card_points}")

    def show_already_played_cards(self, game_state: Dict[str, Any]) -> None:
        print(f"Already played cards: {game_state['cards_played']}")
