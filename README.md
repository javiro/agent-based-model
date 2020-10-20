# Python agent based model

This code allows us to run simulations of populations of agents playing a 2x2 symmetric game within an evolutionary
game theory frame.

## Classes.

### Agent.

The agents are the minimal units interacting in the simulation. They can:
- set_strategy
- update_strategy

### Game.

It's a population game which gives some random agents the possibility of revisiting their strategies, at each tick of
time.
It has the methods:
-
 

### Population.

- get_player
- get_strategy_distribution