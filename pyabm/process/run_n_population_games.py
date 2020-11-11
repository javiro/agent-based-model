import numpy as np
import matplotlib.pyplot as plt

from pyabm.common.conf import Conf
from pyabm.common.constants import OFF
from pyabm.process.run_population_game import play_population_game


def play_n_population_game():
    configuration_path = "resources/conf/pyabm.json"
    conf = Conf(configuration_path)
    number_of_simulations = conf.get_number_of_simulations()
    distributions = []
    for i in range(number_of_simulations):
        distributions.append(play_population_game(show_plot_distribution=OFF))

    mean_distribution = np.array(distributions).mean(axis=0)
    print("The average of distributions is:")
    print(mean_distribution)
    plt.plot(mean_distribution)
    plt.show()
