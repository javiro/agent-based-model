import random
import numpy as np

from networkx.generators.random_graphs import binomial_graph, barabasi_albert_graph, connected_watts_strogatz_graph

from pyabm.common.base.agent import Agent
from pyabm.common.workspace import Workspace


class AgentPopulation(object):
    """Class which implements the populations of players.

    Formulating such a model requires one to specify:

        (i) the number of agents N in the population,
        (ii) the n-strategy normal form game the agents are recurrently matched to play,
        (iii) the rule describing how revision opportunities are assigned to the agents, and
        (iv) the protocol according to which agents revise their strategies when opportunities to do so arise.
    """

    def __init__(self):
        workspace = Workspace()
        self.n_of_agents = workspace.conf.get_number_of_agents()
        self.num_of_channels = workspace.conf.get_number_of_channels()
        self.revision_protocol = workspace.conf.get_revision_protocol()
        self.random_initial_condition = workspace.conf.get_initial_distribution_of_strategies()
        self.initial_condition = self.__get_initial_condition(self.random_initial_condition)
        self.use_population_network = workspace.conf.get_use_population_network()
        self.population, self.population_map = self.__populate_group()
        if self.use_population_network:
            self.probability_of_edge = workspace.conf.get_probability_of_edge()
            self.network_algorithm = workspace.conf.get_random_network_algorithm()
            self.nearest_neighbors = workspace.conf.get_nearest_neighbors()
            self.probability_of_rewiring = workspace.conf.get_probability_of_rewiring()
            self.population_network = self.__get_population_network()

    def __get_initial_condition(self, random_initial_condition):
        if random_initial_condition == 'ON':
            random_initial_distribution = []
            return random_initial_distribution

        elif sum(random_initial_condition) == self.n_of_agents:
            assert len(random_initial_condition) == self.num_of_channels
            random_initial_distribution = random_initial_condition
            return random_initial_distribution

    def __populate_group(self):
        if self.random_initial_condition == 'ON':
            population = [Agent(i, self.num_of_channels, revision_protocol=self.revision_protocol)
                          for i in range(self.n_of_agents)]
        else:
            ids = random.sample(list(range(self.n_of_agents)), self.n_of_agents)
            population = [Agent(ids.pop(), self.num_of_channels, s, revision_protocol=self.revision_protocol)
                          for s in range(self.num_of_channels) for i in range(self.initial_condition[s])]
        population_map = {population[k].player_id: k for k in range(len(population))}
        return population, population_map

    def __get_population_network(self):
        """Returns a random graph, also known as an Erdös-Rényi graph or a binomial graph. It will have as many number
        of nodes as players.

        :return: random graph.
        """
        if self.network_algorithm == "erdos-renyi":
            return binomial_graph(self.n_of_agents, self.probability_of_edge)
        elif self.network_algorithm == "barabasi-albert":
            number_of_links = 1
            return barabasi_albert_graph(self.n_of_agents, number_of_links)
        elif self.network_algorithm == "sw":
            return connected_watts_strogatz_graph(
                self.n_of_agents, k=self.nearest_neighbors, p=self.probability_of_rewiring)

    def get_player(self, player_1):
        """Returns a random opponent avoiding the play of an agent with himself.

        :param player_1:
        :return:
        """
        player_2 = self.population[random.randint(0, len(self.population) - 1)]
        while player_2 == player_1:
            player_2 = self.population[random.randint(0, len(self.population) - 1)]
        return player_2

    def get_opponent(self, player_1):
        """Returns a random opponent avoiding the play of an agent with himself.

        :param player_1:
        :return:
        """
        if self.use_population_network:
            neighbors_index = random.choice(
                list(self.population_network.neighbors(self.population_map[player_1.player_id])))
            return self.population[neighbors_index]
        else:
            player_2 = self.population[random.randint(0, len(self.population) - 1)]
            while player_2 == player_1:
                player_2 = self.population[random.randint(0, len(self.population) - 1)]
            return player_2

    def get_strategy_distribution(self):
        strategies = [player.strategy for player in self.population]
        distribution = np.histogram(strategies, bins=list(range(self.num_of_channels + 1)))[0]
        return distribution
