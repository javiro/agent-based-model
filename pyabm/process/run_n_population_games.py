import numpy as np
import matplotlib.pyplot as plt

from multiprocessing import Pool

from pyabm.common.conf import Conf
from pyabm.common.constants import OFF
from pyabm.process.run_population_game import play_population_game
from pyabm.common.utils.plot import write_results_to_csv


def play_n_population_game():
    configuration_path = "resources/conf/pyabm.json"
    conf = Conf(configuration_path)
    number_of_simulations = conf.get_number_of_simulations()
    distributions = []

    # pool = Pool()  # Create a multiprocessing Pool
    # pool.map(process_image, data_inputs)

    for run_number in range(number_of_simulations):
        distribution = play_population_game(show_plot_distribution=OFF)
        distributions.append(distribution)
        if conf.get_write_results_to_csv():
            write_results_to_csv(run_number,
                                 conf.get_number_of_game_rounds(),
                                 distribution,
                                 number_of_simulations,
                                 conf.get_revision_protocol(),
                                 conf.get_update_strategies_mode(),
                                 conf.get_number_of_agents(),
                                 conf.get_number_of_channels())

    mean_distribution = np.array(distributions).mean(axis=0)
    print("The average of distributions is:")
    print(mean_distribution)
    plt.plot(mean_distribution)
    plt.show()
