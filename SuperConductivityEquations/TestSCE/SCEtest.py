import time

import scipy.constants

from SuperConductivityEquations.SCE import conductivityNormalized, calc_delta, gap_freq, fermiDistrib, conductivity
import matplotlib.pyplot as plt




StartFreq, EndFreq = .01, 15
temp = 1
tc = 14
Pn = 52

step = .05


re,im, freqs = [], [],[]
freq = StartFreq
while freq < EndFreq:


    val = conductivityNormalized(freq, temp, tc)


    # print(val)
    re.append(val.real)
    im.append(val.imag)

    freqs.append(freq)
    freq += step




# plot
fig, ax = plt.subplots()
ax.plot(freqs, re, linewidth=1.0,label='{} Kelvin'.format(temp))
# ax.plot(freqs, im, linewidth=1.0,label='{} Kelvin'.format(temp))

ax.set_ylabel('conductivity')
ax.set_xlabel('frequency')
# plt.ylim([0, 1])
plt.legend()
plt.show()
