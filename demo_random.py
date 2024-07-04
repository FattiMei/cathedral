import correlation as corr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


NSAMPLES = 300


if __name__ == '__main__':
    original = np.random.rand(NSAMPLES)


    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()
    ax.set_title('Autocorrelation of a delayed random track')
    line, = ax.plot(corr.autocorr(corr.delay(original, 0)))
    ax.set_xlabel('tau')
    ax.set_ylabel('Autocorrelation')


    # adjust the main plot to make room for the sliders
    fig.subplots_adjust(left=0.25, bottom=0.5)


    delay_slider = Slider(
        fig.add_axes([0.25, 0.1, 0.65, 0.03]),
        label='time steps',
        valmin=0,
        valmax=original.size-1,
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
        line.set_ydata(corr.autocorr(corr.delay(
            original, 
            time    = int(delay_slider.val),
            level   = level_slider.val,
            feedback= feedback_slider.val
        )))

        fig.canvas.draw_idle()
        
        
    # register the update function with each slider
    delay_slider.on_changed(update)
    feedback_slider.on_changed(update)
    level_slider.on_changed(update)
    plt.show()