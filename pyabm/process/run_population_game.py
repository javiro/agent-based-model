from pyabm.common.base.game import AgentGame


def play_population_game(pool_parameter=None):
    g = AgentGame()

    print("The initial distribution is: {}".format(g.agents.get_strategy_distribution()))
    _, distribution_evolution = g.run_population_game()
    print("The final distribution is: {}".format(g.agents.get_strategy_distribution()))
    return distribution_evolution
