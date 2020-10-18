import seaborn as sns

from src.common.base.game import AgentGame
from src.common.constants import LINEAR_DISSATISFACTION


def play_coordination_linear_dissatisfaction():
    game_rounds = 1000
    ticks_per_second = 5
    num_of_channels = 2
    n_of_agents = 200
    n_of_candidates = num_of_channels
    random_initial_condition = [0, 200]
    prob_revision = 0.2
    n_of_revisions_per_tick = 10
    n_of_trials = 1
    use_prob_revision = "ON"
    consider_imitating_self = True
    mean_dynamics = "OFF"
    payoffs_velocity = 0.2
    microstates = "OFF"
    show_plot_distribution = "OFF"
    prisioner_matrix = [[-5, -1], [-10, -2]]
    penalti_matrix = [[0, 1], [1, 0]]
    flg = [[1, 2, 3], [4, 3, 4], [3, 2, 5]]
    # coordination = [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]]
    coordination = [[1, 0], [0, 2]]
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
                  revision_protocol=LINEAR_DISSATISFACTION,
                  show_plot_distribution=show_plot_distribution)

    print(g.agents.get_strategy_distribution())
    g.simulate_agent_game("microstates")
    print(g.agents.get_strategy_distribution())

    # for i in range(10):
    #     g = DroneGame(game_rounds,
    #                   num_of_channels,
    #                   n_of_agents,
    #                   n_of_candidates,
    #                   random_initial_condition,
    #                   prob_revision,
    #                   n_of_revisions_per_tick,
    #                   n_of_trials,
    #                   use_prob_revision,
    #                   mean_dynamics,
    #                   ticks_per_second,
    #                   consider_imitating_self,
    #                   microstates=microstates)
    #     g.simulate_drone_game("microstates{}".format(i))
    # print(g.drones.get_strategy_distribution())
