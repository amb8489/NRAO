import time

import numpy as np

from super_conductor_model.super_conductor_model import SuperConductivity

temp = 3
tc = 14.28
Pn = 1.008e-6
ts = 3E-7
sc = SuperConductivity(temp, tc, Pn)

condut = []
zss = []
freqs = np.linspace(1E9, 10E9, 1000)

average = 0
trials = 25
for x in range(trials):
    startTime = time.time()
    for freq in freqs:
        val = sc.conductivity(freq)
        # condut.append(val.real)
        # zss.append(sc.Zs(freq,val, ts))
    average += time.time() - startTime

print("avg time per run:", average / trials)

# fig, (ax,a2) = plt.subplots(2)
# ax.plot(freqs, condut, linewidth=1.0, label='{} Kelvin'.format(temp))
# a2.plot(freqs, zss, linewidth=1.0, label='{} Kelvin'.format(temp))
# plt.show()
