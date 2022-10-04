import time

import scipy.constants

from SuperConductivityEquations.SCE import conductivityNormilized, calc_delta, gap_freq, fermiDistrib
import matplotlib.pyplot as plt




StartFreq, EndFreq = 0.001, 10
temp = 1
tc = 14

step = .05






x, freqs = [], []
freq = StartFreq
while freq < EndFreq:


    val = conductivityNormilized(freq, temp, tc)

    # print(val)
    x.append(val)
    freqs.append(freq)
    freq += step




# plot
fig, ax = plt.subplots()
ax.plot(freqs, x, linewidth=1.0,label='{} Kelvin'.format(temp))
ax.set_ylabel('conductivity')
ax.set_xlabel('frequency')
# plt.ylim([0, 1])
plt.legend()
plt.show()
