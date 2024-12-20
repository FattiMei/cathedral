import sys
import time
import argparse
import numpy as np

from track import *


def clip_in_range(x, inf=0, sup=1):
    if x < inf:
        return inf

    elif x > sup:
        return sup

    return x


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='filename of the audio track to apply the delay (only WAV supported)')
    parser.add_argument('-delay', type=float, default=500, help='the amount of milliseconds of delay to apply to the track')
    parser.add_argument('-level', type=float, default=0.5, help='how loud the delay relative to the original signal (ranges from 0 to 1)')
    parser.add_argument('-feedback', type=float, default=0.5, help='controls the repetitions (ranges from 0 to 1, suggested < 0.5)')
    parser.add_argument('-output', '-o', type=str, default='out.wav', help='the name of the resulting file (only WAV supported)')

    args = parser.parse_args()
    track_name  = args.file
    delay_ms    = args.delay
    level       = clip_in_range(args.level)
    feedback    = clip_in_range(args.feedback)

    # tracks may have multiple channels, just merge them
    samplerate, data = load_track(track_name, merge=True)

    sample_delay = int(1e-3 * delay_ms * samplerate)

    start_time = time.perf_counter()
    delayed = apply_delay_vectorized(data, sample_delay, level=level, feedback=feedback)
    print(f'Computation time: {time.perf_counter() - start_time:.2f} seconds')

    save_track(args.output, samplerate, delayed)
