import random

from src.strategies.base_strategy import BaseStrategy


class QLearningStrategy(BaseStrategy):
    def __init__(self):
        self.q_table = {}  # (state, action) → value
        self.epsilon = 0.1  # exploration
        self.alpha = 0.1  # learning rate
        self.gamma = 0.99  # discount

    def update(self, state, action, reward, next_state, possible_actions):
        old = self.q_table.get((state, action), 0)
        future = max(self.q_table.get((next_state, a), 0) for a in possible_actions)
        self.q_table[(state, action)] = old + self.alpha * (
            reward + self.gamma * future - old
        )

    @staticmethod
    def encode_state(game_state, hand):
        last_cards = tuple(card.card_number for card in game_state["last_cards_per_pile"])
        hand_cards = tuple(sorted(card.card_number for card in hand.values()))
        return (last_cards, hand_cards)

    def choose_card_to_play(self, game_state):
        state = self.encode_state(game_state, self.player.hand)

        if random.random() < self.epsilon:
            return random.choice(list(self.player.hand.values()))

        # exploit
        q_values = {}
        for card in self.player.hand.values():
            action = card.card_number
            q_values[action] = self.q_table.get((state, action), 0)

        best_action = max(q_values, key=q_values.get)
        return self.player.hand[best_action]

    def choose_pile_to_replace(self, game_state):
        state = self.encode_state(game_state, self.player.hand)

        if random.random() < self.epsilon:
            return random.randint(0, len(game_state["piles"]) - 1)

        # exploit
        q_values = {}
        for pile_index in range(len(game_state["piles"])):
            action = pile_index
            q_values[action] = self.q_table.get((state, action), 0)

        best_action = max(q_values, key=q_values.get)
        return best_action
