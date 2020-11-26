import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
from os import path

from pyabm.common.constants import *
from pyabm.common.workspace import Workspace


def prepare_plot(length_x, xlabel, ylabel):
    """

    :param length_x:
    :param xlabel:
    :param ylabel:
    :return:
    """
    plt.figure()
    plt.axes(xlim=(0, length_x), ylim=(0, 1))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ion()


def plot_distribution(g, ticks_per_second, distribution, plot_dist):
    """

    :param g:
    :param ticks_per_second:
    :param distribution:
    :param plot_dist:
    :return:
    """
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
    """

    :param run_number:
    :param number_of_game_rounds:
    :param distribution:
    :param number_of_simulations:
    :param revision_protocol:
    :param update_strategies_mode:
    :param number_of_agents:
    :param number_of_channels:
    :param noise:
    :param use_network_structure:
    :param probability_of_edge:
    :param network_algorithm:
    :param probability_of_rewiring:
    :param nearest_neighbors:
    :return:
    """
    workspace = Workspace()
    pd_runs = pd.DataFrame({RUN_NUMBER: run_number,
                            STEP: list(range(number_of_game_rounds + 1)),
                            STRATEGY_RATIO: distribution})
    if use_network_structure:
        if network_algorithm == "sw":
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
        pd_runs.to_csv(path.join(workspace.root, OUTPUTS, filename),
                       header=True if run_number == 0 else False,
                       mode=W if run_number == 0 else A,
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
        pd_runs.to_csv(path.join(workspace.root, OUTPUTS, filename),
                       header=True if run_number == 0 else False,
                       mode=W if run_number == 0 else A,
                       sep="|",
                       index=False)


def write_result_to_csv(number_of_game_rounds, distributions, number_of_simulations, revision_protocol,
                        update_strategies_mode, number_of_agents, number_of_channels, noise, use_network_structure,
                        probability_of_edge, network_algorithm, probability_of_rewiring, nearest_neighbors):
    """

    :param number_of_game_rounds:
    :param distributions:
    :param number_of_simulations:
    :param revision_protocol:
    :param update_strategies_mode:
    :param number_of_agents:
    :param number_of_channels:
    :param noise:
    :param use_network_structure:
    :param probability_of_edge:
    :param network_algorithm:
    :param probability_of_rewiring:
    :return:
    """
    workspace = Workspace()
    run_numbers = [[run_number for game_round in range(number_of_game_rounds + 1)]
                   for run_number in range(number_of_simulations)]
    step = [list(range(number_of_game_rounds + 1)) for run_number in range(number_of_simulations)]

    print(np.array(run_numbers).shape)
    print(np.array(step).shape)
    print(np.array(distributions).shape)
    pd_runs = pd.DataFrame({RUN_NUMBER: np.array(run_numbers).reshape(1, -1)[0],
                            STEP: np.array(step).reshape(1, -1)[0],
                            STRATEGY_RATIO: np.array(distributions).reshape(1, -1)[0]})
    if use_network_structure:
        if network_algorithm == "sw":
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
    else:
        filename = "python_{}_{}_strategies_{}_runs_{}_{}_agents_{}_noise.csv"\
            .format(revision_protocol,
                    number_of_channels,
                    number_of_simulations,
                    update_strategies_mode,
                    number_of_agents,
                    noise)
    pd_runs.to_csv(path.join(workspace.root, OUTPUTS, filename),
                   header=True,
                   sep="|",
                   index=False)
