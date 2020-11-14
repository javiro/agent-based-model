from pyabm.common.base.game import AgentGame
from pyabm.common.conf import Conf


def play_population_game(show_plot_distribution=None):
    configuration_path = "resources/conf/pyabm.json"
    conf = Conf(configuration_path)
    game_rounds = conf.get_number_of_game_rounds()
    ticks_per_second = conf.get_number_of_ticks_per_second()
    num_of_channels = conf.get_number_of_channels()
    n_of_agents = conf.get_number_of_agents()
    n_of_candidates = conf.get_number_of_channels()
    random_initial_condition = conf.get_initial_distribution_of_strategies()
    update_strategies_mode = conf.get_update_strategies_mode()
    number_of_trials = conf.get_number_of_trials()
    coordination = conf.get_matrix_payoffs()
    revision_protocol = conf.get_revision_protocol()
    dynamic_payoff_matrix = conf.get_dynamic_payoff_matrix()
    number_of_steps_to_change_matrix = conf.get_number_of_steps_to_change_matrix()
    if not show_plot_distribution:
        show_plot_distribution = conf.get_show_plot_distribution()
    g = AgentGame(game_rounds, num_of_channels, n_of_agents, n_of_candidates, random_initial_condition,
                  update_strategies_mode, number_of_trials, ticks_per_second, payoff_matrix=coordination,
                  revision_protocol=revision_protocol, show_plot_distribution=show_plot_distribution,
                  dynamic_payoff_matrix=dynamic_payoff_matrix,
                  number_of_steps_to_change_matrix=number_of_steps_to_change_matrix)

    print("The initial distribution is: {}".format(g.agents.get_strategy_distribution()))
    _, distribution_evolution = g.run_population_game()
    print("The final distribution is: {}".format(g.agents.get_strategy_distribution()))
    return distribution_evolution
