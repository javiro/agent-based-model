import random
import numpy as np


class Agent(object):
    """Class which implements the individual actors in the game."""

    def __init__(self, player_id, num_of_channels, strategy=None):
        """Agent initialization.

        :param player_id: integer, between zero and the number of players minus one, which holds the id.
        :param num_of_channels: integer, holding the number of available strategies.
        :param strategy: integer, representing the initial strategy followed by the agent.
        """
        self.player_id = player_id
        self.num_of_channels = num_of_channels
        self.avg_payoff = 0
        if strategy is None:
            self.strategy = random.randint(0, num_of_channels - 1)
        else:
            self.strategy = strategy

    def set_strategy(self, strategy):
        """Given the index of the strategy, it returns the corresponding vector in the space of dimension
        'number of channels'.

        :param strategy: integer representing the index of the strategy.
        :return: the vector in the space of dimension number of channels.
        """
        player = np.zeros(self.num_of_channels)
        player[strategy] = 1
        return player

    @staticmethod
    def __get_test_strategies_for_bep(num_of_channels):
        """Returns the set of strategies that will be tested by the agent who is reviewing.

        :param num_of_channels: integer, holding the number of available strategies.
        :return: list with the set of strategy's index to be tested.
        """
        strategies = list(range(num_of_channels))
        return strategies

    def update_strategy_under_bep_protocol(self, game):
        """Under the best experienced payoff protocol, a revising agent tests each of the strategies against a  new
        randomly drawn opponent. The revising agent then selects the strategy that obtained the greatest payoff. In
        case of ties, they are resolved randomly.

        :param game: an instance of the current game.
        """
        games = []
        n_of_candidates = self.__get_test_strategies_for_bep(game.num_of_channels)
        for strategy in n_of_candidates:
            trials = []
            self.strategy = strategy
            for trial in range(game.number_of_trials):
                player_2 = game.agents.get_opponent(self.player_id)
                trials.append(game.play_agent_game(self.set_strategy(strategy),
                                                   player_2.set_strategy(player_2.strategy)))
            games.append(max(trials))
        games = np.array(games)
        self.strategy = n_of_candidates[random.choice(np.where(games == np.max(games))[0])]

    def update_strategy(self, game):
        """Updates the strategy following the BEP protocol.

        :param game: an instance of the current game.
        """
        if random.random() > game.noise:
            self.update_strategy_under_bep_protocol(game)
        else:
            self.strategy = random.randint(0, game.num_of_channels - 1)
