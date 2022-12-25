from typing import List
import matplotlib.pyplot as plt
from pylab import *

plt.ion()


def get_last_means(scores: List, N: int) -> float:
    """
    Computes the mean of the last N scores.
    """
    vals = scores[-N:]
    return (vals/N)


def plot(scores, mean_scores, last_20_mean, model_name) -> None:
    plt.clf()
    plt.title(f'Training Agent "{model_name}"')
    plt.xlabel('Games')
    plt.ylabel('Scores')

    plt.plot(scores, label='Score', color='blue')
    plt.plot(mean_scores, label='Mean Score', color='red')
    plt.plot(last_20_mean, label='Moving average (20)', color='green')
    plt.ylim(ymin=0, ymax=max(max(scores)*1.1, 1))

    plt.legend()

    plt.pause(0.1)
    # plt.show()
