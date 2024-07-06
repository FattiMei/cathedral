import numpy as np
import unittest


def apply(track, time: int, level: float = 0.5, feedback: float = 0.5):
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


def apply_vectorized(track, time: int, level: float = 0.5, feedback: float = 0.5):
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
        result[(track.size - remainder) :] = track[(track.size - remainder) :] + level * buffer[0 : remainder]

    return result


def remove_delay(track, time: int, level: float = 0.5, feedback: float = 0.5):
    # possibly apply the inverse transformation to reconstruct the original signal
    pass


class TestDelayImplementations(unittest.TestCase):
    def test_no_module(self):
        tau = 30
        samples     = tau * 12
        original = np.random.rand(samples)

        self.assertTrue(
            np.max(np.abs(
                apply(original, tau) - apply_vectorized(original, tau)
            )) < 1e-8
        )


    def test_remainder(self):
        samples = 1000
        tau = 39
        original = np.random.rand(samples)

        self.assertTrue(samples % tau != 0)

        self.assertTrue(
            np.max(np.abs(
                apply(original, tau) - apply_vectorized(original, tau)
            )) < 1e-8
        )


if __name__ == '__main__':
    unittest.main()
