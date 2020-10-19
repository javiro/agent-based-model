import pandas as pd
from matplotlib import pyplot as plt

from pyabm.common.constants import B, G, R, C, M, Y, K


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
