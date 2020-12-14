import random
import numpy as np


class Agent(object):
    """Class which implements the agents in communication game."""

    def __init__(self, player_id, num_of_channels, strategy=None):
        """

        :param player_id:
        :param num_of_channels:
        :param strategy:
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
        strategies = list(range(num_of_channels))
        return strategies

    def update_strategy_under_bep_protocol(self, game):
        """Under the best experienced payoff protocol, a revising agent tests each of the 'n_of_candidates' of
        strategies against a random agent, with each play of each strategy being against a newly drawn opponent. The
        revising agent then selects the strategy that obtained the greater payoff in the test, with ties resolved at
        random.

        :param game:
        :return:
        """
        games = []
        n_of_candidates = self.__get_test_strategies_for_bep(game.num_of_channels)
        for strategy in n_of_candidates:
            trials = []
            self.strategy = strategy
            for trial in range(game.number_of_trials):
                player_2 = game.agents.get_opponent(self)
                trials.append(game.play_agent_game(self.set_strategy(strategy),
                                                   player_2.set_strategy(player_2.strategy)))
            games.append(max(trials))
        games = np.array(games)
        self.strategy = n_of_candidates[random.choice(np.where(games == np.max(games))[0])]

    def update_strategy(self, game):
        """Updates the strategy following the specified protocol.

        :param game: an instance of the current game.
        """
        if random.random() > game.noise:
            self.update_strategy_under_bep_protocol(game)
        else:
            self.strategy = random.randint(0, game.num_of_channels - 1)
