import numpy as np
import matplotlib.pyplot as plt

from pyabm.common.base.game import AgentGame
from pyabm.common.conf import Conf
from pyabm.common.constants import OFF
from pyabm.process.run_population_game import play_population_game


def play_n_population_game():
    configuration_path = "resources/conf/pyabm.json"
    conf = Conf(configuration_path)
    number_of_simulations = conf.get_number_of_simulations()
    payoffs_velocity = conf.get_payoffs_velocity_of_change()
    game_rounds = conf.get_number_of_game_rounds()
    ticks_per_second = conf.get_number_of_ticks_per_second()
    distributions = []
    for i in range(number_of_simulations):
        distributions.append(play_population_game(mean_dynamics=OFF, show_plot_distribution=OFF))

    mean_distribution = np.array(distributions).mean(axis=0)
    print("The average of distributions is:")
    print(mean_distribution)
    plt.plot(mean_distribution)
    payoff_signal = [(np.sin(payoffs_velocity * g) + 1) / 2
                     for g in range(game_rounds // ticks_per_second)]
    plt.plot(payoff_signal)

    plt.show()
