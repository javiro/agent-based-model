import pandas as pd
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


def write_results_to_csv(run_number, number_of_game_rounds, distribution, number_of_simulations, revision_protocol,
                         update_strategies_mode, number_of_agents, number_of_channels):
    pd_runs = pd.DataFrame({"run_number": run_number,
                            "step": list(range(number_of_game_rounds + 1)),
                            "strategy_ratio": distribution})
    pd_runs.to_csv("python_{}_{}_strategies_{}_runs_{}_{}_agents.csv"
                   .format(revision_protocol,
                           number_of_channels,
                           number_of_simulations,
                           update_strategies_mode,
                           number_of_agents),
                   header=True if run_number == 0 else False,
                   mode="w" if run_number == 0 else "a",
                   sep="|",
                   index=False)
