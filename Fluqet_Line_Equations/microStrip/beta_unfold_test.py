import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.microStrip.beta_unfold import SCFL_Model

s = time.time()

# ---------------------------- unit cell inputs from paper
unit_Cell_Len = 0.00402
D2 = 9.5e-5
D1 = 1e-4
D0 = 0.00134
width_loaded = 4e-6
width_unloaded = 1e-6

# ---------------------------- SC inputs
Height = 3e-7
thickness = 6e-8
critical_Temp = 14.7
op_temp = 4
pn = 0.000132
er = 11.44
ground_thickness = Height
tanD = 1.48351e-5

lineModel = SCFL_Model(unit_Cell_Len, D0, D1, D2, width_loaded, width_unloaded, er, Height, thickness, ground_thickness,
                       critical_Temp, pn, tanD, op_temp)

betaUnfoled, folded, freqs = [], [], []
a, r, x = [], [], []

StartFreq, EndFreq, resolution = 1e9, 12e9, 1000
for F in np.linspace(StartFreq, EndFreq, resolution):
    aa, bta, b, rr, xx = lineModel.beta_unfolded(F)
    betaUnfoled.append(bta)
    folded.append(b)
    freqs.append(F)
    a.append(aa)
    x.append(xx)
    r.append(rr)

print("total time: ", time.time() - s)

fig, (axs1, axs2) = plt.subplots(2)
axs1.plot(freqs, betaUnfoled)
axs1.plot(freqs, a)

axs2.plot(freqs, r)
axs2.plot(freqs, x)
plt.show()
