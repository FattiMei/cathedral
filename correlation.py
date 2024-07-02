import numpy as np
import matplotlib.pyplot as plt


NSAMPLES = 300


def autocorr(x):
    # https://stackoverflow.com/questions/643699/how-can-i-use-numpy-correlate-to-do-autocorrelation
    x -= np.mean(x)

    return np.correlate(x, x, mode='full')[(x.size-1):]


def delay(track, tau: int):
    # one repetition for now
    n = track.size

    if tau > 0 and tau < n:
        return track + np.pad(track, (tau, 0))[0:n]
    else:
        return None


if __name__ == '__main__':
    original = np.random.rand(NSAMPLES)
    track = delay(original, 50)


    plt.plot(autocorr(track))
    plt.show()
