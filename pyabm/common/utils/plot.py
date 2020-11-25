import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from pyabm.common.constants import B, G, R, C, M, Y, K


def prepare_plot(length_x, xlabel, ylabel):
    plt.figure()
    plt.axes(xlim=(0, length_x), ylim=(0, 1))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ion()


def plot_distribution(g, ticks_per_second, distribution, plot_dist):
    plot_dist.append(distribution[::-1] / sum(distribution))
    df_plot_dist = pd.DataFrame(plot_dist)
    colors = [B, G, R, C, M, Y, K, K][:len(distribution)]
    df_plot_dist.columns = ["c{}".format(i) for i in range(len(df_plot_dist.columns))]
    plt.stackplot(df_plot_dist.index,
                  [df_plot_dist["{}".format(c)].values for c in df_plot_dist.columns],
                  colors=colors)
    plt.title("Second {}".format(g / ticks_per_second))
    plt.draw()
    plt.pause(0.0001)


def write_partial_results_to_csv(run_number, number_of_game_rounds, distribution, number_of_simulations,
                                 revision_protocol, update_strategies_mode, number_of_agents, number_of_channels,
                                 noise, use_network_structure, probability_of_edge, network_algorithm,
                                 probability_of_rewiring, nearest_neighbors):
    pd_runs = pd.DataFrame({"run_number": run_number,
                            "step": list(range(number_of_game_rounds + 1)),
                            "strategy_ratio": distribution})
    if use_network_structure:
        if "sw" in network_algorithm:
            filename = "python_{}_{}_strategies_{}_runs_{}_{}_agents_{}_noise_{}_rewiring_{}_net_alg_{}_neighbors.csv" \
                .format(revision_protocol,
                        number_of_channels,
                        number_of_simulations,
                        update_strategies_mode,
                        number_of_agents,
                        noise,
                        probability_of_rewiring,
                        network_algorithm,
                        nearest_neighbors)
        else:
            filename = "python_{}_{}_strategies_{}_runs_{}_{}_agents_{}_noise_{}_rewiring_{}_net_alg_{}_prob_edge.csv" \
                       .format(revision_protocol,
                               number_of_channels,
                               number_of_simulations,
                               update_strategies_mode,
                               number_of_agents,
                               noise,
                               probability_of_rewiring,
                               network_algorithm,
                               probability_of_edge)
        pd_runs.to_csv(filename,
                       header=True if run_number == 0 else False,
                       mode="w" if run_number == 0 else "a",
                       sep="|",
                       index=False)
    else:
        filename = "python_{}_{}_strategies_{}_runs_{}_{}_agents_{}_noise.csv" \
                   .format(revision_protocol,
                           number_of_channels,
                           number_of_simulations,
                           update_strategies_mode,
                           number_of_agents,
                           noise)
        pd_runs.to_csv(filename,
                       header=True if run_number == 0 else False,
                       mode="w" if run_number == 0 else "a",
                       sep="|",
                       index=False)


def write_result_to_csv(number_of_game_rounds, distributions, number_of_simulations, revision_protocol,
                        update_strategies_mode, number_of_agents, number_of_channels, noise, use_network_structure,
                        probability_of_edge, network_algorithm, probability_of_rewiring):
    run_numbers = [[run_number for game_round in range(number_of_game_rounds + 1)]
                   for run_number in range(number_of_simulations)]
    step = [list(range(number_of_game_rounds + 1)) for run_number in range(number_of_simulations)]

    print(np.array(run_numbers).shape)
    print(np.array(step).shape)
    print(np.array(distributions).shape)
    pd_runs = pd.DataFrame({"run_number": np.array(run_numbers).reshape(1, -1)[0],
                            "step": np.array(step).reshape(1, -1)[0],
                            "strategy_ratio": np.array(distributions).reshape(1, -1)[0]})
    if use_network_structure:
        filename = "python_{}_{}_strategies_{}_runs_{}_{}_agents_{}_noise_{}_rewiring_{}_net_alg_{}_prob_edge.csv" \
            .format(revision_protocol,
                    number_of_channels,
                    number_of_simulations,
                    update_strategies_mode,
                    number_of_agents,
                    noise,
                    probability_of_rewiring,
                    network_algorithm,
                    probability_of_edge)
    else:
        filename = "python_{}_{}_strategies_{}_runs_{}_{}_agents_{}_noise.csv"\
            .format(revision_protocol,
                    number_of_channels,
                    number_of_simulations,
                    update_strategies_mode,
                    number_of_agents,
                    noise)
    pd_runs.to_csv(filename,
                   header=True,
                   sep="|",
                   index=False)
