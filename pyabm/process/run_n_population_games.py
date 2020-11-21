import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import time

from pyabm.common.conf import Conf
from pyabm.common.constants import OFF
from pyabm.process.run_population_game import play_population_game
from pyabm.common.utils.plot import write_partial_results_to_csv, write_result_to_csv


def play_n_population_game():
    start_time = time.time()
    configuration_path = "resources/conf/pyabm.json"
    conf = Conf(configuration_path)
    number_of_simulations = conf.get_number_of_simulations()
    number_of_processors = conf.get_number_of_processors()
    distributions = []

    if number_of_processors:
        a_pool = multiprocessing.Pool(processes=number_of_processors)
        distributions = a_pool.map(play_population_game, range(number_of_simulations))
        a_pool.close()
        write_result_to_csv(conf.get_number_of_game_rounds(),
                            distributions,
                            number_of_simulations,
                            conf.get_revision_protocol(),
                            conf.get_update_strategies_mode(),
                            conf.get_number_of_agents(),
                            conf.get_number_of_channels(),
                            conf.get_noise(),
                            conf.get_probability_of_edge())

    else:
        for run_number in range(number_of_simulations):
            distribution = play_population_game(show_plot_distribution=OFF)
            distributions.append(distribution)
            if conf.get_write_results_to_csv():
                write_partial_results_to_csv(run_number,
                                             conf.get_number_of_game_rounds(),
                                             distribution,
                                             number_of_simulations,
                                             conf.get_revision_protocol(),
                                             conf.get_update_strategies_mode(),
                                             conf.get_number_of_agents(),
                                             conf.get_number_of_channels(),
                                             conf.get_noise())

    mean_distribution = np.array(distributions).mean(axis=0)
    print("The average of distributions is:")

    print(mean_distribution)
    plt.plot(mean_distribution)
    print("--- %s seconds ---" % (time.time() - start_time))
    plt.show()
