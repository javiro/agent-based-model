import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import time

from pyabm.common.workspace import Workspace
from pyabm.process.run_population_game import play_population_game
from pyabm.common.utils.plot import write_partial_results_to_csv, write_result_to_csv


def play_n_population_game():
    start_time = time.time()
    workspace = Workspace()
    number_of_simulations = workspace.conf.get_number_of_simulations()
    number_of_processors = workspace.conf.get_number_of_processors()
    distributions = []

    if number_of_processors:
        a_pool = multiprocessing.Pool(processes=number_of_processors)
        distributions = a_pool.map(play_population_game, range(number_of_simulations))
        a_pool.close()
        write_result_to_csv(workspace.conf.get_number_of_game_rounds(),
                            distributions,
                            number_of_simulations,
                            workspace.conf.get_revision_protocol(),
                            workspace.conf.get_update_strategies_mode(),
                            workspace.conf.get_number_of_agents(),
                            workspace.conf.get_number_of_channels(),
                            workspace.conf.get_noise(),
                            workspace.conf.get_use_population_network(),
                            workspace.conf.get_probability_of_edge(),
                            workspace.conf.get_random_network_algorithm(),
                            workspace.conf.get_probability_of_rewiring())

    else:
        for run_number in range(number_of_simulations):
            distribution = play_population_game()
            distributions.append(distribution)
            if workspace.conf.get_write_results_to_csv():
                write_partial_results_to_csv(run_number,
                                             workspace.conf.get_number_of_game_rounds(),
                                             distribution,
                                             number_of_simulations,
                                             workspace.conf.get_revision_protocol(),
                                             workspace.conf.get_update_strategies_mode(),
                                             workspace.conf.get_number_of_agents(),
                                             workspace.conf.get_number_of_channels(),
                                             workspace.conf.get_noise())

    mean_distribution = np.array(distributions).mean(axis=0)
    print("The average of distributions is:")

    print(mean_distribution)
    plt.plot(mean_distribution)
    print("--- %s seconds ---" % (time.time() - start_time))
    plt.show()
