import sys
import time
import numpy as np

from track import *


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python demo_wav.py <wav audio file> <delay in ms to apply>")
        sys.exit(1)

    # tracks may have multiple channels, just merge them
    samplerate, data = load_track(sys.argv[1], merge=True)

    ms_delay     = int(sys.argv[2])
    sample_delay = int(1e-3 * ms_delay * samplerate)

    start_time = time.perf_counter()
    delayed = apply_delay(data, sample_delay)
    print(f'Computation time: {time.perf_counter() - start_time:.2f} seconds')

    save_track('out.wav', samplerate, delayed)
