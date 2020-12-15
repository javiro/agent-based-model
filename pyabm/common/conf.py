import json

from pyabm.common.constants import *
from pyabm.common.utils.decorators import handle_config_parser_exception


class Conf:
    """This class holds the methods that interacts with the PyABM configuration file."""

    def __init__(self, conf_path):
        with open(conf_path) as config_file:
            self.conf = json.load(config_file)

    @handle_config_parser_exception("Configuration error: ")
    def get_number_of_game_rounds(self):
        """Returns the number of rounds for the population game that will be simulated.

        :return: number of game rounds.
        """
        return self.conf[NUMBER_OF_GAME_ROUNDS]

    @handle_config_parser_exception("Configuration error: ")
    def get_number_of_ticks_per_second(self):
        """Returns the number of ticks per second.

        :return: number of ticks per second.
        """
        return self.conf[TICKS_PER_SECOND]

    @handle_config_parser_exception("Configuration error: ")
    def get_number_of_channels(self):
        """Returns the number of channels.

        :return: number of channels.
        """
        return self.conf[NUMBER_OF_CHANNELS]

    @handle_config_parser_exception("Configuration error: ")
    def get_number_of_agents(self):
        """Returns the number of agents.

        :return: number of agents.
        """
        return self.conf[NUMBER_OF_AGENTS]

    @handle_config_parser_exception("Configuration error: ")
    def get_initial_distribution_of_strategies(self):
        """Returns the initial distribution of agents playing the available strategies.

        :return: the initial distribution of strategies.
        """
        return self.conf[INITIAL_DISTRIBUTION_OF_STRATEGIES]

    @handle_config_parser_exception("Configuration error: ")
    def get_update_strategies_mode(self):
        """Returns update strategies mode: asynchronous_random_independent or all_in_one_tick.

        :return: the update strategies mode.
        """
        return self.conf[UPDATE_STRATEGIES_MODE]

    @handle_config_parser_exception("Configuration error: ")
    def get_number_of_trials(self):
        """Returns the number of trials.

        :return: the number of trials.
        """
        return self.conf[NUMBER_OF_TRIALS]

    @handle_config_parser_exception("Configuration error: ")
    def get_matrix_payoffs(self):
        """Returns the matrix of payoffs.

        :return: the matrix of payoffs.
        """
        return self.conf[MATRIX_PAYOFFS]

    @handle_config_parser_exception("Configuration error: ")
    def get_show_plot_distribution(self):
        """Returns true if we want to show the distribution plot.

        :return: the show plot distribution.
        """
        return self.conf[SHOW_PLOT_DISTRIBUTION]

    @handle_config_parser_exception("Configuration error: ")
    def get_number_of_simulations(self):
        """Returns the number of simulations to carry on.

        :return: the number of simulations.
        """
        return self.conf[NUMBER_OF_SIMULATIONS]

    @handle_config_parser_exception("Configuration error: ")
    def get_write_results_to_csv(self):
        """Returns True if write results to csv is required and False otherwise.

        :return: True if write results to csv is required and False otherwise.
        """
        return self.conf[WRITE_RESULTS_TO_CSV]

    @handle_config_parser_exception("Configuration error: ")
    def get_noise(self):
        """Returns the noise which will be considered in the simulation.

        :return: the noise.
        """
        return self.conf[NOISE]

    @handle_config_parser_exception("Configuration error: ")
    def get_number_of_processors(self):
        """Returns the number of processors.

        :return: the number of processors.
        """
        return self.conf[NUMBER_OF_PROCESSORS]

    @handle_config_parser_exception("Configuration error: ")
    def get_probability_of_edge(self):
        """Returns the probability of edge in the network game.

        :return: the probability of edge.
        """
        return self.conf[NETWORK][NETWORK_ATTRIBUTES][PROBABILITY_OF_EDGE]

    @handle_config_parser_exception("Configuration error: ")
    def get_random_network_algorithm(self):
        """Returns the random network algorithm generator.

        :return: the random network algorithm generator.
        """
        return self.conf[NETWORK][NETWORK_ATTRIBUTES][NETWORK_ALGORITHM]

    @handle_config_parser_exception("Configuration error: ")
    def get_nearest_neighbors(self):
        """Returns the nearest neighbors in a ring topology.

        :return: the nearest neighbors in a ring topology.
        """
        return self.conf[NETWORK][NETWORK_ATTRIBUTES][NEAREST_NEIGHBORS]

    @handle_config_parser_exception("Configuration error: ")
    def get_probability_of_rewiring(self):
        """Returns the probability of rewiring.

        :return: the probability of rewiring.
        """
        return self.conf[NETWORK][NETWORK_ATTRIBUTES][PROBABILITY_OF_REWIRING]

    @handle_config_parser_exception("Configuration error: ")
    def get_use_population_network(self):
        """Returns bool indicating whether network structure is required or not.

        :return: bool indicating whether network structure is required or not.
        """
        return self.conf[NETWORK][USE_NETWORK_STRUCTURE]
