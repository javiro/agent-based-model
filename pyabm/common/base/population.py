import random
import numpy as np

from networkx.generators.random_graphs import binomial_graph, barabasi_albert_graph, connected_watts_strogatz_graph
from networkx.generators.geometric import navigable_small_world_graph

from pyabm.common.base.agent import Agent


class AgentPopulation(object):
    """Class which implements the populations of players.

    Formulating such a model requires one to specify:

        (i) the number of agents N in the population,
        (ii) the n-strategy normal form game the agents are recurrently matched to play,
        (iii) the rule describing how revision opportunities are assigned to the agents, and
        (iv) the protocol according to which agents revise their strategies when opportunities to do so arise.
    """

    def __init__(self, n_of_agents, num_of_channels, revision_protocol, random_initial_condition='ON',
                 use_population_network=False, probability_of_edge=False, network_algorithm="erdos-renyi",
                 nearest_neighbors=2, probability_of_rewiring=0):
        """

        :param n_of_agents:
        :param num_of_channels:
        :param revision_protocol:
        :param random_initial_condition:
        :param use_population_network:
        :param probability_of_edge:
        :param network_algorithm:
        :param nearest_neighbors:
        :param probability_of_rewiring:
        """
        self.n_of_agents = n_of_agents
        self.num_of_channels = num_of_channels
        self.revision_protocol = revision_protocol
        self.random_initial_condition = random_initial_condition
        self.initial_condition = self.__get_initial_condition(random_initial_condition)
        self.use_population_network = use_population_network
        if self.use_population_network:
            self.population = self.__populate_group()
            self.probability_of_edge = probability_of_edge
            self.network_algorithm = network_algorithm
            self.nearest_neighbors = nearest_neighbors
            self.probability_of_rewiring = probability_of_rewiring
            self.population_network = self.__get_population_network()
        print(self.revision_protocol)

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
        return population

    def __get_population_network(self):
        """Returns a random graph, also known as an Erdös-Rényi graph or a binomial graph. It will have as many number
        of nodes as players.

        :return: random graph.
        """
        if self.network_algorithm == "erdos-renyi":
            return binomial_graph(self.n_of_agents, self.probability_of_edge)
        elif self.network_algorithm == "barabasi-albert":
            print("barabasi-albert")
            number_of_links = int(self.probability_of_edge * self.n_of_agents / 100)
            return barabasi_albert_graph(self.n_of_agents, number_of_links)
        elif self.network_algorithm == "small-world-Kleinberg":
            number_of_links = self.probability_of_edge * self.n_of_agents * (self.n_of_agents - 1) * 50
            return navigable_small_world_graph(self.n_of_agents, q=number_of_links)
        elif self.network_algorithm == "small-world-watts-strogatz":
            return connected_watts_strogatz_graph(
                self.n_of_agents, k=self.nearest_neighbors, p=self.probability_of_rewiring)
        elif self.network_algorithm == "ring":
            print("RING")
            return connected_watts_strogatz_graph(self.n_of_agents, k=2, p=self.probability_of_rewiring)

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
            p2 = random.choice(list(self.population_network.neighbors(player_1.player_id)))
            return self.population[p2]
        else:
            player_2 = self.population[random.randint(0, len(self.population) - 1)]
            while player_2 == player_1:
                player_2 = self.population[random.randint(0, len(self.population) - 1)]
            return player_2

    def get_strategy_distribution(self):
        strategies = [player.strategy for player in self.population]
        distribution = np.histogram(strategies, bins=list(range(self.num_of_channels + 1)))[0]
        return distribution
