# Python agent based model

This code allows the user to run simulations of agents' population playing a generic symmetric game within an 
evolutionary frame with best experienced payoff revision protocol.

### Luis R. Izquierdo, Segismundo S. Izquierdo & Javier Rodríguez.

## How to install the model

To use python-agent-based-model you need to clone the repository or use it online through binder instead.
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/javiro/agent-based-model/HEAD)

## Description of the model

This section explains formally what **python-agent-based-model** implements. The information provided here should 
suffice to re-implement the same formal model in any sophisticated enough modelling platform.

### Population

There is one population consisting of *number_of_agents* individuals who play a generic game defined through its 
*matrix_payoffs*.

### Strategies

There are number_of_channels possible strategies.

### Payoffs

The user can define the matrix of payoffs in the configuration file. In case it were not provided it would be defined as:

$$
\begin{pmatrix}
1 & 0 & \cdots & 0\\
0 & 2 & \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 0 & \cdots & \textrm{number_of_channels}
\end{pmatrix} 
$$

### Sequence of events

Initially, if no distribution of strategies is provided, it is fixed randomly. Then, the agents are assigned a strategy 
following such distribution at random. The model runs in discrete time-steps called ticks. Within each tick the 
following sequence of events takes place:

    The order of the population is resampled.
    If updating mode is set to "all-in-one-tick":
      The process goes over the whole population and every agent revises her strategy and updates it.
    If updating mode is set to "all-in-one-tick":
      The following process is repeated "number_of_agents" times:
        One agent is chosen at random to revisit her strategy and update it.
    Revising agents test each strategy a number of times equal to number_of_trials:
        If there is network structure:
          Each revising agent selects a new opponent among her neighbors at random to play with.
        If there is no network structure:
          Each revising agent selects a new opponent at random to play with.
        The revising agent chooses the strategy which got the highest payoff. In case of ties, she chooses one of the
        best randomly with uniform distribution.

This sequence of events is repeated iteratively.

### Classes

#### Agent

The agents are the minimal interacting units in the simulation. They can:
- set_strategy
- update_strategy --> update_strategy_under_bep_protocol


#### Game

Class which implements the game regarding the revision protocol process.

It has these methods:

- play_agent_game
- let_players_update_strategies: it goes over the population and gives the chance of reviewing with probability 
"probability_revision"
- logging_distributions
- run_population_game

#### Population

Class which implements the populations of players.

- get_opponent
- get_strategy_distribution

## How to use it

The file that holds the parameters of configuration is resources/conf/pyabm.json.

### Parameters

- *number_of_game_rounds*: integer value with the number of game rounds at which the distribution of strategies is 
  requested. Each round lasts
  a second.
- *ticks_per_second*: integer value. At each tick of time, the whole population have the chance to review their 
  strategies.
- *number_of_channels*: integer value. The number of available strategies.
- *number_of_agents*: integer value. The number of agents in the population.
- *initial_distribution_of_strategies*: list, holding the initial distribution of strategies. In case it were empty, it 
  would be filled randomly.
- *number_of_trials*: integer value, representing the number of times that the revising agent repeats the test of each
  strategy.
- *update_strategies_mode*: it can be asynchronous_random_independent or all_in_one_tick.
- *matrix_payoffs*: list of lists, defining the matrix of payoffs. In case it were an empty list or even not present,
  the coordination payoff matrix would be set instead.
- *show_plot_distribution*: must be ON to show the evolution of the distribution.
- *number_of_simulations*: integer value, defining the number of times the simulation must be repeated.
- *noise*: float value, defining the noise in the simulation.
- *number_of_processors*: integer value, defining the number of processors to run the simulations.
- *use_network_structure*: true, if using a network structure in the population is required, or false otherwise.
- *probability_of_edge*: float value, representing the probability of edge in the Watts–Strogatz Small-World network. 
- *network_algorithm*: "barabasi-albert" or "sw".
- *nearest_neighbors*: integer value, holding the number of neighbors.
- *probability_of_rewiring*: float value, representing the probability of rewiring in the Watts–Strogatz Small-World
  network.
- *write_results_to_csv*: true, if writing the results to a csv is required, or false otherwise.

### Running the simulations

We can run just one simulation or a bunch of them:

- python play_game.py
- python simulate_a_bunch_of_games.py

## Plots

Running just one simulation, we can monitor the evolution of the distribution of strategies switching on the parameter
"show_plot_distribution".

In the other hand, the plots which show the comparison of results are the following:

  - [netlogo vs python](notebooks/bep_netlogo_vs_python.ipynb)
  - [netlogo vs python with noise](notebooks/bep_netlogo_vs_python-noise.ipynb)
  - [netlogo vs python over networks](notebooks/bep_netlogo_vs_python_networks.ipynb)

## License

**python-agent-based-model** has been designed to analyse the Best Experienced Payoff protocol in a generic population 
game.      
Copyright (C) 2020 Javier Rodríguez.

This program is free software; you can redistribute it and/or modify it under the terms of the
[GNU General Public License](http://www.gnu.org/copyleft/gpl.html) as published by the Free Software Foundation; either 
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,  but WITHOUT ANY WARRANTY; without even the implied 
warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
[GNU General Public License](http://www.gnu.org/copyleft/gpl.html) for more details.

You can download a copy of the [GNU General Public License](http://www.gnu.org/copyleft/gpl.html) by clicking
[here](https://luis-r-izquierdo.github.io/centipede-test-two/LICENSE); you can also get a printed copy writing to the 
Free Software  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

Contact information:      
Javier Rodríguez
 e-mail: javiroma@gmail.com

## Modellers

This program has been designed by [Luis R. Izquierdo](http://luis.izqui.org),
[Segismundo S. Izquierdo](http://segis.izqui.org) & Javier Rodríguez.

## References

Sandholm, W. H., Izquierdo, S. S., and Izquierdo, L. R. (2019).  Best experienced payoff dynamics and cooperation in
the Centipede game. *Theoretical Economics*, 14: 1347-1385. https://doi.org/10.3982/TE3565

Sandholm, W. H., Izquierdo, S. S., and Izquierdo, L. R. (2020). Stability for best experienced payoff dynamics.
*Journal of Economic Theory*, 185:104957. https://doi.org/10.1016/j.jet.2019.104957

------