import random
import numpy as np
import pandas as pd
import scipy.special

from matplotlib import pyplot as plt

from src.common.base.population import AgentPopulation
from src.common.constants import *


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
                 prob_revision=0.001, n_of_revisions_per_tick=10, n_of_trials=10, use_prob_revision=ON,
                 mean_dynamics=OFF, ticks_per_second=5, consider_imitating_self=True, payoff_matrix=None,
                 microstates=OFF, payoffs_velocity=0.5, revision_protocol=BEP, show_plot_distribution=ON):
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
        :param n_of_trials: specifies the size of the sample of opponents to test the strategies with.
        :param use_prob_revision: defines the assignment of revision opportunities to agents. If it is on, then
            assignments are stochastic and independent.
        :param mean_dynamics:
        :param ticks_per_second: Number of ticks per second.
        :param consider_imitating_self:
        :param payoff_matrix:
        :param microstates:
        :param payoffs_velocity:
        :param revision_protocol:
        """
        # Set internal parameters
        self.game_rounds = game_rounds
        self.tick = None
        self.num_of_channels = num_of_channels
        self.n_of_agents = n_of_agents
        self.n_of_candidates = n_of_candidates
        self.random_initial_condition = random_initial_condition
        self.prob_revision = prob_revision
        self.n_of_revisions_per_tick = n_of_revisions_per_tick
        self.n_of_trials = n_of_trials
        self.use_prob_revision = use_prob_revision
        self.consider_imitating_self = consider_imitating_self
        self.payoff_matrix = self.get_payoff_matrix(payoff_matrix)
        self.maximun_payoff = np.max(self.payoff_matrix)
        self.mean_dynamics = mean_dynamics
        self.microstates = microstates
        self.payoffs_velocity = payoffs_velocity
        self.revision_protocol = revision_protocol
        self.show_plot_distribution = show_plot_distribution
        self.agents = AgentPopulation(self.n_of_agents,
                                      self.num_of_channels,
                                      self.revision_protocol,
                                      self.random_initial_condition,
                                      self.consider_imitating_self)
        self.ticks_per_second = ticks_per_second
        self.count_of_states = self.get_initial_count_of_states()

    def get_payoff_matrix(self, payoff_matrix):
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

    def get_test_strategies(self, player_instance):
        strategies = list(range(self.num_of_channels))
        strategies.remove(player_instance.strategy)
        strategies.insert(0, player_instance.strategy)
        return strategies

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
        if self.payoff_matrix.shape == 2:
            self.payoff_matrix = np.array([[1 + (np.sin(self.payoffs_velocity * g) + 1) / 2, 0],
                                           [0, 1 + (np.cos(self.payoffs_velocity * g) + 1) / 2]])

    def logging_distributions(self, g, plot_dist, ax):
        distribution = self.agents.get_strategy_distribution()
        if self.show_plot_distribution == ON:
            plot_dist.append(distribution[::-1] / sum(distribution))
            df_plot_dist = pd.DataFrame(plot_dist)
            colors = [B, G, R, C, M, Y, K, K][:len(distribution)]
            df_plot_dist.columns = ["c{}".format(i) for i in range(len(df_plot_dist.columns))]
            plt.stackplot(df_plot_dist.index,
                          [df_plot_dist["{}".format(c)].values for c in df_plot_dist.columns],
                          colors=colors)
            plt.title("Second {}".format(g / self.ticks_per_second))
            plt.draw()
            plt.pause(0.0001)
        print("Percentage of strategy 2 at time {}: {}"
              .format(g / self.ticks_per_second, distribution[-1] / self.n_of_agents))

    def get_expectation_value(self):
        distribution = self.agents.get_strategy_distribution()
        # expectation = integral [x f_bar dx], f_bar = f / integral [f_dx]
        x = range(self.num_of_channels)
        integral_f_dx = sum(distribution * np.diff(range(self.num_of_channels + 1)))
        f_bar = distribution / integral_f_dx
        dx = np.diff(range(self.num_of_channels + 1))
        expectation = sum(x * f_bar * dx)
        return expectation

    def get_initial_count_of_states(self):
        num_of_states = int(scipy.special.binom(self.n_of_agents + self.num_of_channels - 1, self.num_of_channels - 1))
        dist_of_states = np.zeros(num_of_states)
        dist_of_states[self.random_initial_condition[1]] = 1
        return dist_of_states

    def get_count_of_states(self):
        distribution = self.agents.get_strategy_distribution()
        self.count_of_states[distribution[1]] += 1
        return self.count_of_states

    def get_mean_dynamics(self):
        count_of_states = self.get_count_of_states()
        # expectation = integral [x f_bar dx], f_bar = f / integral [f_dx]
        # f_bar = distribution_of_states
        # x = np.linspace(0.0, 1.0, len(count_of_states))  # We want the f_bar to give the probability of state n
        x = range(len(count_of_states))
        integral_f_dx = sum(count_of_states * np.diff(range(len(count_of_states) + 1)))
        f_bar = count_of_states / integral_f_dx
        dx = np.diff(range(len(count_of_states) + 1))
        expectation = sum(x * f_bar * dx)
        return expectation

    def simulate_agent_game(self, output_file):
        """
        Under the best experienced payoff protocol, a revising agent tests each of the "n_of_candidates" of strategies
        against a random agent, with each play of each strategy being against a newly drawn opponent. The revising
        agent then selects the strategy that obtained the greater payoff in the test, with ties resolved at random.
        :param output_file:
        :return:
        """
        plt.figure()
        length_x = self.game_rounds / self.ticks_per_second
        if self.mean_dynamics == OFF:
            ax = plt.axes(xlim=(0, length_x), ylim=(0, 1))
        else:
            ax = plt.axes()
        plt.xlabel(SECONDS)
        plt.ylabel(DISTRIBUTION)
        plot_dist = []
        mean_dynamic = []
        plt.ion()
        if self.microstates == ON:
            f = open(output_file, "a")

        for g in range(self.game_rounds):
            self.tick = g
            self.update_strategies()
            if (g % self.ticks_per_second == 0) & (self.mean_dynamics == OFF):
                self.logging_distributions(g, plot_dist, ax)
                self.update_payoff_matrix(g / self.ticks_per_second)
            else:
                # expectation = self.get_expectation_value()
                expectation = self.get_mean_dynamics()
                mean_dynamic.append(expectation)
                if self.microstates == ON:
                    [f.write("{},".format(player.strategy)) for player in self.agents.population[:-1]]
                    f.write("{}".format(self.agents.population[-1].strategy))
                    f.write("\n")
        if self.microstates == ON:
            f.close()

        if self.mean_dynamics == OFF:
            plt.show()
        else:
            plt.plot(mean_dynamic)
            plt.show(block=True)
        return self.agents.get_strategy_distribution(), plot_dist
