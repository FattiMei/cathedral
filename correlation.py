import numpy as np


# maybe we will need FFT based solutions, especially with large tracks
def autocorr(x):
    # https://stackoverflow.com/questions/643699/how-can-i-use-numpy-correlate-to-do-autocorrelation
    x -= np.mean(x)

    return np.correlate(x, x, mode='full')[(x.size-1):]


def delay(track, time: int, level=0.5, feedback=0.5):
    if time == 0:
        return track
    elif time < 0 or time >= track.size:
        return None

    buffer = np.zeros(time)
    result = np.zeros(track.size)

    # serial implementation, later will develop the vectorized
    for i in range(track.size):
        result[i] += track[i] + level * buffer[i % time]
        buffer[i % time] = track[i] + feedback * buffer[i % time]

    return result


def delay_vectorized(track, time: int, level=0.5, feedback=0.5):
    if time == 0:
        return track
    elif time < 0 or time >= track.size:
        return None

    buffer = np.zeros(time)
    result = np.zeros(track.size)

    # update chunks of track
    for i in range(track.size // time):
        result[i*time : (i+1)*time] += track[i*time : (i+1)*time] + level * buffer
        buffer = track[i*time : (i+1)*time] + feedback * buffer

    # deal with remaining chunk
    remainder = track.size % buffer.size

    if remainder != 0:
        result[(track.size - remainder) :] = track[(track.size - remainder) :] + level * buffer

    return result
