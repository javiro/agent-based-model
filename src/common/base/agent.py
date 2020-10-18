import random
import numpy as np

from src.common.constants import BEP, PAIRWISE_DIFFERENCE, LINEAR_DISSATISFACTION


class Agent(object):
    """Class which implements the agents in communication game."""

    def __init__(self, player_id, num_of_channels, strategy=None, revision_protocol=BEP):
        """

        :param player_id:
        :param num_of_channels:
        :param strategy:
        :param revision_protocol:
        """
        # Set internal parameters
        self.player_id = player_id
        self.num_of_channels = num_of_channels
        self.revision_protocol = revision_protocol
        self.avg_payoff = 0
        if strategy is None:
            self.strategy = random.randint(0, num_of_channels - 1)
        else:
            self.strategy = strategy

    def set_strategy(self, strategy):
        player = np.zeros(self.num_of_channels)
        player[strategy] = 1
        return player

    def update_avg_payoff(self, payoff, tick):
        if tick > 0:
            self.avg_payoff = (self.avg_payoff * (tick - 1) + payoff) / tick

    def update_strategy(self, game):
        """Under the best experienced payoff protocol, a revising agent tests each of the 'n_of_candidates' of
        strategies against a random agent, with each play of each strategy being against a newly drawn opponent. The
        revising agent then selects the strategy that obtained the greater payoff in the test, with ties resolved at
        random.

        :param game:
        :return:
        """
        if self.revision_protocol == BEP:
            games = []
            n_of_candidates = game.get_test_strategies(self)
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
        elif self.revision_protocol == PAIRWISE_DIFFERENCE:
            revising_opponent = game.agents.get_player(self)
            payoff_revising_player = game.play_agent_game(self.set_strategy(self.strategy),
                                                          revising_opponent.set_strategy(revising_opponent.strategy))
            imitating_player = game.agents.get_player(self)
            imitating_opponent = game.agents.get_player(imitating_player)
            payoff_imitating_player = game.play_agent_game(imitating_player.set_strategy(imitating_player.strategy),
                                                           imitating_opponent.set_strategy(imitating_opponent.strategy))
            if payoff_revising_player + payoff_imitating_player > 0:
                change_probability = max((payoff_imitating_player - payoff_revising_player) /
                                         (payoff_revising_player + payoff_imitating_player), 0)
                if random.random() < change_probability:
                    self.strategy = imitating_player.strategy
        elif self.revision_protocol == LINEAR_DISSATISFACTION:
            player_2 = game.agents.get_player(self)
            payoff = game.play_agent_game(self.set_strategy(self.strategy), player_2.set_strategy(player_2.strategy))
            self.update_avg_payoff(payoff, game.tick)
            probability_of_change = (game.maximun_payoff - self.avg_payoff) / (game.maximun_payoff + self.avg_payoff)
            if random.random() < probability_of_change:
                strategies = list(range(game.payoff_matrix.shape[0]))
                strategies.remove(self.strategy)
                self.strategy = np.random.choice(strategies)

            # if self.player_id == 10:
            #     print("El promedio de pagos es: {}".format(self.avg_payoff))
            # linear-*, the agent switches to the alternative strategy with probability proportional to the
            # difference between the maximum possible payoff in the game and the revising agent’s average payoff (
            # under linear- dissatisfaction), or between the alternative strategy’s average payoff and the minimum
            # possible payoff in the game (under linear-attraction).
            pass
