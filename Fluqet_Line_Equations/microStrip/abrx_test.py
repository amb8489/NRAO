'''

Testing file for calculating A B R X
'''

import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.microStrip.abrx import SCFL_Model
from Supports.Support_Functions import nanoMeters_to_Meters, microMeters_to_Meters, mm_To_Meters, toGHz
s = time.time()

# ---------------------------- inputs ----------------------------
a, r, x, beta, betaUf, freqs = [], [], [], [], [], []



# ---------------------------- unit cell inputs from paper
# unit_Cell_Len = microMeters_to_Meters(2300)
# l1 = microMeters_to_Meters(50)
# width_unloaded = microMeters_to_Meters(1.49)
# width_loaded = width_unloaded * 1.2
#
# D0 = .0007666666666666666666
# D1 = 5e-5
# D2 = 5e-5
# D3 = .0001
# In_Order_loads_Widths = [D1, D2, D3]
# number_of_loads = len(In_Order_loads_Widths)
#
# # ---------------------------- SC inputs
# er = 10
# Height = nanoMeters_to_Meters(250)
# line_thickness = nanoMeters_to_Meters(60)
# ground_thickness = nanoMeters_to_Meters(300)
# Tc = 14.28
# T = 0
# pn = 1.008e-6
# tanD = 0
# Jc = 1




# # ---------------------------- unit cell inputs from paper
width_unloaded = microMeters_to_Meters(1)
width_loaded = microMeters_to_Meters(4)
D0 = mm_To_Meters(1.34)
D1 = microMeters_to_Meters(100)
D2 = microMeters_to_Meters(100)
D3 = microMeters_to_Meters(95)
unit_Cell_Len = mm_To_Meters(4.02)

In_Order_loads_Widths = [D1, D2, D3]
number_of_loads = len(In_Order_loads_Widths)

# ---------------------------- SC inputs
Height = nanoMeters_to_Meters(300)
line_thickness = nanoMeters_to_Meters(60)
ground_thickness = nanoMeters_to_Meters(300)
Tc = 14.7
T = 4
pn = 132
er = 11.44
tanD = 1.48351e-5
Jc = 1





Floquet_line = SCFL_Model(unit_Cell_Len, D0, In_Order_loads_Widths, number_of_loads, width_unloaded, width_loaded, er,
                       Height, line_thickness, ground_thickness, Tc, pn, tanD, T, Jc)

# ---------------------------- calculations -------------------

for F in np.linspace(toGHz(1), toGHz(8), 1000):
    aa, bta, unfolded, rr, xx = Floquet_line.abrx(F)
    beta.append(bta)
    betaUf.append(unfolded)
    a.append(aa)
    r.append(rr)
    x.append(xx)
    freqs.append(F)

print("total time: ", time.time() - s)

# ---------------------------- plots----------------------------
fig, (a1, a2, a3, a4) = plt.subplots(4)
a1.plot(freqs, beta)
a1.set_title('beta Unfolded')
a1.plot(freqs, betaUf)

a2.set_title('A')
a2.plot(freqs, a)

a3.set_title('R')
a3.plot(freqs, r)

a4.set_title('X')
a4.plot(freqs, x)
plt.subplots_adjust(hspace=1)
plt.show()
