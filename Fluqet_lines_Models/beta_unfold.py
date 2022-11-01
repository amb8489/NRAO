import cmath
import math
import time

import numpy as np
from matplotlib import pyplot as plt

from BlockTwoTransmissionLineModels.lineModels.MicroStripModel import SuperConductingMicroStripModel
from Fluqet_lines_Models.Fluqet_line_equations import ABCD_TL, GammaDZBN, UnitCellABCD_mats, S21Ncell, S12
from Supports.constants import PI


def Pd(mat):
    mat_A = mat[0][0]
    mat_D = mat[1][1]

    return np.arccosh((mat_A + mat_D) / 2)


def Zb(mat):
    mat_A = mat[0][0]
    mat_B = mat[0][1]
    mat_D = mat[1][1]

    ADs2 = cmath.sqrt(pow(mat_A + mat_D, 2) - 4)

    B2 = 2 * mat_B

    ADm = mat_A - mat_D

    return [- (B2 / (ADm + ADs2)), - (B2 / (ADm - ADs2))]


# ---------------------------- unit cell inputs
d = 0.0023
l1 = 5e-5
# width of unloaded
Wu = 1.49e-6
A = 1.2
B = 2
# width of loads
Wl = A * Wu

# ---------------------------- sce inputs
er = 10
H = 2.5e-7
ts = 6e-8
tg = 3e-7
Tc = 14.28
pn = 1.008E-6
tanD = 0
op_temp = 0

N = 100

model_unloaded = SuperConductingMicroStripModel(H, Wu, ts, er, tanD)
model_loaded = SuperConductingMicroStripModel(H, Wl, ts, er, tanD)

prev = 0
StartFreq, EndFreq, step = 1000, 30e9, 1e7
#
betaUnfoled, folded, freqs = [], [], []
F = StartFreq

region = 0
PiMult = 0
flipping = False
looking = True

s = time.time()

while F < EndFreq:
    # calc Zc for load and unloaded
    loaded_char_imp = model_loaded.characteristic_impedance_auto(F, op_temp, Tc, pn)
    Unloaded_char_imp = model_unloaded.characteristic_impedance_auto(F, op_temp, Tc, pn)

    # calc propagation const for loaded and unloaded
    loaded_prop = model_loaded.propagation_constant_auto(F, op_temp, Tc, pn)
    Unloaded_prop = model_loaded.propagation_constant_auto(F, op_temp, Tc, pn)

    ZcCL = Unloaded_char_imp
    propagation2 = Unloaded_prop
    central_line = ABCD_TL(ZcCL, propagation2, d)

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
    ZB = Zb(ABCD_UC)[1]
    pb = Pd(ABCD_UC)

    bta = pb.imag

    # at a top or bottom
    if looking and (bta == 0 or bta >= 3.141):
        print(f"found flat freq:{F}")
        looking = False

    # on a slope
    else:
        if not looking and (bta > 0 and bta < 3.141):
            region += 1
            PiMult += PI
            flipping = not flipping
            print(f"found flat end of flat   Freq:{F} starting region {region}    flipped = {flipping}\n")
            looking = True

    b = bta
    if flipping:
        bta += 2 * abs(PI - bta) + (PiMult - PI)
    else:
        bta += PiMult

    betaUnfoled.append(bta)
    folded.append(b)
    freqs.append(F)

    F += step

print("total time: ", time.time() - s)

fig, axs = plt.subplots()
axs.plot(freqs, betaUnfoled)
axs.plot(freqs, folded)

plt.show()
