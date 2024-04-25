import sys
import matplotlib.pyplot as plt


if __name__ == '__main__':
    data = [float(x) for x in sys.stdin.read().splitlines()]

    plt.plot(data)
    plt.title("Cross correlation")
    plt.show()
