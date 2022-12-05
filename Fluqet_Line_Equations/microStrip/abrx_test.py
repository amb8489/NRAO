'''
Testing file for calculating A B R X
'''

import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.microStrip.abrx import SCFL_Model
from Supports.Support_Functions import nanoMeters_to_Meters, microMeters_to_Meters, mm_To_Meters, toGHz
from Supports.constants import PI2

s = time.time()

# ---------------------------- inputs ----------------------------
a, r, x, beta, betaUf, freqs,RR,LL,GG,CC = [], [], [], [], [], [],[], [], [], []

# ---------------------------- unit cell inputs from paper
unit_Cell_Len = microMeters_to_Meters(2300)
l1 = microMeters_to_Meters(50)
width_unloaded = microMeters_to_Meters(1.49)
width_loaded = width_unloaded * 1.2

D0 = .0007666666666666666666
D1 = 5e-5
D2 = 5e-5
D3 = .0001
In_Order_loads_Widths = [D1, D2, D3]
number_of_loads = len(In_Order_loads_Widths)

# ---------------------------- SC inputs
er = 10
Height = nanoMeters_to_Meters(250)
line_thickness = nanoMeters_to_Meters(60)
ground_thickness = nanoMeters_to_Meters(300)
Tc = 14.28
T = 0
pn = 1.008e-6
tanD = 0
Jc = 1

# # ---------------------------- unit cell inputs from paper
# width_unloaded = microMeters_to_Meters(1)
# width_loaded = microMeters_to_Meters(4)
# D0 = mm_To_Meters(1.34)
# D1 = microMeters_to_Meters(100)
# D2 = microMeters_to_Meters(100)
# D3 = microMeters_to_Meters(95)
# unit_Cell_Len = mm_To_Meters(4.02)
#
# In_Order_loads_Widths = [D1, D2, D3]
# number_of_loads = len(In_Order_loads_Widths)
#
# # ---------------------------- SC inputs
# Height = nanoMeters_to_Meters(300)
# line_thickness = nanoMeters_to_Meters(60)
# ground_thickness = nanoMeters_to_Meters(300)
# Tc = 14.7
# T = 4  # what equatioins to use when temp is > 0
# pn = 132
# er = 11.44
# tanD = 1.48351e-5
# Jc = 1


Floquet_line = SCFL_Model(unit_Cell_Len, D0, In_Order_loads_Widths, number_of_loads, width_unloaded, width_loaded, er,
                          Height, line_thickness, ground_thickness, Tc, pn, tanD, T, Jc)

# ---------------------------- calculations -------------------
FRange = np.linspace(toGHz(6), toGHz(25), 1000)

for F in FRange:
    aa, bta, unfolded, rr, xx, R,L,G,C = Floquet_line.abrx(F)

    # RR.append(R)
    # LL.append(L)
    # GG.append(G)
    # CC.append(C)

    beta.append(bta)
    betaUf.append(unfolded)
    a.append(aa)
    r.append(rr)
    x.append(xx)
    freqs.append(F)

print("total time: ", time.time() - s)



# RR,LL,GG,CC = np.array(RR),np.array(LL),np.array(GG),np.array(CC)
#
#
#
#
# I = .2
# I3 = I * I * I
#
# w = FRange*PI2
# WW = w*w
#
#
# #todo gamma*I
# CLWWI = CC*LL * WW * I
# CRwI = CC*RR*w*I
# GLwI = GG*LL*w*I
# RGI = RR*GG*I
# GLIIIwDiv3 = GG*LL*I3*(w/3)
# CLIIIWWDiv3  = CC*LL*I3*(WW/3)













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
a2.axvspan(Floquet_line.A//3, Floquet_line.B//3, facecolor='g', alpha=0.3)

# a1.plot(freqs, CLWWI)
# a2.plot(freqs, CRwI)
# a3.plot(freqs, GLwI)
# a4.plot(freqs, RGI)
# a5.plot(freqs, GLIIIwDiv3)
# a6.plot(freqs, CLIIIWWDiv3)


plt.show()
