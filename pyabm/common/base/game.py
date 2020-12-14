import random
import numpy as np

from pyabm.common.base.population import AgentPopulation
from pyabm.common.constants import *
from pyabm.common.exceptions import PyABMException
from pyabm.common.utils.plot import prepare_plot, plot_distribution
from pyabm.common.workspace import Workspace


class AgentGame(object):
    """
    Class which implements the communication between Agents within the frame of evolutionary game theory .

    Formulating such a model requires one to specify

        (i) the number of agents N in the population,
        (ii) the n-strategy normal form game the agents are recurrently matched to play,
        (iii) the rule describing how revision opportunities are assigned to the agents, and
        (iv) the protocol according to which agents revise their strategies when opportunities
        to do so arise.

    """

    def __init__(self):
        """Complete matching is off since BEP does not consider it. Then the agents play his current strategy against a
        random sample of opponents. The size of this sample is specified by the parameter n-of-trials.
        Single sample is off, so the agent tests each of his candidate strategies against distinct, independent samples
        of n-of-trials opponents.
        """
        workspace = Workspace()
        self.game_rounds = workspace.conf.get_number_of_game_rounds()
        self.tick = None
        self.num_of_channels = workspace.conf.get_number_of_channels()
        self.n_of_agents = workspace.conf.get_number_of_agents()
        self.number_of_trials = workspace.conf.get_number_of_trials()
        self.update_strategies_mode = workspace.conf.get_update_strategies_mode()
        self.payoff_matrix = self.__get_payoff_matrix(workspace.conf.get_matrix_payoffs())
        self.noise = workspace.conf.get_noise()
        self.show_plot_distribution = workspace.conf.get_show_plot_distribution()
        self.agents = AgentPopulation()
        self.ticks_per_second = workspace.conf.get_number_of_ticks_per_second()

    def __get_payoff_matrix(self, payoff_matrix):
        n = self.num_of_channels
        if not payoff_matrix:
            payoff_matrix = np.zeros((n, n))
            for i in range(n):
                payoff_matrix[i, i] = i + 1
            return payoff_matrix
        else:
            payoff_matrix = np.array(payoff_matrix)
            assert payoff_matrix.shape == (n, n)
            return payoff_matrix

    def play_agent_game(self, player_1, player_2):
        return player_1 @ self.payoff_matrix @ player_2

    def update_strategies(self):
        """Under the best experienced payoff protocol, a revising agent tests each of the "n_of_candidates" of
        strategies against a random agent, with each play of each strategy being against a newly drawn opponent.
        The revising agent then selects the strategy that obtained the greater payoff in the test, with ties resolved
        at random.

        """
        if self.update_strategies_mode == ALL_IN_ONE_TICK:
            reordered_ids = random.sample(list(range(self.n_of_agents)), self.n_of_agents)
            for i in reordered_ids:
                player_1 = self.agents.population[i]
                player_1.update_strategy(self)
        elif self.update_strategies_mode == ASYNCHRONOUS_RANDOM_INDEPENDENT:
            for i in range(self.n_of_agents):
                player_1 = self.agents.population[random.randint(0, self.n_of_agents - 1)]
                player_1.update_strategy(self)
        else:
            raise PyABMException(UPDATE_STRATEGIES_MODE_REQUIRED)

    def logging_distributions(self, g, plot_dist):
        distribution = self.agents.get_strategy_distribution()
        if self.show_plot_distribution == ON:
            plot_distribution(g, self.ticks_per_second, distribution, plot_dist)
        else:
            plot_dist.append(distribution[-1] / self.n_of_agents)

    def run_population_game(self):
        """Starts up the clock and runs the population game allowing some agents to review their strategies, at each
        tick of time.

        :return: the distribution of strategies and a list needed to plot it.
        """
        if self.show_plot_distribution == ON:
            length_x = self.game_rounds / self.ticks_per_second
            prepare_plot(length_x, SECONDS, DISTRIBUTION)

        plot_dist = []
        self.tick = 0
        self.logging_distributions(0, plot_dist)
        for tick in range(1, self.game_rounds + 1):
            self.tick = tick
            self.update_strategies()
            if tick % self.ticks_per_second == 0:
                self.logging_distributions(tick, plot_dist)

        return self.agents.get_strategy_distribution(), plot_dist
