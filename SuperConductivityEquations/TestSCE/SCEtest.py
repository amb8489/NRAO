import time

import numpy as np

from SuperConductivityEquations.SCE import conductivityNormalized, calc_delta, gap_freq, fermiDistrib, conductivity, Zs
import matplotlib.pyplot as plt

temp = 10
tc = 14
Pn = 1.008e-6
ts = 3E-7

condut = []
zss = []
freqs = np.linspace(1, 10E9, 1000)

average = 0
trials = 1
for x in range(trials):
    startTime = time.time()
    for i, freq in enumerate(freqs):
        val = conductivity(freq, temp, tc, Pn)



        condut.append(val.real)
        zss.append(Zs(freq,val, ts))
    average += time.time() - startTime

print("avg time per run:", average / trials)

fig, (ax,a2) = plt.subplots(2)
ax.plot(freqs, condut, linewidth=1.0, label='{} Kelvin'.format(temp))
a2.plot(freqs, zss, linewidth=1.0, label='{} Kelvin'.format(temp))

plt.show()
