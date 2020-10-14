import seaborn as sns

from src.process.coordination_bep import play_coordination_bep
from src.process.coordination_pairwise_difference import play_coordination_pairwise_difference

sns.set(style="whitegrid")


def main():
    # play_coordination_bep()
    play_coordination_pairwise_difference()


if __name__ == '__main__':
    main()
