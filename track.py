import numpy as np
import unittest
from scipy.io import wavfile


def load_track(file, merge=False):
    samplerate, data = wavfile.read(file)

    # a cast to a floating point type is necessary to properly process the audio
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768

    if merge and len(data.shape) == 2:
        data = merge_tracks(data[:,0], data[:,1])

    return samplerate, data


def save_track(file, samplerate, data):
    wavfile.write(file, samplerate, data)


def merge_tracks(a, b):
    return (a + b) / 2


def apply_delay(track, time: int, level: float = 0.5, feedback: float = 0.5):
    if time == 0:
        return track
    elif time < 0 or time >= track.size:
        return None

    buffer = np.zeros(time)
    result = np.zeros(track.size)

    for i in range(track.size):
        result[i] += (1 - level) * track[i] + level * buffer[i % time]
        buffer[i % time] = track[i] + feedback * buffer[i % time]

    return result


def apply_delay_vectorized(track, time: int, level: float = 0.5, feedback: float = 0.5):
    if time == 0:
        return track
    elif time < 0 or time >= track.size:
        return None

    buffer = np.zeros(time)
    result = np.zeros(track.size)

    # update chunks of track
    for i in range(track.size // time):
        result[i*time : (i+1)*time] += (1 - level) * track[i*time : (i+1)*time] + level * buffer
        buffer = track[i*time : (i+1)*time] + feedback * buffer

    # deal with remaining chunk
    remainder = track.size % buffer.size

    if remainder != 0:
        result[(track.size - remainder) :] = track[(track.size - remainder) :] + level * buffer[0 : remainder]

    return result
