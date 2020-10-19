from pyabm.common.base.game import AgentGame
from pyabm.common.conf import Conf


def play_population_game():
    configuration_path = "resources/conf/pyabm.json"
    conf = Conf(configuration_path)
    game_rounds = conf.get_number_of_game_rounds()
    ticks_per_second = conf.get_number_of_ticks_per_second()
    num_of_channels = conf.get_number_of_channels()
    n_of_agents = conf.get_number_of_agents()
    n_of_candidates = conf.get_number_of_channels()
    random_initial_condition = conf.get_initial_distribution_of_strategies()
    prob_revision = conf.get_probability_of_revision()
    n_of_revisions_per_tick = conf.get_number_of_revisions_per_tick()
    n_of_trials = conf.get_number_of_trials()
    use_prob_revision = conf.get_use_probability_of_revision()
    consider_imitating_self = conf.get_consider_imitating_self()
    mean_dynamics = conf.get_mean_dynamics()
    payoffs_velocity = conf.get_payoffs_velocity_of_change()
    coordination = conf.get_matrix_payoffs()
    show_plot_distribution = conf.get_show_plot_distribution()
    revision_protocol = conf.get_revision_protocol()
    g = AgentGame(game_rounds,
                  num_of_channels,
                  n_of_agents,
                  n_of_candidates,
                  random_initial_condition,
                  prob_revision,
                  n_of_revisions_per_tick,
                  n_of_trials,
                  use_prob_revision,
                  mean_dynamics,
                  ticks_per_second,
                  consider_imitating_self,
                  payoff_matrix=coordination,
                  payoffs_velocity=payoffs_velocity,
                  revision_protocol=revision_protocol,
                  show_plot_distribution=show_plot_distribution)

    print(g.agents.get_strategy_distribution())
    g.simulate_agent_game()
    print(g.agents.get_strategy_distribution())
