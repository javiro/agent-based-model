import random
import numpy as np
import scipy.special

from pyabm.common.base.population import AgentPopulation
from pyabm.common.constants import *
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
                 prob_revision=0.001, n_of_revisions_per_tick=10, number_of_trials=10, use_prob_revision=ON,
                 ticks_per_second=5, consider_imitating_self=True, payoff_matrix=None, payoffs_velocity=0.5,
                 revision_protocol=BEP, show_plot_distribution=ON, dynamic_payoff_matrix=False):
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
        :param prob_revision: defines the probability that an agent is assigned an opportunity of revision.
        :param n_of_revisions_per_tick: if use_prob_revision is off, this parameter defines the number of revising
            agents.
        :param number_of_trials: specifies the size of the sample of opponents to test the strategies with.
        :param use_prob_revision: defines the assignment of revision opportunities to agents. If it is on, then
            assignments are stochastic and independent.
        :param ticks_per_second: Number of ticks per second.
        :param consider_imitating_self:
        :param payoff_matrix:
        :param payoffs_velocity:
        :param revision_protocol:
        :param dynamic_payoff_matrix:
        """
        self.game_rounds = game_rounds
        self.tick = None
        self.num_of_channels = num_of_channels
        self.n_of_agents = n_of_agents
        self.n_of_candidates = n_of_candidates
        self.random_initial_condition = random_initial_condition
        self.prob_revision = prob_revision
        self.n_of_revisions_per_tick = n_of_revisions_per_tick
        self.number_of_trials = number_of_trials
        self.use_prob_revision = use_prob_revision
        self.consider_imitating_self = consider_imitating_self
        self.payoff_matrix = self.__get_payoff_matrix(payoff_matrix)
        self.maximum_payoff = np.max(self.payoff_matrix)
        self.minimum_payoff = np.min(self.payoff_matrix)
        self.payoffs_velocity = payoffs_velocity
        self.revision_protocol = revision_protocol
        self.show_plot_distribution = show_plot_distribution
        self.dynamic_payoff_matrix = dynamic_payoff_matrix
        self.agents = AgentPopulation(self.n_of_agents,
                                      self.num_of_channels,
                                      self.revision_protocol,
                                      self.random_initial_condition,
                                      self.consider_imitating_self)
        self.ticks_per_second = ticks_per_second
        self.count_of_states = self.__get_initial_count_of_states()

    def __get_payoff_matrix(self, payoff_matrix):
        n = self.num_of_channels
        if payoff_matrix is None:
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
        if self.use_prob_revision == ON:
            for player_1 in self.agents.population:
                if random.random() < self.prob_revision:
                    player_1.update_strategy(self)
        else:
            revising_population = random.sample(self.agents.population, self.n_of_revisions_per_tick)
            for player_1 in revising_population:
                player_1.update_strategy(self)

    def update_payoff_matrix(self, g):
        if self.payoff_matrix.shape[0] == 2:
            self.payoff_matrix = np.array([[1 + (np.sin(self.payoffs_velocity * g) + 1) / 2, 0],
                                           [0, 1 + (np.cos(self.payoffs_velocity * g) + 1) / 2]])

    def logging_distributions(self, g, plot_dist):
        distribution = self.agents.get_strategy_distribution()
        if self.show_plot_distribution == ON:
            plot_distribution(g, self.ticks_per_second, distribution, plot_dist)
        else:
            plot_dist.append(distribution[-1] / self.n_of_agents)
        print("Percentage of strategy 2 at time {}: {}"
              .format(g / self.ticks_per_second, distribution[-1] / self.n_of_agents))

    def __get_initial_count_of_states(self):
        num_of_states = int(scipy.special.binom(self.n_of_agents + self.num_of_channels - 1, self.num_of_channels - 1))
        dist_of_states = np.zeros(num_of_states)
        dist_of_states[self.random_initial_condition[1]] = 1
        return dist_of_states

    def get_count_of_states(self):
        distribution = self.agents.get_strategy_distribution()
        self.count_of_states[distribution[1]] += 1
        return self.count_of_states

    def run_population_game(self):
        """Starts up the clock and runs the population game allowing some agents to review their strategies, at each
        tick of time.

        :return: the distribution of strategies and a list needed to plot it.
        """
        if self.show_plot_distribution == ON:
            length_x = self.game_rounds / self.ticks_per_second
            prepare_plot(length_x, SECONDS, DISTRIBUTION)

        plot_dist = []
        for g in range(self.game_rounds):
            self.tick = g
            self.update_strategies()
            if g % self.ticks_per_second == 0:
                self.logging_distributions(g, plot_dist)
                if self.dynamic_payoff_matrix:
                    self.update_payoff_matrix(g / self.ticks_per_second)

        return self.agents.get_strategy_distribution(), plot_dist
