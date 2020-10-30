# Python agent based model

This code allows us to run simulations of populations of agents playing a generic symmetric game within an evolutionary
game theory frame.

## Classes.

### Agent.

The agents are the minimal units interacting in the simulation. They can:
- set_strategy
- update_strategy

### Game.

It's a population game which gives some random agents the possibility of revisiting their strategies, at each tick of
time.
It has these methods:

- update_strategies: it goes over the population and gives the chance of reviewing with probability 
"probability_revision"
- logging_distributions
- update_payoff_matrix

### Population.

Class which implements the populations of players.

- get_player
- get_strategy_distribution