import time
from SuperConductivityEquations.SCE import conductivity
import matplotlib.pyplot as plt

StartFreq, EndFreq = .001, 50
Tc = 14
tempK = 0.5




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
ax.set_ylabel('conductivity')
ax.set_xlabel('frequency')
# ax.axvline(x = Tc)

plt.show()
