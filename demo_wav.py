import sys
import correlation as corr
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt


def solve_inverse_delay(x, shift_range):
    x -= np.mean(x)
    result = np.zeros(len(shift_range))

    for i in shift_range:
        result[i] = corr.cross_correlation(x, i)

    return result


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python demo_wav.py <wav audio file>")
        sys.exit(1)


    # tracks may have multiple channels
    samplerate, data = wavfile.read(sys.argv[1])
    merged_channels = np.asarray(np.sum(data, axis=1), dtype=np.float64)

    plt.plot(
        np.linspace(0, 1, samplerate),
        solve_inverse_delay(merged_channels, range(samplerate))
    )

    plt.show()
