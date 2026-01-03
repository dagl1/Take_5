from typing import Dict, Any, TYPE_CHECKING
from src.strategies.base_strategy import BaseStrategy
if TYPE_CHECKING:
    from src.game.cards import Card

class HumanInputStrategy(BaseStrategy):
    """
    This strategy is a human player requiring console input and will temporarily
    stop the program while waiting for input. Not to be used in monte carlo simulations or
    with machine learning training.
    """

    def choose_card_to_play(self, game_state: Dict[str, Any]) -> Card:
        valid_input = False
        back_to_start = False
        per_pile_message = "\n".join([
            f"Pile {idx+1} "
            f"of size {len(game_state['piles'][idx])}, "
            f"last card: {game_state['last_cards_per_pile'][idx]}"
            for idx in range(len(game_state['piles']))
        ])
        message = (
            f"{per_pile_message}\n"
            "Type one of the following options:\n"
              "1: Show full piles\n"
              "2: Show your hand\n"
              "3: Show already played cards this turn\n"
              "4: Choose card to play")
        print(message)
        while not valid_input:
            user_input = input("Your choice: ")
            if user_input == "1":
                self.show_per_pile_cards(game_state)
            elif user_input == "2":
                self.show_player_hand()
            elif user_input == "3":
                self.show_already_played_cards(game_state)
            elif user_input == "4":
                print("Choose card to play or type 0 to exit to the previous menu")
                self.show_player_hand()
                while not valid_input:
                    chosen_card_number = input("Your choice: ")
                    try:
                        if int(chosen_card_number) == 0:
                            back_to_start = True
                            break
                    except ValueError:
                        pass
                    if chosen_card_number.isdigit():
                        chosen_card_number_int = int(chosen_card_number)
                        card_numbers_in_hand = [
                            card.card_number for card in self.player.hand.values()
                        ]
                        if chosen_card_number_int in card_numbers_in_hand:
                            chosen_card = self.player.hand[chosen_card_number_int]
                            print(chosen_card)
                            return chosen_card
                    print("Invalid card number. Please try again.")
            if back_to_start:
                back_to_start = False
                print(message)
            else:
                print("Invalid option. Please try again.")
        raise RuntimeError("Exited loop without returning, in function "
                           "'choose_pile_to_replace' in 'HumanInputStrategy'")

    def choose_pile_to_replace(self, game_state: Dict[str, Any]) -> int:
        valid_input = False
        back_to_start = False
        message = ("Type one of the following options:\n"
              "1: Show piles\n"
              "2: Show your hand\n"
              "3: Show already played cards this turn\n"
              "4: Choose pile to replace")
        print(message)
        while not valid_input:
            user_input = input("Your choice: ")
            if user_input == "1":
                self.show_per_pile_cards(game_state)
            elif user_input == "2":
                self.show_player_hand()
            elif user_input == "3":
                self.show_already_played_cards(game_state)
            elif user_input == "4":
                print("Enter the pile number to replace (1-4) or 5 to return "
                                       "to the previous menu: ")
                while not valid_input:
                    pile_index = input("Your choice: ")
                    if pile_index == "5":
                        back_to_start = True
                        break
                    if pile_index in ["1", "2", "3", "4"]:
                        return int(pile_index) - 1
                    print("Invalid pile number. Please try again.")
            if back_to_start:
                back_to_start = False
                print(message)
            else:
                print("Invalid option. Please try again.")
        raise RuntimeError("Exited loop without returning, in function "
                           "'choose_pile_to_replace' in 'HumanInputStrategy'")



