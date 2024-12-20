import numpy as np
import correlation
import delay
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


NSAMPLES = 300


if __name__ == '__main__':
    track = np.random.uniform(low=-1.0, high=1.0, size=NSAMPLES)
    correlogram = lambda track: correlation.correlogram(track, NSAMPLES-1, method='fft')

    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()
    ax.set_title('Autocorrelation of a delayed random track')
    ax.set_xlabel('tau')
    ax.set_ylabel('Autocorrelation')

    corr = correlogram(track)
    line, = ax.plot(corr)
    point = ax.scatter(0, corr[0], color='red', facecolors='none', marker='o')

    # adjust the main plot to make room for the sliders
    fig.subplots_adjust(left=0.25, bottom=0.5)

    delay_slider = Slider(
        fig.add_axes([0.25, 0.1, 0.65, 0.03]),
        label='time steps',
        valmin=0,
        valmax=track.size-1,
        valinit=0,
        valstep=1
    )

    feedback_slider = Slider(
        fig.add_axes([0.25, 0.2, 0.65, 0.03]),
        label='feedback',
        valmin=0,
        valmax=1,
        valinit=0.5,
    )

    level_slider = Slider(
        fig.add_axes([0.25, 0.3, 0.65, 0.03]),
        label='level',
        valmin=0,
        valmax=1,
        valinit=0.5,
    )

    # The function to be called anytime a slider's value changes
    def update(val):
        shift = int(delay_slider.val)

        corr = correlogram(delay.apply(
            track, 
            time    = shift,
            level   = level_slider.val,
            feedback= feedback_slider.val
        ))

        line.set_ydata(corr)
        point.set_offsets([shift, corr[shift]])

        fig.canvas.draw_idle()

    # register the update function with each slider
    delay_slider.on_changed(update)
    feedback_slider.on_changed(update)
    level_slider.on_changed(update)
    plt.show()
