import random
import numpy as np

from pyabm.common.base.population import AgentPopulation
from pyabm.common.constants import *
from pyabm.common.exceptions import PyABMException
from pyabm.common.utils.plot import prepare_plot, plot_distribution


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

    def __init__(self, game_rounds, num_of_channels, n_of_agents, n_of_candidates, random_initial_condition,
                 update_strategies_mode, noise, number_of_trials=10, ticks_per_second=5, payoff_matrix=None,
                 revision_protocol=BEP, show_plot_distribution=ON, dynamic_payoff_matrix=False,
                 number_of_steps_to_change_matrix=100, use_population_network=False, probability_of_edge=0.0,
                 network_algorithm="erdos-renyi", nearest_neighbors=2, probability_of_rewiring=0):
        """
        Complete matching is off since BEP does not consider it. Then the agents play his current strategy against a
        random sample of opponents. The size of this sample is specified by the parameter n-of-trials.
        Single sample is off, so the agent tests each of his candidate strategies against distinct, independent samples
        of n-of-trials opponents.

        Parameters
        ----------

        :param game_rounds:
        :param num_of_channels:
        :param n_of_agents:
        :param n_of_candidates: determines the total number of strategies the revising agent considers. The revising
            agent’s current strategy is always part of the set of candidates.
        :param update_strategies_mode:
        :param noise:
        :param number_of_trials: specifies the size of the sample of opponents to test the strategies with.
        :param ticks_per_second: Number of ticks per second.
        :param payoff_matrix:
        :param revision_protocol:
        :param dynamic_payoff_matrix:
        :param number_of_steps_to_change_matrix:
        :param use_population_network:
        :param probability_of_edge:
        :param network_algorithm:
        :param nearest_neighbors: Each node is joined with its k nearest neighbors in a ring topology.
        :param probability_of_rewiring:
        """
        self.game_rounds = game_rounds
        self.tick = None
        self.num_of_channels = num_of_channels
        self.n_of_agents = n_of_agents
        self.n_of_candidates = n_of_candidates
        self.random_initial_condition = random_initial_condition
        self.number_of_trials = number_of_trials
        self.update_strategies_mode = update_strategies_mode
        self.payoff_matrix = self.__get_payoff_matrix(payoff_matrix)
        self.maximum_payoff = np.max(self.payoff_matrix)
        self.minimum_payoff = np.min(self.payoff_matrix)
        self.revision_protocol = revision_protocol
        self.show_plot_distribution = show_plot_distribution
        self.dynamic_payoff_matrix = dynamic_payoff_matrix
        self.number_of_steps_to_change_matrix = number_of_steps_to_change_matrix
        self.noise = noise
        self.use_population_network = use_population_network
        self.probability_of_edge = probability_of_edge
        self.network_algorithm = network_algorithm
        self.nearest_neighbors = nearest_neighbors
        self.probability_of_rewiring = probability_of_rewiring
        self.agents = AgentPopulation(self.n_of_agents,
                                      self.num_of_channels,
                                      self.revision_protocol,
                                      self.random_initial_condition,
                                      self.use_population_network,
                                      self.probability_of_edge,
                                      self.network_algorithm,
                                      self.nearest_neighbors,
                                      self.probability_of_rewiring)
        self.ticks_per_second = ticks_per_second

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

    def update_payoff_matrix(self, g):
        if self.payoff_matrix.shape[0] == 2:
            if (g != 0) & (g % self.number_of_steps_to_change_matrix == 0):
                np.fill_diagonal(self.payoff_matrix,
                                 np.array(range(1, self.num_of_channels + 1))[self.payoff_matrix.diagonal() %
                                                                              self.num_of_channels])

    def logging_distributions(self, g, plot_dist):
        distribution = self.agents.get_strategy_distribution()
        if self.show_plot_distribution == ON:
            plot_distribution(g, self.ticks_per_second, distribution, plot_dist)
        else:
            plot_dist.append(distribution[-1] / self.n_of_agents)
            # print("tick: {}, ratio: {}".format(g, distribution[-1] / self.n_of_agents))
        # if self.num_of_channels < 3:
        #     print("Percentage of strategy 2 at time {}: {}"
        #           .format(g / self.ticks_per_second, distribution[-1] / self.n_of_agents))
        # else:
        #     print("Distribution of strategies at time {}: {}"
        #           .format(g / self.ticks_per_second, distribution / self.n_of_agents))

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
                if self.dynamic_payoff_matrix:
                    self.update_payoff_matrix(tick)

        return self.agents.get_strategy_distribution(), plot_dist
