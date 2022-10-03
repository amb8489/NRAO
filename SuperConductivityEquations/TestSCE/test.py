import time

import scipy.constants

from SuperConductivityEquations.SCE import conductivity, calc_delta, gap_freq
import matplotlib.pyplot as plt




StartFreq, EndFreq = 0, 10
temp = 3
tc = 14

step = .05




D = calc_delta(0, 14.1)
print("delta:  ", D)
print("fgap : ", gap_freq(D))









x, freqs = [], []
freq = StartFreq
while freq < EndFreq:


    val = conductivity(freq, temp, tc)

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
