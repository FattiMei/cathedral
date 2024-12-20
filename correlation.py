import numpy as np
from scipy.fft import fft, ifft


def xcorr(x: np.array, shift: int):
    # only overlapping part is computed and result is normalized with the number of samples under the window
    return np.dot(x[shift:], x[:(x.size-shift)]) / (x.size - shift)


def correlogram(x: np.array, maxshift: int, method='fft'):
    assert(0 < maxshift < len(x))

    if method == 'fft':
        X = fft(x)
        P = np.abs(X) ** 2

        corr = ifft(P).real
        corr = corr / corr[0]

        return corr[0:maxshift]

    elif method == 'serial':
        corr = np.zeros(maxshift)

        x = np.asarray(x, np.float32)
        x = x - np.mean(x)

        for i in range(maxshift):
            corr[i] = xcorr(x, i)

        return corr

    else:
        ValueError("Supported methods for autocorrelation are {'fft, 'serial'}")
