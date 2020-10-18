import seaborn as sns

from src.process.coordination_bep import play_coordination_bep
from src.process.coordination_pairwise_difference import play_coordination_pairwise_difference
from src.process.coordination_linear_dissatisfaction import play_coordination_linear_dissatisfaction

sns.set(style="whitegrid")


def main():
    # play_coordination_bep()
    play_coordination_pairwise_difference()
    # play_coordination_linear_dissatisfaction()


if __name__ == "__main__":
    main()
