from src.game.rounds import Game
from src.game.player import Player
from src.strategies import (
    FullRandomStrategy,
    RandomCardStrategy,
    DescendingOrderStrategy,
    HumanInputStrategy,
)

if __name__ == "__main__":
    players = [
        Player(player_id=1, strategy=DescendingOrderStrategy()),
        Player(player_id=2, strategy=FullRandomStrategy()),
        Player(player_id=3, strategy=RandomCardStrategy()),
        Player(player_id=4, strategy=HumanInputStrategy()),
    ]
    game = Game(
        players=players,
        amount_of_rounds=3,
        amount_of_piles=4,
        amount_of_cards_per_player=10,
    )
    game.play_game()
