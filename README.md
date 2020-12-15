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


### Payoffs


### Sequence of events

- Under construction.

### Classes.

#### Agent.

The agents are the minimal interacting units in the simulation. They can:
- set_strategy
- update_strategy --> update_strategy_under_bep_protocol


#### Game.

Class which implements the game regarding the revision protocol process.

It has these methods:

- play_agent_game
- let_players_update_strategies: it goes over the population and gives the chance of reviewing with probability 
"probability_revision"
- logging_distributions
- run_population_game

#### Population.

Class which implements the populations of players.

- get_opponent
- get_strategy_distribution

## How to use it

### Parameters (Under construction.)

- *number_of_game_rounds*: Number of game rounds at which the distribution of strategies is requested. Each round lasts
  a second.
- *ticks_per_second*: 
- *number_of_channels*: The number of available strategies.
- *number_of_agents*: The number of agents in the population.
- *initial_distribution_of_strategies*:
- *number_of_trials*:
- *update_strategies_mode*:
- *payoffs_velocity_of_change*:
- *matrix_payoffs*:
- *show_plot_distribution*:
- *number_of_simulations*:
- *noise*:
- *number_of_processors*:
- *use_network_structure*:
- *probability_of_edge*:
- *network_algorithm*:
- *nearest_neighbors*:
- *probability_of_rewiring*:
- *write_results_to_csv*:

### Buttons

- Under construction.

## Plots

- Under construction.

## License

**python-agent-based-model** has been designed to analyse the Best Experienced Payoff protocol in a generic population 
game.      
Copyright (C) 2020 Javier Rodríguez.

This program is free software; you can redistribute it and/or modify it under the terms of the [GNU General Public License](http://www.gnu.org/copyleft/gpl.html) as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,  but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU General Public License](http://www.gnu.org/copyleft/gpl.html) for more details.

You can download a copy of the [GNU General Public License](http://www.gnu.org/copyleft/gpl.html) by clicking [here](https://luis-r-izquierdo.github.io/centipede-test-two/LICENSE); you can also get a printed copy writing to the Free Software  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

Contact information:      
Javier Rodríguez
 e-mail: javiroma@gmail.com

## Modellers

This program has been designed by [Luis R. Izquierdo](http://luis.izqui.org), [Segismundo S. Izquierdo](http://segis.izqui.org) & Javier Rodríguez.

## References

Sandholm, W. H., Izquierdo, S. S., and Izquierdo, L. R. (2019).  Best experienced payoff dynamics and cooperation in the Centipede game. *Theoretical Economics*, 14: 1347-1385. https://doi.org/10.3982/TE3565

Sandholm, W. H., Izquierdo, S. S., and Izquierdo, L. R. (2020). Stability for best experienced payoff dynamics. *Journal of Economic Theory*, 185:104957. https://doi.org/10.1016/j.jet.2019.104957

------