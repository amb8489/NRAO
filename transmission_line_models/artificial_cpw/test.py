import time

import matplotlib.pyplot as plt
import numpy as np

from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.artificial_cpw.super_conducting_artificial_cpw_model import \
    SuperConductingArtificialCPWLine
from utills.functions import toGHz

# ------------------------------------


er = 11.44

s = 1 / 500000

wH = 1 / 500000

lH = 1 / 500000

wL = 9 / 250000  # <-----

lL = 1 / 500000

h = 1 / 2000

t = 3 * (10 ** -8)

# ------------------------------------

# CHAR IMPEDANCE: 139.711


pn = 1.32 * 10 ** -6
op_temp = 0
tc = 14.4

super_conductivity_model = SuperConductivity(op_temp, tc, pn)

line = SuperConductingArtificialCPWLine(lH, wH, lL, wL, s, 38, er, t, h, super_conductivity_model)

frequencys_range = np.linspace(toGHz(1), toGHz(25), 100)
outputs = []
s = time.time()
for f in frequencys_range:
    outputs.append(line.get_propagation_constant_characteristic_impedance(f))
print(time.time() - s)

plt.plot(frequencys_range, outputs)
plt.show()
