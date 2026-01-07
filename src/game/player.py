from typing import TYPE_CHECKING, Dict, List, Any, ClassVar, Type, Union

if TYPE_CHECKING:
    from src.game.cards import Card
    from src.strategies.base_strategy import BaseStrategy as Strategy


class Player:
    def __init__(
        self,
        player_id: int,
        strategy: Union[Strategy, Type[Strategy]],
    ):
        self.player_id: int = player_id
        self.hand: Dict[int, Card] = {}
        if isinstance(strategy, type):
            strategy_instance = strategy()
        else:
            strategy_instance = strategy

        strategy_instance._set_player(self)
        self.strategy: Strategy = strategy_instance
        self.strategy_name: str = strategy.__class__.__name__
        self.taken_cards: List[Card] = []
        self.turn_score: int = 0
        self.round_score: int = 0

    def receive_cards(self, cards: List[Card]) -> None:
        for card in cards:
            self.hand[card.card_number] = card
        self.hand = dict(sorted(self.hand.items()))

    def choose_card_to_play(self, game_state: Dict[str, Any]) -> Card:
        card_to_play = self.strategy.choose_card_to_play(game_state)
        return card_to_play

    def choose_pile_to_replace(self, game_state: Dict[str, Any]) -> int:
        pile_index_to_replace = self.strategy.choose_pile_to_replace(game_state)
        return pile_index_to_replace

    def take_pile(self, pile: List[Card]) -> None:
        self.calculate_turn_score(pile)
        self.taken_cards.extend(pile)

    def calculate_turn_score(self, pile: List[Card]) -> int:
        points = sum(card.card_points for card in pile)
        self.turn_score += points
        return points

    def calculate_round_score(self) -> int:
        self.round_score += self.turn_score
        return self.round_score

    def reset_for_next_round(self) -> None:
        self.hand.clear()
        self.taken_cards.clear()
        self.turn_score = 0
