import time
from SuperConductivityEquations.SCE import conductivity
import matplotlib.pyplot as plt

StartFreq, EndFreq = .001, 30
Tc = 14.1
tempK = 0




step = .1
freq = StartFreq
x, freqs = [], []
while freq < EndFreq:

    val = conductivity(freq, tempK, Tc)

    # print(val)
    x.append(val)
    freqs.append(freq)
    freq += step

# plot
fig, ax = plt.subplots()
ax.plot(freqs, x, linewidth=1.0)
plt.show()
