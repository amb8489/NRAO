from SuperConductivityEquations.SCE import conductivity, Zs, conductivityNormalized
import time

startTime = time.time()
"""


        BLOCK 1 SUPER CONDUCTIVITY EQUATIONS


"""
# surface_impedance_Zs = Zs(fStart, MaterialConductivity, Thickness_ts)


# visualize


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


# The parametrized function to be plotted
def f(fRange, Temp, critTemp, PN):
    return [conductivity(freq, Temp, critTemp, PN) for freq in fRange]


freqRange = np.linspace(.1, 10, 100)

# Define initial parameters

# --- INPUTS ---

Tc = 14
Pn = 52
fStart = 1
fEnd = 10
Thickness_ts = 1
init_Temp = 0

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = ax.plot(freqRange, f(freqRange, init_Temp, Tc, Pn), lw=2)

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
axTemp = fig.add_axes([0.25, 0.1, 0.65, 0.03])
temp_slider = Slider(
    ax=axTemp,
    label='Temperature  [K]',
    valmin=0,
    valmax=Tc,
    valinit=init_Temp,
)


# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(f(freqRange, temp_slider.val, Tc, Pn))
    fig.canvas.draw_idle()


# register the update function with each slider
temp_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    temp_slider.reset()


button.on_clicked(reset)

plt.show()
