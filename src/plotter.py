import matplotlib.pyplot as plt

plt.ion()


def plot(scores, mean_scores) -> None:
    plt.title('Training Agent')
    plt.xlabel('Games')
    plt.ylabel('Scores')

    plt.plot(scores)
    plt.plos(mean_scores)
    plt.ylim(ymin=0)

    plt.sleep(0.1)
    plt.show()
