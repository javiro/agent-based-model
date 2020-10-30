import random
import numpy as np

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
                 consider_imitating_self=True):
        """

        :param n_of_agents:
        :param num_of_channels:
        :param revision_protocol:
        :param random_initial_condition:
        :param consider_imitating_self:
        """
        self.n_of_agents = n_of_agents
        self.num_of_channels = num_of_channels
        self.revision_protocol = revision_protocol
        self.random_initial_condition = random_initial_condition
        self.initial_condition = self.__get_initial_condition(random_initial_condition)
        self.population = self.__populate_group()
        self.consider_imitating_self = consider_imitating_self
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

    def get_player(self, player_1):
        """Returns a random opponent avoiding the play of an agent with himself if consider_imitating_self is set to
        false.

        :param player_1:
        :return:
        """
        player_2 = self.population[random.randint(0, len(self.population) - 1)]
        if self.consider_imitating_self:
            return player_2
        else:
            while player_2 == player_1:
                player_2 = self.population[random.randint(0, len(self.population) - 1)]
            return player_2

    def get_strategy_distribution(self):
        strategies = [player.strategy for player in self.population]
        distribution = np.histogram(strategies, bins=list(range(self.num_of_channels + 1)))[0]
        return distribution
