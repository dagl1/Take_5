from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from src.game.cards import Card
    from src.game.player import Player


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

    def update(self, state, action, reward, next_state, possible_actions):  # noqa: B027
        pass

    def show_per_pile_cards(self, game_state: Dict[str, Any]) -> None:
        for i, pile in enumerate(game_state["piles"]):
            print(
                f"Pile {i + 1} ({len(pile)} Cards, {game_state['points_per_pile'][i]}"
                f" Points): {pile}"
            )

    def show_player_hand(self) -> None:
        print(f"Hand with {len(self.player.hand)} cards:")
        cards_per_line = 3  # Number of cards to display per line
        for idx, (card_number, card) in enumerate(self.player.hand.items(), 1):
            print(f"Card: {card_number}, points: {card.card_points}", end="\t")
            if idx % cards_per_line == 0:
                print()  # New line after every 'cards_per_line' cards
        if len(self.player.hand) % cards_per_line != 0:
            print()  # New line if the last line wasn't complete
        # for card_number, card in self.player.hand.items():
        #     print(f"Card: {card_number}, points: {card.card_points}")

    def show_already_played_cards(self, game_state: Dict[str, Any]) -> None:
        print(f"Already played cards: {game_state['played_cards']}")

    def show_total_points_per_player(self, game_state: Dict[str, Any]) -> None:
        print("Total points per player:")
        for player_id, total_points in game_state["points_per_player_per_round"].items():
            print(f"Player {player_id}: {total_points} points")
