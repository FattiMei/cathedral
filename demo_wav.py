import sys
import time
import numpy as np
import correlation
import matplotlib.pyplot as plt

from track import *


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python demo_wav.py <wav audio file>")
        sys.exit(1)

    track_name = sys.argv[1]
    _, _, track_name_abbr = track_name.partition('/')

    # tracks may have multiple channels, just merge them
    samplerate, data = load_track(track_name, merge=True)
    print(f'{data.size} samples at {samplerate} Hz')

    # do cross correlations with a maximum shift of 1 second
    start_time = time.perf_counter()
    solution = correlation.correlogram(data, samplerate)
    end_time = time.perf_counter()
    print(f'Computation time: {end_time - start_time:.2f} seconds')

    plt.title(f'Autocorrelation of `{track_name_abbr}`')
    plt.xlabel('delay [s]')
    plt.ylabel('autocorrelation')

    plt.plot(np.linspace(0, 1, samplerate), solution)
    plt.show()
