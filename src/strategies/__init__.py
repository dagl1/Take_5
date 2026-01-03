# add descending, full random, humanimnput, and neural net to the strategies module
from src.strategies.descending_order_strategy import DescendingOrderStrategy
from src.strategies.random_strategies import FullRandomStrategy, RandomCardStrategy
from src.strategies.human_input_strategy import HumanInputStrategy
from src.strategies.Neural_network_strategy import NeuralNetworkStrategy

__all__ = [
    "DescendingOrderStrategy",
    "FullRandomStrategy",
    "RandomCardStrategy",
    "HumanInputStrategy",
    "NeuralNetworkStrategy",
]
