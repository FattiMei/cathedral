import sys
import time
import correlation
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python demo_wav.py <wav audio file>")
        sys.exit(1)


    # tracks may have multiple channels, just merge them
    samplerate, data = wavfile.read(sys.argv[1])
    merged_channels = np.sum(data, axis=1)


    # do cross correlations with a maximum shift of 1 second
    start_time = time.perf_counter()
    solution = correlation.invert_delay_opencl(merged_channels, samplerate)
    print(f'Computation time: {time.perf_counter() - start_time:.2f} seconds')

    fig, ax = plt.subplots()
    ax.set_title('Autocorrelation of a music track')
    ax.set_xlabel('delay [s]')
    ax.set_ylabel('autocorrelation')
    
    plt.plot(np.linspace(0, 1, samplerate), solution)
    plt.show()
