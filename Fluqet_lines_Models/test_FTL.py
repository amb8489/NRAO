import cmath
import math

import numpy as np
from matplotlib import pyplot as plt

from BlockTwoTransmissionLineModels.lineModels.MicroStripModel import SuperConductingMicroStripModel
from Fluqet_lines_Models.Fluqet_line_equations import ABCD_TL, GammaDZBN, UnitCellABCD_mats


def Pd(mat):
    A = mat[0][0]
    D = mat[1][1]

    return np.arccosh((A + D) / 2)
    # return np.arccosh((A + D) / 2)


def Zb(mat):
    A = mat[0][0]
    B = mat[0][1]
    D = mat[1][1]

    ADs2 = cmath.sqrt(pow(A + D, 2) - 4)

    B2 = 2 * B
    ADm = A - D

    # return [- (B2 / (ADm + ADs2)), - (B2 / (ADm - ADs2))]
    return -B2 / (ADm + ADs2)


# ---------------------------- unit cell inputs
d = 0.0023
l1 = 5e-5
# width of unloaded
Wu = 1.49e-6
a = 1.2
b = 2
# width of loads
Wl = a * Wu

# ---------------------------- sce inputs
er = 10
H = 2.5e-7
ts = 6e-8
tg = 3e-7
Tc = 14.28
pn = 1.008E-6
tanD = 0
op_temp = 1

model_unloaded = SuperConductingMicroStripModel(H, Wu, ts, er, tanD)
model_loaded = SuperConductingMicroStripModel(H, Wl, ts, er, tanD)

StartFreq, EndFreq, step = 6.99e9, 7.01e9, 1e4
#
a, b, r, x, freqs = [], [], [], [], []
F = StartFreq
while F < EndFreq:
    # calc Zc for load and unloaded
    loaded_char_imp = model_loaded.characteristic_impedance_auto(F, op_temp, Tc, pn)
    Unloaded_char_imp = model_unloaded.characteristic_impedance_auto(F, op_temp, Tc, pn)

    # calc propagation const for loaded and unloaded
    loaded_prop = model_loaded.propagation_constant_auto(F, op_temp, Tc, pn)
    Unloaded_prop = model_loaded.propagation_constant_auto(F, op_temp, Tc, pn)

    # ------------- ABCD 1 -------------
    Zc1 = loaded_char_imp
    propagation1 = loaded_prop
    Length1 = 0.5 * ((d / 3) - l1)
    mat1 = ABCD_TL(Zc1, propagation1, Length1)

    # ------------- ABCD 2 -------------
    Zc2 = Unloaded_char_imp
    propagation2 = Unloaded_prop
    length1 = l1
    mat2 = ABCD_TL(Zc2, propagation2, length1)

    # ------------- ABCD 4 -------------
    Zc4 = Unloaded_char_imp
    propagation4 = Unloaded_prop
    length2 = l1
    mat4 = ABCD_TL(Zc4, propagation4, length2)

    # ------------- ABCD 3 -------------
    Zc3 = loaded_char_imp
    propagation3 = loaded_prop
    Length2 = (d / 3) - 0.5 * (length1 + length2)
    mat3 = ABCD_TL(Zc3, propagation3, Length2)

    # ------------- ABCD 6 -------------
    Zc6 = Unloaded_char_imp
    propagation6 = Unloaded_prop
    length3 = 2 * length1
    mat6 = ABCD_TL(Zc6, propagation6, length3)

    # ------------- ABCD 5 -------------
    Zc5 = loaded_char_imp
    propagation5 = loaded_prop
    Length3 = (d / 3) - 0.5 * (length2 + length3)
    mat5 = ABCD_TL(Zc5, propagation5, Length3)

    # ------------- ABCD 7 -------------
    Zc7 = loaded_char_imp
    propagation7 = loaded_prop
    Length4 = 0.5 * ((d / 3) - length3)
    mat7 = ABCD_TL(Zc7, propagation7, Length4)

    # ------------- ABCD UNIT CELL-------------
    ABCD_UC = UnitCellABCD_mats([mat1, mat2, mat3, mat4, mat5, mat6, mat7])

    ZB = Zb(ABCD_UC)
    pb = Pd(ABCD_UC)

    a.append(pb.real)
    b.append(pb.imag)

    r.append(ZB.real)
    x.append(ZB.imag)

    freqs.append(F)

    F += step

# plt.plot(freqs, a, linewidth=1.0, label='a')
# plt.plot(freqs, b, linewidth=1.0, label='b')
# plt.plot(freqs, r, linewidth=1.0, label='r')
# plt.plot(freqs, x, linewidth=1.0, label='x')
plt.show()
