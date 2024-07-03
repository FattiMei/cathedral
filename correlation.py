import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import Slider


NSAMPLES = 300


def autocorr(x):
    # https://stackoverflow.com/questions/643699/how-can-i-use-numpy-correlate-to-do-autocorrelation
    x -= np.mean(x)

    return np.correlate(x, x, mode='full')[(x.size-1):]


def delay(track, tau: int, effect = 0.5, feedback = 0.5):
    if tau == 0:
        return track
    elif tau < 0 or tau >= track.size:
        return None

    buffer = np.zeros(tau)
    result = np.zeros(track.size)

    # serial implementation, later will develop the vectorized
    for i in range(track.size):
        result[i] += track[i] + effect * buffer[i % tau]
        buffer[i % tau] = track[i] + feedback * buffer[i % tau]

    return result


if __name__ == '__main__':
    original = np.random.rand(NSAMPLES)


    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()
    line, = ax.plot(autocorr(delay(original, 0)))
    ax.set_xlabel('tau')
    ax.set_ylabel('Autocorrelation')


    # adjust the main plot to make room for the sliders
    fig.subplots_adjust(left=0.25, bottom=0.25)


    # Make a horizontal slider to control the frequency.
    ax_delay = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    delay_slider = Slider(
        ax=ax_delay,
        label='delay steps',
        valmin=0,
        valmax=original.size-1,
        valinit=0,
        valstep=1
    )


    # The function to be called anytime a slider's value changes
    def update(val):
        line.set_ydata(autocorr(delay(original, int(delay_slider.val))))
        fig.canvas.draw_idle()
        
        
    # register the update function with each slider
    delay_slider.on_changed(update)
    plt.show()
