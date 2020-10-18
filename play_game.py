import seaborn as sns

from pyabm.process.coordination_bep import play_coordination_bep
from pyabm.process.run_population_game import play_population_game
from pyabm.process.coordination_linear_dissatisfaction import play_coordination_linear_dissatisfaction

sns.set(style="whitegrid")


def main():
    # play_coordination_bep()
    play_population_game()
    # play_coordination_linear_dissatisfaction()


if __name__ == "__main__":
    main()
