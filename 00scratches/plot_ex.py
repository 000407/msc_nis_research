import numpy as np
import matplotlib.pyplot as plt


def plot(x, y, fn):
    plt.scatter(x, y, fn)
    plt.grid()
    plt.show()


def main():
    a = -1
    b = 1
    rng = 10
    step = 1

    y, x = np.ogrid[0: rng: step, 0: rng: step]
    x = x.ravel()
    y = y.ravel()

    plt = (np.sqrt((x ** 3) - x * a - b)) % 53

    print(plt)


if __name__ == '__main__':
    main()
