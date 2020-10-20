import random
import numpy as np

from pyabm.common.constants import BEP, PAIRWISE_DIFFERENCE, LINEAR_DISSATISFACTION


class Agent(object):
    """Class which implements the agents in communication game."""

    def __init__(self, player_id, num_of_channels, strategy=None, revision_protocol=BEP):
        """

        :param player_id:
        :param num_of_channels:
        :param strategy:
        :param revision_protocol:
        """
        self.player_id = player_id
        self.num_of_channels = num_of_channels
        self.revision_protocol = revision_protocol
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

    def __get_test_strategies_for_bep(self, num_of_channels):
        strategies = list(range(num_of_channels))
        strategies.remove(self.strategy)
        strategies.insert(0, self.strategy)
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
            for trial in range(game.n_of_trials):
                player_2 = game.agents.get_player(self)
                trials.append(game.play_agent_game(self.set_strategy(strategy),
                                                   player_2.set_strategy(player_2.strategy)))
            games.append(max(trials))
        games = np.array(games)
        self.strategy = n_of_candidates[random.choice(np.where(games == np.max(games))[0])]

    def update_strategy_under_pairwise_difference_protocol(self, game):
        """Under the best pairwise difference protocol, a revising agent selects a player to observe at random. This
        imitating player will chose a random opponent to play with. She will be imitated with a probability proportional
        to the payoff difference:

            probability of change = max(0, (imitating_payoff - own_payoff) / (imitating_payoff + own_payoff))

        :param game: an instance of the current game.
        """
        revising_opponent = game.agents.get_player(self)
        payoff_revising_player = game.play_agent_game(self.set_strategy(self.strategy),
                                                      revising_opponent.set_strategy(revising_opponent.strategy))
        imitating_player = game.agents.get_player(self)
        imitating_opponent = game.agents.get_player(imitating_player)
        payoff_imitating_player = game.play_agent_game(imitating_player.set_strategy(imitating_player.strategy),
                                                       imitating_opponent.set_strategy(imitating_opponent.strategy))
        if payoff_revising_player + payoff_imitating_player > 0:
            change_probability = max((payoff_imitating_player - payoff_revising_player) /
                                     (game.maximum_payoff - game.minimum_payoff), 0)
            if random.random() < change_probability:
                self.strategy = imitating_player.strategy

    def update_strategy_under_linear_dissatisfaction_protocol(self, game):
        """Under linear-dissatisfaction, the agent plays with 'number_of_trials' opponents randomly chosen. Then, she
        imitates a different random agent -imitating_player- with a probability which is proportional to the difference
        between the maximum payoff and the average obtained in these trials.

        :param game: an instance of the current game.
        """
        payoffs = []
        for trial in range(game.number_of_trials):
            current_opponent = game.agents.get_player(self)
            payoffs.append(game.play_agent_game(self.set_strategy(self.strategy),
                                                current_opponent.set_strategy(current_opponent.strategy)))
        probability_of_change = (game.maximum_payoff - np.mean(payoffs)) / (game.maximum_payoff - game.minimum_payoff)
        if random.random() < probability_of_change:
            imitating_player = game.agents.get_player(self)
            self.strategy = imitating_player.strategy

    def update_strategy(self, game):
        """Updates the strategy following the specified protocol.

        :param game: an instance of the current game.
        """
        if self.revision_protocol == BEP:
            self.update_strategy_under_bep_protocol(game)
        elif self.revision_protocol == PAIRWISE_DIFFERENCE:
            self.update_strategy_under_pairwise_difference_protocol(game)
        elif self.revision_protocol == LINEAR_DISSATISFACTION:
            self.update_strategy_under_linear_dissatisfaction_protocol(game)
