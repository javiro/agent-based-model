import seaborn as sns

from pyabm.common.base.game import AgentGame
from pyabm.common.constants import BEP


def play_coordination_bep():
    game_rounds = 100
    ticks_per_second = 5
    num_of_channels = 2
    n_of_agents = 200
    n_of_candidates = num_of_channels
    random_initial_condition = [100, 100]
    prob_revision = 0.2
    n_of_revisions_per_tick = 10
    n_of_trials = 1
    use_prob_revision = 'ON'
    consider_imitating_self = True
    mean_dynamics = 'OFF'
    payoffs_velocity = 0.2
    microstates = 'OFF'
    prisioner_matrix = [[-5, -1], [-10, -2]]
    penalti_matrix = [[0, 1], [1, 0]]
    flg = [[1, 2, 3], [4, 3, 4], [3, 2, 5]]
    # coordination = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
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
                  revision_protocol=BEP)

    print(g.agents.get_strategy_distribution())
    g.simulate_agent_game('microstates')
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
    #     g.simulate_drone_game('microstates{}'.format(i))
    # print(g.drones.get_strategy_distribution())
