import json

from pyabm.common.constants import *
from pyabm.common.exceptions import PyABMException
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
    def get_probability_of_revision(self):
        """Returns the probability of revision.

        :return: the probability of revision.
        """
        return self.conf[PROBABILITY_OF_REVISION]

    @handle_config_parser_exception("Configuration error: ")
    def get_number_of_revisions_per_tick(self):
        """Returns the number of revisions per tick.

        :return: the number of revisions per tick.
        """
        return self.conf[NUMBER_OF_REVISIONS_PER_TICK]

    @handle_config_parser_exception("Configuration error: ")
    def get_number_of_trials(self):
        """Returns the number of trials.

        :return: the number of trials.
        """
        return self.conf[NUMBER_OF_TRIALS]

    @handle_config_parser_exception("Configuration error: ")
    def get_use_probability_of_revision(self):
        """Returns true in case the use of probability of revision is selected.

        :return: the use of probability of revision.
        """
        return self.conf[USE_PROBABILITY_OF_REVISION]

    @handle_config_parser_exception("Configuration error: ")
    def get_consider_imitating_self(self):
        """Returns true in case of considering imitating self.

        :return: the consideration of imitating self.
        """
        return self.conf[CONSIDER_IMITATING_SELF]

    @handle_config_parser_exception("Configuration error: ")
    def get_mean_dynamics(self):
        """Returns true in case of mean dynamics is switched on.

        :return: the consideration of imitating self.
        """
        return self.conf[MEAN_DYNAMICS]

    @handle_config_parser_exception("Configuration error: ")
    def get_payoffs_velocity_of_change(self):
        """Returns the velocity of change of the payoffs.

        :return: the velocity of change of the payoffs.
        """
        return self.conf[PAYOFFS_VELOCITY_OF_CHANGE]

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
    def get_revision_protocol(self):
        """Returns the revision protocol: bep, pairwise_difference or linear_dissatisfaction.

        :return: the revision protocol.
        """
        revision_protocol = self.conf[REVISION_PROTOCOL]
        allowed_protocols = [BEP, PAIRWISE_DIFFERENCE, LINEAR_DISSATISFACTION]
        if revision_protocol not in allowed_protocols:
            raise PyABMException(NOT_VALID_PROTOCOL.format(revision_protocol, allowed_protocols))
        return revision_protocol

    @handle_config_parser_exception("Configuration error: ")
    def get_number_of_simulations(self):
        """Returns the number of simulations to carry on.

        :return: the number of simulations.
        """
        return self.conf[NUMBER_OF_SIMULATIONS]
