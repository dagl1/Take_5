from typing import List, Optional, TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from src.game.player import Player
    from src.game.cards import Card

from src.game.cards import Deck


class Game:
    # a round consists of n turns ,where n is the amount of cards per player
    # each player puts down a card based on the current piles, the round number, and their strategy
    # rules = lowest card goes first
    # if card is lower than any last card in a pile, they replace a pile and take the
    # minus points, if a card is higher than any last card in a pile, it goes on the
    # pile with the highest last card that is still lower than the played card
    # if a pile reaches 6 cards, the player who placed the last card takes the pile and
    # the played card starts a new pile, aftr each round, the scores are calculated based
    # on how many points each player has taken, the least points wins

    # relevant variables public variables:
    # last cards per pile
    # total players/cards
    # cards already played and thus out of game
    # current round number
    # min and max card
    # cards per player
    # points per player per round
    # how many rounds left

    # relevant player variables:
    # cards in hand (thus not in game), strategy,
    def __init__(
        self,
        players: List["Player"],
        amount_of_rounds: Optional[int] = 5,
        amount_of_piles: Optional[int] = 4,
        amount_of_cards_per_player: Optional[int] = 10,
    ):
        self.deck: Deck = Deck()
        self.players: List["Player"] = players
        self.plays_per_player: Dict[int, List[int]] = {
            player.player_id: [] for player in players
        }
        self.amount_of_rounds: int = amount_of_rounds
        self.amount_of_piles: int = amount_of_piles
        self.amount_of_cards_per_player: int = amount_of_cards_per_player
        self.piles: List[List[Card]] = [[] for _ in range(self.amount_of_piles)]
        self.scores_per_player_per_turn: Dict[int, List[int]] = {
            player.player_id: [0 for _ in range(self.amount_of_rounds)] for player in players
        }
        self.scores_per_player_per_round: Dict[int, List[int]] = {
            player.player_id: [0 for _ in range(self.amount_of_rounds)] for player in players
        }

    def initialize_game(self) -> None:
        # give each player their cards
        # draw 1 card for each pile
        for player in self.players:
            cards = [self.deck.draw_card() for _ in range(self.amount_of_cards_per_player)]
            player.receive_cards(cards)
        for i in range(self.amount_of_piles):
            card = self.deck.draw_card()
            self.piles[i].append(card)

    def get_last_cards_per_pile(self) -> List[Card]:
        last_cards = []
        for pile in self.piles:
            if pile:
                last_cards.append(pile[-1])
        return last_cards

    def get_played_cards(self) -> List[Card]:
        played_cards = []
        for pile in self.piles:
            played_cards.extend(pile)
        return played_cards

    def get_current_turn_number(self) -> int:
        return self.amount_of_rounds - sum(
            1
            for round_scores in self.scores_per_player_per_round[
                list(self.scores_per_player_per_round.keys())[0]
            ]
            if round_scores == 0
        )

    def get_current_round_number(self) -> int:
        return self.amount_of_rounds - sum(
            1
            for round_scores in self.scores_per_player_per_round[
                list(self.scores_per_player_per_round.keys())[0]
            ]
            if round_scores == 0
        )

    def provide_game_state_to_player(
        self, cards_played: Optional[List[Card]] = None
    ) -> Dict[str, Any]:
        game_state = {
            "total_players": len(self.players),
            "min_card": min(self.deck.cards.keys()) if self.deck.cards else None,
            "max_card": max(self.deck.cards.keys()) if self.deck.cards else None,
            "cards_per_player": self.amount_of_cards_per_player,
            "total_piles": self.amount_of_piles,
            "total_rounds": self.amount_of_rounds,
            "played_cards": self.get_played_cards(),
            "last_cards_per_pile": self.get_last_cards_per_pile(),
            "piles": self.piles,
            "points_per_pile": [
                sum(card.card_points for card in pile) for pile in self.piles
            ],
            "points_per_player_per_turn": self.scores_per_player_per_turn,
            "points_per_player_per_round": self.scores_per_player_per_round,
            "current_turn_number": (self.amount_of_rounds - self.get_current_turn_number()),
            "current_round_number": self.get_current_round_number(),
            "cards_played": cards_played,
        }
        return game_state

    def get_player_card_choice(self) -> Dict[int, Card]:
        player_moves = {}
        for player in self.players:
            game_state = self.provide_game_state_to_player()
            chosen_card = player.choose_card_to_play(game_state)
            player_moves[player.player_id] = chosen_card
        return player_moves

    def get_player_replaces_pile_choice(
        self,
        player_id: int,
        cards_played: List[Card],
    ) -> int:
        player = next(p for p in self.players if p.player_id == player_id)
        game_state = self.provide_game_state_to_player(cards_played)
        chosen_pile_index = player.choose_pile_to_replace(game_state)
        return chosen_pile_index

    def get_players_turn_score(self) -> None:
        for player in self.players:
            player_index = player.player_id
            self.scores_per_player_per_turn[player_index][
                self.get_current_turn_number() - 1
            ] = player.turn_score

    def check_if_card_playable(
        self,
        card_number: int,
    ) -> bool:
        last_cards_per_pile = self.get_last_cards_per_pile()
        for last_card in last_cards_per_pile:
            if card_number > last_card.card_number:
                return True
        return False

    def handle_unplayable_card(
        self,
        player_id: int,
        card_number: Card,
        player_moves: Dict[int, Card],
    ) -> int:
        player = next(p for p in self.players if p.player_id == player_id)
        # player must replace a pile
        chosen_pile_index = self.get_player_replaces_pile_choice(
            player_id, list(player_moves.values())
        )
        # player takes the pile
        taken_pile = self.piles[chosen_pile_index]
        sum_points = sum(card.card_points for card in taken_pile)
        player.take_pile(taken_pile)
        self.piles[chosen_pile_index] = [card_number]
        return chosen_pile_index, sum_points

    def handle_playable_card(
        self,
        player_id: int,
        card: Card,
    ) -> None:
        valid_piles = [
            (i, pile[-1])
            for i, pile in enumerate(self.piles)
            if pile and pile[-1].card_number < card.card_number
        ]
        chosen_pile_index = max(valid_piles, key=lambda x: x[-1].card_number)[0]
        # place the card on the chosen pile
        self.piles[chosen_pile_index].append(card)
        chosen_pile = chosen_pile_index + 1  # for user-friendly display
        pile_points = sum(c.card_points for c in self.piles[chosen_pile_index])
        print(
            f"Player {player_id} successfully plays card {card.card_number}"
            f", it is placed on pile {chosen_pile}: {len(self.piles[chosen_pile_index])} "
            f"cards, {pile_points} points."
        )
        if len(self.piles[chosen_pile_index]) > 5:
            # pile reached 6 cards, player takes the pile
            print(
                "As this pile reached 6 cards, the player takes the pile."
                f"collecting {pile_points} points and placing {card.card_number} "
                f"as new pile."
            )

            player = next(p for p in self.players if p.player_id == player_id)
            taken_pile = self.piles[chosen_pile_index][:-1]
            player.take_pile(taken_pile)
            # start a new pile with the played card
            self.piles[chosen_pile_index] = [card]

    def play_turn(self) -> None:
        player_moves = self.get_player_card_choice()
        # process player moves and update piles accordingly
        print("\n--- player moves: ---")
        # print(player_moves)
        # sort cards on card number
        sorted_cards = sorted(
            player_moves.items(),
            key=lambda x: x[1].card_number,
        )

        for player_id, card in sorted_cards:
            if not self.check_if_card_playable(
                card.card_number,
            ):
                print(
                    f"Player {player_id} cannot play card {card.card_number} "
                    f"and must replace a pile"
                )
                chosen_pile, pile_points = self.handle_unplayable_card(
                    player_id,
                    card,
                    player_moves,
                )
                print(
                    f"They chose pile {chosen_pile} with {pile_points} points, "
                    f"replacing it with card"
                    f" {card.card_number} of {card.card_points} points"
                )
            else:
                # find the pile with the highest last card that is
                # still lower than the played card
                self.handle_playable_card(
                    player_id,
                    card,
                )

        # add code that reports what happened this turn
        print("---New turn ---\n")
        self.get_players_turn_score()

    def play_round(self) -> None:
        for turn in range(self.amount_of_cards_per_player):
            self.play_turn()
        # calculate scores for each player and store them in scores_per_player_per_round
        for player_index, player in enumerate(self.players):
            self.scores_per_player_per_round[player_index][self.amount_of_rounds - 1] = (
                player.calculate_round_score()
            )

    def reset_for_next_round(self) -> None:
        # shuffle deck
        self.deck = Deck()
        # reset piles and players for next round
        self.piles = [[] for _ in range(self.amount_of_piles)]
        for player in self.players:
            player.reset_for_next_round()
        self.initialize_game()

    def play_game(self) -> None:
        self.initialize_game()
        for round_number in range(self.amount_of_rounds):
            self.play_round()
            self.reset_for_next_round()
