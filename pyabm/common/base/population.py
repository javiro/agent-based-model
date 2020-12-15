import random
import numpy as np

from networkx.generators.random_graphs import barabasi_albert_graph, connected_watts_strogatz_graph

from pyabm.common.base.agent import Agent
from pyabm.common.constants import *
from pyabm.common.exceptions import PyABMException
from pyabm.common.workspace import Workspace


class AgentPopulation(object):
    """Class which implements the populations of players who review their strategies following the best experienced
    payoff protocol.
    """

    def __init__(self):
        workspace = Workspace()
        self.n_of_agents = workspace.conf.get_number_of_agents()
        self.num_of_channels = workspace.conf.get_number_of_channels()
        self.random_initial_condition = workspace.conf.get_initial_distribution_of_strategies()
        self.use_population_network = workspace.conf.get_use_population_network()
        self.population, self.population_map = self.__populate_group()
        if self.use_population_network:
            self.probability_of_edge = workspace.conf.get_probability_of_edge()
            self.network_algorithm = workspace.conf.get_random_network_algorithm()
            self.nearest_neighbors = workspace.conf.get_nearest_neighbors()
            self.probability_of_rewiring = workspace.conf.get_probability_of_rewiring()
            self.population_network = self.__get_population_network()

    def __check_initial_condition(self, random_initial_condition):
        """Checks whether the initial condition match the number of players and channels.

        :param random_initial_condition: list, holding the initial distribution of players with each strategy.
        """
        if sum(random_initial_condition) != self.n_of_agents:
            raise PyABMException(INITIAL_CONDITION_DO_NOT_MATCH_THE_NUMBER_OF_PLAYERS)
        if len(random_initial_condition) != self.num_of_channels:
            raise PyABMException(INITIAL_CONDITION_DO_NOT_MATCH_THE_NUMBER_OF_CHANNELS)

    def __populate_group(self):
        """It settles the crowd of agents following the initial condition in case it were required or randomly
        otherwise. It's important to note that it ensures that the strategies are randomly spread.

        :return:
            - A crowded instance of the classed.
            - Python dictionary which maps the id to the index within the instance.
        """
        if self.random_initial_condition == ON:
            population = [Agent(i, self.num_of_channels) for i in range(self.n_of_agents)]
        else:
            self.__check_initial_condition(self.random_initial_condition)
            ids = random.sample(list(range(self.n_of_agents)), self.n_of_agents)
            strategies = random.sample(
                [s for s in range(self.num_of_channels) for i in range(self.random_initial_condition[s])],
                self.n_of_agents)
            population = [Agent(ids.pop(), self.num_of_channels, s) for s in strategies]
        population_map = {population[k].player_id: k for k in range(len(population))}
        return population, population_map

    def __get_population_network(self):
        """Returns a random graph which is built following one of these algorithms: Barabasi-Albert o Small World. It
        will have as many number of nodes as players.

        :return: NetworkX random graph, following the required algorithm.
        """
        if self.network_algorithm == BARABASI_ALBERT:
            number_of_links = 1
            return barabasi_albert_graph(self.n_of_agents, number_of_links)
        elif self.network_algorithm == SMALL_WORLD:
            return connected_watts_strogatz_graph(
                self.n_of_agents, k=self.nearest_neighbors, p=self.probability_of_rewiring)
        else:
            raise PyABMException(
                NOT_VALID_NETWORK_ALGORITHM.format(self.network_algorithm, [BARABASI_ALBERT, SMALL_WORLD]))

    def get_opponent(self, player_id):
        """Returns a random opponent avoiding the play of an agent with himself.

        :param player_id: integer, holding the id of the player who is looking for an opponent.
        :return: agent, who represents the opponent.
        """
        if self.use_population_network:
            neighbors_index = random.choice(
                list(self.population_network.neighbors(self.population_map[player_id])))
            return self.population[neighbors_index]
        else:
            player_2 = self.population[random.randint(0, len(self.population) - 1)]
            while player_2.player_id == player_id:
                player_2 = self.population[random.randint(0, len(self.population) - 1)]
            return player_2

    def get_strategy_distribution(self):
        """Returns the histogram of strategies which are being used by the players of the population.

        :return: numpy array, holding the distribution of strategies.
        """
        strategies = [player.strategy for player in self.population]
        distribution = np.histogram(strategies, bins=list(range(self.num_of_channels + 1)))[0]
        return distribution
