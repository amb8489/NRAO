import matplotlib.pyplot as plt
import numpy as np

from transmission_line_models.artificial_cpw.super_conducting_artificial_cpw_model import \
    SuperConductingArtificialCPWLine
from utills.functions import toGHz

# ------------------------------------


er = 11.44

s = 1 / 500000

wH = 1 / 500000

lH = 1 / 500000

wL = 0.0002072

lL = 1 / 500000

h = 1 / 2000

t = 3 * (10 ** -8)

# ------------------------------------

# CHAR IMPEDANCE: 139.711


tc = 14.4

sigma = 757576

line = SuperConductingArtificialCPWLine(lH, wH, lL, wL, s, 16, er, t, h, tc, sigma)

frequency = toGHz(23.7)

# print("propagation_constant: ",line.propagation_constant(1,2,.1,500000))
# print("characteristic_impedance: ",line.characteristic_impedance(1,2,.1,500000))
#

frequencys = np.linspace(toGHz(1), toGHz(25), 1000)
freq = []
for f in frequencys:
    freq.append(line.get_propagation_constant_characteristic_impedance(f))

plt.plot(frequencys, freq)
plt.show()
