import numpy as np


def cross_correlation(x, shift):
    # only overlapping part is computed
    # normalize with the number of samples under the window
    return np.dot(x[shift:], x[:(x.size-shift)]) / (x.size - shift)


def invert_delay_serial(x, max_shift):
    x  = np.asarray(x, np.float32)
    x -= np.mean(x)

    result = np.zeros(max_shift)

    for i in range(result.size):
        result[i] = cross_correlation(x, i)

    return result
