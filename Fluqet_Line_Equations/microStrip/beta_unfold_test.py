import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.microStrip.beta_unfold import SCFL_Model
from Supports.Support_Functions import nanoMeter_to_Meter, microMeter_to_Meters


# ---------------------------- unit cell inputs from paper
unit_Cell_Len = microMeter_to_Meters(2300)
l1 = microMeter_to_Meters(50)
width_unloaded = microMeter_to_Meters(1.49)
a = 1.2
b = 2

# ---------------------------- SC inputs
er = 10
Height = nanoMeter_to_Meter(250)
line_thickness = nanoMeter_to_Meter(60)
ground_thickness = nanoMeter_to_Meter(300)
critical_Temp = 14.28
op_temp = 0
pn = 1.008e-6
tanD = 0

lineModel = SCFL_Model(unit_Cell_Len, l1, width_unloaded, a, b, er, Height, line_thickness, ground_thickness,
                       critical_Temp, pn, tanD, op_temp)

betaUnfoled, folded, freqs = [], [], []
a, r, x = [], [], []

s = time.time()
StartFreq, EndFreq, resolution = 1, 7e9, 1000

for F in np.linspace(StartFreq, EndFreq, resolution):
    aa, bta, b, rr, xx = lineModel.beta_unfolded(F)
    betaUnfoled.append(bta)
    a.append(aa)
    folded.append(b)
    r.append(rr)
    x.append(xx)
    freqs.append(F)

print(lineModel.tot)
totaltime = time.time() - s
print("total time: ", totaltime," time taken up to calc conductivity",lineModel.tot *100 / totaltime,"%")

fig, (a1, a2, a3, a4) = plt.subplots(4)
a1.plot(freqs, betaUnfoled)
a1.plot(freqs, folded)
a2.plot(freqs, a)
a3.plot(freqs, r)
a4.plot(freqs, x)
plt.show()
