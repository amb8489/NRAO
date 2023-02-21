from transmission_line_models.artificial_cpw.super_conducting_artificial_cpw_model import \
    SuperConductingArtificialCPWLine
from utills.functions import toGHz

# ------------------------------------


er = 11.44

s = 1 / 500000

wH = 1 / 500000

lH = 1 / 500000

wL = 7 * (10 ** -6)

lL = 1 / 500000

h = 1 / 2000

t = 3 * (10 ** -8)

# ------------------------------------

# CHAR IMPEDANCE: 139.711







line = SuperConductingArtificialCPWLine(lH,wH,lL,wL,s,3,er,t,h)

frequency = toGHz(5)

print(line.get_propagation_constant_characteristic_impedance(frequency))
